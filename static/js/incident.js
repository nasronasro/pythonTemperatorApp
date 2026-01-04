// incident.js

async function loadIncident() {
    try {
        let res = await fetch("/api/incident/");
        if (!res.ok) {
            console.log("Erreur API, statut:", res.status);
            return;
        }

        let data = await res.json();

        const box = document.getElementById("incidentStatus");
        const link = document.getElementById("incidentLink");
        const form = document.getElementById("incidentForm");

        if (!box || !link || !form) return;

        if (data.incident === null) {
            box.innerHTML = "<span class='incident-normal'>Aucun incident</span>";
            link.style.display = "none";
            form.style.display = "none"; // cacher le formulaire
        } else {
            box.innerHTML =
                `<span class='incident-alert'>Incident actif</span><br>
                 Temp max : ${data.incident.temperature_max}°C<br>
                 Alertes : ${data.incident.compteur_alerte}<br>
                 Début : ${new Date(data.incident.date_debut).toLocaleString()}`;

            link.href = "/incident/" + data.incident.id + "/";
            link.style.display = "inline-block";

            // afficher le formulaire
            form.style.display = "block";

            // Ajouter le listener pour update
            const updateBtn = document.getElementById("updateIncidentBtn");
           updateBtn.onclick = async () => {
    const commentaire = document.getElementById("incidentComment").value;
    const resolu = document.getElementById("incidentResolved").checked;
    const accuse = document.getElementById("incidentAck").checked;

    try {
        const updateRes = await fetch(`/api/incident/${data.incident.id}/update/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                commentaire: commentaire,
                resolu: resolu,
                accuse_reception: accuse
            }),
        });

        if (!updateRes.ok) {
            alert("Erreur lors de la mise à jour de l'incident");
            return;
        }

        alert("Incident mis à jour avec succès !");
        loadIncident();
    } catch (err) {
        console.error("Erreur update incident:", err);
        alert("Erreur lors de la mise à jour de l'incident");
    }
};

        }

    } catch (e) {
        console.error("Erreur incident API:", e);
    }
}

// Chargement initial
loadIncident();

// Actualisation toutes les 20 secondes
setInterval(loadIncident, 20000);
