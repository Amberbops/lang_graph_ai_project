"""
Model registry for DevPilot agents_v2.

Provider strategy (avoids free-tier quota exhaustion):

  ROUTER / FAST  →  Gemini  gemini-3.5-flash-lite
                    Low-traffic nodes (1-2 calls per run, simple tasks).

  REASONING      →  Groq    (auto-selected from GROQ_CANDIDATES)
  CODING         →  Groq    (auto-selected from GROQ_CANDIDATES)
                    Heavy nodes: architect, planner, coder, debugger.
                    Groq free tier: 14,400 req/day — no 20-req hard cap.

Auto-selection:
  _probe_groq() pings each candidate with a 1-token request at startup
  and picks the first model that responds without a 404.  This means
  the agent always uses a live model, regardless of which Llama variants
  the API key has been granted access to.

Keys are loaded exclusively from .env (GOOGLE_API_KEY, GROQ_API_KEY).
"""

import os
import time
import logging

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    _HAS_GEMINI = True
except ImportError:
    ChatGoogleGenerativeAI = None
    _HAS_GEMINI = False

from langchain_groq import ChatGroq

load_dotenv()

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Gemini (lightweight tasks)
# ------------------------------------------------------------------

GEMINI_LITE_MODEL = "gemini-3.5-flash-lite"


# ------------------------------------------------------------------
# Groq candidate list — tried in order; first live model wins
# ------------------------------------------------------------------

GROQ_CANDIDATES = [
    # --- Models confirmed available (from user's Groq console) ---
    "openai/gpt-oss-120b",       # Largest — best reasoning & tool use
    "openai/gpt-oss-20b",        # Smaller, faster fallback
    "groq/compound",             # Groq's agentic compound model
    "groq/compound-mini",        # Lighter compound model
    "qwen/qwen3.8-27b",          # Qwen 3.8 27B (partially visible in console)
    # --- Possible access (worth probing) ---
    "llama-3.3-70b-versatile",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.1-8b-instant",
]

# Cache — populated lazily on first call
_GROQ_MODEL_CACHE: str | None = None


# ------------------------------------------------------------------
# Factories
# ------------------------------------------------------------------

def _gemini(model_name: str, temperature: float = 0) -> BaseChatModel:
    if _HAS_GEMINI and os.getenv("GOOGLE_API_KEY"):
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
    return _groq_auto(temperature=temperature)


def _groq(model_name: str, temperature: float = 0) -> ChatGroq:
    return ChatGroq(
        model=model_name,
        temperature=temperature,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        max_tokens=8192,
    )



def _probe_groq() -> str:
    """
    Try each model in GROQ_CANDIDATES with a tiny request.
    Return the first model ID that responds without error.
    Raises RuntimeError if none work.
    """
    global _GROQ_MODEL_CACHE

    if _GROQ_MODEL_CACHE:
        return _GROQ_MODEL_CACHE

    groq_key = os.getenv("GROQ_API_KEY", "")
    if not groq_key:
        raise RuntimeError("GROQ_API_KEY is not set. Add it to .env.")

    probe_msg = [HumanMessage(content="Hi")]

    for model_id in GROQ_CANDIDATES:
        try:
            client = _groq(model_id)
            client.invoke(probe_msg, max_tokens=1)
            print(f"  ✅ Groq model selected: {model_id}")
            _GROQ_MODEL_CACHE = model_id
            return model_id
        except Exception as exc:
            err_str = str(exc).lower()
            # Skip gracefully for: 404, decommissioned, no access
            skip_kws = ("404", "not found", "not exist", "decommission",
                        "no longer supported", "does not have access")
            if any(kw in err_str for kw in skip_kws):
                print(f"  ⚠️  {model_id} — unavailable/decommissioned, trying next …")
            else:
                print(f"  ⚠️  {model_id} — error: {exc}, trying next …")
            continue

    raise RuntimeError(
        "No Groq model is available for this API key.\n"
        "Candidates tried: " + ", ".join(GROQ_CANDIDATES)
    )


