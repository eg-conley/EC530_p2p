# https://medium.com/@amannagpal4/how-to-create-your-own-decentralized-file-sharing-service-using-python-2e00005bdc4a
# https://github.com/Ezi0aaudit0re/P2P-music-sharing/blob/master/server_client/client.py
"""
    This file is the constants of the peer to peer network
"""

import socket
import threading
import sys
import time
from random import randint
from music import *
import fileIO

BYTE_SIZE = 1024
HOST = '127.0.0.1'
PORT = 5000
PEER_BYTE_DIFFERENTIATOR = b'\x11'
RAND_TIME_START = 1
RAND_TIME_END = 2
REQUEST_STRING = "req"