import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(server_address)

msg = input("Enter numbers separated by spaces: ")

# Send length and message
s.send(len(msg).to_bytes(4, 'big'))
s.send(msg.encode('utf-8'))


resp_length = int.from_bytes(s.recv(4), 'big')
total = s.recv(resp_length).decode('utf-8')
print("Sum received from server:", total)

s.close()
