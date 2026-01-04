document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const res = await fetch("/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await res.json(); // on suppose que la réponse est JSON

        if (data.success) {
            window.location.href = "/dashboard/"; // redirection vers ton dashboard
        } else {
            document.getElementById("error-message").textContent = data.error;
        }

    } catch (err) {
        console.log("Erreur JS fetch :", err);
        document.getElementById("error-message").textContent = "Erreur serveur, réessayez.";
    }
});
