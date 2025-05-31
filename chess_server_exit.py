import socket

##################################################
# Connect to server
##################################################
server_address="localhost"
server_port = 65535

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, server_port))

request = f"exit"
client_socket.send(request.encode("utf-8"))