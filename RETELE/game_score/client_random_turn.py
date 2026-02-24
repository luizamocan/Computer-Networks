import socket
import threading
import random
import time

HOST = '127.0.0.1'
PORT = 5555

running = True
current_state = "standby"
my_turn = False


def send_data(sock):
    global running, current_state, my_turn
    while running:
        if current_state == "playing" and my_turn:
            num = random.randint(1, 51)
            sock.send(str(num).encode('utf-8'))
            print(f"I guessed: {num}")
            my_turn = False  # wait for next turn
        time.sleep(0.1)


def receive_broadcast(sock):
    global running, current_state, my_turn
    while running:
        data = sock.recv(1024)
        if not data:
            break
        msg = data.decode('utf-8')
        if "NEW ROUND" in msg:
            current_state = "playing"
            print(msg)
        elif "YOUR_TURN" in msg:
            my_turn = True
            print("👉 It's my turn!")
        elif "WAIT" in msg:
            my_turn = False
        elif "GAME OVER" in msg:
            print(msg)
            current_state = "standby"
        else:
            print("[SERVER]", msg)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
print('Connected to server. Waiting for game to start...')

threading.Thread(target=receive_broadcast, args=(sock,), daemon=True).start()
threading.Thread(target=send_data, args=(sock,), daemon=True).start()

try:
    while running:
        time.sleep(1)
except KeyboardInterrupt:
    running = False

sock.close()
print('Disconnected from server.')
