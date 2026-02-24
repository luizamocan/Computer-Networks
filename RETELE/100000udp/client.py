import socket
import sys

def validate_number(s: str) -> bool:
    return s.isdigit()

def validate_ip(ip: str) -> bool:
    if ip is None:
        return False
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not validate_number(part):
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True

def main():
    if len(sys.argv) < 3:
        print("Give server and port.")
        return 1

    server_ip = sys.argv[1]
    port_str = sys.argv[2]

    if not validate_ip(server_ip):
        print("Server must be a valid ip address server.")
        return 2

    if not validate_number(port_str):
        print("Port must be integer.")
        return 3

    port = int(port_str)

    print("Creating socket.")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print(f"Socket creation failed: {e}")
        sys.exit(1)

    server = (server_ip, port)

    for i in range(10000):
        # Convert i to network byte order (big-endian)
        j = i.to_bytes(4, byteorder='big')
        sock.sendto(j, server)
        print(f"Sent {i} to the server")

    sock.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())