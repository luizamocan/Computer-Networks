import socket
import threading
HOST='127.0.0.1'
PORT=5555

def handle_client(connection,client_address):
	print("Connected: ",client_address)
	try:
		while True:
			data=connection.recv(4)
			if not data:
				break
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

	except Exception as e:
		print(f"Error with {connection}: {e}")
	finally:
		connection.close()

def start_server():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((HOST,PORT))
	s.listen(5)
	print(f"Server is listening on {HOST}:{PORT}")

	while True:
		connection,client_address=s.accept()
		thread=threading.Thread(target=handle_client,args=(connection,client_address))
		thread.daemon=True
		thread.start()

if __name__=="__main__":
	start_server()