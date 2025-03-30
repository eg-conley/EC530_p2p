# https://medium.com/@amannagpal4/how-to-create-your-own-decentralized-file-sharing-service-using-python-2e00005bdc4a
# derived from code from DeepSeek + edited


import socket
import json

class Client:

    @staticmethod
    def connect_to_peer(ip, port, peer_id, local_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ip, port))

                # send handshake first to establish connection
                handshake = {
                'type': 'handshake',
                'peer_id': peer_id,
                'port': local_port
                }
                sock.sendall(json.dumps(handshake).encode('utf-8'))

                # wait for response
                data = sock.recv(4096)
                return json.loads(data.decode('utf-8')) # return the response

        except Exception as e:
            print(f"ERROR CONNECTING TO PEER: {e}")
            return None

    @staticmethod
    # send message to a specific peer
    def send_message(ip, port, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((ip, port))
                client_socket.sendall(json.dumps(message).encode('utf-8'))
                return True
        except Exception as e:
            print(f"ERROR SENDING MESSAGE: {e}")
            return False