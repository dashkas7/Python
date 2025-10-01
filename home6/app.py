'''
Создать базовый шаблон для FLASK со 
стандартной сеткой (flex или grid)
перенести свои страницы на этот шаблон
подписать каждый элемент сетки

применить к своим страницам какие-нибудь стили на свое усмотрение




---- необязательное задание для самых любопытных -----

* добавить на сайт меню для просмотра курсов нац банка на сегодня
     ссылка на API - https://www.nbrb.by/apihelp/exrates
     
** добавить на сайт в меню  конвертор валют на основе курсов nbrb.by 
    с пересчетом на любую дату по валютам BYN, USD, EURO, RUB
    
'''



from flask import Flask, render_template, request, redirect, url_for, session
import requests, random, re
from werkzeug.security import generate_password_hash, check_password_hash
from users import load_users, save_users
from decorators import login_required

app = Flask(__name__)
app.secret_key = "super_secret_key"

@app.route("/")
def index():
    user = session.get("user")
    return render_template("main.html", user=user)

@app.route("/duck/")
@login_required
def duck():
    data = requests.get("https://random-d.uk/api/random").json()
    return render_template("duck.html", duck_url=data["url"], duck_number=random.randint(1, 999))


@app.route("/fox/")
@app.route("/fox/<int:number>/")
@login_required
def fox(number=1):
    if number < 1 or number > 10:
        return '<h1 style="color:red; text-align:center;">Можно выбрать количество от 1 до 10</h1>'
    data = requests.get("https://randomfox.ca/floof/").json()
    return render_template("fox.html", foxs=[data["image"]] * number, number=number)


@app.route("/weather-minsk/")
@login_required
def weather_minsk():
    url = "https://api.open-meteo.com/v1/forecast?latitude=53.9&longitude=27.5667&current_weather=true"
    data = requests.get(url).json().get("current_weather", {})
    return render_template("weatherminsk.html", temp=data.get("temperature"), wind=data.get("windspeed"))


@app.route("/weather/")
@app.route("/weather/<city>/")
@login_required
def weather_city(city="Gomel"):
    geo_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json&limit=1"
    geo_resp = requests.get(geo_url, headers={"User-Agent": "Mozilla/5.0"}).json()
    if not geo_resp:
        return f"<h1>Город '{city}' не найден</h1>"

    lat, lon = geo_resp[0]["lat"], geo_resp[0]["lon"]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data = requests.get(url).json().get("current_weather", {})
    return render_template("weathercity.html", temp=data.get("temperature"), wind=data.get("windspeed"), city=city.capitalize())


@app.route("/dogs/")
@login_required
def dogs():
    return render_template("dogs.html", title="Породы собак")

@app.route("/registration/", methods=["GET", "POST"])
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
            errors.append("Имя только русскими буквами")
        if not re.fullmatch(r"[А-Яа-яЁё]+", surname or ""):
            errors.append("Фамилия только русскими буквами")
        if not age.isdigit() or not (12 <= int(age) <= 100):
            errors.append("Возраст от 12 до 100")
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email or ""):
            errors.append("Некорректный email")
        if not re.fullmatch(r"[A-Za-z0-9_]{6,20}", login_value or ""):
            errors.append("Логин: латиница/цифры/_, длина 6–20")
        if not re.fullmatch(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,15}", password or ""):
            errors.append("Пароль: строчная+заглавная+цифра, длина 8–15")

        users = load_users()
        if login_value in users:
            errors.append("Логин уже существует")

        if errors:
            return render_template("registration.html", errors=errors, form=request.form)

        users[login_value] = {
            "name": name, "surname": surname, "age": age, "email": email,
            "password": generate_password_hash(password)
        }
        save_users(users)
        return redirect(url_for("login"))

    return render_template("registration.html", errors=[], form={})

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_value = request.form.get("login")
        password = request.form.get("password")
        users = load_users()
        user = users.get(login_value)

        if user and check_password_hash(user["password"], password):
            session["user"] = {"login": login_value, "name": user["name"], "surname": user["surname"]}
            return redirect(url_for("index"))
        return render_template("login.html", error="Неверный логин или пароль", form=request.form)

    return render_template("login.html", error=None, form={})

@app.route("/homework/", endpoint="homework")
def homework():
    return render_template("homework.html")

@app.route("/logout/")
@login_required
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
@app.route("/rates/")
@login_required
def rates():
    url = "https://www.nbrb.by/api/exrates/rates?periodicity=0"
    try:
        response = requests.get(url)
        rates = response.json()
    except Exception as e:
        rates = None
    return render_template("rates.html", rates=rates)


@app.errorhandler(404)
def not_found(e):
    return '<h1 style="color:red;text-align:center;">Такой страницы нет</h1>'

if __name__ == "__main__":
    app.run(debug=True)
