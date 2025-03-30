# https://medium.com/@amannagpal4/how-to-create-your-own-decentralized-file-sharing-service-using-python-2e00005bdc4a
# derived from code from DeepSeek + edited

import socket
import threading
import json

class Server:

    # constructor
    def __init__(self, port, message_handler, peer_id):
        self.port = port
        self.message_handler = message_handler
        self.isRunning = False
        self.thread = None
        self.peer_id = peer_id

    # starts thread with peer "servers"
    def start(self):
        self.isRunning = True
        self.thread = threading.Thread(target=self.start_server, daemon=True)
        self.thread.start()

    def stop(self):
        self.isRunning = False
        # dummy connection to unblock accept()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('127.0.0.1', self.port))
        except:
            pass

        if self.thread:
            self.thread.join()

    # actual server that listen for new peer connections
    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to reuse ports if needed
            server_socket.bind(('0.0.0.0', self.port))
            server_socket.listen()

            # complete connection with handshake
            while self.isRunning:
                try:
                    conn, addr = server_socket.accept()
                    print(f"\nNEW CONNECTION FROM: {addr}")
                    # start new thread
                    threading.Thread(target=self.handle_client, args=(conn, addr)).start()
                except:
                    break

    # handle new connections
    def handle_client(self, conn, addr):
        try:
            data = conn.recv(1024)
            if not data:
                return

            # decode data
            message = json.loads(data.decode('utf-8'))
            self.message_handler(message, addr)

            if message.get('type') == 'handshake':
                response = {
                    'type': 'handshake_response',
                    'peer_id': self.peer_id,
                    'port': self.port
                    }
                conn.sendall(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print(f"ERROR WITH CONNECTION: {e}")
        # disconnect if connection error
        finally:
            conn.close()