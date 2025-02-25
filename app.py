from flask import Flask, request, jsonify, send_file, render_template
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__, template_folder=".")

# Load trained model, scaler, and label encoders
model = joblib.load("mobile_price_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/style.css")
def serve_css():
    return send_file("style.css", mimetype="text/css")

@app.route("/script.js")
def serve_js():
    return send_file("script.js", mimetype="application/javascript")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        brand = data.get("brand", "").strip().title()
        ram = float(data.get("ram", 0))
        storage = float(data.get("storage", 0))
        battery = float(data.get("battery", 0))

        # Prevent negative or zero values
        if ram <= 0 or storage <= 0 or battery <= 0:
            return jsonify({"error": "Invalid input. RAM, Storage, and Battery must be positive values."}), 400

        # Encode brand
        brand_encoder = label_encoders["Brand"]
        brand_encoded = brand_encoder.transform([brand])[0] if brand in brand_encoder.classes_ else 0

        # Prepare input
        user_input = pd.DataFrame([[brand_encoded, ram, storage, battery]], 
                                  columns=["Brand me", "RAM", "ROM", "Battery_Power"])

        # Scale input
        user_input_scaled = scaler.transform(user_input)

        # Predict price
        predicted_price = max(0, model.predict(user_input_scaled)[0])  # Prevent negative output
        return jsonify({"predicted_price": round(predicted_price, 2)})

    except Exception as e:
        return jsonify({"error": "Prediction failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
