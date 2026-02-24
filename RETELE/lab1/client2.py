import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(server_address)

msg=input("Enter string: ")
msg_length=len(msg)

s.send(msg_length.to_bytes(4,'big'))
s.send(msg.encode('utf-8'))

nr_spaces=int.from_bytes(s.recv(4),'big')
print("Number of spaces in the string: ", nr_spaces)
s.close()