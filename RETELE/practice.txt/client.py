import socket
import threading
import random
import time

HOST='127.0.0.1'
PORT=5555

def send_data(sock):
	global running,current_state
	while running:
		if current_state in ["even","odd"]:
			if current_state=="even":
				num=random.choice([2,4,6,8])
			else:
				num=random.choice([1,3,5,7,9])
			sock.send(str(num).encode('utf-8'))	
			print(f"Sent: {num}")
		time.sleep(2)

def receive_broadcast(sock):
	global running,current_state
	while running:
		data=sock.recv(1024)
		if not data:
			break
		msg=data.decode('utf-8')
		if msg in ["even", "odd"]:
			current_state=msg
			print(f"[SERVER STATE] Server requires {current_state} numbers.")
		elif msg=="stop":
			print("[SERVER STOP] Disconnecting")
			running=False
			break


sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((HOST,PORT))
print("Connected to server")


running=True
current_state="standby"

threading.Thread(target=receive_broadcast,args=(sock,),daemon=True).start()
threading.Thread(target=send_data,args=(sock,),daemon=True).start()

while running:
	time.sleep(1)

sock.close()
print("Disconnected")