document.addEventListener("DOMContentLoaded", function () {
    console.log("Operator Dashboard Loaded");

    const operatorNameEl = document.getElementById("operator-name");
    const operatorIdEl = document.getElementById("operator-id");
    const operatorLeavesEl = document.getElementById("operator-leaves");
    const queueListEl = document.getElementById("queue-list");
    const customersAssistedEl = document.getElementById("customers-assisted");
    const avgServiceTimeEl = document.getElementById("avg-service-time");

    let timestamps = [];
    let servedData = [];

    fetchOperatorDetails();
    fetchQueueData();
    fetchPerformanceData();

    // Auto-refresh queue every 30 seconds
    setInterval(fetchQueueData, 30000);

    // Initialize Performance Chart
    const ctx = document.getElementById("performanceChart").getContext("2d");
    let performanceChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: timestamps,
            datasets: [
                {
                    label: "Customers Assisted",
                    data: servedData,
                    backgroundColor: "#0077B6",
                    borderColor: "#005F9E",
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: { ticks: { color: getChartColors().text } },
                y: { ticks: { color: getChartColors().text } }
            }
        }
    });

    // Fetch Operator Details
    function fetchOperatorDetails() {
        fetch("/api/operator/details")
            .then(response => response.json())
            .then(data => {
                operatorNameEl.textContent = data.name || "N/A";
                operatorIdEl.textContent = data.operatorId || "N/A";
            })
            .catch(error => console.error("Error fetching operator details:", error));
    }

    // Fetch Live Queue Data
    function fetchQueueData() {
        fetch("/api/operator/queue")
            .then(response => response.json())
            .then(data => {
                queueListEl.innerHTML = "";
                if (data.length === 0) {
                    queueListEl.innerHTML = `<tr><td colspan="6" class="text-center">No guests in queue</td></tr>`;
                    return;
                }

                data.forEach((guest, index) => {
                    queueListEl.innerHTML += `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${guest.name}</td>
                            <td>${guest.contact}</td>
                            <td>${guest.issue}</td>
                            <td>${guest.estimatedServiceTime} mins</td>
                            <td>
                                <button class="btn btn-success btn-sm">Serve</button>
                            </td>
                        </tr>`;
                });
            })
            .catch(error => console.error("Error fetching queue data:", error));
    }

    // Fetch Performance Data
    function fetchPerformanceData() {
        fetch("/api/operator/performance")
            .then(response => response.json())
            .then(data => {
                customersAssistedEl.textContent = data.customersAssisted || "0";
                avgServiceTimeEl.textContent = `${data.avgServiceTime || 0} mins`;

                timestamps = data.performanceHistory.map(entry => entry.date);
                servedData = data.performanceHistory.map(entry => entry.customers);

                performanceChart.data.labels = timestamps;
                performanceChart.data.datasets[0].data = servedData;
                performanceChart.update();
            })
            .catch(error => console.error("Error fetching performance data:", error));
    }

    // Get Chart Colors Based on Dark/Light Mode
    function getChartColors() {
        return document.body.classList.contains("dark-mode")
            ? { text: "white" }
            : { text: "black" };
    }
});
