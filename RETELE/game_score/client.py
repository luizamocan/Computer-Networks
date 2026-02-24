import socket
import threading
import random
import time

HOST='127.0.0.1'
PORT=5555

def send_data(sock):
    global running,current_state
    while running:
        if current_state=="playing":
            num=random.randint(1,51)
            sock.send(str(num).encode('utf-8'))
            print(f"Guesses: {num}")
        time.sleep(2)

def receive_broadcast(sock):
    global running,current_state
    while running:
        data=sock.recv(1024)
        if not data:
            break
        msg=data.decode('utf-8')
        if "NEW GAME" in msg or "ROUND" in msg:
            current_state="playing"
            print(msg)
        elif "too low" in msg or "too high" in msg:
            print(msg)
        elif "GAME OVER" in msg:
            print(msg)
            current_state="standby"
        else:
            print("[SERVER]", msg)




sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
print('Connected to server.Waiting for game to start...')
running=True
current_state="standby"

threading.Thread(target=receive_broadcast,args=(sock,),daemon=True).start()
threading.Thread(target=send_data,args=(sock,),daemon=True).start()
while running:
    time.sleep(1)

sock.close()
print('Disconnected from server')