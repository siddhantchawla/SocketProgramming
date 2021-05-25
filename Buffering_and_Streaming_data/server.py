import socket
import time

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET - IPv4, SOCK_STREAM - TCP
s.bind((socket.gethostbyname(""), 12345))
s.listen(5)

while True:
	clientsocket, address = s.accept()
	print(f"connection from {address} has been established!")

	msg = "Welcome to the server!"
	msg = f'{len(msg):<{HEADERSIZE}}' + msg

	clientsocket.send(bytes(msg, "utf-8"))

	while True:
		time.sleep(3)
		msg = f'The time is {time.time()}!'
		msg = f'{len(msg):<{HEADERSIZE}}' + msg

		clientsocket.send(bytes(msg, "utf-8"))
