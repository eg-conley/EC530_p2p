# https://realpython.com/python-sockets/
# https://docs.python.org/3/howto/sockets.html
import socket
import threading # for tracking multiple client connections

# define HOST and PORT
HOST = "127.0.0.1" # server's hostname/IP addr
PORT = 8000 # same port as the server

# simple echo server
def start_server():
    # establish socket on server side
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen() # start listening
    print(f"LISTENING ON:{HOST}, {PORT}")

    # complete connection/handshake with client
    while True:
        client_socket, address = server.accept()

        # start new thread for multiple connections
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()
        print(f"ACTIVE CONNECTIONS: {threading.active_count() - 1}")

# receive messages from client
def handle_client(client_socket, address):
    print(f"NEW CLIENT: {address}")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[RECEIVED MESSAGE FROM {address}:] {message}")
            reply = "RECEIVED YOUR MESSAGE: " + message
            client_socket.sendall(reply.encode('utf-8)'))
        except:
            break

    # disconnect if connection error
    print(f"DISCONNECTED FROM {address}")
    print(f"ACTIVE CONNECTIONS: {threading.active_count() - 1}")
    client_socket.close()

if __name__ == "__main__":
    start_server()