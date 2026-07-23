from flask import Flask, render_template, request
from api import get_weather
import datetime

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])

def home():
    weather = None
    error = None
    current_hour = datetime.datetime.now().hour

    if 7 <= current_hour < 19:
        theme = "day"
    else:
        theme = "night"

    if request.method == "POST":
        city = request.form["city"]
        weather = get_weather(city)

        if weather is None:
            error = "City not found. Please try again."
            theme = request.form.get("theme", theme)
        else:
            theme = weather["theme"]

    return render_template(
        "Website.html",
        weather=weather,
        error=error,
        theme=theme
    )

app.run(debug=True)