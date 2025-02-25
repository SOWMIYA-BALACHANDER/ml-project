from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load trained model, scaler, and label encoders
try:
    model = joblib.load("mobile_price_model.pkl")
    scaler = joblib.load("scaler.pkl")
    label_encoders = joblib.load("label_encoders.pkl")
    print("✅ Model, scaler, and encoders loaded successfully!")
except Exception as e:
    print("❌ Error loading model files:", e)
    model, scaler, label_encoders = None, None, None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None or scaler is None or label_encoders is None:
            return jsonify({"error": "Model files are missing. Check server logs."}), 500

        data = request.json
        if not data:
            return jsonify({"error": "Invalid input data"}), 400
        
        brand = data.get("brand", "").strip().title()
        ram = data.get("ram")
        storage = data.get("storage")
        battery = data.get("battery")

        # Validate input data
        if not brand or ram is None or storage is None or battery is None:
            return jsonify({"error": "Missing input values"}), 400

        # Convert to float
        try:
            ram = float(ram)
            storage = float(storage)
            battery = float(battery)
        except ValueError:
            return jsonify({"error": "RAM, Storage, and Battery must be numbers"}), 400

        # Encode brand
        brand_encoder = label_encoders["Brand"]
        if brand in brand_encoder.classes_:
            brand_encoded = brand_encoder.transform([brand])[0]
        else:
            print(f"⚠️ Warning: Brand '{brand}' not found. Assigning default value 0.")
            brand_encoded = 0

        # Prepare input as DataFrame
        user_input = pd.DataFrame([[brand_encoded, ram, storage, battery]], 
                                  columns=["Brand me", "RAM", "ROM", "Battery_Power"])

        # Scale input
        user_input_scaled = scaler.transform(user_input)

        # Predict price
        predicted_price = model.predict(user_input_scaled)[0]
        print(f"✅ Predicted Price: ₹{predicted_price}")
        return jsonify({"predicted_price": round(predicted_price, 2)})

    except Exception as e:
        print("❌ Error during prediction:", str(e))
        return jsonify({"error": "Prediction failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
