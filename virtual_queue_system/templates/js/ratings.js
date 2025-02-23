function rateExperience(stars) {
    const message = document.getElementById("rating-message");
    const starElements = document.querySelectorAll(".star");

    // Reset all stars to default color
    starElements.forEach((star, index) => {
        star.style.color = index < stars ? "gold" : "gray"; // Highlight selected stars
    });

    // Display thank-you message
    message.textContent = `Thank you! You rated us ${stars} ⭐`;

    // Store rating in local storage
    localStorage.setItem("guestRating", stars);

    // Send rating to backend 
    sendRatingToBackend(stars);
}

// Function to Send Rating to Backend API
function sendRatingToBackend(stars) {
    fetch("http://127.0.0.1:8000/api/submit-rating/", {  // Update with your actual API URL
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ rating: stars, guest_id: 1 })  // will Replace `1` with dynamic user ID
    })
    .then(response => response.json())
    .then(data => console.log("Rating Submitted:", data))
    .catch(error => console.error("Error submitting rating:", error));
}

// Restore rating from local storage when page loads
document.addEventListener("DOMContentLoaded", function () {
    const savedRating = localStorage.getItem("guestRating");
    if (savedRating) {
        rateExperience(parseInt(savedRating));
    }
});
