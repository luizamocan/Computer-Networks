import socket
import threading

def handle_client(connection,client_address):
	print("New client connected: ",client_address)
	try:
		while True:
			data=connection.recv(4)
			if not data:
				continue
			mes_len=int.from_bytes(data,'big')
			mes=connection.recv(mes_len).decode('utf-8')
			nr_spaces=0
			for i in range(0,len(mes)):
				if mes[i]==" ":
					nr_spaces+=1
			connection.send(str(nr_spaces).encode('utf-8'))
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

