import socket
import sys
import struct

def validate_number(s: str) -> bool:
    return s.isdigit()

def main():
    if len(sys.argv) < 2:
        print("Give me a port.")
        return 1

    if not validate_number(sys.argv[1]):
        print("Port must be integer.")
        return 2

    port = int(sys.argv[1])

    print("Creating socket.")
    server_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_addr = ('', port)  # '' means INADDR_ANY

    print(f"Binding socket to port {port}")
    try:
        server_fd.bind(server_addr)
    except socket.error as e:
        print(f"Bind error.\n{e}")
        sys.exit(1)

    print("Waiting for clients...")

    prev = -1
    while True:
        for i in range(10000):
            data, client_addr = server_fd.recvfrom(4)  # expecting 4 bytes for int
            if len(data) < 4:
                continue
            num = struct.unpack('!I', data)[0]  # network byte order to host

            if num != prev + 1:
                print(f"Wrong order at {i}\nexpecting: {prev + 1}\nreceived: {num}")

            prev = num

            print(f"Received from {client_addr[0]} : {num}")

if __name__ == "__main__":
    main()