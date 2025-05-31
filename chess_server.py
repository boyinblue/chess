import socket
import threading
from queue import Queue

host = "0.0.0.0"
port = 65535

state = 0
white_socket = None
black_socket = None

logins = set()
sockets = {}

def service(client_socket, login):
    global logins, sockets

    logins.add(login)
    sockets[login] = client_socket

    print(f"logins : {logins}")
    print(f"sockets : {sockets}")

    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                continue

            print(f"Recv : {data}")

            if data == "login":
                client_socket.send(f"{login}".encode("utf-8"))
                print(f"Response login {login}")

            elif data == "list":
                response = ""
                for login in logins:
                    if response == "":
                        response = str(login)
                    else:
                        response = response + "," + str(login)
                client_socket.send(f"{response}".encode("utf-8"))
            
            elif data == "exit":
                server_socket.close()
                exit(0)
                return
            else:
                client_socket.send(data)

        except Exception as e:
            print(f"Socket {login} Closed by exception {e}")
            client_socket.close()
            logins.remove(login)
            return

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print(f"서버가 {host}:{port}에서 대기 중입니다...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"클라이언트 {client_address}가 연결되었습니다.")

    login = client_address[1]
    thread = threading.Thread(target=service, args=(client_socket, login))
    thread.start()