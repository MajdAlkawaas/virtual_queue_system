document.addEventListener("DOMContentLoaded", function () {
    console.log("Queue Management Loaded ");

    // Queue DOM Elements
    const queuePositionElement = document.getElementById("queue-position");
    const waitTimeElement = document.getElementById("wait-time");
    const progressBar = document.getElementById("progress-bar");
    const queueList = document.getElementById("queue-list");
    const refreshQueueBtn = document.getElementById("refresh-queue");

    // Entertainment & Rating Elements
    const musicButton = document.querySelector(".btn-success");
    const gameButton = document.querySelector(".btn-primary[onclick='startGame()']");
    const feedbackButton = document.querySelector(".btn-primary.w-100");
    const stars = document.querySelectorAll(".star");
    const ratingMessage = document.getElementById("rating-message");
    const feedbackTextarea = document.getElementById("feedback");

    let queuePosition = 5;
    let estimatedWaitTime = queuePosition * 3; // Assuming 3 minutes per guest

    // Fetch Queue Data from Backend
    function fetchQueueData() {
        const guestId = localStorage.getItem("guest_id") || 1; // Default guest_id=1

        fetch(`http://127.0.0.1:8000/api/guest/${guestId}/`)
            .then(response => response.json())
            .then(data => {
                queuePositionElement.textContent = data.queue_number || "N/A";
                waitTimeElement.textContent = data.guests_ahead ? `${data.guests_ahead * 3} min` : "N/A";
                updateProgressBar(data.guests_ahead);
            })
            .catch(error => {
                console.error("Error fetching queue data:", error);
                queuePositionElement.textContent = "Error";
                waitTimeElement.textContent = "Error";
                progressBar.textContent = "Error Loading Data";
            });
    }

    // Update Progress Bar Dynamically
    function updateProgressBar(guestsAhead) {
        if (guestsAhead === 0) {
            progressBar.style.width = "100%";
            progressBar.innerText = "It's Your Turn!";
            progressBar.classList.add("bg-success");
        } else {
            let percentage = 100 - (guestsAhead * 10);
            progressBar.style.width = `${Math.max(10, percentage)}%`;
            progressBar.innerText = `Waiting...`;
            progressBar.classList.remove("bg-success");
        }
    }

    // Function to Refresh Queue List from Backend
    function refreshQueue() {
        fetch("http://127.0.0.1:8000/api/queue/")
            .then(response => response.json())
            .then(data => {
                queueList.innerHTML = "";
                data.forEach((guest, index) => {
                    let listItem = document.createElement("li");
                    listItem.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");
                    listItem.innerHTML = `
                        <span>${guest.name}</span>
                        <button class="btn btn-success serve-btn" data-id="${guest.id}">Serve</button>
                    `;
                    queueList.appendChild(listItem);
                });

                // Attach event listeners to new serve buttons
                document.querySelectorAll(".serve-btn").forEach(button => {
                    button.addEventListener("click", serveGuest);
                });

                console.log("Queue Updated ");
            })
            .catch(error => {
                console.error("Error fetching queue list:", error);
                queueList.innerHTML = `<p class="text-danger">Error loading queue data.</p>`;
            });
    }

    //  Serve Guest Functionality
    function serveGuest(event) {
        const guestId = event.target.getAttribute("data-id");
        const guestItem = event.target.closest(".list-group-item");

        fetch(`http://127.0.0.1:8000/api/serve-guest/${guestId}/`, {
            method: "POST",
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    guestItem.remove();
                    console.log(`Guest ${guestId} served `);
                }
            })
            .catch(error => console.error("Error serving guest:", error));
    }

    // Auto-refresh queue every 30 seconds
    setInterval(refreshQueue, 30000);
    fetchQueueData();
    refreshQueue();

    // Redirect to Game Page Instead of Alert
    function startGame() {
        window.location.href = "game.html";
    }

    // Placeholder Music Feature
    function playMusic() {
        alert("🎵 Music feature is coming soon!");
    }

    // Handle Star Rating
    function rateExperience(rating) {
        stars.forEach((star, index) => {
            star.style.color = index < rating ? "gold" : "gray";
        });

        ratingMessage.textContent = `Thank you for rating us ${rating} stars!`;
    }

    // Submit Feedback 
    function submitFeedback() {
        const feedback = feedbackTextarea.value.trim();
        if (feedback.length > 0) {
            feedbackTextarea.value = "";
            ratingMessage.textContent = "Thank you for your feedback!";
        } else {
            ratingMessage.textContent = "⚠ Please enter feedback before submitting.";
        }
    }

    // Event Listeners
    document.querySelector(".btn-info").addEventListener("click", fetchQueueData);
    musicButton.addEventListener("click", playMusic);
    gameButton.addEventListener("click", startGame);
    feedbackButton.addEventListener("click", submitFeedback);

    stars.forEach((star, index) => {
        star.addEventListener("click", () => rateExperience(index + 1));
    });

    refreshQueueBtn.addEventListener("click", refreshQueue);
});
