import socket

# SOCK_DGRAM - UDP, SOCK_STREAM - TCP, AF_INET - ip v4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1',7777))

sock.send('1234567, я Ваня'.encode('utf-8'))
   
data=sock.recv(1024).decode('utf-8')
print("Сообщение:", data)

sock.close()