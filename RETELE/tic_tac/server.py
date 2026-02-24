import socket
import random
HOST='127.0.0.1'
PORT=5555

def print_board(table):
	print(table[:3])
	print(table[3:6])
	print(table[6:])

def check_win(table):
	#coloane
	for i in range(3):
		if table[i]==table[i+3]==table[i+6]:
			if table[i]=='X':
				message="User won!"
				connection.send(message.encode('utf-8'))
				return True
			elif table[i]=='0':
				message="Computer won"
				connection.send(message.encode('utf-8'))
				return True
	if table[0]==table[4]==table[8]:
		if table[0]=='X':
			message="User won!"
			connection.send(message.encode('utf-8'))
			return True
		elif table[0]=='0':
			message="Computer won!"
			connection.send(message.encode('utf-8'))
			return True

	if table[2]==table[4]==table[6]:
		if table[2]=='X':
			message="User won!"
			connection.send(message.encode('utf-8'))
			return True
		elif table[2]=='0':
			message="Computer won!"
			connection.send(message.encode('utf-8'))
			return True
	for i in range(0,7,3):
		if table[i]==table[i+1]==table[i+2]:
			if table[i]=='X':
				message="User won!"
				connection.send(message.encode('utf-8'))
				return True
			elif table[i]=='0':
				message="Computer won!"
				connection.send(message.encode('utf-8'))
				return True
	return False

def check_tie(table):
	for i in range(9):
		if table[i]=='-':
			return False
	return True

def print_table(table):
	print(table[:3])
	print(table[3:6])
	print(table[6:])
	print()

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)
connection,client_address=s.accept()

done=False
table="---------"
connection.send(table.encode('utf-8'))
while not done:
	data=connection.recv(1024)	
	table=data.decode('utf-8')
	print("Last user's move: \n")
	print_table(table)

	if check_win(table):
		done=True
		print_table(table)
	
	if not check_tie(table):
		index=random.randint(0,8)
		while table[index]!='-':
			index=random.randint(0,8)
		table=table[:index]+'0'+table[index+1:]
		connection.send(table.encode('utf-8'))
		if not done:
			if check_win(table):
				done=True
	else:
		done=True
		message="Tie"
		print(message)
		connection.send(message.encode('utf-8'))
connection.close()
	


				

				