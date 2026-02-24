import socket

HOST = '127.0.0.1'
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
print(f"Server is listening on {HOST}:{PORT}")

while True:
    print("Waiting for clients...")
    conn, addr = s.accept()
    with conn:
        print("Connected:", addr)

        data = conn.recv(4)
        if not data:
            continue
        msg_length = int.from_bytes(data, 'big')

        msg = conn.recv(msg_length).decode('utf-8')
        print("Received:", msg)

        try:
            numbers = [float(x) for x in msg.split()]
            total = sum(numbers)
        except ValueError:
            total = 0.0

        total_str = str(total).encode('utf-8')
        conn.send(len(total_str).to_bytes(4, 'big'))
        conn.send(total_str)

        print(f"Sent sum: {total}")
