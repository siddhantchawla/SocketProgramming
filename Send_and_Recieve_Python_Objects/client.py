import socket
import pickle

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET - IPv4, SOCK_STREAM - TCP
s.connect((socket.gethostbyname(""), 12345))

while True:
	full_msg = b''
	new_msg = True
	while True:
		msg = s.recv(16) #TCP socket is a stream of data.
		
		if new_msg:
			print(f"New message length: {msg[:HEADERSIZE]}")
			msglen = int(msg[:HEADERSIZE])
			new_msg = False

		full_msg += msg

		if len(full_msg) - HEADERSIZE == msglen:
			print("Full message recieved")
			print(full_msg[HEADERSIZE:])

			d = pickle.loads(full_msg[HEADERSIZE:])
			print(d)
			
			new_msg = True
			full_msg = b''