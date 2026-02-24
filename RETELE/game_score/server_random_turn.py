import random
import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 5555
MIN_CLIENTS = 3

clients = []
scores = {}
state = "standby"
lock = threading.Lock()
secret_number = None


def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            pass


def handle_client(connection, client_address):
    global state, secret_number
    print(f"Client {client_address} connected")
    scores[client_address] = 0
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            guess = int(data.decode('utf-8'))
            with lock:
                if state != "playing":
                    connection.send("Game paused, wait for more players.".encode('utf-8'))
                    continue
                if state == "playing":
                    if guess < secret_number:
                        connection.send("too low".encode('utf-8'))
                    elif guess > secret_number:
                        connection.send("too high".encode('utf-8'))
                    else:
                        scores[client_address] += 1
                        broadcast(f"Player {client_address} guessed correctly: {guess}")
                        print(f"Round Result: {client_address} wins a point!")
                        if scores[client_address] == 3:
                            broadcast(f"GAME OVER! Player {client_address} wins the full game!")
                            state = "standby"
                            scores.clear()
                        else:
                            secret_number = random.randint(1, 50)
                            broadcast("NEW ROUND STARTED! Guess a number between 1 and 50.")
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        connection.close()
        with lock:
            if connection in clients:
                clients.remove(connection)
            if client_address in scores:
                del scores[client_address]
        print(f"Client {client_address} disconnected")


def accept_clients(server_socket):
    global state
    while True:
        connection, client_address = server_socket.accept()
        with lock:
            clients.append(connection)
        threading.Thread(target=handle_client, args=(connection, client_address), daemon=True).start()
        print(f"[ACTIVE CLIENTS] {len(clients)} clients connected")


def control_loop():
    global state, secret_number
    while True:
        with lock:
            client_count = len(clients)
            if state == "standby" and client_count >= MIN_CLIENTS:
                state = "playing"
                secret_number = random.randint(1, 50)
                print(f"[GAME START] Enough players connected")
                broadcast("NEW ROUND STARTED! Guess a number between 1 and 50.") 

            elif client_count < MIN_CLIENTS and state == "playing":
                state = "standby"
                secret_number = None
                broadcast(f"Not enough players. Waiting for at least {MIN_CLIENTS} clients...")
                print(f"[GAME PAUSED] Waiting for more players...")

            # --- NEW FEATURE: choose one random player to guess ---
            if state == "playing" and len(clients) > 0:
                chosen = random.choice(clients)
                for c in clients:
                    if c == chosen:
                        c.send("YOUR_TURN".encode('utf-8'))
                    else:
                        c.send("WAIT".encode('utf-8'))
        time.sleep(2)


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    threading.Thread(target=accept_clients, args=(s,), daemon=True).start()
    control_loop()
    s.close()


if __name__ == "__main__":
    start_server()
