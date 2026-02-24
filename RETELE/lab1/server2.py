import socket

socket_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(socket_address)
s.listen(1)
print("Server is listening on:", socket_address)

while True:
	print("Waiting for clients")
	connection,client_address=s.accept()
	with connection:
		print("Connected: ", client_address)
		data=connection.recv(4)
		if not data:
			continue
		msg_length=int.from_bytes(data,'big')
		msg=connection.recv(msg_length).decode('utf-8')
		print("Received: ", msg)
		
		counter=0
		for i in range(0,len(msg)):
			if msg[i]==" ":
				counter=counter+1
		connection.send(counter.to_bytes(4,'big'))


