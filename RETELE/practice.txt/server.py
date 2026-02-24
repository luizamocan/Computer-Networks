import socket
import threading
import time

HOST='127.0.0.1'
PORT=5555

MIN_CLIENTS=3
clients=[]
total_sum=0
data_count=0
state="standby"
lock=threading.Lock()

def broadcast(message):
	for c in clients:
		try:
			c.send(message.encode('utf-8'))	
		except:
			pass
def handle_client(connection,client_address):
	global total_sum,data_count,state
	print(f"Client {client_address} connected")
	try:
		while True:
			data=connection.recv(1024)
			if not data:
				break
			number=int(data.decode('utf-8'))
			with lock:
				total_sum+=number
				data_count+=1
				print(f"Received {number} from {client_address}. Total sum: {total_sum} ({data_count} data)")

				if data_count%100==0:
					if state=="odd":
						state="even"
					else:
						state="odd"
					print(f"[STATE CHANGED] Server requesting {state} numbers now.")
					broadcast(state)
	
				if total_sum>9000:
					print("[STOP] Total exceeded 9000.")
					broadcast("stop")
					break
	except Exception as e:
		print(f"Error with {client_address}: {e}")
	finally:	
		connection.close()
		with lock:
			if connection in clients:
				clients.remove(connection)
		print(f"[DISCONNECTED] {client_address} disconnected")


def accept_clients(server_socket):
	global state
	while True:
		connection,client_address=server_socket.accept()
		with lock:
			clients.append(connection)
		threading.Thread(target=handle_client,args=(connection,client_address),daemon=True).start()	
		print(f"[ACTIVE CLIENTS]{len(clients)}")

def control_loop():
	global state
	while True:
		with lock:
			client_count=len(clients)
		if state=="standby" and client_count>=MIN_CLIENTS:
			state="even"
			print("[STATE CHANGE] Minimum clients reached. Starting data collection (even numbers).")
			broadcast("even")
		elif total_sum>9000:
			break
		time.sleep(1)


def start_server():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((HOST,PORT))
	s.listen(10)
	print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

	threading.Thread(target=accept_clients,args=(s,),daemon=True).start()
	control_loop()
	print("[SERVER SHUTDOWN] Collection finished. Total sum:", total_sum)
	s.close()

if __name__=='__main__':
	start_server()

			