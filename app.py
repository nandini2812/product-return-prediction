from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained ML model
model = joblib.load("return_model.pkl")


@app.route("/", methods=["GET"])
def home():
    return render_template(
        "index.html",
        probability=None,
        risk=None,
        price="",
        quantity="",
        discount="",
        age=""
    )


# Function to make prediction
def predict_return(input_data):
    df = pd.DataFrame([input_data])
    probability = model.predict_proba(df)[0][1] * 100
    return round(probability, 2)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])
        discount = float(request.form["discount"])
        age = int(request.form["age"])

        if price < 0 or quantity <= 0 or discount < 0 or age <= 0:
            raise ValueError("Invalid input values")

        input_data = {
            "price": price,
            "quantity": quantity,
            "discount": discount,
            "age": age
        }

        probability = predict_return(input_data)

        if probability > 60:
         risk = "High"
        elif probability > 30:
         risk = "Medium"
        else:
         risk = "Low"

        # DEBUG PRINTS
        print("PROBABILITY:", probability)
        print("RISK:", risk)

        return render_template(
        "index.html",
        probability=probability,
        risk=risk,
        price=price,
        quantity=quantity,
        discount=discount,
        age=age
       )


    except Exception as e:
        return render_template(
            "index.html",
            probability=None,
            risk=None,
            error=str(e)
        )


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
