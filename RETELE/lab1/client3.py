import socket

server_address = ('127.0.0.1', 6543)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server_address)

msg = input("Message: ")
msg_length = len(msg)
s.send(msg_length.to_bytes(4, 'big'))
s.send(msg.encode('utf-8'))
reversed_msg = s.recv(1024).decode('utf-8')
print("Reversed from server:", reversed_msg)

s.close()
