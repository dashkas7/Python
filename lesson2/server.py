import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind('127.0.0.1', 6666)
server_socket.listen(2)

print('Сервер ждёт подключения...')

conn, addr= server_socket.accept()
print('Подключился клиент:', addr)

data = conn.recv(1024).decode
print ('Получено:', data)

conn.sendall('Привет от сервера').encode()


server_socket.close()
