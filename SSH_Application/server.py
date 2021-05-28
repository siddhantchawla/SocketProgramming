import socket
import select
import getpass
import os
import subprocess

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}
print(f'Listening for connections on {IP}:{PORT}...')

def execute_command(command):
	result = ""
	result = result.encode('utf-8')

	if len(command):
		l = command.split()
		if l[0] == 'cd' and len(l) == 2:
			try:
				os.chdir(l[1])
			except:
				result = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
				result = result.stdout.read() + result.stderr.read()
		else:
			result = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
			result = result.stdout.read() + result.stderr.read()

	result_header = f"{len(result):<{HEADER_LENGTH}}".encode('utf-8')

	curdir = os.getcwd()
	curdir = curdir.encode('utf-8')
	curdir_header = f"{len(curdir):<{HEADER_LENGTH}}".encode('utf-8')

	return curdir_header + curdir + result_header + result


def receive_message(client_socket):
	try:
		message_header = client_socket.recv(HEADER_LENGTH)
		if not len(message_header):
			return False
		
		message_length = int(message_header.decode("utf-8").strip())
		return {"header":message_header, "data":client_socket.recv(message_length)}

	except:
		return False


while True:
	read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

	for notified_socket in read_sockets:
		if notified_socket == server_socket:
			client_socket, client_address = server_socket.accept()
			user = receive_message(client_socket)
			if user is False:
				continue

			sockets_list.append(client_socket)
			clients[client_socket] = user

			print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username : {user['data'].decode('utf-8')}")

			user = getpass.getuser().encode('utf-8')
			user_header = f"{len(user):<{HEADER_LENGTH}}".encode('utf-8')

			servername = os.uname()[1].split('.')
			servername = (servername[0]+':').encode('utf-8')
			servername_header = f"{len(servername):<{HEADER_LENGTH}}".encode('utf-8')

			result = execute_command("")
			client_socket.send(user_header + user + servername_header + servername + result) 


		else:
			message = receive_message(notified_socket)
			if message is False:
				print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
				sockets_list.remove(notified_socket)
				del clients[notified_socket]
				continue

			user = clients[notified_socket]
			print(f"Received message from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')}")

			result = execute_command(message['data'].decode("utf-8"))
			notified_socket.send(result)
			




