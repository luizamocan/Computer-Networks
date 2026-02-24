import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(server_address)
s.listen(5)
print("Server is listening on:", server_address)

while True:
	print('Waiting for clients: ')
	connection,client_address=s.accept()
	with connection:
		print("Client connected: ",client_address)
		data=connection.recv(4)
		if not data:
			continue
		string_length=int.from_bytes(data,'big')
		string=connection.recv(string_length).decode('utf-8')

		data=connection.recv(4)
		character_length=int.from_bytes(data,'big')
		character=connection.recv(character_length).decode('utf-8')

		positions=" "
		for i in range (0,len(string)):
			if string[i]==character:
				positions+=str(i)+" "
		connection.send(len(positions).to_bytes(4,'big'))
		connection.send(positions.encode('utf-8'))

