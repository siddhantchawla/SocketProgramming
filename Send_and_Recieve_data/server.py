import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET - IPv4, SOCK_STREAM - TCP
s.bind((socket.gethostbyname(""), 12345))
s.listen(5)

while True:
	clientsocket, address = s.accept()
	print(f"connection from {address} has been established!")
	clientsocket.send(bytes("Welcome to the server!", "utf-8"))
	clientsocket.close()