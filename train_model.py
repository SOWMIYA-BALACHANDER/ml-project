import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression

# Load dataset
file_path = "Mobile Price.csv"  
df = pd.read_csv(file_path)

# Check if required columns exist
required_columns = ["Brand me", "RAM", "ROM", "Battery_Power", "Price"]
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

# Handle missing values
df.dropna(subset=["Brand me"], inplace=True)  
df.fillna(df.mean(numeric_only=True), inplace=True)

# Encode the Brand column
label_encoder = LabelEncoder()
df["Brand me"] = label_encoder.fit_transform(df["Brand me"])

# Select features and target
X = df[["Brand me", "RAM", "ROM", "Battery_Power"]]
y = df["Price"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Save model, scaler, and label encoder
joblib.dump(model, "mobile_price_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump({"Brand": label_encoder}, "label_encoders.pkl")

print("✅ Model training complete. Files saved successfully!")
