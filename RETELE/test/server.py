import socket
import time
import random
HOST='127.0.0.1'
PORT=5555


TOTAL_NUMBERS=40
CALLED_NUMBERS=20
CARD_SIZED=5
MIN_PLAYERS=3


def print_card(card):
	for i in range(0,25,5):
		print(card[i:i+5])
	print()


def check_win(marks):
	for r in range(5):
		if all(marks[r]): 
			return True
	for c in range(5):
		for r in range(5):
			if all(marks[r][c]):
				return True
	for i in range(5):
		if all(marks[i][i]):
			return True
	for i in range(5):
		if all(marks[i][4-i]):
			return True
	return False
			

print("Server started.Waiting for clients...")
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)

connections=[]
cards=[]
marks=[]
while len(connections)<MIN_PLAYERS:
	connection,client_address=s.accept()
	print(f"New client connected: {client_address}")
	connections.append(connection)
	card=random.sample(range(1,TOTAL_NUMBERS+1),25)
	cards.append(card)
	marks.append([[False]*5 for _ in range(5)])
	connection.send((" ".join(map(str, card))).encode('utf-8'))
	
print("Enough players!Starting the game...")

winner_found=False
numbers_to_call=random.sample(range(1,TOTAL_NUMBERS+1),20)

for num in numbers_to_call:
	if winner_found:
		break
	print(f"Calling number: {num}")
	for c in connections:
		c.send(f"CALL {num}".encode('utf-8'))
	time.sleep(1)
	for idx,connection in enumerate(connections):
		try:
			data=connection.recv(1024).decode('utf-8')
			if data.startswith("HAVE"):
				parts=data.split()
				have_num=int(parts[1])
				if have_num==num:
					i=cards[idx].index(have_num)
					r,c=divmod(i,5)
					marks[idx][r][c]=True
					print(f"Player {idx+1} marked {num}")
					if check_win(marks[idx]):
						print(f"Player {idx+1} has bingo!")
						for c2 in connections:
							c2.send(f"Win at player {idx+1}".encode('utf-8'))
						winner_found=True
						break
		except Exception as e:
			print(e)

if not winner_found:
	print("No winner found")
	for c in connections:
		c.send("END No winner".encode('utf-8'))

for c in connections:
	c.close()

s.close()
print("Game over.Server closing.")
			