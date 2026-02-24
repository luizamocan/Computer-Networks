import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(server_address)

msg1=input("ENTER THE FIRST STRING: ")
s.send(len(msg1).to_bytes(4,'big'))
s.send(msg1.encode('utf-8'))

msg2=input("ENTER THE SECOND STRING: ")
s.send(len(msg2).to_bytes(4,'big'))
s.send(msg2.encode('utf-8'))

resp_length=int.from_bytes(s.recv(4),'big')
resp=s.recv(resp_length).decode('utf-8')
print("SORTED STRING: ", resp)
s.close()