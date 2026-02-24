import socket

HOST = '127.0.0.1'
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f"Server is listening on {HOST}:{PORT}")


while True:
	print('Waiting for clients: ')
	connection,client_address=s.accept()
	with connection:
		print("Client connected: ",client_address)
		data=connection.recv(4)
		if not data:
			continue

		msg_length = int.from_bytes(data, 'big')
		msg = connection.recv(msg_length).decode('utf-8')
		print("Received:", msg)
		array1=[int(x) for x in msg.split()]

		data=connection.recv(4)
		msg_length2 = int.from_bytes(data, 'big')
		msg2 = connection.recv(msg_length2).decode('utf-8')
		print("Received:", msg2)
		array2=[int(x) for x in msg2.split()]

		result=" "
		for i in range (0,len(array1)):
			found=False
			for j in range(0,len(array2)):
				if array1[i]==array2[j]:
					found=True
			if found==False:
				result+=str(array1[i])+" "
				
		connection.send(len(result).to_bytes(4,'big'))
		connection.send(result.encode('utf-8'))

