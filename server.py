import socket
import threading

# Server CONSTS
# HOST = "192.168.1.108"
HOST = "127.0.0.1"
PORT = 12345

# Listener                    IP Type(IPV4)   TCP Protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT)) # Connection between socket to IP:PORT 
server_socket.listen(5)
print(f"Test : {server_socket}")