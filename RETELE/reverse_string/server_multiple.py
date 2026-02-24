import socket
import threading

def handle_client(connection,client_address):
	print("new client connected:",client_address)
	try:
		while True:
			data=connection.recv(4)
			if not data:
				continue
			msg_len=int.from_bytes(data,'big')
			msg=connection.recv(msg_len).decode('utf-8')
			msg=msg[::-1]
			connection.send(len(msg).to_bytes(4,'big'))
			connection.send(msg.encode('utf-8'))
	except Exception as e:
		print(e)
	finally:
		connection.close()




def start_server():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_address=('127.0.0.1',5555)
	s.bind(server_address)
	s.listen(5)
	print("Server listening on:",server_address)

	while True:
		connection,client_address=s.accept()
		threading.Thread(target=handle_client,args=(connection,client_address),daemon=True).start()

if __name__=='__main__':
	start_server()