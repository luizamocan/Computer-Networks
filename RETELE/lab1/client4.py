import socket

server_address=('127.0.0.1',5555)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(server_address)


array1=input("Input the first array of characters:" )
array2=input("Input the second array of characters: ")

s.send(len(array1).to_bytes(4,'big'))
s.send(array1.encode('utf-8'))

s.send(len(array2).to_bytes(4,'big'))
s.send(array2.encode('utf-8'))


result_length=int.from_bytes(s.recv(4),'big')
result=s.recv(result_length).decode('utf-8')
print("Merged array: ", result)
s.close()