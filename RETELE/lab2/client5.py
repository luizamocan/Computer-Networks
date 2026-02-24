import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(server_address)

msg1=input("ENTER THE NUMBER: ")
s.send(len(msg1).to_bytes(4,'big'))
s.send(msg1.encode('utf-8'))

resp_length=int.from_bytes(s.recv(4),'big')
resp=s.recv(resp_length).decode('utf-8')
print("LIST OF DIVISORS: ", resp)
s.close()