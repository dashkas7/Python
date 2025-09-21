import socket

HOST=('127.0.0.1',7777)
# SOCK_DGRAM - UDP, SOCK_STREAM - TCP, AF_INET - ip v4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


sock.connect(HOST)
sock.send('1234567 Ваня'.encode('utf-8'))
sock.recv(1024)
#sock.close()