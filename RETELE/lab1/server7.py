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
		position_length=int.from_bytes(data,'big')
		position=connection.recv(position_length).decode('utf-8')
		position_number=int(position)

		data=connection.recv(4)
		length_string_length=int.from_bytes(data,'big')
		length_string=connection.recv(length_string_length).decode('utf-8')
		length=int(length_string)

		#string, position_number, length 

		substring=" "
		j=position_number
		for i in range (0,length):
			substring+=string[j]
			j+=1
		connection.send(len(substring).to_bytes(4,'big'))
		connection.send(substring.encode('utf-8'))

