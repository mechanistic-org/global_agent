import socket
import threading
import sys
import time

def read_and_forward(src, dst, direction):
    # direction: "C2S" (Client->Server) or "S2C" (Server->Client)
    try:
        while True:
            data = src.recv(4096)
            if not data:
                print(f"[{direction}] Connection closed.")
                sys.stdout.flush()
                break
            
            with open(f"proxy_{direction}.log", "ab") as f:
                f.write(data)
                
            dst.send(data)
    except Exception as e:
        print(f"[{direction}] Error: {e}")
    finally:
        src.close()
        dst.close()

def handle_client(client_socket):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.connect(('127.0.0.1', 8001))
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        client_socket.close()
        return

    print("Proxying new connection...")
    sys.stdout.flush()
    t1 = threading.Thread(target=read_and_forward, args=(client_socket, server_socket, "C2S"))
    t2 = threading.Thread(target=read_and_forward, args=(server_socket, client_socket, "S2C"))
    t1.start()
    t2.start()

def main():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.bind(('127.0.0.1', 8000))
    proxy.listen(5)
    print("Proxy listening on 8000...")
    sys.stdout.flush()

    while True:
        client, addr = proxy.accept()
        t = threading.Thread(target=handle_client, args=(client,))
        t.start()

if __name__ == "__main__":
    main()
