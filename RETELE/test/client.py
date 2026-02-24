
import socket
import random

HOST = '127.0.0.1'
PORT = 5555

def print_card(card, marked):
    for i in range(5):
        row = []
        for j in range(5):
            num = card[i*5 + j]
            if marked[i][j]:
                row.append(f"[{num:2d}]")
            else:
                row.append(f" {num:2d} ")
        print(" ".join(row))
    print()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = s.recv(1024).decode('utf-8')
card = list(map(int, data.split()))
marked = [[False]*5 for _ in range(5)]
print("Your Bingo card:")
print_card(card, marked)


while True:
    data = s.recv(1024).decode('utf-8')
    if not data:
        break

    if data.startswith("CALL"):
        _, num_str = data.split()
        num = int(num_str)
        print(f"Number called: {num}")

        if num in card:
            i = card.index(num)
            r, c = divmod(i, 5)
            marked[r][c] = True
            print(f"You have {num}! Reporting to server...")
            s.send(f"HAVE {num}".encode('utf-8'))
        print_card(card, marked)

    elif data.startswith("WIN"):
        print(data)
        print("Game over! Someone won.")
        break

    elif data.startswith("END"):
        print(data)
        break

s.close()