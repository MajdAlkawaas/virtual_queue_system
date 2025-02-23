document.addEventListener("DOMContentLoaded", function () {
    console.log("Manager Dashboard Loaded");

    /* ================== FETCH MANAGER DETAILS ================== */
    function fetchManagerDetails() {
        fetch("/api/manager/details")
            .then(response => response.json())
            .then(data => {
                document.getElementById("manager-name").textContent = data.name || "N/A";
                document.getElementById("manager-id").textContent = data.manager_id || "N/A";
            })
            .catch(error => showError("Error fetching manager details."));
    }

    /* ================== FETCH QUEUE & OPERATOR DATA ================== */
    function fetchQueues() {
        const queueList = document.getElementById("queue-list");
        queueList.innerHTML = `<tr><td colspan="6" class="text-center">Loading...</td></tr>`;

        fetch("/api/queues")
            .then(response => response.json())
            .then(data => {
                queueList.innerHTML = "";
                if (data.length === 0) {
                    queueList.innerHTML = `<tr><td colspan="6" class="text-center">No active queues.</td></tr>`;
                    return;
                }

                data.forEach((queue, index) => {
                    queueList.innerHTML += `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${queue.name}</td>
                            <td>${queue.operator || "Unassigned"}</td>
                            <td>${queue.guests_count}</td>
                            <td>${queue.avg_wait_time || "N/A"} mins</td>
                            <td>
                                <button class="btn btn-danger btn-sm remove-queue" data-id="${queue.id}">🗑️ Remove</button>
                            </td>
                        </tr>
                    `;
                });

                // Attach event listeners after rendering
                document.querySelectorAll(".remove-queue").forEach(button => {
                    button.addEventListener("click", removeQueue);
                });
            })
            .catch(error => showError("Error fetching queues."));
    }

    function fetchOperators() {
        const operatorList = document.getElementById("operator-list");
        operatorList.innerHTML = `<tr><td colspan="5" class="text-center">Loading...</td></tr>`;

        fetch("/api/operators")
            .then(response => response.json())
            .then(data => {
                operatorList.innerHTML = "";
                if (data.length === 0) {
                    operatorList.innerHTML = `<tr><td colspan="5" class="text-center">No active operators.</td></tr>`;
                    return;
                }

                data.forEach((operator, index) => {
                    operatorList.innerHTML += `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${operator.name}</td>
                            <td>${operator.operator_id}</td>
                            <td>${operator.queue_load || "N/A"}</td>
                            <td>
                                <button class="btn btn-warning btn-sm modify-operator" data-id="${operator.id}">⚙ Modify</button>
                            </td>
                        </tr>
                    `;
                });

                // Attach event listeners after rendering
                document.querySelectorAll(".modify-operator").forEach(button => {
                    button.addEventListener("click", modifyOperator);
                });
            })
            .catch(error => showError("Error fetching operators."));
    }

    /* ================== REMOVE QUEUE ================== */
    function removeQueue(event) {
        const queueId = event.target.dataset.id;
        if (!confirm("Are you sure you want to remove this queue?")) return;

        fetch(`/api/queues/${queueId}`, { method: "DELETE" })
            .then(response => {
                if (!response.ok) throw new Error("Failed to delete queue.");
                return response.json();
            })
            .then(() => {
                alert("Queue removed successfully.");
                fetchQueues(); // Refresh data
            })
            .catch(error => showError("Error removing queue."));
    }

    /* ================== MODIFY OPERATOR ================== */
    function modifyOperator(event) {
        const operatorId = event.target.dataset.id;
        alert(`Modify Operator feature for ID: ${operatorId} is under development!`);
    }

    /* ================== QR CODE GENERATION ================== */
    function generateQRCode() {
        fetch("/api/generate_qr")
            .then(response => response.json())
            .then(data => {
                if (!data.qr_link) throw new Error("Invalid QR response.");
                alert("📌 QR Code Generated: " + data.qr_link);
                window.open(data.qr_link, "_blank");
            })
            .catch(error => showError("Error generating QR Code."));
    }

    /* ================== ERROR HANDLING ================== */
    function showError(message) {
        alert(`❌ ${message}`);
    }

    /* ================== EVENT LISTENERS ================== */
    document.getElementById("generate-qrcode").addEventListener("click", generateQRCode);
    document.getElementById("add-queue").addEventListener("click", () => alert("Queue creation feature coming soon!"));

    /* ================== INITIAL DATA LOAD ================== */
    fetchManagerDetails();
    fetchQueues();
    fetchOperators();
});
