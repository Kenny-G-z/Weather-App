from flask import Flask, render_template, request
from api import get_weather

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    error = None

    if request.method == "POST":
        city = request.form["city"]

        weather = get_weather(city)

        if weather is None:
            error = "City not found. Please try again."

    return render_template("Website.html", weather=weather, error=error)

app.run(debug=True)