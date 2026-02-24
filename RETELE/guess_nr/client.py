import socket
import threading
import time
import random

HOST='127.0.0.1'
PORT=5555

def listen_server(sock):
	while True:
		data=sock.recv(1024)
		if not data:
			break
		msg=data.decode('utf-8')
		if msg.startswith("YOUR TURN"):
			guess=input("Enter your guess: ")
			sock.send(guess.encode('utf-8'))
		elif "GAME OVER" in msg:
			break



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
print("Connected to the guessing game server!")

threading.Thread(target=listen_server, args=(sock,), daemon=True).start()

while True:
    time.sleep(1)