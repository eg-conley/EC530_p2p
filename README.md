# Peer-to-Peer Chat Application
An interactive chat application using peer-to-peer networking.

## Table of Contents
 1. [Overview](#overview)
 2. [File Structure](#file-structure)
 3. [How to Use](#how-to-use)
 4. [Future Improvements](#future-improvements)

## Overview
This chat application 

### Features
* Data is distrubted and not stored in a central server
* Local data is stored on the clients
* Data stored on the device is non-volatile
* Key is different between chats

### Menu Options
 1. CONNECT TO PEER
 2. SEND CHAT
 3. CHAT HISTORY
 4. LIST PEERS
 5. EXIT

## File Structure
EC530_p2p/ \
|--client_server # files for testing client-server architecture, not needed to run \
  |--... \
|-- client_p2p.py # "client" side of p2p \
|-- main.py # main application to run \
|-- message_data.py # handles + stores message data \
|-- server_p2p.py # "server" side of p2p \

## How to Use
### Requirements
* Python 3.9 or newer
* MacOS, Windows
* Python packages: threading

### Steps
 1. Clone the repository
 2. Navigate to the directory containing the files
 3. Open a terminal/shel
 4. Run python3 main.py [port] (in virtual environment)

### Example Use
In Terminal 1: python3 main.py 6000
  * This will pull up the options menu for user 1
In Terminal 2: python3 main.py 6001
  * This will pull up the options menu for user 2
In Terminal 1: type [1] to connect to another peer
  * You will be prompted to enter the ip address (127.0.0.1) and port (6001) to connect to user 2
  * You will connect to user 2 and can now send chats by entering [2]

## Future Improvements
* Transfer data to proper database
* Create a UI
