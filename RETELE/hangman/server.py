import socket
import threading
import random
import time

HOST = '127.0.0.1'
PORT = 5555

def pick_word():
    words = ["computer", "science", "test", "intelligence", "dance"]
    return random.choice(words)

def handle_client(connection, client_address):
    print(f"New client connected: {client_address}")
    random.seed(time.time())

    word = pick_word()
    hidden = ["_"] * len(word)
    chances = random.randint(5, 7)
    guessed = set()
    done = False

    # Send the length of the word first
    connection.send(f"{len(word)}".encode('utf-8'))
    print(f"Client {client_address} must guess '{word}' in {chances} tries")

    while not done:
        try:
            data = connection.recv(1024)
            if not data:
                break

            guess = data.decode('utf-8').strip().lower()

            # Invalid input check
            if len(guess) != 1 or not guess.isalpha():
                connection.send("Please send a single letter.".encode('utf-8'))
                continue

            if guess in guessed:
                connection.send("Already guessed.".encode('utf-8'))
                continue

            guessed.add(guess)

            if guess in word:
                for i, c in enumerate(word):
                    if c == guess:
                        hidden[i] = guess
                connection.send(f"Correct! {''.join(hidden)}".encode('utf-8'))
            else:
                chances -= 1
                connection.send(f"Wrong! {''.join(hidden)} ({chances} tries left)".encode('utf-8'))

            # Check win condition
            if "_" not in hidden:
                message = f"You won! The word was '{word}'. BYE"
                connection.send(message.encode('utf-8'))
                print(f"[WIN] {client_address} guessed the word '{word}'")
                done = True
                break

            # Check lose condition
            elif chances == 0:
                message = f"You lost! The word was '{word}'. BYE"
                connection.send(message.encode('utf-8'))
                print(f"[LOSE] {client_address} failed the word '{word}'")
                done = True
                break

        except Exception as e:
            print(f"[ERROR] {client_address}: {e}")
            break

    connection.close()
    print(f"{client_address} disconnected")

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        connection, client_address = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address), daemon=True)
        client_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
