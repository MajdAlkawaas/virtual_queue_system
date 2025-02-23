document.addEventListener("DOMContentLoaded", function () {
    const darkModeToggle = document.getElementById("dark-mode-toggle");
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarCollapse = document.getElementById("navbarNav");

    // Bootstrap JavaScript is loaded before using navbar toggling
    if (typeof bootstrap !== "undefined") {
        navbarToggler.addEventListener("click", function () {
            navbarCollapse.classList.toggle("show");
        });

        // Close Navbar When Clicking Outside
        document.addEventListener("click", function (event) {
            if (!navbarToggler.contains(event.target) && !navbarCollapse.contains(event.target)) {
                navbarCollapse.classList.remove("show");
            }
        });
    } else {
        console.error("Bootstrap JS not loaded!");
    }

    // Dark Mode Handling
    function updateDarkModeIcon() {
        darkModeToggle.innerHTML = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
    }

    if (localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
    }
    updateDarkModeIcon();

    darkModeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "enabled" : "disabled");
        updateDarkModeIcon();
    });

    // Smooth Scroll Handling (Prevents Errors)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            const target = document.querySelector(this.getAttribute("href"));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: "smooth" });
            }
        });
    });

    // Button Hover Effects 
    document.querySelectorAll(".btn").forEach(btn => {
        btn.addEventListener("mouseover", function () {
            this.style.backgroundColor = getComputedStyle(document.documentElement).getPropertyValue("--accent-color");
        });
        btn.addEventListener("mouseleave", function () {
            this.style.backgroundColor = "";
        });
    });

    // Add Fade-in Effect on Scroll 
    const fadeElements = document.querySelectorAll(".fade-in");
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                }
            });
        }, { threshold: 0.3 });

        fadeElements.forEach(element => observer.observe(element));
    } else {
        // Fallback for older browsers 
        fadeElements.forEach(element => element.classList.add("visible"));
    }
});
