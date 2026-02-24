import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(server_address)
s.listen(1)
print("Server is listening on:", server_address)

while True:
	print('Waiting for clients: ')
	connection,client_address=s.accept()
	with connection:
		print("Client connected: ",client_address)
		data=connection.recv(4)
		if not data:
			continue
		msg_length=int.from_bytes(data,'big')
		msg=connection.recv(msg_length).decode('utf-8')
		num=int(msg)
		divisors_string=""
		for i in range(1,num+1):
			if num%i==0:
				divisors_string+=str(i)+" "
		
		connection.send(len(divisors_string).to_bytes(4,'big'))
		connection.send(divisors_string.encode('utf-8'))
