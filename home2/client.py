"""

написать приложение-клиент используя модуль socket работающее в домашней 
локальной сети.
Приложение должно соединятся с сервером по известному адрес:порт и отправлять 
туда текстовые данные.

известно что сервер принимает данные следующего формата:
    "command:reg; login:<login>; password:<pass>" - для регистрации пользователя
    "command:signin; login:<login>; password:<pass>" - для входа пользователя
    
    
с помощью программы зарегистрировать несколько пользователей на сервере и произвести вход


"""

import socket

# адрес сервера (замените на IP сервера в вашей сети)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7777

def send_message(message: str):
    """Отправка строки на сервер и получение ответа"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    sock.send(message.encode("utf-8"))
    response = sock.recv(1024).decode("utf-8")
    sock.close()
    return response

if __name__ == "__main__":
    # регистрируем пользователей
    users = [
        ("student1", "password123"),
        ("student2", "mypassword9"),
        ("student3", "qwerty2024"),
    ]

    for login, password in users:
        msg = f"command:reg; login:{login}; password:{password}"
        print("Отправляем:", msg)
        print("Ответ сервера:", send_message(msg))

    print("-" * 40)

    # вход пользователей
    for login, password in users:
        msg = f"command:signin; login:{login}; password:{password}"
        print("Отправляем:", msg)
        print("Ответ сервера:", send_message(msg))
