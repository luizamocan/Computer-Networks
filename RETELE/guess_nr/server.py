import socket
import threading
import time
import random

HOST='127.0.0.1'
PORT=5555

MIN_CLIENTS=3
clients=[]
client_names={}
lock=threading.Lock()

game_started=False
target_number=random.randint(1,20)
turn_index=0
game_over=False

def broadcast(message):
	for c in clients:
		try:
			c.send(message.encode('utf-8'))
		except:
			pass

def handle_player(connection,client_address):
	global game_over,turn_index
	name = f"Player_{client_address[1]}"
	client_names[connection] = name
	print(f"{name} connected from {client_address}")
	
	try:
		while not game_over:
			data=connection.recv(1024)
			if not data:
				break
			guess_str=data.decode('utf-8')
			if not guess_str.isdigit():
				continue
			guess=int(guess_str)
			with lock:
				current_player=clients[turn_index % len(clients)]
				if connection==current_player:
					print(f"{name} guessed : {guess}")
					if guess==target_number:
						broadcast(f"[GAME OVER]{name} guessed the correct number: {target_number}")
						game_over=True
						break
					elif guess<target_number:
						connection.send("Too low.".encode())
					else:
						connection.send("Too high.".encode())
					turn_index+=1
				else:
					connection.send("Not your turn!".encode())
	except Exception as e:
		print(f"Error with {name}: {e}")
	finally:
		with lock:
			if connection in clients:
				clients.remove(connection)
			del client_names[connection]
		connection.close()
		print(f"{name} disconnected")
		check_player_count()

def check_player_count():
	global game_over
	if not game_over and len(clients)<MIN_CLIENTS/2:
		print("[GAME OVER] Too few players remain.")
		broadcast("[GAME OVER] Too few players remain.")
		game_over=True

def control_game():
	global game_started,turn_index,game_over
	while not game_started:
		time.sleep(1)
		with lock:
			if len(clients)>=MIN_CLIENTS:
				game_started=True
				print(f"[GAME STARTED] Target number is between 1 and 20 (secret: {target_number})")
				broadcast("[GAME STARTED] Guess the number between 1 and 20!")
	while not game_over:
		with lock:
			if len(clients) == 0:
				break
			current_player = clients[turn_index % len(clients)]
			name = client_names[current_player]
			for c in clients:
				if c == current_player:
					c.send("YOUR TURN\n".encode())
				else:
					c.send(f"WAIT — {name}'s turn\n".encode())
		time.sleep(1.5)
	broadcast("Server shutting down. Thanks for playing!")
	
def accept_clients(server_socket):
	while not game_over:
		connection,client_address=server_socket.accept()
		with lock:
			clients.append(connection)	
		threading.Thread(target=handle_player,args=(connection,client_address),daemon=True).start()
		print(f"Active clients: {len(clients)}")

def start_server():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((HOST,PORT))
	s.listen(10)
	print(f"[LISTENING] Server running on {HOST}:{PORT}")

	threading.Thread(target=accept_clients,args=(s,),daemon=True).start()
	control_game()

	s.close()
	print("[SERVER SHUTDOWN]")


if __name__=='__main__':
	start_server()
		
