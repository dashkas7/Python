import socket

#HOST=socket.gethostname()
#print(HOST)

HOST=('127.0.0.1',7777)
# SOCK_DGRAM - UDP, SOCK_STREAM - TCP, AF_INET - ip v4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()

print("--start--")

conn, addr = sock.accept()
print ('Подключился клиент:', addr)

data = conn.recv(1024).decode()
print("Сообщение от клиента:", data)
        
conn.send(data.encode("utf-8"))
conn.close()

print ("--end--") 
sock.close()