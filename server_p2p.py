# https://medium.com/@amannagpal4/how-to-create-your-own-decentralized-file-sharing-service-using-python-2e00005bdc4a
# derived from code from DeepSeek + edited

# import socket
# import threading
# import json
#
# class Server:
#
#     # constructor
#     def __init__(self, port, message_handler):
#         self.port = port
#         self.message_handler = message_handler
#         self.isRunning = False
#         self.thread = None
#
#     # starts thread with peer "servers"
#     def start(self):
#         self.isRunning = True
#         self.thread = threading.Thread(target=self.start_server, daemon=True)
#         self.thread.start()
#
#     def stop(self):
#         self.isRunning = False
#         # dummy connection to unblock accept()
#         try:
#             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#                 sock.connect(('127.0.0.1', self.port))
#         except:
#             pass
#
#         if self.thread:
#             self.thread.join()
#
#     # actual server that listen for new peer connections
#     def start_server(self):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#             server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to reuse ports if needed
#             server_socket.bind(('0.0.0.0', self.port))
#             server_socket.listen()
#
#             # complete connection with handshake
#             while self.isRunning:
#                 try:
#                     conn, addr = server_socket.accept()
#                     print(f"NEW CONNECTION FROM: {addr}")
#                     # start new thread
#                     threading.Thread(target=self.handle_client, args=(conn, addr)).start()
#                 except:
#                     break
#
#     # handle new connections
#     def handle_client(self, conn, addr):
#         try:
#             data = conn.recv(1024)
#             if not data:
#                 return
#
#             # decode data
#             message = json.loads(data.decode('utf-8'))
#             self.message_handler(message, addr)
#
#         except Exception as e:
#             print(f"ERROR WITH CONNECTION: {e}")
#         # disconnect if connection error
#         finally:
#             print(f"DISCONNECTED FROM {addr}")
#             conn.close()


import socket
import threading
import json # for database functionality
from datetime import datetime # for logging

class Server:

    # constructor
    def __init__(self, port, message_handler):
        self.port = port
        self.message_handler = message_handler
        self.running = False
        self.server_thread = None

    # start "server" and listen for connections
    def start(self):
        self.running = True
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    # stop server
    def stop(self):
        self.running = False
        # Create a dummy connection to unblock the accept() call
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', self.port))
        except:
            pass

        if self.server_thread:
            self.server_thread.join()

    # main server loop that listens for connections
    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', self.port))
            s.listen()

            while self.running:
                try:
                    conn, addr = s.accept() # accept the connection
                    threading.Thread(target=self.handle_connection, args=(conn, addr)).start() # run the connection on thread
                except:
                    break

    # this fxn handles new connections
    def handle_connection(self, conn, addr):
        try:
            data = conn.recv(4096)
            if not data:
                return

            message = json.loads(data.decode('utf-8')) # decode data
            self.message_handler(message, addr)

        except Exception as e:
            print(f"Error handling connection: {e}")
        finally:
            conn.close()