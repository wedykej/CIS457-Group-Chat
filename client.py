import socket
import threading
import sys

stop_threads = False

# Server connection details
HOST = '127.0.0.1'
PORT = 5000  # Port for SSH tunnel

# Emoji shortcuts dictionary
emojis = {
    ":)": "😊",    # Add smile emoji for :)
    ":(": "☹",    # Add sad face emoji for :(
    ":3": "😺",    # Add cat face emoji for :3
    "<3": "❤"     # Add heart emoji for <3
}

# Create client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
except Exception as e:
    print(f"Unable to connect to server: {e}")
    sys.exit()

def replace_emojis(message):
    for shortcut, emoji in emojis.items():
        message = message.replace(shortcut, emoji)
    return message

def receive_messages():
    global stop_threads
    while not stop_threads:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                print("Disconnected from server.")
                stop_threads = True
                break
            print(message)  # Print received messages from the server
        except:
            if not stop_threads:
                print("Lost connection to the server.")
            stop_threads = True
            break

def send_messages():
    global stop_threads
    nickname = input("Choose your nickname: ")
    client.send(nickname.encode('utf-8'))

    while not stop_threads:
        try:
            message = input()  # User inputs a message
            message = replace_emojis(message)

            if message == "/help":
                print("Available commands:\n/help - Show help menu\n/list - Show active users\n/exit - Exit chat")
                continue
            elif message == "/exit":
                client.send(message.encode('utf-8'))
                print("Exiting chat...")
                stop_threads = True
                client.close()
                break

            # Send the message to the server, but don't print it on the user's side
            client.send(message.encode('utf-8'))

        except:
            break

if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    write_thread = threading.Thread(target=send_messages)
    write_thread.start()
