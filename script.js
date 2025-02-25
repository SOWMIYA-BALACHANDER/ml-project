document.getElementById("prediction-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const brand = document.getElementById("brand").value.trim();
    const ram = parseFloat(document.getElementById("ram").value);
    const storage = parseFloat(document.getElementById("storage").value);
    const battery = parseFloat(document.getElementById("battery").value);

    // Prevent negative or zero values
    if (ram <= 0 || storage <= 0 || battery <= 0) {
        alert("❌ Please enter valid positive values for RAM, Storage, and Battery.");
        return;
    }

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
            document.getElementById("result").innerHTML = `<h2>💰 Predicted Price: ₹${Math.max(0, data.predicted_price)}</h2>`;
        } else {
            document.getElementById("result").innerHTML = `<h3 style="color: red;">⚠️ Error: ${data.error || "Unknown error"}</h3>`;
        }
    } catch (error) {
        console.error("Error fetching prediction:", error);
        document.getElementById("result").innerHTML = `<h3 style="color: red;">⚠️ Error predicting price. Try again.</h3>`;
    }
});
