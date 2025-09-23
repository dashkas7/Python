'''
написать приложение-сервер используя модуль socket работающее в домашней 
локальной сети.
Приложение должно принимать данные с любого устройства в сети отправленные 
или через программу клиент или через браузер
    - если данные пришли по протоколу http создать возможность след.логики:
        - если путь "/" - вывести главную страницу
        
        - если путь содержит /test/<int>/ вывести сообщение - тест с номером int запущен
        
        - если путь содержит message/<login>/<text>/ вывести в консоль/браузер сообщение
            "{дата время} - сообщение от пользователя {login} - {text}"
        
        - если путь содержит указание на файл вывести в браузер этот файл
        
        - во всех остальных случаях вывести сообщение:
            "пришли неизвестные  данные по HTTP - путь такой то"
                   
         
    - если данные пришли НЕ по протоколу http создать возможность след.логики:
        - если пришла строка формата "command:reg; login:<login>; password:<pass>"
            - выполнить проверку:
                login - только латинские символы и цифры, минимум 6 символов
                password - минимум 8 символов, должны быть хоть 1 цифра
            - при успешной проверке:
                1. вывести сообщение на стороне клиента: 
                    "{дата время} - пользователь {login} зарегистрирован"
                2. добавить данные пользователя в список/словарь на сервере
            - если проверка не прошла вывести сообщение на стороне клиента:
                "{дата время} - ошибка регистрации {login} - неверный пароль/логин"
                
        - если пришла строка формата "command:signin; login:<login>; password:<pass>"
            выполнить проверку зарегистрирован ли такой пользователь на сервере:                
            
            при успешной проверке:
                1. вывести сообщение на стороне клиента: 
                    "{дата время} - пользователь {login} произведен вход"
                
            если проверка не прошла вывести сообщение на стороне клиента:
                "{дата время} - ошибка входа {login} - неверный пароль/логин"
        
        - во всех остальных случаях вывести сообщение на стороне клиента:
            "пришли неизвестные  данные - <присланные данные>"       
                 

'''

import socket
import datetime

HOST = ('127.0.0.1', 7777)
users = {}

# # вспомогательная функция для времени
# def now():
#     return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# простая проверка, HTTP это или нет
def is_http(data: str):
    return data.startswith("GET") or data.startswith("POST")

# обработка HTTP запросов
def handle_http(data: str):
    lines = data.split("\r\n")
    if not lines:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"
    line = lines[0]
    parts = line.split()
    if len(parts) < 2:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    path = parts[1]

    if path == "/":
        body = "<h1>Главная страница</h1>"
    elif path.startswith("/test/"):
        try:
            num = path.split("/")[2]
            body = f"тест с номером {num} запущен"
        except IndexError:
            body = "Ошибка: номер теста не указан"
    elif path.startswith("/message/"):
        parts = path.split("/")
        if len(parts) >= 4:
            login = parts[2]
            text = parts[3]
            msg = f"{now()} - сообщение от пользователя {login} - {text}"
            print(msg)
            body = msg
        else:
            body = "Ошибка: формат /message/<login>/<text>/"
    else:
        body = f"пришли неизвестные данные по HTTP - путь {path}"

    return "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + body

# обработка обычных сообщений (не HTTP)
def handle_custom(text: str):
    parts = {}
    for kv in text.split(";"):
        if ":" in kv:
            k, v = kv.split(":", 1)
            parts[k.strip()] = v.strip()
    cmd = parts.get("command")
    login = parts.get("login")
    password = parts.get("password")

    if cmd == "reg":
        if login and len(login) >= 6 and password and len(password) >= 8 and any(ch.isdigit() for ch in password):
            users[login] = password
            return f"{now()} - пользователь {login} зарегистрирован"
        else:
            return f"{now()} - ошибка регистрации {login} - неверный пароль/логин"
    elif cmd == "signin":
        if login in users and users[login] == password:
            return f"{now()} - пользователь {login} произведен вход"
        else:
            return f"{now()} - ошибка входа {login} - неверный пароль/логин"
    else:
        return f"пришли неизвестные данные - {text}"

# запуск сервера
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(HOST)
sock.listen()

print("--start--")

while True:
    conn, addr = sock.accept()
    print("Подключился клиент:", addr)

    data = conn.recv(1024).decode(errors="ignore")
    if not data:
        conn.close()
        continue

    print("Сообщение от клиента:", data)

    if is_http(data):
        response = handle_http(data)
        conn.send(response.encode("utf-8"))
    else:
        response = handle_custom(data)
        conn.send((response + "\n").encode("utf-8"))

    conn.close()