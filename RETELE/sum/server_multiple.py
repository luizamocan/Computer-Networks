import socket
import threading

def handle_client(connection,client_address):
	print("New client connected: ",client_address)
	try:
		while True:
			data=connection.recv(4)
			if not data:
				continue
			msg_len1=int.from_bytes(data,'big')
			msg1=connection.recv(msg_len1).decode('utf-8')
		
			data=connection.recv(4)
			msg_len2=int.from_bytes(data,'big')
			msg2=connection.recv(msg_len2).decode('utf-8')

			nr1=int(msg1)
			nr2=int(msg2)
			sum=nr1+nr2
			sum_str=str(sum)

			connection.send(len(sum_str).to_bytes(4,'big'))
			connection.send(sum_str.encode('utf-8'))
	except Exception as e:
		print(e)
	finally:
		connection.close()
			
def start_server():
	server_address=('127.0.0.1',5555)
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind(server_address)
	s.listen(5)
	print("Server listening on: ", server_address)
	
	while True:
		connection,client_address=s.accept()
		threading.Thread(target=handle_client,args=(connection,client_address),daemon=True).start()


if __name__=='__main__':
	start_server()

