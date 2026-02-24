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
			string1_length=int.from_bytes(data,'big')
			string1=connection.recv(string1_length).decode('utf-8')
			
			data=connection.recv(4)
			character_length=int.from_bytes(data,'big')
			character=connection.recv(character_length).decode('utf-8')

			result_list=""
			for i in range(0,len(string1)):
				if string1[i]==character:
					result_list+=str(i)+" "
			connection.send(len(result_list).to_bytes(4,'big'))
			connection.send(result_list.encode('utf-8'))
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