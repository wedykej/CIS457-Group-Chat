import socket
import threading
from datetime import datetime

# Server settings
HOST = '127.0.0.1'
PORT = 5000  # Port for SSH tunnel

# Server socket setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message, sender=None, sender_client=None):
    """
    Sends a message to all clients except the sender.
    If sender is None, it's a system message and goes to everyone.
    """
    timestamp = datetime.now().strftime('%H:%M:%S')
    for client in clients:
        try:
            if sender:
                # User message: send only to others
                if client != sender_client:
                    formatted = f"[{timestamp}] {sender}: {message}"
                    client.send(formatted.encode('utf-8'))
            else:
                # System message: send to everyone
                formatted = f"[{timestamp}] {message}"
                client.send(formatted.encode('utf-8'))
        except:
            remove_client(client)

def handle(client):
    """
    Handles messages from a client.
    """
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break

            index = clients.index(client)
            nickname = nicknames[index]

            if message == "/exit":
                remove_client(client)
                break
            elif message == "/list":
                active_users = ", ".join(nicknames)
                client.send(f"Active users: {active_users}\n".encode('utf-8'))
            else:
                # Broadcast message to other clients excluding sender
                broadcast(message, sender=nickname, sender_client=client)

        except:
            index = clients.index(client)
            client.close()
            nickname = nicknames.pop(index)
            clients.remove(client)
            broadcast(f"{nickname} left the chat.", sender=None)
            break

def remove_client(client):
    """
    Removes a client from lists and notifies others.
    """
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)
        broadcast(f"{nickname} has left the chat.", sender=None)
        client.close()

def receive_connections():
    """
    Accept new clients and start handling them.
    """
    print(f"Server is running on {HOST}:{PORT}")
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            client.send("NICKNAME".encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')

            nicknames.append(nickname)
            clients.append(client)

            print(f"Nickname of the client is {nickname}")
            broadcast(f"{nickname} joined the chat!", sender=None)

            client.send("Connected to the server! (/help for help)\n".encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except Exception as e:
            print(f"Server error: {e}")
            break

if __name__ == "__main__":
    try:
        receive_connections()
    except KeyboardInterrupt:
        print("Server shutting down...")
        for client in clients:
            client.close()
        server.close()
