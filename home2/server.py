 
# import os
# import re
# import json
# import socket
# import threading
# import urllib.parse
# from datetime import datetime

# # ================== НАСТРОЙКИ ==================
# HOST, PORT = "127.0.0.1", 8888
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_DIR = os.path.join(BASE_DIR, "static")
# USERS_DB = os.path.join(BASE_DIR, "users.json")

# # ================== ДАННЫЕ ПОЛЬЗОВАТЕЛЕЙ ==================
# users = {}
# lock = threading.Lock()
# login_re = re.compile(r"^[A-Za-z0-9]{6,}$")

# def load_users():
#     """Загрузить пользователей из файла JSON"""
#     global users
#     if os.path.exists(USERS_DB):
#         with open(USERS_DB, "r", encoding="utf-8") as f:
#             users = json.load(f)

# def save_users():
#     """Сохранить пользователей в файл JSON"""
#     with open(USERS_DB, "w", encoding="utf-8") as f:
#         json.dump(users, f, ensure_ascii=False, indent=2)

# def validate(login, pw):
#     """Проверка логина и пароля"""
#     if not login_re.match(login): return False, "логин некорректный"
#     if len(pw) < 8 or not any(c.isdigit() for c in pw):
#         return False, "пароль некорректный"
#     return True, ""

# # ================== УТИЛИТЫ ==================
# def now():
#     return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# def http_resp(code, body, ctype="text/plain; charset=utf-8"):
#     """Формируем HTTP-ответ"""
#     body = body.encode() if isinstance(body, str) else body
#     headers = f"HTTP/1.1 {code}\r\nContent-Type: {ctype}\r\nContent-Length: {len(body)}\r\n\r\n"
#     return headers.encode() + body

# # ================== HTTP-ОБРАБОТЧИКИ ==================
# def http_root():
#     """Главная страница"""
#     f = os.path.join(STATIC_DIR,"index.html")
#     if os.path.exists(f): 
#         return http_resp("200 OK", open(f,"rb").read(),"text/html")
#     return http_resp("200 OK","<h1>Главная</h1>","text/html")

# def http_register(q):
#     """Регистрация через браузер"""
#     login, pw = q.get("login",[""])[0], q.get("password",[""])[0]
#     ok, reason = validate(login, pw)
#     if not ok: return http_resp("400 Bad Request", f"{now()} - ошибка регистрации {login} - {reason}")
#     with lock:
#         if login in users: return http_resp("409 Conflict", f"{now()} - ошибка {login} - логин занят")
#         users[login] = pw; save_users()
#     return http_resp("200 OK", f"{now()} - пользователь {login} зарегистрирован")

# def http_signin(q):
#     """Авторизация через браузер"""
#     login, pw = q.get("login",[""])[0], q.get("password",[""])[0]
#     with lock: ok = users.get(login) == pw
#     if ok: return http_resp("200 OK", f"{now()} - пользователь {login} вошёл")
#     return http_resp("403 Forbidden", f"{now()} - ошибка входа {login}")

# def handle_http(conn, data):
#     """Обработка HTTP-запросов"""
#     try:
#         line = data.split(b"\r\n",1)[0].decode()
#         _, raw_path, _ = line.split()
#         parsed = urllib.parse.urlsplit(raw_path)
#         path, q = parsed.path, urllib.parse.parse_qs(parsed.query)

#         if path == "/": resp = http_root()
#         elif path == "/register": resp = http_register(q)
#         elif path == "/signin": resp = http_signin(q)
#         elif re.fullmatch(r"/test/(\d+)/?", path):
#             num = path.split("/")[2]; resp = http_resp("200 OK", f"тест {num} запущен")
#         else:
#             resp = http_resp("404 Not Found", f"Неизвестный путь {path}")

#         conn.sendall(resp)
#     except Exception as e:
#         conn.sendall(http_resp("500 Internal Server Error", f"Ошибка: {e}"))

# # ================== НЕ-HTTP ОБРАБОТЧИК ==================
# def handle_non_http(conn, data):
#     """Регистрация/вход через текстовые команды"""
#     text=data.decode().strip()
#     fields={p.split(":")[0].strip():p.split(":")[1].strip() for p in text.split(";") if ":" in p}
#     cmd, login, pw = fields.get("command"), fields.get("login",""), fields.get("password","")

#     if cmd=="reg":
#         ok, reason=validate(login,pw)
#         if ok:
#             with lock:
#                 if login in users: resp=f"{now()} - ошибка {login} - логин занят"
#                 else: users[login]=pw; save_users(); resp=f"{now()} - {login} зарегистрирован"
#         else: resp=f"{now()} - ошибка регистрации {login} - {reason}"

#     elif cmd=="signin":
#         with lock: ok=users.get(login)==pw
#         resp=f"{now()} - вход {login}" if ok else f"{now()} - ошибка входа {login}"
#     else: resp=f"Неизвестные данные: {text}"

