import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET - IPv4, SOCK_STREAM - TCP
s.connect((socket.gethostbyname(""), 12345))

full_msg = ''
while True:
	msg = s.recv(8) #TCP socket is a stream of data. 1024 is the size of the chunks of data that we recieve
	if len(msg) <= 0:
		break
	full_msg += msg.decode("utf-8")

print(full_msg)