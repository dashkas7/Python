# '''
# написать приложение-сервер используя модуль socket работающее в домашней 
# локальной сети.
# Приложение должно принимать данные с любого устройства в сети отправленные 
# или через программу клиент или через браузер
#     - если данные пришли по протоколу http создать возможность след.логики:
#         - если путь "/" - вывести главную страницу
        
#         - если путь содержит /test/<int>/ вывести сообщение - тест с номером int запущен
        
#         - если путь содержит message/<login>/<text>/ вывести в консоль/браузер сообщение
#             "{дата время} - сообщение от пользователя {login} - {text}"
        
#         - если путь содержит указание на файл вывести в браузер этот файл
        
#         - во всех остальных случаях вывести сообщение:
#             "пришли неизвестные  данные по HTTP - путь такой то"
                   
         
#     - если данные пришли НЕ по протоколу http создать возможность след.логики:
#         - если пришла строка формата "command:reg; login:<login>; password:<pass>"
#             - выполнить проверку:
#                 login - только латинские символы и цифры, минимум 6 символов
#                 password - минимум 8 символов, должны быть хоть 1 цифра
#             - при успешной проверке:
#                 1. вывести сообщение на стороне клиента: 
#                     "{дата время} - пользователь {login} зарегистрирован"
#                 2. добавить данные пользователя в список/словарь на сервере
#             - если проверка не прошла вывести сообщение на стороне клиента:
#                 "{дата время} - ошибка регистрации {login} - неверный пароль/логин"
                
#         - если пришла строка формата "command:signin; login:<login>; password:<pass>"
#             выполнить проверку зарегистрирован ли такой пользователь на сервере:                
            
#             при успешной проверке:
#                 1. вывести сообщение на стороне клиента: 
#                     "{дата время} - пользователь {login} произведен вход"
                
#             если проверка не прошла вывести сообщение на стороне клиента:
#                 "{дата время} - ошибка входа {login} - неверный пароль/логин"
        
#         - во всех остальных случаях вывести сообщение на стороне клиента:
#             "пришли неизвестные  данные - <присланные данные>"       
                 

# '''

import os
import re
import json
import socket
import threading
import urllib.parse
from datetime import datetime
from typing import Tuple

HOST = "0.0.0.0"
PORT = 8080

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
USERS_DB_PATH = os.path.join(BASE_DIR, "users.json")

