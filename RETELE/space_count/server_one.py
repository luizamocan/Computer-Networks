import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(server_address)
s.listen(5)
print("Current server listening on: ",server_address)

while True:
	print("Waiting for clients...")
	connection,client_address=s.accept()
	with connection:
		print("New client connected: ",client_address)
		data=connection.recv(4)
		if not data:
			continue
		msg_length=int.from_bytes(data,'big')
		msg=connection.recv(msg_length).decode('utf-8')
		
		nr_spaces=0
		for i in range(0,len(msg)):
			if msg[i]==" ":
				nr_spaces+=1
		connection.send(str(nr_spaces).encode('utf-8'))
