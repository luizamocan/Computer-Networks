import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address=('127.0.0.1',5555)
s.bind(server_address)
s.listen(5)
print("Server listening on:",server_address)

while True:
	connection,client_address=s.accept()
	print("new client connected:",client_address)
	with connection:
		data=connection.recv(4)
		if not data:
			continue
		msg_len=int.from_bytes(data,'big')
		msg=connection.recv(msg_len).decode('utf-8')
		msg=msg[::-1]

		connection.send(msg_len.to_bytes(4,'big'))
		connection.send(msg.encode('utf-8'))