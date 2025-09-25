import socket

HOST = ('127.0.0.1', 7777)

while True:
    cmd = input("Введите команду (reg <login> <pass> | signin <login> <pass> | exit): ").strip()
    if not cmd:
        continue
    if cmd == "exit":
        break

    parts = cmd.split()
    if parts[0] not in ("reg", "signin") or len(parts) < 3:
        print("Ошибка: используйте reg <логин> <пароль> или signin <логин> <пароль>")
        continue

    login, password = parts[1], parts[2]

    # Формируем строку для сервера
    if parts[0] == "reg":
        send_data = f"command:reg; login:{login}; password:{password}"
    else:
        send_data = f"command:signin; login:{login}; password:{password}"

    # Создаём сокет и отправляем
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(HOST)

    sock.send(send_data.encode("utf-8"))   # отправляем строку
    sock.shutdown(socket.SHUT_WR)          # закрываем запись, чтобы сервер понял, что всё передано

    # Получаем ответ
    data = sock.recv(4096).decode("utf-8", errors="replace")
    print("Ответ сервера:", data)

    sock.close()
