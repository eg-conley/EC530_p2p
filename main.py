# derived from code from DeepSeek + edited

from server_p2p import Server
from client_p2p import Client
from message_data import MessageData
import uuid
import socket
import json
from datetime import datetime


class P2PChatApplication:

    # constructor
    def __init__(self, port):
        self.port = port
        self.peer_id = f"peer_{port}_{uuid.uuid4().hex[:8]}" # 4 digit id number
        self.message_data = MessageData(self.peer_id) # create instance of MessageData
        self.server = Server(port, self.handle_type, self.peer_id) # create instance of Server

    # start the application
    def start(self):
        self.server.start()
        print(f"PEER ID: {self.peer_id}")
        print(f"LISTENING ON PORT: {self.port}")

    # stop the application
    def stop(self):
        self.server.stop()

    # handle types of messages
    def handle_type(self, message, addr):
        try:
            if message['type'] == 'handshake':
                self.handle_handshake(message, addr)
            elif message['type'] == 'chat':
                self.handle_chat(message)
        except Exception as e:
            print(f"ERROR HANDLING MESSAGE: {e}")

    # handle peer connection
    def handle_handshake(self, message, addr):
        peer_id = message['peer_id']
        self.message_data.add_peer(peer_id, addr[0], message['port'])

        # send response back
        response = {
            'type': 'handshake_response',
            'peer_id': self.peer_id
        }
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((addr[0], message['port']))
            sock.sendall(json.dumps(response).encode())


    # handle chat message
    def handle_chat(self, message):
        peer_id = message['peer_id']
        self.message_data.add_message(peer_id, peer_id, message['content'])
        print(f"\nNEW MESSAGE FROM {peer_id}: {message['content']}")

    # connect to peer
    def connect_to_peer(self, ip, port):
        response = Client.connect_to_peer(ip, port, self.peer_id, self.port)
        if response and response['type'] == 'handshake_response':
            peer_id = response['peer_id']
            self.message_data.add_peer(peer_id, ip, port)
            print(f"CONNECTED TO PEER: {peer_id}")
            return True
        return False

    # send chat to peer
    def send_chat(self, peer_id, text):
        peer = self.message_data.get_peers().get(peer_id)
        if not peer:
            print(f"PEER {peer_id} NOT FOUND")
            return False

        chat = {
            'type': 'chat',
            'peer_id': self.peer_id,
            'content': text,
            'timestamp': str(datetime.now())
        }

        if Client.send_message(peer['ip'], peer['port'], chat):
            self.message_data.add_message(peer_id, 'me', text)
            return True
        return False

    # display chat history with a peer
    def show_chat(self, peer_id):
        messages = self.message_data.get_chat_history(peer_id)
        if messages:
            print(f"\nCHAT HISTORY WITH {peer_id}:")
            for msg in messages:
                print(f"[{msg['timestamp']}] {msg['sender']}: {msg['message']}")
        else:
            print(f"NO CHATS WITH {peer_id}")

    # list all peers
    def list_peers(self):
        peers = self.message_data.get_peers()
        print("\nCONNECTED PEERS:")
        for peer_id, info in peers.items():
            print(f"{peer_id} - {info['ip']}:{info['port']}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python main.py [port]")
        sys.exit(1)

    # get port value from the terminal and start application with it
    port = int(sys.argv[1])
    app = P2PChatApplication(port)
    app.start()

    try:
        while True:
            print("\nOPTIONS:")
            print("1: CONNECT TO PEER 🛜")
            print("2: SEND CHAT 💬")
            print("3: CHAT HISTORY ⏳")
            print("4: LIST PEERS 📋")
            print("5: EXIT 👋")

            # determine function depending on input
            choice = input("Enter option number: ")
            if choice == '1':
                ip = input("Enter peer IP: ")
                port = int(input("Enter peer port: "))
                app.connect_to_peer(ip, port)
            elif choice == '2':
                peer_id = input("Enter peer ID: ")
                message = input("Enter message: ")
                app.send_chat(peer_id, message)
            elif choice == '3':
                peer_id = input("Enter peer ID: ")
                app.show_chat(peer_id)
            elif choice == '4':
                app.list_peers()
            elif choice == '5':
                break

    except KeyboardInterrupt:
        print("\nSHUTTING DOWN..")
    finally:
        app.stop()