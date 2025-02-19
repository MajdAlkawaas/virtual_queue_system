document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("register-form");

    if (registerForm) {
        registerForm.addEventListener("submit", function (e) {
            e.preventDefault();

            // ✅ Collect Form Data
            const formData = {
                name: document.getElementById("name").value,
                email: document.getElementById("email").value,
                phone: document.getElementById("phone").value,
                issue: document.getElementById("issue").value,
                description: document.getElementById("description").value
            };

            // ✅ Save to Local Storage (Temporary Mock Data)
            localStorage.setItem("guestData", JSON.stringify(formData));

            // ✅ Redirect to Queue Dashboard (Adjust if API is used)
            alert("Registration Successful! Redirecting to Queue Dashboard...");
            window.location.href = "queue_dashboard.html";
        });
    }
});
