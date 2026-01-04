document.getElementById("sensorForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const tempInput = parseFloat(document.getElementById("tempInput").value);
    const humInput = parseFloat(document.getElementById("humInput").value);

    if (isNaN(tempInput) || isNaN(humInput)) {
        document.getElementById("responseMsg").textContent = "Valeurs invalides";
        return;
    }

    fetch("/push-data/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ temperature: tempInput, humidity: humInput })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("responseMsg").textContent = data.message || data.error;
    })
    .catch(err => {
        document.getElementById("responseMsg").textContent = "Erreur : " + err;
    });
});
