
import socket, os, re, json, urllib.parse, threading
from datetime import datetime

HOST = ("127.0.0.1", 7777)

OK = b"HTTP/1.1 200 OK\r\n"
ERR_404 = b"HTTP/1.1 404 Not Found\r\n\r\n"
HEADERS_HTML = b"Content-Type: text/html; charset=utf-8\r\n\r\n"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")

# ================= Пользователи =================
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

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validate(login, pw):
    if not re.fullmatch(r"[A-Za-z0-9]{5,}", login):
        return False, "логин некорректный"
    if len(pw) < 6 or not any(c.isdigit() for c in pw):
        return False, "пароль некорректный"
    return True, ""

# ================= Утилиты =================
def send_file(path, conn):
    try:
        file_path = os.path.join(BASE_DIR, path.lstrip('/'))
        with open(file_path, "rb") as f:
            conn.send(OK)
            conn.send(HEADERS_HTML)
            conn.send(f.read())
    except IOError:
        conn.send(ERR_404)
        conn.send(b"<h1>404 Not Found</h1>")

def handle_http(data, conn):
    try:
        method, path, ver = data.split("\n")[0].split(" ", 2)
        print(f"[HTTP] {method} {path}")

        params = {}
        if "?" in path:
            path, query = path.split("?", 1)
            params = urllib.parse.parse_qs(query)

        if path == "/":
            send_file("static/index.html", conn)

        elif re.fullmatch(r"/test/(\d+)/?", path):
            num = path.split("/")[2]
            html = f"<p1>Тест {num} запущен</p1>"
            conn.send(OK); conn.send(HEADERS_HTML); conn.send(html.encode())

        elif re.fullmatch(r"/message/([^/]+)/(.+?)/?", path):
            _, login, text, *_ = path.split("/")
            msg = f"{now()} - сообщение от пользователя {login} - {text}"
            print(msg)
            conn.send(OK); conn.send(HEADERS_HTML); conn.send(msg.encode())

        elif path == "/register":
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

        elif path == "/signin":
            login = params.get("login", [""])[0]
            pw = params.get("password", [""])[0]
            if login in users and users[login] == pw:
                resp = f"{now()} - пользователь {login} вошёл"
            else:
                resp = f"{now()} - ошибка входа {login}"
            conn.send(OK); conn.send(HEADERS_HTML); conn.send(resp.encode())

        else:
            conn.send(ERR_404)
            conn.send(b"<h1>404 Not Found</h1>")

    except Exception as e:
        conn.send(OK)
        conn.send(HEADERS_HTML)
        conn.send(f"Ошибка: {e}".encode())

def handle_command(data, conn):
    text = data.strip()
    print(f"[CMD] {text}")

    # разбираем команду
    fields = dict(item.split(":", 1) for item in text.split(";") if ":" in item)
    cmd = fields.get("command")
    login = fields.get("login", "")
    pw = fields.get("password", "")

    if cmd == "reg":
        ok, reason = validate(login, pw)
        if not ok:
            resp = f"{now()} - ошибка регистрации {login} - {reason}"
        elif login in users:
            resp = f"{now()} - ошибка регистрации {login} - логин занят"
        else:
            users[login] = pw
            save_users(users)
            resp = f"{now()} - пользователь {login} зарегистрирован"
        conn.send(resp.encode())

    elif cmd == "signin":
        if login in users and users[login] == pw:
            resp = f"{now()} - пользователь {login} вошёл"
        else:
            resp = f"{now()} - ошибка входа {login}"
        conn.send(resp.encode())

    else:
        conn.send(f"пришли неизвестные данные: {text}".encode())

# ================= Сервер =================
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

    if data.startswith("GET") or data.startswith("POST"):
        handle_http(data, conn)
    else:
        handle_command(data, conn)

    conn.close()
