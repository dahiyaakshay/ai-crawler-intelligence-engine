const API_BASE = "http://127.0.0.1:8000";

let scoreChart, depthChart, scatterChart, burstChart;

async function uploadLog() {
    const fileInput = document.getElementById("logFile");
    const file = fileInput.files[0];
    if (!file) return alert("Select a log file.");

    const formData = new FormData();
    formData.append("file", file);

    await fetch(`${API_BASE}/upload`, { method: "POST", body: formData });
    loadDashboard();
}

async function loadDashboard() {
    await loadSummary();
    await loadBots();
}

async function loadSummary() {
    const res = await fetch(`${API_BASE}/summary`);
    const data = await res.json();

    document.getElementById("totalBots").textContent = data.total_bots || 0;
    document.getElementById("aiBots").textContent = data.ai_bots || 0;
    document.getElementById("suspiciousBots").textContent = data.suspicious_bots || 0;
    document.getElementById("avgScore").textContent =
        data.average_ai_score ? Number(data.average_ai_score).toFixed(2) : 0;
}

async function loadBots() {
    const res = await fetch(`${API_BASE}/bots`);
    const bots = await res.json();

    const tbody = document.querySelector("#botsTable tbody");
    tbody.innerHTML = "";

    const scores = [];
    const depths = [];
    const bursts = [];
    const scatterData = [];

    bots.forEach((bot, i) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${bot.ip_address}</td>
            <td>${bot.user_agent}</td>
            <td>${bot.total_requests}</td>
            <td>${bot.avg_url_depth}</td>
            <td>${bot.burst_rate}</td>
            <td class="score">${bot.ai_score}</td>
            <td class="${bot.bot_type}">${bot.bot_type}</td>
        `;
        tbody.appendChild(row);

        scores.push(bot.ai_score);
        depths.push(bot.avg_url_depth);
        bursts.push(bot.burst_rate);

        scatterData.push({
            x: bot.avg_url_depth,
            y: bot.ai_score
        });
    });

    renderScoreDistribution(scores);
    renderDepthChart(depths);
    renderBurstChart(bursts);
    renderScatter(scatterData);
    generateIntelligenceSummary(bots);
}

function renderScoreDistribution(scores) {
    const buckets = [0,0,0,0,0];
    scores.forEach(score => {
        if (score < 20) buckets[0]++;
        else if (score < 40) buckets[1]++;
        else if (score < 60) buckets[2]++;
        else if (score < 80) buckets[3]++;
        else buckets[4]++;
    });

    if (scoreChart) scoreChart.destroy();
    scoreChart = new Chart(document.getElementById("scoreDistributionChart"), {
        type: "bar",
        data: {
            labels: ["0-20","20-40","40-60","60-80","80-100"],
            datasets: [{
                label: "Bots",
                data: buckets,
                backgroundColor: "#FF6B35"
            }]
        },
        options: darkOptions()
    });
}

function renderDepthChart(depths) {
    if (depthChart) depthChart.destroy();
    depthChart = new Chart(document.getElementById("depthChart"), {
        type: "bar",
        data: {
            labels: depths.map((_, i) => `Bot ${i+1}`),
            datasets: [{
                label: "Avg Depth",
                data: depths,
                backgroundColor: "#ffa366"
            }]
        },
        options: darkOptions()
    });
}

function renderBurstChart(bursts) {
    if (burstChart) burstChart.destroy();
    burstChart = new Chart(document.getElementById("burstChart"), {
        type: "bar",
        data: {
            labels: bursts.map((_, i) => `Bot ${i+1}`),
            datasets: [{
                label: "Burst Rate",
                data: bursts,
                backgroundColor: "#ff944d"
            }]
        },
        options: darkOptions()
    });
}

function renderScatter(data) {
    if (scatterChart) scatterChart.destroy();
    scatterChart = new Chart(document.getElementById("scatterChart"), {
        type: "scatter",
        data: {
            datasets: [{
                label: "Depth vs AI Score",
                data: data,
                backgroundColor: "#FF6B35"
            }]
        },
        options: {
            ...darkOptions(),
            scales: {
                x: { title: { display: true, text: "Avg URL Depth", color: "#fff" }, ticks: { color: "#fff" }},
                y: { title: { display: true, text: "AI Score", color: "#fff" }, ticks: { color: "#fff" }}
            }
        }
    });
}

function generateIntelligenceSummary(bots) {
    let aiLike = bots.filter(b => b.ai_score >= 60).length;
    let suspicious = bots.filter(b => b.ai_score >= 30 && b.ai_score < 60).length;

    const summary = `
        <p>Total analyzed bots: <strong>${bots.length}</strong></p>
        <p>High likelihood AI retrieval patterns: <strong>${aiLike}</strong></p>
        <p>Moderate retrieval signals detected: <strong>${suspicious}</strong></p>
        <p>Behavioral clustering indicates deeper crawl depth correlates with higher AI scoring.</p>
    `;

    document.getElementById("intelligenceSummary").innerHTML = summary;
}

function darkOptions() {
    return {
        scales: {
            x: { ticks: { color: "#ffffff" }},
            y: { ticks: { color: "#ffffff" }, beginAtZero: true }
        },
        plugins: {
            legend: { labels: { color: "#ffffff" }}
        }
    };
}

window.onload = loadDashboard;
