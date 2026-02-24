import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address=('127.0.0.1',5555)
s.connect(server_address)

msg=input("enter the message:")
len_msg=len(msg)

s.send(len_msg.to_bytes(4,'big'))
s.send(msg.encode('utf-8'))

s.close()