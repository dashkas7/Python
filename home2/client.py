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

HOST = "127.0.0.1" # замените на IP сервера в вашей сети (напр., 192.168.1.23)
PORT = 8888




def send_raw(line: str) -> str:
    with socket.create_connection((HOST, PORT), timeout=5) as s:
        s.sendall(line.encode('utf-8'))
        s.shutdown(socket.SHUT_WR)
        data = s.recv(65536)
        return data.decode('utf-8', errors='replace')


def make_reg(login: str, password: str) -> None:
    cmd = f"command:reg; login:{login}; password:{password}"
    print(send_raw(cmd))


def make_signin(login: str, password: str) -> None:
    cmd = f"command:signin; login:{login}; password:{password}"
    print(send_raw(cmd))



def main():
    print("Уважаемый клиент. Команды: reg <login> <password> | signin <login> <password> | exit")
    while True:
        try:
            parts = input("> ").strip().split()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not parts:
            continue
        if parts[0] == 'exit':
            break
        if parts[0] == 'reg' and len(parts) >= 3:
            make_reg(parts[1], parts[2])
            continue
        if parts[0] == 'signin' and len(parts) >= 3:
            make_signin(parts[1], parts[2])
            continue
        print("Неизвестная команда. Пример: reg user123 passw0rd")



if __name__ == "__main__":
    main()
