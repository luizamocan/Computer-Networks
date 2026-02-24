import socket

server_address = ('127.0.0.1', 5555)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(server_address)
s.listen(5)
print("Server listening on:", server_address)

while True:
    print("Waiting for client...")
    connection, client_address = s.accept()
    with connection:
        print("Client connected:", client_address)

        data = connection.recv(4)
        if not data:
            continue
        msg_length = int.from_bytes(data, 'big')


        msg_data = b''
        while len(msg_data) < msg_length:
            msg_data += connection.recv(msg_length - len(msg_data))

        person_str = msg_data.decode('utf-8')
        print("Received person string:", person_str)

        fields = person_str.split('|')
        firstname, lastname, gender, age = fields[0], fields[1], fields[2], int(fields[3])

 
        age += 1


        updated_person_str = f"{firstname}|{lastname}|{gender}|{age}"
        encoded = updated_person_str.encode('utf-8')

        connection.send(len(encoded).to_bytes(4, 'big'))
        connection.send(encoded)

        print("Sent updated person string:", updated_person_str)
