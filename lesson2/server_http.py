import socket

def send_file(file_name, conn):
    try:
        with open(file_name.lstrip('/'), 'rb') as f:
            print(f"send file {file_name}") 
            conn.send(OK)
            conn.send(HEADERS)
            conn.send(f.read())
    except IOError:
        print(f"file not found") 
        conn.send(ERR_404)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 7777))
sock.listen()

print('--start--')

OK = b'HTTP/1.1 200 OK\n'
HEADERS = b'Host: some.ru\nHost1: some1.ru\n\n'
ERR_404 = b'HTTP/1.1 404 Not Found\n\n'

while True:
    print('--listen--')
    conn, addr= sock.accept()
    #print('Подключился клиент:', addr)
    print(addr)
    print(conn)


    data = conn.recv(1024).decode("utf-8")
    print ('Получено:', data)
    # # conn.send(OK)
    # # conn.send(HEADERS)
    # # #conn.send(b'HELLO PYTHON:)')
    # # html = "<H1> Hello Python!!! </H1> <p> параграф \n 123 </p>"
    # #conn.send(html.encode("utf-8"))
    # send_file(r"1.html", conn)
    
    try:
        file_name = data.split('\n')[0].split(' ')[1]
        if file_name == '/':
            file_name = '/1.html'  # по умолчанию
    except IndexError:
        file_name = '/1.html'

send_file(file_name, conn)
conn.close()
