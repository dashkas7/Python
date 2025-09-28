'''Написать веб-приложение на Flask со следующими ендпоинтами:
    - главная страница - содержит ссылки на все остальные страницы
    - /duck/ - отображает заголовок "рандомная утка №ххх" и картинка утки 
                которую получает по API https://random-d.uk/api/random
                
    - /fox/<int>/ - аналогично утке только с лисой (- https://randomfox.ca), 
                    но количество разных картинок определено int. 
                    если int больше 10 или меньше 1 - вывести сообщение 
                    что можно только от 1 до 10
    
    - /weather-minsk/ - показывает погоду в минске в красивом формате
    
    - /weather/<city>/ - показывает погоду в городе указанного в city
                    если такого города нет - н аписать об этом
    
    - по желанию добавить еще один ендпоинт на любую тему 
    
    
Добавить обработчик ошибки 404. (есть в example)'''

from flask import Flask, render_template
import requests
import random

app =Flask(__name__)

@app.route("/")
def index():
    return render_template('main.html', admin=True)

@app.route("/duck/")
def duck():
    response = requests.get("https://random-d.uk/api/random")
    data = response.json()
    duck_url = data["url"]
    duck_number = random.randint(1, 999)
    
    return render_template('duck.html',duck_url=duck_url, duck_number=duck_number)

@app.route ("/fox/")
@app.route ("/fox/<int:number>/")
def fox(number = None):
    if number is None:
        number = 1
    if number < 1 or number > 10 :
        return '<h1 style="color:red; text-align:center; font-size:48px">Можно выбрать количество от 1 до 10</h1>'
       
    response = requests.get("https://randomfox.ca/floof/")
    data = response.json()
    fox_url = data["image"]
        
    foxs = [fox_url] * number
    return render_template('fox.html', foxs=foxs, number=number)


@app.route("/weather-minsk/")
def weather_minsk():
    lat, lon = 53.9, 27.5667
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data = requests.get(url).json()

    weather = data.get("current_weather", {})
    temp = weather.get("temperature", "?")
    wind = weather.get("windspeed", "?")

    return render_template("weatherminsk.html", temp=temp, wind=wind)

@app.route("/weather/")
@app.route("/weather/<city>/")
def weather_city(city=None):
    if city is None:
        city="Gomel"
            
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

@app.route("/dogs/")
def animals():
    return render_template("dogs.html", title="Породы собак")

@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red; text-align:center; font-size:48px">Такой страницы не существует</h1>'

if __name__ == "__main__":
    app.run(debug=True) 