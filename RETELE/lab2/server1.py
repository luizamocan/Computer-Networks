import socket
import threading

HOST='127.0.0.1'
PORT=5555


def handle_client(connection,client_address):
	print("Connected: ", client_address)
	try:
		while True:
			data=connection.recv(4)
			if not data:
				break
			msg_length=int.from_bytes(data,'big')
			msg=connection.recv(msg_length).decode('utf-8')
			try:
				numbers=[int(x) for x in msg.split()]
				total=sum(numbers)
			except ValueError:
				total=0
			connection.send(total.to_bytes(4,'big'))
			connection.send(str(total).encode('utf-8'))
	except Exception as e:
		print(f"Error with {client_address}: {e}")
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