document.addEventListener("DOMContentLoaded", function () {
    console.log("Analytics Module Loaded");

    // Elements to Display Data
    const totalServedEl = document.getElementById("total-served");
    const avgWaitTimeEl = document.getElementById("avg-wait-time");
    const peakTimeEl = document.getElementById("peak-time");
    const queueLoadEl = document.getElementById("queue-load");

    let timestamps = [];
    let servedData = [];
    let waitTimeData = [];

    //  Fetch Initial Data
    fetchAnalyticsData();
    getQueuePredictions();

    // Auto-refresh every 30 seconds
    setInterval(fetchAnalyticsData, 30000);

    //  Initialize Chart.js for Analytics
    const ctx = document.getElementById("analyticsChart").getContext("2d");
    let analyticsChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: timestamps,
            datasets: [
                {
                    label: "Guests Served",
                    data: servedData,
                    borderColor: "#0FA3B1",
                    backgroundColor: "rgba(15, 163, 177, 0.2)",
                    borderWidth: 2,
                    fill: true
                },
                {
                    label: "Avg Wait Time (min)",
                    data: waitTimeData,
                    borderColor: "#FFD60A",
                    backgroundColor: "rgba(255, 214, 10, 0.2)",
                    borderWidth: 2,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: getChartColors().text } }
            },
            scales: {
                x: { ticks: { color: getChartColors().text }, grid: { color: getChartColors().grid } },
                y: { ticks: { color: getChartColors().text }, grid: { color: getChartColors().grid } }
            }
        }
    });

    /* ================= FETCH LIVE ANALYTICS DATA ================= */
    function fetchAnalyticsData() {
        fetch("/api/analytics/live")
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
                    updateAnalyticsChart(data);
                    updateSummaryStats(data);
                } else {
                    showErrorOnChart();
                }
            })
            .catch(error => {
                console.error("Error fetching analytics data:", error);
                showErrorOnChart();
            });
    }

    /* ================= UPDATE SUMMARY STATS ================= */
    function updateSummaryStats(data) {
        if (!data || data.length === 0) {
            totalServedEl.textContent = "0";
            avgWaitTimeEl.textContent = "N/A";
            peakTimeEl.textContent = "N/A";
            queueLoadEl.textContent = "N/A";
            return;
        }

        const totalServed = data.reduce((sum, entry) => sum + (entry.guestsServed || 0), 0);
        const avgWaitTime = (data.reduce((sum, entry) => sum + (entry.waitTime || 0), 0) / data.length).toFixed(1);

        totalServedEl.textContent = totalServed;
        avgWaitTimeEl.textContent = `${avgWaitTime} min`;
    }

    /* ================= UPDATE ANALYTICS CHART ================= */
    function updateAnalyticsChart(data) {
        timestamps = data.map(entry => entry.timestamp || "N/A");
        servedData = data.map(entry => entry.guestsServed || 0);
        waitTimeData = data.map(entry => entry.waitTime || 0);

        analyticsChart.data.labels = timestamps;
        analyticsChart.data.datasets[0].data = servedData;
        analyticsChart.data.datasets[1].data = waitTimeData;
        analyticsChart.update();
    }

    /* ================= GET AI QUEUE PREDICTIONS ================= */
    function getQueuePredictions() {
        fetch("/api/queue/predict")
            .then(response => response.json())
            .then(data => {
                peakTimeEl.textContent = data.peakTime || "N/A";
                queueLoadEl.textContent = data.queueLoad || "N/A";
            })
            .catch(error => console.error("Error fetching AI predictions:", error));
    }

    /* ================= HANDLE CHART ERROR STATE ================= */
    function showErrorOnChart() {
        analyticsChart.data.labels = ["No Data"];
        analyticsChart.data.datasets.forEach(dataset => dataset.data = [0]);
        analyticsChart.update();
    }

    /* ================= DARK MODE SUPPORT ================= */
    function applyDarkModeToChart() {
        const colors = getChartColors();
        analyticsChart.options.scales.x.ticks.color = colors.text;
        analyticsChart.options.scales.y.ticks.color = colors.text;
        analyticsChart.options.scales.x.grid.color = colors.grid;
        analyticsChart.options.scales.y.grid.color = colors.grid;
        analyticsChart.update();
    }

    // Monitor Dark Mode Toggle
    document.getElementById("dark-mode-toggle").addEventListener("click", () => {
        setTimeout(() => {
            applyDarkModeToChart();
        }, 200);
    });

    //  Get Chart Colors Based on Dark/Light Mode
    function getChartColors() {
        return document.body.classList.contains("dark-mode")
            ? { text: "white", grid: "rgba(255, 255, 255, 0.2)", background: "#002b5b" }
            : { text: "black", grid: "rgba(0, 0, 0, 0.1)", background: "white" };
    }

    /*  Expose Functions Globally */
    window.fetchAnalyticsData = fetchAnalyticsData;
    window.getQueuePredictions = getQueuePredictions;
});