def _groq_auto(temperature: float = 0) -> ChatGroq:
    """Return a ChatGroq instance using the best available model."""
    model_id = _probe_groq()
    return _groq(model_id, temperature=temperature)


# ------------------------------------------------------------------
# Named constructors (used by each node)
# ------------------------------------------------------------------

def get_router_model() -> BaseChatModel:
    """Gemini flash-lite if available, else Groq."""
    if _HAS_GEMINI and os.getenv("GOOGLE_API_KEY"):
        return _gemini(GEMINI_LITE_MODEL)
    return _groq_auto()


def get_fast_model() -> BaseChatModel:
    """Gemini flash-lite if available, else Groq."""
    if _HAS_GEMINI and os.getenv("GOOGLE_API_KEY"):
        return _gemini(GEMINI_LITE_MODEL)
    return _groq_auto()


def get_reasoning_model() -> BaseChatModel:
    """
    Primary Groq model with automatic multi-model fallback.
    If primary model hits rate/TPM limits, seamlessly fails over.
    """
    primary_id = _probe_groq()
    primary = _groq(primary_id)

    fallbacks = []
    for cand in GROQ_CANDIDATES:
        if cand != primary_id and not any(skip in cand for skip in ("whisper", "safeguard", "orpheus", "prompt-guard")):
            fallbacks.append(_groq(cand))

    if _HAS_GEMINI and os.getenv("GOOGLE_API_KEY"):
        fallbacks.append(_gemini(GEMINI_LITE_MODEL))

    return primary.with_fallbacks(fallbacks) if fallbacks else primary


def get_coding_model() -> BaseChatModel:
    """
    Best available model with automatic multi-model fallback for tool-calling.
    If openai/gpt-oss-120b hits the 8,000 TPM limit (413), it seamlessly
    switches to openai/gpt-oss-20b, groq/compound, or Gemini!
    """
    primary_id = _probe_groq()
    primary = _groq(primary_id)

    fallbacks = []
    for cand in GROQ_CANDIDATES:
        if cand != primary_id and not any(skip in cand for skip in ("whisper", "safeguard", "orpheus", "prompt-guard")):
            fallbacks.append(_groq(cand))

    if _HAS_GEMINI and os.getenv("GOOGLE_API_KEY"):
        fallbacks.append(_gemini(GEMINI_LITE_MODEL))

    return primary.with_fallbacks(fallbacks) if fallbacks else primary


# ------------------------------------------------------------------
# Retry wrapper — catches 429 / 413 / 503 and backs off automatically
# ------------------------------------------------------------------

def invoke_with_retry(
    runnable,
    input_data,
    max_retries: int = 5,
    base_wait: float = 8.0,
):
    """
    Call runnable.invoke(input_data), retrying on quota, TPM, or server errors.
    Waits base_wait * (attempt + 1) seconds between retries.
    """
    last_exc = None

    for attempt in range(max_retries):
        try:
            return runnable.invoke(input_data)

        except Exception as exc:
            err_str = str(exc).lower()

            retryable = any(
                kw in err_str
                for kw in (
                    "429",
                    "413",
                    "tpm",
                    "tokens per minute",
                    "request too large",
                    "resource_exhausted",
                    "rate",
                    "503",
                    "overloaded",
                    "rate_limit_exceeded",
                )
            )

            if not retryable:
                raise

            wait = base_wait * (attempt + 1)
            logger.warning(
                "API rate/TPM limit error (attempt %d/%d). Retrying in %.0fs...",
                attempt + 1, max_retries, wait,
            )
            print(
                f"  ⏳ Rate/TPM limit reached — retrying in {wait:.0f}s "
                f"(attempt {attempt + 1}/{max_retries}) …"
            )
            time.sleep(wait)
            last_exc = exc

    raise RuntimeError(
        f"All {max_retries} retry attempts exhausted."
    ) from last_exc

