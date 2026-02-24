import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(server_address)

msg=input("ENTER THE STRING: ")

s.send(len(msg).to_bytes(4,'big'))
s.send(msg.encode('utf-8'))

resp_length=int.from_bytes(s.recv(4),'big')
print("Number of spaces in the string: ", resp_length)
s.close()