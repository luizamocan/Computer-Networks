import socket

HOST = '127.0.0.1'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

word_len = client.recv(1024).decode()
print(f"The word has {word_len} letters.")

while True:
    letter = input("Enter a letter: ")
    client.send(letter.encode('utf-8'))
    response = client.recv(1024).decode()
    print(response)
    if "BYE" in response.lower() or  "won" in response.lower() or "lost" in response.lower():
        print("Game over, connection closed.")
        client.close()
