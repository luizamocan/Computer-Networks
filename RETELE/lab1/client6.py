import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(server_address)

msg=input("ENTER STRING: ")
character=input("ENTER CHARACTER: ")

s.send(len(msg).to_bytes(4,'big'))
s.send(msg.encode('utf-8'))

s.send(len(character).to_bytes(4,'big'))
s.send(character.encode('utf-8'))

result_length=int.from_bytes(s.recv(4),'big')
result=s.recv(result_length).decode('utf-8')
print("Result: ", result)
s.close()