document.addEventListener("DOMContentLoaded", function () {
    const queuePositionElement = document.getElementById("queue-position");
    const waitTimeElement = document.getElementById("wait-time");
    const progressBar = document.getElementById("progress-bar");

    const musicButton = document.querySelector(".btn-success");
    const gameButton = document.querySelector(".btn-primary[onclick='startGame()']");
    const feedbackButton = document.querySelector(".btn-primary.w-100");

    const stars = document.querySelectorAll(".star");
    const ratingMessage = document.getElementById("rating-message");
    const feedbackTextarea = document.getElementById("feedback");

    let queuePosition = 5;
    let estimatedWaitTime = 10;

    // ✅ Function to Simulate Queue Update
    function updateQueue() {
        if (queuePosition > 1) {
            queuePosition -= 1;
            estimatedWaitTime -= 2;
        } else {
            queuePosition = 1;
            estimatedWaitTime = 0;
        }

        queuePositionElement.textContent = queuePosition;
        waitTimeElement.textContent = `${estimatedWaitTime} min`;

        let progressPercentage = ((10 - queuePosition) / 10) * 100;
        progressBar.style.width = `${progressPercentage}%`;

        if (queuePosition === 1) {
            progressBar.textContent = "It's Your Turn!";
            progressBar.classList.add("bg-success");
        } else {
            progressBar.textContent = "Queue Progress";
            progressBar.classList.remove("bg-success");
        }
    }

    // ✅ Redirect to Game Page Instead of Alert
    function startGame() {
        window.location.href = "game.html"; // Directs to game.html
    }

    // ✅ Placeholder Music Feature
    function playMusic() {
        alert("🎵 Music feature is coming soon!");
    }

    // ✅ Handle Star Rating
    function rateExperience(rating) {
        stars.forEach((star, index) => {
            star.style.color = index < rating ? "gold" : "gray";
        });

        ratingMessage.textContent = `Thank you for rating us ${rating} stars!`;
    }

    // ✅ Submit Feedback with UI Enhancement
    function submitFeedback() {
        const feedback = feedbackTextarea.value.trim();
        if (feedback.length > 0) {
            feedbackTextarea.value = "";
            ratingMessage.textContent = "Thank you for your feedback!";
        } else {
            ratingMessage.textContent = "⚠ Please enter feedback before submitting.";
        }
    }

    // ✅ Event Listeners
    document.querySelector(".btn-info").addEventListener("click", updateQueue);
    musicButton.addEventListener("click", playMusic);
    gameButton.addEventListener("click", startGame);
    feedbackButton.addEventListener("click", submitFeedback);

    stars.forEach((star, index) => {
        star.addEventListener("click", () => rateExperience(index + 1));
    });
});

document.addEventListener("DOMContentLoaded", function () {
    console.log("Queue Management Loaded ✅");

    const queueList = document.getElementById("queue-list");
    const refreshQueueBtn = document.getElementById("refresh-queue");

    // ✅ Serve Guest Functionality
    function serveGuest(event) {
        const guestItem = event.target.closest(".list-group-item");
        const guestName = guestItem.querySelector("span").textContent;

        // Move to history log
        addToHistory(guestName);

        // Remove from queue
        guestItem.remove();

        // Update analytics
        updateAnalytics();
    }

    // ✅ Refresh Queue (Simulating Incoming Guests)
    function refreshQueue() {
        queueList.innerHTML = ""; // Clear queue

        let newGuests = [
            "Guest A", "Guest B", "Guest C", "Guest D", "Guest E"
        ];

        newGuests.forEach((guest) => {
            let listItem = document.createElement("li");
            listItem.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");
            listItem.innerHTML = `
                <span>${guest}</span>
                <button class="btn btn-success serve-btn">✅ Serve</button>
            `;
            queueList.appendChild(listItem);
        });

        // Attach event listeners to new serve buttons
        document.querySelectorAll(".serve-btn").forEach(button => {
            button.addEventListener("click", serveGuest);
        });

        console.log("Queue Updated 🔄");
    }

    // ✅ Attach Event Listeners
    refreshQueueBtn.addEventListener("click", refreshQueue);
    document.querySelectorAll(".serve-btn").forEach(button => {
        button.addEventListener("click", serveGuest);
    });

    // ✅ Auto-refresh queue every 30 seconds
    setInterval(refreshQueue, 30000);
});

