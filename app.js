document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide icons
    lucide.createIcons();

    // Elements
    const runBtn = document.getElementById('run-btn');
    const protocolSelect = document.getElementById('protocol-select');
    const bitCountSlider = document.getElementById('bit-count');
    const bitCountVal = document.getElementById('bit-count-val');
    const noiseSlider = document.getElementById('noise-level');
    const noiseVal = document.getElementById('noise-val');
    const eveToggle = document.getElementById('eve-toggle');
    const eveNode = document.getElementById('eve-node');
    const stepsLog = document.getElementById('steps-log');
    const photonStream = document.getElementById('photon-stream');
    const backendStatus = document.getElementById('backend-status');
    const summaryStats = document.getElementById('summary-stats');

    // Charts
    let qberChart, yieldChart;

    // State
    let isRunning = false;

    // Update UI labels
    bitCountSlider.addEventListener('input', (e) => {
        bitCountVal.textContent = e.target.value;
    });

    noiseSlider.addEventListener('input', (e) => {
        noiseVal.textContent = Math.round(e.target.value * 100) + '%';
    });

    eveToggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            eveNode.classList.remove('invisible');
        } else {
            eveNode.classList.add('invisible');
        }
    });

    // Check backend status
    async function checkHealth() {
        try {
            const res = await fetch('/health');
            if (res.ok) {
                backendStatus.className = 'status-badge online';
                backendStatus.innerHTML = '<span class="dot"></span> Backend: Online';
            }
        } catch (e) {
            backendStatus.className = 'status-badge';
            backendStatus.innerHTML = '<span class="dot"></span> Backend: Offline';
        }
    }
    checkHealth();
    setInterval(checkHealth, 5000);

    // Run Simulation
    runBtn.addEventListener('click', async () => {
        if (isRunning) return;
        isRunning = true;
        runBtn.disabled = true;
        runBtn.textContent = 'Processing...';
        stepsLog.innerHTML = '';
        photonStream.innerHTML = '';

        const config = {
            protocol: protocolSelect.value,
            n_bits: parseInt(bitCountSlider.value),
            noise: parseFloat(noiseSlider.value),
            eve: eveToggle.checked
        };

        log('System', `Initializing ${config.protocol.toUpperCase()} protocol with ${config.n_bits} qubits...`);

        try {
            // Get detailed steps for animation
            const res = await fetch(`/protocol/step-by-step?protocol=${config.protocol}&n_bits=${config.n_bits}&eve=${config.eve}&noise=${config.noise}`);
            const steps = await res.json();

            // Run through steps
            for (const step of steps) {
                await processStep(step);
                await delay(800);
            }

            // Get full simulation results for charts
            const fullRes = await fetch('/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    protocols: [config.protocol],
                    n_bits: 1000, // Use more bits for stable stats in charts
                    noise_levels: [0.0, 0.05, 0.1, 0.15, 0.2],
                    n_sim: 1
                })
            });
            const stats = await fullRes.json();
            updateCharts(stats, config.protocol);
            updateSummary(steps[steps.length - 1].data);

            log('Success', 'Simulation complete. Analytics updated.');
        } catch (error) {
            log('Error', `Failed to run simulation: ${error.message}`);
            console.error(error);
        }

        isRunning = false;
        runBtn.disabled = false;
        runBtn.textContent = 'Initialize Simulation';
    });

    async function processStep(step) {
        switch (step.step) {
            case 'alice_sent':
                log('Alice', `Generated ${step.data.bits.length} random bits and bases. Sending photons...`);
                createPhotons(step.data.bits.length);
                break;
            case 'eve_intercepted':
                log('Eve', 'Intercepted photon stream! Measuring and re-sending...');
                highlightEve();
                break;
            case 'channel_noise':
                log('Channel', `${step.data.noise_indices.length} qubits affected by quantum decoherence (noise).`);
                break;
            case 'bob_measured':
                log('Bob', `Photons received. Measured using random bases.`);
                break;
            case 'sifting':
                log('System', `Public discussion: ${step.data.indices.length} matching bases identified (sifted key).`);
                break;
            case 'results':
                log('System', `Quantum Bit Error Rate (QBER): ${step.data.qber.toFixed(2)}%`);
                break;
        }
    }

    function log(label, msg) {
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        const time = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
        entry.innerHTML = `<span class="log-time">[${time}]</span> <span class="log-label" style="color: ${getLabelColor(label)}">${label}:</span> <span class="log-msg">${msg}</span>`;
        stepsLog.appendChild(entry);
        stepsLog.scrollTop = stepsLog.scrollHeight;
    }

    function getLabelColor(label) {
        if (label === 'Alice') return 'var(--alice-color)';
        if (label === 'Bob') return 'var(--bob-color)';
        if (label === 'Eve') return 'var(--eve-color)';
        if (label === 'Success') return '#2ecc71';
        if (label === 'Error') return '#ff4d4d';
        return 'var(--accent-primary)';
    }

    function createPhotons(count) {
        photonStream.innerHTML = '';
        const limit = Math.min(count, 12); // Don't overwhelm UI
        for (let i = 0; i < limit; i++) {
            const p = document.createElement('div');
            p.className = 'photon';
            p.style.top = (Math.random() * 80 + 10) + 'px';
            p.style.animation = `movePhoton ${1 + Math.random()}s linear ${i * 0.1}s forwards`;
            photonStream.appendChild(p);
        }
    }

    function highlightEve() {
        eveNode.classList.add('pulse');
        setTimeout(() => eveNode.classList.remove('pulse'), 1000);
    }

    function updateSummary(results) {
        summaryStats.innerHTML = `
            <div class="stat-card">
                <span class="stat-val">${results.qber.toFixed(1)}%</span>
                <span class="stat-label">QBER</span>
            </div>
            <div class="stat-card">
                <span class="stat-val">${results.mismatches ? results.mismatches.length : 0}</span>
                <span class="stat-label">Mismatches</span>
            </div>
            <div class="stat-card">
                <span class="stat-val">${results.qber < 11 ? 'Secure' : 'Insecure'}</span>
                <span class="stat-label">Status</span>
            </div>
        `;
    }

    function updateCharts(data, protocol) {
        const noiseLabels = data.noise.map(n => (n * 100).toFixed(0) + '%');
        
        if (qberChart) qberChart.destroy();
        if (yieldChart) yieldChart.destroy();

        const ctxQber = document.getElementById('qber-chart').getContext('2d');
        qberChart = new Chart(ctxQber, {
            type: 'line',
            data: {
                labels: noiseLabels,
                datasets: [
                    {
                        label: 'QBER (No Eve)',
                        data: data[`${protocol}_qber_no_eve`],
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'QBER (With Eve)',
                        data: data[`${protocol}_qber_with_eve`],
                        borderColor: '#e67e22',
                        backgroundColor: 'rgba(230, 126, 34, 0.1)',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'QBER vs Noise', color: '#fff' },
                    legend: { labels: { color: '#aaa' } }
                },
                scales: {
                    x: { ticks: { color: '#666' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { ticks: { color: '#666' }, grid: { color: 'rgba(255,255,255,0.05)' } }
                }
            }
        });

        const ctxYield = document.getElementById('yield-chart').getContext('2d');
        yieldChart = new Chart(ctxYield, {
            type: 'bar',
            data: {
                labels: noiseLabels,
                datasets: [
                    {
                        label: 'Key Yield (No Eve)',
                        data: data[`${protocol}_key_final_no_eve`],
                        backgroundColor: '#2ecc71'
                    },
                    {
                        label: 'Key Yield (With Eve)',
                        data: data[`${protocol}_key_final_with_eve`],
                        backgroundColor: '#c0392b'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Final Key Yield', color: '#fff' },
                    legend: { labels: { color: '#aaa' } }
                },
                scales: {
                    x: { ticks: { color: '#666' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { ticks: { color: '#666' }, grid: { color: 'rgba(255,255,255,0.05)' } }
                }
            }
        });
    }

    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
});
