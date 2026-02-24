import socket

server_address = ('127.0.0.1', 6543)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(server_address)
s.listen(5) #allow 5 pending connections
print("Server is listening on", server_address)

while True:
    print('Waiting for clients...')
    connection, client_address = s.accept()
    with connection:
        print('Connected:', client_address)
        data = connection.recv(4)
        if not data:
            continue

        msg_length = int.from_bytes(data, 'big')
        msg = connection.recv(msg_length).decode('utf-8')
        print("Received:", msg)

        reversed_msg = msg[::-1]
        connection.send(reversed_msg.encode('utf-8'))
