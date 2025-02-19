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

    // Disable further clicks after rating
    starElements.forEach(star => {
        star.onclick = null;
    });
}

// Function to restore rating from local storage
document.addEventListener("DOMContentLoaded", function () {
    const savedRating = localStorage.getItem("guestRating");
    if (savedRating) {
        rateExperience(parseInt(savedRating));
    }
});
