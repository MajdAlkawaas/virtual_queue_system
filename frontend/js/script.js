document.addEventListener("DOMContentLoaded", function () {
    const darkModeToggle = document.getElementById("dark-mode-toggle");
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarCollapse = document.getElementById("navbarNav");

    // Ensure Bootstrap JavaScript is working
    if (typeof bootstrap !== "undefined") {
        navbarToggler.addEventListener("click", function () {
            navbarCollapse.classList.toggle("show");
        });

        // To Close Navbar When Clicking Outside
        document.addEventListener("click", function (event) {
            if (!navbarToggler.contains(event.target) && !navbarCollapse.contains(event.target)) {
                navbarCollapse.classList.remove("show");
            }
        });
    } else {
        console.error("Bootstrap JS not loaded!");
    }

    // Dark Mode Handling with Icons Only
    if (localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
        darkModeToggle.innerHTML = "☀️";
    } else {
        darkModeToggle.innerHTML = "🌙";
    }

    darkModeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "enabled" : "disabled");
        darkModeToggle.innerHTML = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
    });

    // for Smooth Scroll Effect
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute("href")).scrollIntoView({
                behavior: "smooth"
            });
        });
    });

    // Button Hover Effects (Updated Colors)
    document.querySelectorAll(".btn").forEach(btn => {
        btn.addEventListener("mouseover", function () {
            this.style.backgroundColor = getComputedStyle(document.documentElement).getPropertyValue('--accent-color');
        });
        btn.addEventListener("mouseleave", function () {
            this.style.backgroundColor = getComputedStyle(document.documentElement).getPropertyValue('--secondary-color');
        });
    });

    // Add Fade-in Effect on Scroll
    const fadeElements = document.querySelectorAll(".fade-in");
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    }, { threshold: 0.3 });

    fadeElements.forEach(element => observer.observe(element));
});
