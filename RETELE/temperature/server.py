import socket
import time
import threading

HOST='127.0.0.1'
PORT=5555

MIN_CLIENTS=5
clients=[]
nr_temps=0
total_sum=0
average=0
state="standby"
lock=threading.Lock()

def broadcast(message):
	for c in clients:
		try:
			c.send(message.encode('utf-8'))
		except:
			pass

def handle_client(connection,client_address):
	global nr_temps,total_sum,state,average
	print(f"CLient {client_address} connected.")
	try:
		while True:
			data=connection.recv(1024)
			if not data:
				break
			number=int(data.decode('utf-8'))
			with lock:
				nr_temps+=1
				total_sum+=number
				current_average=float(total_sum/nr_temps)
				print(f"Received {number} from {client_address}. Average : {current_average}")

				if abs(current_average-average)>=2:
					state="monitor"
					print(f"[AVERAGE CHANGED]New average: {current_average}")
					broadcast(f"{current_average:.2f}")
				if current_average>40:
					print("ALERT:OVERHEAT")
					broadcast("ALERT:OVERHEAT")
					break
				average=current_average
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
		print(f"Active clients: {len(clients)}")

def control_loop():
	global state
	while True:
		with lock:
			client_len=len(clients)
			if state=="standby" and client_len>=MIN_CLIENTS:
				state="monitor"
				print("[STATE CHANGEd] Minimum clients reached. Starting data collection")
				broadcast("monitor")
			elif average>40:
				break
		time.sleep(1)

def start_server():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((HOST,PORT))
	s.listen(10)
	print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

	threading.Thread(target=accept_clients,args=(s,),daemon=True).start()
	control_loop()
	print("[SERVER SHUTDOWN] Collection finished. Final average:", average)
	s.close()

if __name__=='__main__':
	start_server()

			


				
	