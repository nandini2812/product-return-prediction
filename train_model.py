import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv(r"C:\Users\Nandini Thapliyal\Downloads\dataset return.csv")

# Rename columns
df = df.rename(columns={
    "Product_Price": "price",
    "Order_Quantity": "quantity",
    "Discount_Applied": "discount",
    "User_Age": "age",
    "Return_Status": "returned"
})

# --- CLEAN TARGET COLUMN (IMPORTANT) ---
df["returned"] = df["returned"].astype(str).str.strip().str.lower()

df["returned"] = df["returned"].map({
    "yes": 1,
    "no": 0,
    "returned": 1,
    "not returned": 0,
    "1": 1,
    "0": 0
})

# Drop rows where target is still NaN
df = df.dropna(subset=["returned"])

# Select features and target
X = df[["price", "quantity", "discount", "age"]]
y = df["returned"]

# Handle missing feature values
X = X.fillna(X.median())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

# Train model
pipeline.fit(X_train, y_train)

# Save model
joblib.dump(pipeline, "return_model.pkl")

print("Model trained and saved successfully!")
print("Target distribution:")
print(y.value_counts())
print("Features used:", X.columns.tolist())
