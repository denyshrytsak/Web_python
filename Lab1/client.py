import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12321

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((SERVER_IP, SERVER_PORT))

print("exit-щоб вийти")
while True:
    message = input("Напишіть повідомлення для відправки на сервер: ")

    if message.lower() == 'exit':
        print("Щасливо")
        break

    client_socket.send(message.encode('utf-8'))

client_socket.close()

