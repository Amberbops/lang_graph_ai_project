// ==============================================================================
// NEON GENESIS — FRONTEND CONTROLLER, LIVE ANTIGRAVITY TIMERS & AUTH SESSIONS
// ==============================================================================

(function () {
    'use strict';

    // DOM Elements
    const form = document.getElementById('generator-form');
    const promptInput = document.getElementById('prompt-input');
    const cleanChk = document.getElementById('clean-workspace-chk');
    const generateBtn = document.getElementById('generate-btn');
    const telemetrySection = document.getElementById('telemetry-section');
    const masterTimerEl = document.getElementById('master-timer');
    const pipelineProgressBar = document.getElementById('pipeline-progress-bar');
    const pipelineStatusText = document.getElementById('pipeline-status-text');
    const activeStepBadge = document.getElementById('active-step-badge');
    const pipelineStepsContainer = document.getElementById('pipeline-steps-container');
    const completionCard = document.getElementById('completion-card');
    const completionStats = document.getElementById('completion-stats');
    const terminalLogs = document.getElementById('terminal-logs');
    const clearLogsBtn = document.getElementById('clear-logs-btn');
    const previewFilesBtn = document.getElementById('preview-files-btn');
    const newGenBtn = document.getElementById('new-gen-btn');
    const previewModal = document.getElementById('preview-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const modalFileList = document.getElementById('modal-file-list');
    const viewerFilename = document.getElementById('viewer-filename');
    const viewerCodeContent = document.getElementById('viewer-code-content');
    const chips = document.querySelectorAll('.chip');

    // Live App Preview & Export Elements
    const appPreviewIframe = document.getElementById('app-preview-iframe');
    const previewViewport = document.getElementById('preview-viewport');
    const reloadPreviewBtn = document.getElementById('reload-preview-btn');
    const deviceDesktopBtn = document.getElementById('device-desktop-btn');
    const deviceMobileBtn = document.getElementById('device-mobile-btn');
    const externalPreviewLink = document.getElementById('external-preview-link');
    const downloadZipBtn = document.getElementById('download-zip-btn');

    // User Profile / Supabase Auth Elements
    const userProfileBadge = document.getElementById('user-profile-badge');
    const userDisplayEmail = document.getElementById('user-display-email');
    const navLoginBtn = document.getElementById('nav-login-btn');
    const navLogoutBtn = document.getElementById('nav-logout-btn');

    // State
    let isRunning = false;
    let localStartTime = 0;
    let timerInterval = null;
    let pollInterval = null;
    let cachedFiles = [];
    let knownLogCount = 0;

    // Pipeline Steps Template
    const DEFAULT_STEPS = [
        { id: "router", title: "Router", icon: "🧭", desc: "Analyzing intent & classifying request" },
        { id: "inspector", title: "Workspace Inspector", icon: "🔍", desc: "Scanning project filesystem & dependencies" },
        { id: "architect", title: "System Architect", icon: "📐", desc: "Designing technical architecture & components" },
        { id: "planner", title: "Strategic Planner", icon: "📋", desc: "Breaking architecture into prioritized tasks" },
        { id: "coder", title: "Coding Agent", icon: "⚡", desc: "Writing code, styling & application files" },
        { id: "tester", title: "Verification & Tester", icon: "🧪", desc: "Executing test suites & validating output" },
        { id: "packager", title: "ZIP Packager", icon: "📦", desc: "Compressing project into downloadable ZIP archive" },
    ];

    // ==========================================================================
    // AUTH SESSION HELPERS
    // ==========================================================================

    function getAuthToken() {
        return localStorage.getItem('devpilot_token') || '';
    }

    function getUserId() {
        return localStorage.getItem('devpilot_user_id') || 'default';
    }

    function getUserEmail() {
        return localStorage.getItem('devpilot_email') || '';
    }

    function updateDownloadAndPreviewLinks() {
        const userId = getUserId();
        const downloadUrl = `/api/download-zip?user_id=${encodeURIComponent(userId)}`;
        if (downloadZipBtn) {
            downloadZipBtn.href = downloadUrl;
        }
        const modalDownloadBtns = document.querySelectorAll('.modal-download-btn');
        modalDownloadBtns.forEach(btn => {
            btn.href = downloadUrl;
        });
        if (externalPreviewLink) {
            externalPreviewLink.href = `/preview/?user_id=${encodeURIComponent(userId)}`;
        }
    }

    function initAuthSession() {
        const token = getAuthToken();
        const userId = getUserId();
        const email = getUserEmail();

        if (token && userId && userId !== 'default') {
            if (userProfileBadge && userDisplayEmail) {
                userDisplayEmail.textContent = email || 'Authenticated User';
                userProfileBadge.classList.remove('hidden');
            }
            if (navLoginBtn) navLoginBtn.classList.add('hidden');
            if (navLogoutBtn) navLogoutBtn.classList.remove('hidden');
        } else {
            if (userProfileBadge) userProfileBadge.classList.add('hidden');
            if (navLoginBtn) navLoginBtn.classList.remove('hidden');
            if (navLogoutBtn) navLogoutBtn.classList.add('hidden');
        }

        updateDownloadAndPreviewLinks();
    }

    // ==========================================================================
    // INITIALIZATION & EVENT LISTENERS
    // ==========================================================================

    function init() {
        initAuthSession();
        renderStepCards(DEFAULT_STEPS);
        setupEventListeners();
        checkInitialStatus();
    }

    function setupEventListeners() {
        form.addEventListener('submit', handleFormSubmit);

        chips.forEach(chip => {
            chip.addEventListener('click', () => {
                promptInput.value = chip.dataset.prompt;
                promptInput.focus();
                // Brief neon glow feedback
                promptInput.style.borderColor = 'var(--neon-pink)';
                promptInput.style.boxShadow = '0 0 25px var(--neon-pink-glow)';
                setTimeout(() => {
                    promptInput.style.borderColor = '';
                    promptInput.style.boxShadow = '';
                }, 400);
            });
        });

        clearLogsBtn.addEventListener('click', () => {
            terminalLogs.innerHTML = '';
        });

        if (navLogoutBtn) {
            navLogoutBtn.addEventListener('click', () => {
                localStorage.removeItem('devpilot_token');
                localStorage.removeItem('devpilot_user_id');
                localStorage.removeItem('devpilot_email');
                document.cookie = "devpilot_user_id=; Path=/preview/; Max-Age=0; SameSite=Lax";
                window.location.replace('/login');
            });
        }

        previewFilesBtn.addEventListener('click', openPreviewModal);
        closeModalBtn.addEventListener('click', closePreviewModal);

        previewModal.addEventListener('click', (e) => {
            if (e.target === previewModal) closePreviewModal();
        });

        newGenBtn.addEventListener('click', () => {
            completionCard.classList.add('hidden');
            telemetrySection.classList.add('hidden');
            if (appPreviewIframe) appPreviewIframe.src = 'about:blank';
            promptInput.value = '';
            promptInput.focus();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // App Preview Controls
        if (reloadPreviewBtn) {
            reloadPreviewBtn.addEventListener('click', () => {
                if (appPreviewIframe) {
                    const userId = getUserId();
                    appPreviewIframe.src = `/preview/?user_id=${encodeURIComponent(userId)}&t=${Date.now()}`;
                }
            });
        }

        if (deviceDesktopBtn && deviceMobileBtn && previewViewport) {
            deviceDesktopBtn.addEventListener('click', () => {
                deviceDesktopBtn.classList.add('active');
                deviceMobileBtn.classList.remove('active');
                previewViewport.className = 'browser-viewport desktop';
            });

            deviceMobileBtn.addEventListener('click', () => {
                deviceMobileBtn.classList.add('active');
                deviceDesktopBtn.classList.remove('active');
                previewViewport.className = 'browser-viewport mobile';
            });
        }
    }

    // ==========================================================================
    // RENDER STEP CARDS
    // ==========================================================================

    function renderStepCards(steps) {
        pipelineStepsContainer.innerHTML = '';
        steps.forEach(step => {
            const card = document.createElement('div');
            card.className = 'step-card pending';
            card.id = `step-card-${step.id}`;

            card.innerHTML = `
                <div class="step-top">
                    <div class="step-icon-title">
                        <span class="step-icon">${step.icon}</span>
                        <span class="step-title">${step.title}</span>
                    </div>
                    <span class="step-timer-badge" id="timer-badge-${step.id}">00:00.0s</span>
                </div>
                <p class="step-desc">${step.desc}</p>
                <div class="step-status-pill" id="status-pill-${step.id}">
                    <span>QUEUED</span>
                </div>
            `;
            pipelineStepsContainer.appendChild(card);
        });
    }

    // ==========================================================================
    // FORM SUBMISSION & API CALLS
    // ==========================================================================

    async function handleFormSubmit(e) {
        e.preventDefault();
        const prompt = promptInput.value.trim();
        if (!prompt || isRunning) return;

        const clean = cleanChk.checked;
        const userId = getUserId();
        const token = getAuthToken();

        // Reset UI
        completionCard.classList.add('hidden');
        terminalLogs.innerHTML = '';
        knownLogCount = 0;
        masterTimerEl.textContent = '00:00.00';
        pipelineProgressBar.style.width = '0%';
        pipelineStatusText.textContent = 'AGENT PIPELINE ACTIVE';
        telemetrySection.classList.remove('hidden');

        // Scroll to telemetry
        telemetrySection.scrollIntoView({ behavior: 'smooth' });

        // Lock form
        isRunning = true;
        generateBtn.disabled = true;
        generateBtn.querySelector('.btn-text').textContent = 'SYNTHESIZING...';

        // Start high-frequency local timer
        localStartTime = Date.now();
        startMasterTimerTicker();

        try {
            const headers = { 'Content-Type': 'application/json' };
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            const res = await fetch('/api/generate', {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({ prompt, clean, user_id: userId })
            });

            const data = await res.json();
            if (data.error) {
                alert('Generation Error: ' + data.error);
                stopGeneration(false);
                return;
            }

            // Start polling status
            startPolling();

        } catch (err) {
            console.error('Fetch error:', err);
            alert('Failed to connect to backend server: ' + err.message);
            stopGeneration(false);
        }
    }

    // ==========================================================================
    // LIVE TIMERS (ANTIGRAVITY STYLE)
    // ==========================================================================

    function startMasterTimerTicker() {
        if (timerInterval) clearInterval(timerInterval);

        timerInterval = setInterval(() => {
            if (!isRunning) return;
            const elapsedMs = Date.now() - localStartTime;
            masterTimerEl.textContent = formatDuration(elapsedMs / 1000);
        }, 60); // 60ms for smooth millisecond updates
    }

    function formatDuration(sec) {
        if (!sec || isNaN(sec)) sec = 0;
        const m = Math.floor(sec / 60);
        const s = Math.floor(sec % 60);
        const ms = Math.floor((sec % 1) * 100);

        const mm = String(m).padStart(2, '0');
        const ss = String(s).padStart(2, '0');
        const mss = String(ms).padStart(2, '0');

        return `${mm}:${ss}.${mss}`;
    }

    function formatStepDuration(sec) {
        if (!sec || isNaN(sec)) return '00:00.0s';
        const m = Math.floor(sec / 60);
        const s = Math.floor(sec % 60);
        const ms = Math.floor((sec % 1) * 10);

        const mm = String(m).padStart(2, '0');
        const ss = String(s).padStart(2, '0');

        return `${mm}:${ss}.${ms}s`;
    }

    // ==========================================================================
    // POLLING STATUS
    // ==========================================================================

    function startPolling() {
        if (pollInterval) clearInterval(pollInterval);
        pollInterval = setInterval(pollStatus, 400); // 400ms poll
    }

    async function pollStatus() {
        try {
            const res = await fetch('/api/status');
            if (!res.ok) return;
            const state = await res.json();

            updateUIFromState(state);

            // Only stop when terminal state is reached
            if (state.status === 'COMPLETED' || state.status === 'FAILED') {
                stopGeneration(state.status === 'COMPLETED');
            }
        } catch (err) {
            console.warn('Poll error:', err);
        }
    }

    function updateUIFromState(state) {
        // Active badge
        if (state.current_step_id) {
            activeStepBadge.textContent = state.current_step_id.toUpperCase();
        }

        // Steps update
        let completedCount = 0;
        const steps = state.steps || [];

        steps.forEach(step => {
            const card = document.getElementById(`step-card-${step.id}`);
            const timerBadge = document.getElementById(`timer-badge-${step.id}`);
            const statusPill = document.getElementById(`status-pill-${step.id}`);

            if (!card) return;

            card.className = `step-card ${step.status}`;

            if (step.status === 'completed') {
                completedCount++;
                statusPill.innerHTML = '<span>✓ COMPLETED</span>';
                timerBadge.textContent = formatStepDuration(step.duration);
            } else if (step.status === 'running') {
                statusPill.innerHTML = '<span class="step-spinner"></span><span>ACTIVE</span>';
                timerBadge.textContent = formatStepDuration(step.duration);
            } else if (step.status === 'failed') {
                statusPill.innerHTML = '<span>✕ FAILED</span>';
                timerBadge.textContent = formatStepDuration(step.duration);
            } else {
                statusPill.innerHTML = '<span>QUEUED</span>';
                timerBadge.textContent = '00:00.0s';
            }
        });

        // Progress bar
        const total = steps.length || 7;
        const progressPct = Math.round((completedCount / total) * 100);
        pipelineProgressBar.style.width = `${progressPct}%`;

        // Logs
        if (state.logs && state.logs.length > knownLogCount) {
            const newLogs = state.logs.slice(knownLogCount);
            newLogs.forEach(log => {
                appendLog(log.timestamp, log.message, log.level);
            });
            knownLogCount = state.logs.length;
        }

        // Final stats
        if (state.status === 'COMPLETED') {
            pipelineStatusText.textContent = 'SYNTHESIS COMPLETE';
            activeStepBadge.textContent = 'FINISHED';

            const files = state.files_generated || [];
            const totalBytes = files.reduce((acc, f) => acc + (f.size || 0), 0);
            const kbSize = (totalBytes / 1024).toFixed(1);

            completionStats.textContent = `${files.length} project files generated • ${kbSize} KB total`;
            
            // Only load iframe once on completion transition
            if (completionCard.classList.contains('hidden')) {
                completionCard.classList.remove('hidden');
                const userId = getUserId();
                if (appPreviewIframe) {
                    const cacheBuster = Date.now();
                    appPreviewIframe.src = `/preview/?user_id=${encodeURIComponent(userId)}&t=${cacheBuster}`;
                }
                updateDownloadAndPreviewLinks();
                setTimeout(() => {
                    completionCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 300);
            }
        } else if (state.status === 'FAILED') {
            pipelineStatusText.textContent = 'SYNTHESIS FAILED: ' + (state.error_message || 'Error occurred');
            activeStepBadge.textContent = 'ERROR';
            pipelineProgressBar.style.background = 'var(--neon-red)';
            pipelineProgressBar.style.boxShadow = '0 0 15px var(--neon-red)';
        }
    }

    function appendLog(timestamp, msg, level) {
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        entry.innerHTML = `
            <span class="log-time">[${timestamp}]</span>
            <span class="log-msg ${level || ''}">${escapeHtml(msg)}</span>
        `;
        terminalLogs.appendChild(entry);
        terminalLogs.scrollTop = terminalLogs.scrollHeight;
    }

    function stopGeneration(success) {
        isRunning = false;
        if (timerInterval) clearInterval(timerInterval);
        if (pollInterval) clearInterval(pollInterval);

        generateBtn.disabled = false;
        generateBtn.querySelector('.btn-text').textContent = '⚡ INITIATE SYNTHESIS';

        if (success) {
            pipelineProgressBar.style.width = '100%';
        }
    }

    async function checkInitialStatus() {
        try {
            const res = await fetch('/api/status');
            if (!res.ok) return;
            const state = await res.json();
            if (state.is_running) {
                telemetrySection.classList.remove('hidden');
                isRunning = true;
                generateBtn.disabled = true;
                generateBtn.querySelector('.btn-text').textContent = 'SYNTHESIZING...';
                localStartTime = state.start_time * 1000;
                startMasterTimerTicker();
                startPolling();
            } else if (state.status === 'COMPLETED') {
                // Restore completed project and live preview after page refresh
                telemetrySection.classList.remove('hidden');
                updateUIFromState(state);
                const userId = getUserId();
                if (appPreviewIframe) {
                    appPreviewIframe.src = `/preview/?user_id=${encodeURIComponent(userId)}&t=${Date.now()}`;
                }
                updateDownloadAndPreviewLinks();
            } else if (state.status === 'FAILED') {
                telemetrySection.classList.remove('hidden');
                updateUIFromState(state);
            }
        } catch (_) {}
    }

    // ==========================================================================
    // FILE PREVIEW MODAL
    // ==========================================================================

    async function openPreviewModal() {
        const userId = getUserId();
        const token = getAuthToken();
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const res = await fetch(`/api/files?user_id=${encodeURIComponent(userId)}`, {
                headers: headers
            });
            if (!res.ok) return;
            const data = await res.json();
            cachedFiles = data.files || [];

            renderModalFileList(cachedFiles);
            previewModal.classList.remove('hidden');

            if (cachedFiles.length > 0) {
                displayFileInViewer(cachedFiles[0]);
            }
        } catch (err) {
            console.error('Failed to load files:', err);
        }
    }

    function closePreviewModal() {
        previewModal.classList.add('hidden');
    }

    function renderModalFileList(files) {
        modalFileList.innerHTML = '';
        if (files.length === 0) {
            modalFileList.innerHTML = '<div style="color: var(--text-dim); padding: 8px;">No files found.</div>';
            return;
        }

        files.forEach((file, idx) => {
            const item = document.createElement('div');
            item.className = `file-list-item ${idx === 0 ? 'active' : ''}`;
            item.textContent = file.name;
            item.addEventListener('click', () => {
                document.querySelectorAll('.file-list-item').forEach(el => el.classList.remove('active'));
                item.classList.add('active');
                displayFileInViewer(file);
            });
            modalFileList.appendChild(item);
        });
    }

    function displayFileInViewer(file) {
        viewerFilename.textContent = `📄 ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
        viewerCodeContent.textContent = file.content;
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Run
    init();
})();
