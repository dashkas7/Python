from flask import Flask
from routes.auth import auth_bp
from routes.animals import animals_bp
from routes.weather import weather_bp
from routes.homework import homework_bp

app = Flask(__name__)
app.secret_key = "super_secret_key"

app.register_blueprint(auth_bp)
app.register_blueprint(animals_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(homework_bp)

if __name__ == "__main__":
    app.run(debug=True)
