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
		string_length1=int.from_bytes(data,'big')
		string1=connection.recv(string_length1).decode('utf-8')

		data=connection.recv(4)
		string_length2=int.from_bytes(data,'big')
		string2=connection.recv(string_length2).decode('utf-8')

		freq=[0]*256
		i=0
		while i<len(string1) and i<len(string2):
			if string1[i]==string2[i]:
				freq[ord(string1[i])]+=1
			i+=1
		max_freq=0
		max_char=" "
		for i in range(0,256):
			if freq[i]>max_freq:
				max_freq=freq[i]
				max_char=chr(i)


		connection.send(len(max_char).to_bytes(4,'big'))
		connection.send(max_char.encode('utf-8'))

		connection.send(len(str(max_freq)).to_bytes(4,'big'))
		connection.send(str(max_freq).encode('utf-8'))