LOGIN_RE = re.compile(r"^[A-Za-z0-9]{6,}$")


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_users() -> dict:
    if not os.path.exists(USERS_DB_PATH):
        return {}
    try:
        with open(USERS_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(users: dict) -> None:
    tmp = USERS_DB_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    os.replace(tmp, USERS_DB_PATH)


USERS = load_users()
USERS_LOCK = threading.Lock()


def validate_credentials(login: str, password: str) -> Tuple[bool, str]:
    if not LOGIN_RE.match(login or ""):
        return False, "логин должен быть латиницей/цифрами и минимум 6 символов"
    if not password or len(password) < 8:
        return False, "пароль минимум 8 символов"
    if not any(ch.isdigit() for ch in password):
        return False, "пароль должен содержать хотя бы одну цифру"
    return True, ""


def guess_mime(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    return {
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".ico": "image/x-icon",
        ".txt": "text/plain; charset=utf-8",
    }.get(ext, "application/octet-stream")


def http_response(status: str, body: bytes, headers: dict = None) -> bytes:
    headers = headers or {}
    base = [
        f"HTTP/1.1 {status}",
        "Server: PySocketServer",
        f"Content-Length: {len(body)}",
        "Connection: close",
    ]
    for k, v in headers.items():
        base.append(f"{k}: {v}")
    resp = ("\r\n".join(base) + "\r\n\r\n").encode("utf-8") + body
    return resp


def http_text(status: str, text: str, content_type: str = "text/plain; charset=utf-8") -> bytes:
    return http_response(status, text.encode("utf-8"), {"Content-Type": content_type})


def handle_http(conn: socket.socket, request: bytes) -> None:
    try:
        header, _, body = request.partition(b"\r\n\r\n")
        lines = header.split(b"\r\n")
        if not lines:
            conn.sendall(http_text("400 Bad Request", "пустой HTTP запрос"))
            return

        request_line = lines[0].decode("utf-8", errors="replace")
        parts = request_line.split()
        if len(parts) < 3:
            conn.sendall(http_text("400 Bad Request", "неверная стартовая строка"))
            return
        method, raw_path, _ = parts

        parsed = urllib.parse.urlsplit(raw_path)
        path = urllib.parse.unquote(parsed.path)
        query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)

        if path == "/":
            index_path = os.path.join(STATIC_DIR, "index.html")
            if os.path.exists(index_path):
                with open(index_path, "rb") as f:
                    data = f.read()
                conn.sendall(http_response("200 OK", data, {"Content-Type": guess_mime(index_path)}))
            else:
                conn.sendall(http_text("200 OK", "<h1>Главная страница</h1>", "text/html; charset=utf-8"))
            return

        m = re.fullmatch(r"/test/(\d+)/?", path)
        if m:
            num = m.group(1)
            conn.sendall(http_text("200 OK", f"тест с номером {num} запущен"))
            return

        m = re.fullmatch(r"/message/([^/]+)/(.+?)/?", path)
        if m:
            login = urllib.parse.unquote(m.group(1))
            text = urllib.parse.unquote(m.group(2))
            msg = f"{now_str()} - сообщение от пользователя {login} - {text}"
            print(msg)
            conn.sendall(http_text("200 OK", msg))
            return

        if path == "/register":
            login = (query.get("login", [""])[0] or "").strip()
            password = (query.get("password", [""])[0] or "").strip()
            ok, reason = validate_credentials(login, password)
            if not ok:
                conn.sendall(http_text("400 Bad Request", f"{now_str()} - ошибка регистрации {login} - {reason}"))
                return
            with USERS_LOCK:
                if login in USERS:
                    conn.sendall(http_text("409 Conflict", f"{now_str()} - ошибка регистрации {login} - логин занят"))
                    return
                USERS[login] = password
                save_users(USERS)
            conn.sendall(http_text("200 OK", f"{now_str()} - пользователь {login} зарегистрирован"))
            return

        safe = os.path.normpath(path).lstrip("/")
        file_path = os.path.join(STATIC_DIR, safe)
        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                data = f.read()
            conn.sendall(http_response("200 OK", data, {"Content-Type": guess_mime(file_path)}))
            return

        conn.sendall(http_text("404 Not Found", f"пришли неизвестные данные по HTTP - путь {path}"))
    except Exception as e:
        conn.sendall(http_text("500 Internal Server Error", f"ошибка сервера: {e}"))


def parse_kv_command(s: str) -> dict:
    parts = [p.strip() for p in s.split(";") if p.strip()]
    data = {}
    for p in parts:
        if ":" in p:
            k, v = p.split(":", 1)
            data[k.strip().lower()] = v.strip()
    return data


def handle_non_http(conn: socket.socket, data: bytes) -> None:
    try:
        text = data.decode("utf-8", errors="replace").strip()
        fields = parse_kv_command(text)
        cmd = fields.get("command")
        login = fields.get("login", "")
        password = fields.get("password", "")

        if cmd == "reg":
            ok, reason = validate_credentials(login, password)
            if ok:
                with USERS_LOCK:
                    if login in USERS:
                        resp = f"{now_str()} - ошибка регистрации {login} - логин занят"
                    else:
                        USERS[login] = password
                        save_users(USERS)
                        resp = f"{now_str()} - пользователь {login} зарегистрирован"
            else:
                resp = f"{now_str()} - ошибка регистрации {login} - {reason}"
            conn.sendall((resp + "\n").encode("utf-8"))
            return

        if cmd == "signin":
            with USERS_LOCK:
                ok = login in USERS and USERS.get(login) == password
            if ok:
                resp = f"{now_str()} - пользователь {login} произведен вход"
            else:
                resp = f"{now_str()} - ошибка входа {login} - неверный пароль/логин"
            conn.sendall((resp + "\n").encode("utf-8"))
            return

        conn.sendall((f"пришли неизвестные данные - {text}\n").encode("utf-8"))
    except Exception as e:
        conn.sendall((f"ошибка сервера: {e}\n").encode("utf-8"))


def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    with conn:
        data = conn.recv(65536)
        if not data:
            return
        is_http = data.startswith(b"GET ") or data.startswith(b"POST ") or b"HTTP/" in data[:64]
        if is_http:
            handle_http(conn, data)
        else:
            handle_non_http(conn, data)


def main():
    os.makedirs(STATIC_DIR, exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(100)
        print(f"[{now_str()}] Сервер слушает {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
