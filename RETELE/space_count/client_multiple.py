import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(server_address)

msg=input("Enter the string:")
msg_len=len(msg)


s.send(msg_len.to_bytes(4,'big'))
s.send(msg.encode('utf-8'))

response=s.recv(1024).decode('utf-8')
print("Number of spaces:", response)
s.close()