# ENTIRELY WRITTEN W CHATGPT- initial investigation of client-server interactions

import socket
import threading

HOST = '127.0.0.1'  # server address
PORT = 8000 # same port as server

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[SERVER]: {message}")
        except ConnectionResetError:
            break

    print("[CONNECTION CLOSED]")
    client_socket.close()

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("[CONNECTED] Connected to the server.")

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == "exit":
            break
        client.send(message.encode('utf-8'))

    client.close()
    print("[DISCONNECTED] Client closed connection.")

if __name__ == "__main__":
    start_client()
