from flask import Flask, render_template, request, redirect, url_for, session
import requests
import random
import os
import re
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json

app = Flask(__name__)
app.secret_key = "super_secret_key"

USERS_FILE = "users.json"


# ------------------- Работа с пользователями -------------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


# ------------------- Декоратор для защиты -------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ------------------- Главная -------------------
@app.route("/")
def index():
    user = session.get("user")
    return render_template("main.html", user=user)


# ------------------- Уточки -------------------
@app.route("/duck/", endpoint="duck")
@login_required
def duck():
    response = requests.get("https://random-d.uk/api/random")
    data = response.json()
    duck_url = data["url"]
    duck_number = random.randint(1, 999)
    return render_template("duck.html", duck_url=duck_url, duck_number=duck_number)


# ------------------- Лисички -------------------
@app.route("/fox/", endpoint="fox")
@app.route("/fox/<int:number>/", endpoint="fox")
@login_required
def fox(number=None):
    if number is None:
        number = 1
    if number < 1 or number > 10:
        return '<h1 style="color:red; text-align:center; font-size:48px">Можно выбрать количество от 1 до 10</h1>'

    response = requests.get("https://randomfox.ca/floof/")
    data = response.json()
    fox_url = data["image"]

    foxs = [fox_url] * number
    return render_template("fox.html", foxs=foxs, number=number)


# ------------------- Погода в Минске -------------------
@app.route("/weather-minsk/", endpoint="weather_minsk")
@login_required
def weather_minsk():
    lat, lon = 53.9, 27.5667
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data = requests.get(url).json()

    weather = data.get("current_weather", {})
    temp = weather.get("temperature", "?")
    wind = weather.get("windspeed", "?")

    return render_template("weatherminsk.html", temp=temp, wind=wind)


# ------------------- Погода в любом городе -------------------
@app.route("/weather/", endpoint="weather_city")
@app.route("/weather/<city>/", endpoint="weather_city")
@login_required
def weather_city(city=None):
    if city is None:
        city = "Gomel"

    geo_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json&limit=1"
    geo_resp = requests.get(geo_url, headers={"User-Agent": "Mozilla/5.0"}).json()

    if not geo_resp:
        return f"<h1>Город '{city}' не найден</h1>"

    lat = geo_resp[0]["lat"]
    lon = geo_resp[0]["lon"]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data = requests.get(url).json()

    weather = data.get("current_weather", {})
    temp = weather.get("temperature", "?")
    wind = weather.get("windspeed", "?")

    return render_template("weathercity.html", temp=temp, wind=wind, city=city.capitalize())


# ------------------- Собаки -------------------
@app.route("/dogs/", endpoint="dogs")
@login_required
def animals():
    return render_template("dogs.html", title="Породы собак")


# ------------------- Регистрация -------------------
@app.route("/registration/", methods=["GET", "POST"], endpoint="registration")
def registration():
    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        age = request.form.get("age")
        email = request.form.get("email")
        login_value = request.form.get("login")
        password = request.form.get("password")

        errors = []

        if not re.fullmatch(r"[А-Яа-яЁё]+", name or ""):
            errors.append("Имя должно содержать только русские буквы.")
        if not re.fullmatch(r"[А-Яа-яЁё]+", surname or ""):
            errors.append("Фамилия должна содержать только русские буквы.")
        if not age.isdigit() or not (12 <= int(age) <= 100):
            errors.append("Возраст должен быть числом от 12 до 100.")
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email or ""):
            errors.append("Некорректный email.")
        if not re.fullmatch(r"[A-Za-z0-9_]{6,20}", login_value or ""):
            errors.append("Логин должен содержать латиницу, цифры и _, длина 6-20 символов.")
        if not re.fullmatch(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,15}", password or ""):
            errors.append("Пароль должен содержать хотя бы 1 строчную, 1 заглавную букву и 1 цифру (от 8 до 15 символов).")

        if errors:
            return render_template("registration.html", errors=errors, form=request.form)

        users = load_users()
        if login_value in users:
            errors.append("Такой логин уже существует.")
            return render_template("registration.html", errors=errors, form=request.form)

        users[login_value] = {
            "name": name,
            "surname": surname,
            "age": age,
            "email": email,
            "password": generate_password_hash(password),
        }
        save_users(users)

        return redirect(url_for("login"))

    return render_template("registration.html", errors=[], form={})


# ------------------- Вход -------------------
@app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "POST":
        login_value = request.form.get("login")
        password = request.form.get("password")

        users = load_users()
        user = users.get(login_value)

        if user and check_password_hash(user["password"], password):
            session["user"] = {
                "login": login_value,
                "name": user["name"],
                "surname": user["surname"],
            }
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Неверный логин или пароль", form=request.form)

    return render_template("login.html", error=None, form={})


# ------------------- Выход -------------------
@app.route("/logout/", endpoint="logout")
@login_required
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


# ------------------- Ошибка 404 -------------------
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red; text-align:center; font-size:48px">Такой страницы не существует</h1>'


if __name__ == "__main__":
    app.run(debug=True)
