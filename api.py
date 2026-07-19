import requests
import datetime
import sys

api_key = "60aa88ba4f408585988dc81483516b84"

print("Welcome to the Weather App!")
print("Enter 'quit' at anytime to conclude your session.")
print()

def exit_app():
    print()
    print("Thanks for using the Weather App!")
    sys.exit()

def get_input(prompt):
    user_input = input(prompt).lower()
    if user_input == "quit":
        exit_app()
    return user_input

while True:
    while True:
        city = get_input("Enter a city:     ")

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            break
        else:
            print("City not found; Please try again.")
            print()

    options = {"weather": data["weather"][0]["description"].title(),
            "temperature": f'{data["main"]["temp"]}°F',
            "humidity": f'{data["main"]["humidity"]}%',
            "feels like": f'{data["main"]["feels_like"]}°F',
            "sunrise": datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p"),
            "sunset": datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")}

    print("\nYou can ask for:")
    for option in options:
        print(f"- {option}")
    print()

    while True:
        user_req = get_input("What would you like to know?  ")
        if user_req in options:
            answer = options[user_req]
            print(user_req, ":", answer)
            print()
        else:
            print("Please choose one of the options.")
            print()
            continue
        
        while True:
            repeat = get_input("Would you like to know anything else? (y/n):      ")
            print()

            if repeat in ["y", "n"]:
                break
            else:
                print("Please enter y/n")

        if repeat == "n":
            break

    while True:
        another_city = get_input("Would you like to search another city? (y/n):     ")
        print()

        if another_city == "y":
            break
        elif another_city == "n":
            exit_app()
        else:
            print("Please enter y/n")
            print()