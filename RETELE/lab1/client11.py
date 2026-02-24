import socket

server_address = ('127.0.0.1', 5555)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server_address)


firstname = input("Enter first name: ")
lastname = input("Enter last name: ")
gender = input("Enter gender: ")
age = input("Enter age: ")

person_str = f"{firstname}|{lastname}|{gender}|{age}"
encoded = person_str.encode('utf-8')

s.send(len(encoded).to_bytes(4, 'big'))
s.send(encoded)


data_length = int.from_bytes(s.recv(4), 'big')
recv_data = b''
while len(recv_data) < data_length:
    recv_data += s.recv(data_length - len(recv_data))

updated_person_str = recv_data.decode('utf-8')
fields = updated_person_str.split('|')
print(f"Updated person received from server: {fields[0]} {fields[1]}, {fields[2]}, {fields[3]} years old")

s.close()
