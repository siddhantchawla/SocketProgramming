import socket

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234

my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)


servername_header = client_socket.recv(HEADER_LENGTH)
servername_length = int(servername_header.decode('utf-8').strip())
servername = client_socket.recv(servername_length).decode('utf-8')


while True:

	curdir_header = client_socket.recv(HEADER_LENGTH)
	curdir_length = int(curdir_header.decode('utf-8').strip())
	curdir = client_socket.recv(curdir_length).decode('utf-8')

	stdout_header = client_socket.recv(HEADER_LENGTH)
	stdout_length = int(stdout_header.decode('utf-8').strip())
	stdout = client_socket.recv(stdout_length).decode('utf-8')

	
	if stdout:
		print(f"{stdout}")

	command = input(f"{servername}:{curdir}> ")
	command = command.encode('utf-8')
	command_header = f"{len(command):<{HEADER_LENGTH}}".encode('utf-8')
	client_socket.send(command_header + command)


