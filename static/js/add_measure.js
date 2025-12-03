// add_measure.js

document.addEventListener("DOMContentLoaded", () => {
    const addForm = document.getElementById("addForm");
    const formMsg = document.getElementById("formMsg");

    if (!addForm) return;

    addForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const temp = parseFloat(document.getElementById("tempInput").value);
        const hum  = parseFloat(document.getElementById("humInput").value);

        formMsg.textContent = "Envoi en cours...";

        try {
            const res = await fetch("/api/post", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ temp, hum })  // ✅ keys match your backend
            });

            if (!res.ok) {
                const errText = await res.text();
                throw new Error(errText || "Erreur serveur");
            }

            formMsg.textContent = "✅ Mesure ajoutée !";
            addForm.reset();

            // refresh dashboard immediately
            if (typeof loadLatest === "function") loadLatest();

        } catch (err) {
            console.error("Erreur ajout:", err);
            formMsg.textContent = "❌ " + err.message;
        }
    });
});
