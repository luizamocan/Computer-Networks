import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address=('127.0.0.1',5555)
s.connect(server_address)

msg1=input("enter the first number:")
len_msg1=len(msg1)

msg2=input("enter the second number:")
len_msg2=len(msg2)

s.send(len_msg1.to_bytes(4,'big'))
s.send(msg1.encode('utf-8'))
s.send(len_msg2.to_bytes(4,'big'))
s.send(msg2.encode('utf-8'))

resp_length=int.from_bytes(s.recv(4),'big')
resp=s.recv(resp_length).decode('utf-8')
print("Sum of the numbers:", resp)
s.close()