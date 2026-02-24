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
			string1=connection.recv(string1_length).decode('utf-8').split(' ')

			data=connection.recv(4)
			string2_length=int.from_bytes(data,'big')
			string2=connection.recv(string2_length).decode('utf-8').split(' ')
			
			result=" "
			i=0
			j=0
			while i<len(string1) and j<len(string2):
				if string1[i]<string2[j]:
					result+=string1[i]
					i+=1
				else:
					result+=string2[j]
					j+=1
			while i<len(string1):
				result+=string1[i]+" "
				i+=1
			while j<len(string2):
				result+=string2[j]+" "
				j+=1

				
			connection.send(len(result).to_bytes(4,'big'))
			connection.send(result.encode('utf-8'))
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