import socket
import datetime

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12321

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((SERVER_IP, SERVER_PORT))

server_socket.listen(1)
print(f"Сервер прослуховується {SERVER_IP}:{SERVER_PORT}")

client_socket, client_address = server_socket.accept()
print(f"Підключення від {client_address}")

while True:
    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        break

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Отримано: '{data}' в {current_time}")

    if data.lower() == 'вихід':
        break

    import time
    time.sleep(5)

    client_socket.send(data.encode('utf-8'))

client_socket.close()
server_socket.close()