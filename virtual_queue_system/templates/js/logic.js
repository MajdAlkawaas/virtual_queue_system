document.addEventListener("DOMContentLoaded", function () {
    console.log("App Loaded");

    const registerForm = document.getElementById("register-form");
    const loginForm = document.getElementById("login-form");
    const forgotPasswordForm = document.getElementById("forgot-password-form");
    const messageBox = document.getElementById("form-message");
    const errorMessage = document.getElementById("error-message");

    /* ========================= REGISTER LOGIC ========================= */
    if (registerForm) {
        registerForm.addEventListener("submit", function (e) {
            e.preventDefault();

            // Collect Form Data
            const name = document.getElementById("name");
            const email = document.getElementById("email");
            const phone = document.getElementById("phone");
            const issue = document.getElementById("issue");
            const description = document.getElementById("description");

            // Reset error classes
            [name, email, phone, issue].forEach(field => field.classList.remove("is-invalid"));
            let isValid = true;

            // Input Validation
            if (name.value.trim() === "") name.classList.add("is-invalid"), isValid = false;
            if (!email.value.match(/^[^@]+@[^@]+\.[a-zA-Z]{2,}$/)) email.classList.add("is-invalid"), isValid = false;
            if (!phone.value.match(/^\d{10}$/)) phone.classList.add("is-invalid"), isValid = false;
            if (issue.value === "") issue.classList.add("is-invalid"), isValid = false;

            if (!isValid) return;

            // Show processing message
            messageBox.innerHTML = `<p class="text-info">Processing...</p>`;

            const formData = {
                name: name.value,
                email: email.value,
                phone: phone.value,
                issue: issue.value,
                description: description.value
            };

            // Send Data to Backend
            fetch("/api/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    sessionStorage.setItem("guestData", JSON.stringify(formData));
                    messageBox.innerHTML = `<p class="text-success">Registration Successful! Redirecting...</p>`;
                    setTimeout(() => window.location.href = "queue_dashboard.html", 1500);
                } else {
                    messageBox.innerHTML = `<p class="text-danger">${data.message || "Unknown error occurred."}</p>`;
                }
            })
            .catch(error => {
                messageBox.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
            });
        });
    }

    /* ========================= LOGIN LOGIC ========================= */
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const email = document.getElementById("email");
            const password = document.getElementById("password");

            // Reset error messages
            [email, password].forEach(field => field.classList.remove("is-invalid"));
            errorMessage.classList.add("d-none");

            let isValid = true;

            /* // Validation
            if (!email.value.match(/^[^@]+@[^@]+\.[a-zA-Z]{2,}$/)) email.classList.add("is-invalid"), isValid = false;
            if (password.value.trim().length < 6) password.classList.add("is-invalid"), isValid = false;

            if (!isValid) return; */

            // Show loading state
            errorMessage.innerHTML = `<p class="text-info">Logging in...</p>`;
            errorMessage.classList.remove("d-none");

            const loginData = {
                email: email.value,
                password: password.value
            };

            /*// Send Login Request to Backend
            fetch("/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(loginData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    sessionStorage.setItem("user", JSON.stringify(data.user));

                    // Redirect Based on User Role
                    const role = data.user.role;
                    const redirectPage = role === "manager" ? "manager_dashboard.html"
                                      : role === "operator" ? "operator_dashboard.html"
                                      : "queue_dashboard.html";

                    window.location.href = redirectPage;
                } else {
                    errorMessage.innerHTML = `<p class="text-danger">${data.message || "Invalid credentials."}</p>`;
                }
            })
            .catch(error => {
                errorMessage.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
            });*/
        });
    }

    /* ========================= FORGOT PASSWORD LOGIC ========================= */
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const email = document.getElementById("email");
            email.classList.remove("is-invalid");

            if (!email.value.match(/^[^@]+@[^@]+\.[a-zA-Z]{2,}$/)) {
                email.classList.add("is-invalid");
                return;
            }

            messageBox.innerHTML = `<p class="text-info">Processing...</p>`;

            fetch("/api/forgot-password", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email.value })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    messageBox.innerHTML = `<p class="text-success">Reset link sent! Check your email.</p>`;
                } else {
                    messageBox.innerHTML = `<p class="text-danger">${data.message || "Error sending reset link."}</p>`;
                }
            })
            .catch(error => {
                messageBox.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
            });
        });
    }

    /* ========================= LOGOUT LOGIC ========================= */
    if (window.location.pathname.includes("logout.html")) {
        console.log("Logging out user...");
        
        // Clear Session Storage
        sessionStorage.removeItem("user");

        // Countdown Before Redirecting
        let countdown = 3;
        const countdownElement = document.getElementById("countdown");

        const interval = setInterval(() => {
            countdown--;
            if (countdownElement) countdownElement.textContent = countdown;
            if (countdown === 0) {
                clearInterval(interval);
                window.location.href = "index.html"; // Redirect to home page
            }
        }, 1000);
    }
});
