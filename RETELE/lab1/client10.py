import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(server_address)

string1 = input("Enter string 1 : ")
s.send(len(string1).to_bytes(4, 'big'))
s.send(string1.encode('utf-8'))

string2 = input("Enter string 2: ")
s.send(len(string2).to_bytes(4, 'big'))
s.send(string2.encode('utf-8'))

char_length = int.from_bytes(s.recv(4), 'big')
max_char = s.recv(char_length).decode('utf-8')

occurences_length=int.from_bytes(s.recv(4),'big')
occurences=s.recv(occurences_length).decode('utf-8')
print(f"Most used character: {max_char} with number of occurences: {occurences}")

s.close()