#     conn.sendall((resp+"\n").encode())

# # ================== СЕРВЕР ==================
# def client(conn, addr):
#     with conn:
#         data=conn.recv(65536)
#         if not data: return
#         if data.startswith(b"GET ") or b"HTTP/" in data[:64]: handle_http(conn,data)
#         else: handle_non_http(conn,data)

# def main():
#     load_users()
#     os.makedirs(STATIC_DIR, exist_ok=True)
#     with socket.socket() as s:
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         s.bind((HOST, PORT)); s.listen()
#         print(f"[{now()}] Сервер слушает {HOST}:{PORT}")
#         while True:
#             conn, addr = s.accept()
#             threading.Thread(target=client, args=(conn,addr), daemon=True).start()

# if __name__=="__main__": main()



import os
import re
import json
import socket
import threading
import urllib.parse
from datetime import datetime


# ------------------ Константы ------------------
HOST = ('127.0.0.1', 7777)
OK = b'HTTP/1.1 200 OK\n'
ERR_404 = b'HTTP/1.1 404 Not Found\n\n'
HEADERS_HTML = b"Content-Type: text/html; charset=utf-8\r\n\r\n"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")


# ------------------ Пользователи ------------------
users = {}
lock = threading.Lock()
login_re = re.compile(r"^[A-Za-z0-9]{6,}$")

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

users = load_users()


def validate(login, pw):
    if not re.fullmatch(r"[A-Za-z0-9]{6,}", login):
        return False, "логин некорректный"
    if len(pw) < 8 or not any(c.isdigit() for c in pw):
        return False, "пароль некорректный"
    return True, ""


# ------------------ Утилиты ------------------
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_file(path, conn):
    try:
        file_path = os.path.join(BASE_DIR, path.lstrip('/'))
        with open(file_path, "rb") as f:
            conn.send(OK)
            conn.send(HEADERS_HTML)
            conn.send(f.read())
    except IOError:
        conn.send(ERR_404)

def is_file(path):
    if '.' in path:
        ext = path.split(".")[-1]
        if ext in ['jpg','png','gif','ico','txt','html','json','css']:
            return True
    return False

# ------------------ Основной сервер ------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(HOST)
sock.listen()
print("-- start --")

while True:
    conn, addr = sock.accept()
    data = conn.recv(4096).decode(errors="ignore")
    if not data:
        conn.close()
        continue

    try:
        method, path, ver = data.split('\n')[0].split(" ", 2)
        print(f"[{now()}] {method} {path}")

        # Разделяем query-параметры
        params = {}
        if "?" in path:
            path, query = path.split("?", 1)
            params = urllib.parse.parse_qs(query)

        # ----------- Роутинг -----------
        if is_file(path):                     # отдаём статические файлы
            send_file(path.lstrip("/"), conn)

        elif path == "/":                     # главная
            send_file("static/index.html", conn)

        elif re.fullmatch(r"/test/(\d+)/?", path):  # тест
            num = path.split("/")[2]
            html = f"<h1>ТЕСТ {num} ЗАПУЩЕН</h1>"
            conn.send(OK); conn.send(HEADERS_HTML); conn.send(html.encode())

        elif re.fullmatch(r"/message/([^/]+)/(.+?)/?", path):  # сообщение
            login, text = path.split("/")[2], path.split("/")[3]
            msg = f"{now()} - сообщение от пользователя {login} - {text}"
            print(msg)
            conn.send(OK); conn.send(HEADERS_HTML); conn.send(msg.encode())

        elif path == "/register":             # регистрация
            login = params.get("login", [""])[0]
            pw = params.get("password", [""])[0]
            ok, reason = validate(login, pw)
            if not ok:
                resp = f"{now()} - ошибка регистрации {login} - {reason}"
            elif login in users:
                resp = f"{now()} - ошибка регистрации {login} - логин занят"
            else:
                users[login] = pw
                save_users(users)
                resp = f"{now()} - пользователь {login} зарегистрирован"
            conn.send(OK); conn.send(HEADERS_HTML); conn.send(resp.encode())

        elif path == "/signin":               # вход
            login = params.get("login", [""])[0]
            pw = params.get("password", [""])[0]
            if login in users and users[login] == pw:
                resp = f"{now()} - пользователь {login} вошёл"
            else:
                resp = f"{now()} - ошибка входа {login}"
            conn.send(OK); conn.send(HEADERS_HTML); conn.send(resp.encode())

        else:                                 # неизвестный путь
            conn.send(ERR_404)
            conn.send(b"<h1>404 Not Found</h1>")

    except Exception as e:
        conn.send(OK)
        conn.send(HEADERS_HTML)
        conn.send(f"Ошибка: {e}".encode())

    conn.close()
