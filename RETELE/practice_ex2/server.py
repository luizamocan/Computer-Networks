import socket
import threading
import time

HOST='127.0.0.1'
PORT=5555

MIN_CLIENTS=4
clients=[]
state="standby"
lock=threading.Lock()
data_count=0
total_sum=0

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            pass

def handle_client(connection,client_address):
    global total_sum,data_count,state
    print(f"Client {client_address} connected")
    try:
        while True:
            data=connection.recv(1024)
            if not data:
                break
            number=int(data.decode('utf-8'))
            with lock:
                total_sum+=number
                data_count+=1
                print(f"Received {number}C from {client_address}. Total sum: {total_sum}, Data count: {data_count},Average temeprature {total_sum/data_count}")
                if data_count==200:
                    if state=="normal":
			#could remove the if but have not tested,worked in my ex
                        state="high"
                        print(f"[STATE CHANGED] Server requiring {state} temperatures. ")
                        broadcast(state)
                if total_sum/data_count>=30:
                    print("[STOP] Average temperature exceeded 30 Celsius degrees.")
                    broadcast("shutdown")
                    break
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        connection.close()
        with lock:
            if connection in clients:
                clients.remove(connection)
        print(f"Client {client_address} disconnected")

def accept_clients(server_socket):
    global state
    while True:
        connection,client_address=server_socket.accept()
        with lock:
            clients.append(connection)
        threading.Thread(target=handle_client,args=(connection,client_address),daemon=True).start()
        print(f"[ACTIVE CLIENTS] {len(clients)} clients connected")

def control_loop():
    global state
    while True:
        with lock:
            client_count=len(clients)
            if state=="standby" and client_count>=MIN_CLIENTS:
                state="normal"
                print(f"[STATE CHANGE] Requesting {state} temperatures. ")
                broadcast("normal")
            elif data_count>0 and total_sum/data_count>=30:
                break

def start_server():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(5)
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    threading.Thread(target=accept_clients,args=(s,),daemon=True).start()
    control_loop()
    print("[SERVER SHUTDOWN] Collection finished. Average: {total_sum/data_count:.2f}")
    s.close()

if __name__ == "__main__":
    start_server()


