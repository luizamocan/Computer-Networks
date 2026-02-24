import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(server_address)

list1 = input("Enter array 1 separated by spaces: ")
s.send(len(list1).to_bytes(4, 'big'))
s.send(list1.encode('utf-8'))

list2 = input("Enter array 2 separated by spaces: ")
s.send(len(list2).to_bytes(4, 'big'))
s.send(list2.encode('utf-8'))

resp_length = int.from_bytes(s.recv(4), 'big')
total = s.recv(resp_length).decode('utf-8')
print("Elements that appear in the first list, but not in the second:", total)

s.close()
