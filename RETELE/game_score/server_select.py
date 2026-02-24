import socket
import select
import random
import time

HOST = '127.0.0.1'
PORT = 5555
MIN_CLIENTS = 3

clients = []
scores = {}
state = "standby"
secret_number = None
last_check = time.time()

def broadcast(message):
    for c in clients:
        try:
            c.send(message.encode('utf-8'))
        except:
            clients.remove(c)

def start_new_round():
    global secret_number, state
    secret_number = random.randint(1, 50)
    state = "playing"
    print(f"[NEW ROUND] Secret number = {secret_number}")
    broadcast("NEW ROUND STARTED! Guess a number between 1 and 50.")

def handle_guess(client, guess, addr):
    global secret_number, state
    if state != "playing":
        client.send("Game paused, wait for more players.".encode('utf-8'))
        return

    try:
        guess = int(guess)
    except:
        client.send("Invalid input. Enter a number.".encode('utf-8'))
        return

    if guess < secret_number:
        client.send("too low".encode('utf-8'))
    elif guess > secret_number:
        client.send("too high".encode('utf-8'))
    else:
        scores[addr] += 1
        broadcast(f"Player {addr} guessed correctly: {guess}")
        print(f"[ROUND RESULT] {addr} scores (total {scores[addr]})")

        if scores[addr] >= 3:
            broadcast(f"GAME OVER! Player {addr} wins the game!")
            print("[GAME OVER] Restarting in standby mode.")
            scores.clear()
            state = "standby"
        else:
            start_new_round()

def main():
    global state, last_check

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    server_socket.setblocking(False)
    print(f"[LISTENING] Server running on {HOST}:{PORT}")

    inputs = [server_socket]

    while True:
        readable, _, exceptional = select.select(inputs, [], inputs, 0.5)

        # Periodic state check
        if time.time() - last_check > 1:
            last_check = time.time()
            if state == "standby" and len(clients) >= MIN_CLIENTS:
                print("[GAME START] Enough players connected.")
                start_new_round()
            elif len(clients) < MIN_CLIENTS and state == "playing":
                state = "standby"
                secret_number = None
                broadcast(f"Not enough players. Waiting for {MIN_CLIENTS} clients...")
                print("[GAME PAUSED] Waiting for more players...")

        for s in readable:
            if s is server_socket:
                client, addr = server_socket.accept()
                client.setblocking(False)
                inputs.append(client)
                clients.append(client)
                scores[addr] = 0
                print(f"[CONNECT] {addr} joined. {len(clients)} players total.")
                client.send("Welcome! Waiting for game to start...\n".encode('utf-8'))
            else:
                try:
                    data = s.recv(1024)
                    if data:
                        addr = s.getpeername()
                        handle_guess(s, data.decode('utf-8').strip(), addr)
                    else:
                        addr = s.getpeername()
                        print(f"[DISCONNECT] {addr}")
                        inputs.remove(s)
                        if s in clients:
                            clients.remove(s)
                        s.close()
                        if addr in scores:
                            del scores[addr]
                except:
                    inputs.remove(s)
                    if s in clients:
                        clients.remove(s)
                    s.close()

        for s in exceptional:
            inputs.remove(s)
            if s in clients:
                clients.remove(s)
            s.close()

if __name__ == "__main__":
    main()