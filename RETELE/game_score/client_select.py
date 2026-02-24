import socket
import select
import random
import time

HOST = '127.0.0.1'
PORT = 5555

current_state = "standby"
next_guess_time = 0

def main():
    global current_state, next_guess_time

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    sock.setblocking(False)
    print("Connected to server. Waiting for game to start...")

    inputs = [sock]  # Only monitor the socket
    outputs = []

    while True:
        readable, _, exceptional = select.select(inputs, outputs, inputs, 0.5)

        for s in readable:
            if s is sock:
                try:
                    data = s.recv(1024)
                    if not data:
                        print("Server disconnected.")
                        sock.close()
                        return
                    msg = data.decode('utf-8').strip()
                    print(msg)

                    # Update game state
                    if "ROUND" in msg:
                        current_state = "playing"
                        next_guess_time = 0  # trigger immediate guess
                    elif "GAME OVER" in msg:
                        current_state = "standby"
                except:
                    print("Lost connection to server.")
                    return

        # Automatic guessing every 2 seconds
        if current_state == "playing" and time.time() > next_guess_time:
            num = random.randint(1, 50)
            try:
                sock.send(str(num).encode('utf-8'))
                print(f"Auto-guess: {num}")
            except BrokenPipeError:
                print("Server closed connection.")
                return
            next_guess_time = time.time() + 2

        for s in exceptional:
            print("Socket error.")
            s.close()
            inputs.remove(s)

if __name__ == "__main__":
    main()