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
		array1_length=int.from_bytes(data,'big')
		array1=connection.recv(array1_length).decode('utf-8').split(' ')
		
		data=connection.recv(4)
		array2_length=int.from_bytes(data,'big')
		array2=connection.recv(array2_length).decode('utf-8').split(' ')
		
		merged=" "
		i=0
		j=0
		while i<len(array1) and j<len(array2):
			if array1[i]< array2[j]:
				merged+=array1[i]+ " "
				i+=1
			else:
				merged+=array2[j]+ " "
				j+=1
		while i<len(array1):
			merged+=array1[i]+ " "
			i+=1
		
		while j<len(array2):
			merged+=array2[j]+ " "
			j+=1

		connection.send(len(merged).to_bytes(4,'big'))
		connection.send(merged.encode('utf-8'))