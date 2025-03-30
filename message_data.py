# derived code from DeepSeek + edited

import json
import os
from datetime import datetime


class MessageData:
    def __init__(self, peer_id):
        self.peer_id = peer_id
        self.data_dir = f"chat_data_{self.peer_id}"
        os.makedirs(self.data_dir, exist_ok=True)
        self.messages = {}
        self.peers = {}
        self.load_messages()

    # load messages from disk
    def load_messages(self):
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                peer_id = filename[:-5]
                try:
                    with open(os.path.join(self.data_dir, filename), 'r') as f:
                        self.messages[peer_id] = json.load(f)
                except:
                    self.messages[peer_id] = []

    # save messages to local disk
    def save_messages(self, peer_id):
        if peer_id in self.messages:
            filename = os.path.join(self.data_dir, f"{peer_id}.json")
            with open(filename, 'w') as f:
                json.dump(self.messages[peer_id], f)

    # add new peer to "database"
    def add_peer(self, peer_id, ip, port):
        self.peers[peer_id] = {
            'ip': ip,
            'port': port
        }

    # add message to "database"
    def add_message(self, peer_id, sender, message):
        if peer_id not in self.messages:
            self.messages[peer_id] = []

        self.messages[peer_id].append({
            'sender': sender,
            'message': message,
            'timestamp': str(datetime.now())
        })
        self.save_messages(peer_id)

    # chat history with peer
    def get_chat_history(self, peer_id):
        return self.messages.get(peer_id, [])

    # list of peers
    def get_peers(self):
        return self.peers