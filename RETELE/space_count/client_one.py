import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(server_address)

msg=input("Enter message:" )
len_msg=len(msg)
s.send(len_msg.to_bytes(4,'big'))
s.send(msg.encode('utf-8'))

response_msg=s.recv(1024).decode('utf-8')
print("Number of spaces: ",response_msg)
s.close()