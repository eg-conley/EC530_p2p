# https://realpython.com/python-sockets/
# https://docs.python.org/3/howto/sockets.html
import socket
import threading

# define HOST and PORT
HOST = "127.0.0.1" # server's hostname/IP addr
PORT = 8000 # same port as the server

def start_client():
    # create socket object and specify .SOCK_STREAM for TCP default protocol (.SOCK_DGRAM for UDP)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT)) # connect to server
    print("CONNECTED TO THE SERVER")

    receive_thread = threading.Thread(target=handle_server, args=(client,))
    receive_thread.start()

    # send messages to the server
    while True:
        message = input()
        if (message == "QUIT"): # way to break server
            break
        client.sendall(message.encode('utf-8')) # encode and send input message to server

    # close server on QUIT command
    client.close()
    print("DISCONNECTED FROM THE SERVER")
    print(f"ACTIVE CONNECTIONS: {threading.active_count() - 1}")

def handle_server(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except ConnectionResetError:
            break

    print(f"DISCONNECTED FROM SERVER")
    client_socket.close()

if __name__ == "__main__":
    start_client()