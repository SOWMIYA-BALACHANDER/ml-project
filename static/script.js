document.getElementById("prediction-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const brand = document.getElementById("brand").value.trim();
    const ram = document.getElementById("ram").value;
    const storage = document.getElementById("storage").value;
    const battery = document.getElementById("battery").value;

    // Show loading message
    document.getElementById("result").innerHTML = `<h3>🔄 Predicting...</h3>`;

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ brand, ram, storage, battery })
        });

        const data = await response.json();
        console.log("API Response:", data);

        if (data.predicted_price !== undefined) {
            document.getElementById("result").innerHTML = `<h2>💰 Predicted Price: ₹${data.predicted_price}</h2>`;
        } else {
            document.getElementById("result").innerHTML = `<h3 style="color: red;">⚠️ Error: ${data.error || "Unknown error"}</h3>`;
        }
    } catch (error) {
        console.error("Error fetching prediction:", error);
        document.getElementById("result").innerHTML = `<h3 style="color: red;">⚠️ Error predicting price. Try again.</h3>`;
    }
});
