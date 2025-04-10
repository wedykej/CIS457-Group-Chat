Real-time Multi-User Group Chat


This project is a real-time multi-user group chat application implemented in Python using sockets and threading. It allows users to connect to a central server, communicate with each other in a chatroom, and interact with features like sending messages, listing active users, and using emojis. The server handles multiple client connections simultaneously, broadcasting messages to all connected users except the sender.


Features:
Real-time Messaging: Users can send messages to the group, and the messages are broadcast to all active users (except the sender).

Nickname Assignment: Clients must choose a unique nickname upon connecting to the server.

Emoji Support: Simple emoji shortcuts like :), :(, :3, and <3 are automatically replaced with their corresponding emoji images.

User Management: Users can see a list of active participants in the chatroom using the /list command.

Exit Command: Users can exit the chat by typing /exit, which removes them from the server and notifies others.

Multi-client Support: The server can handle multiple clients simultaneously, with each client running in its own thread.


Technologies Used:
Python: The application is written in Python.

Socket Programming: Communication between the server and clients is handled using TCP sockets.

Threading: Each client operates in its own thread, allowing for simultaneous handling of multiple clients.

Datetime: Timestamps are used to log when messages are sent.


How It Works:
Server:
The server listens for incoming client connections.

Upon accepting a connection, it assigns a nickname to the client and starts a thread to handle their messages.

The server broadcasts all user messages (except the sender's) to every other client.

Client:
Each client connects to the server, chooses a nickname, and enters a loop to send and receive messages.

Clients can use special commands to interact with the chat, such as /list to see active users and /exit to leave the chat.


Commands:
/help: Displays a list of available commands.

/list: Lists all active users in the chatroom.

/exit: Exits the chatroom and disconnects the client from the server.


I, Josh Wedyke, completed this assignment by myself

https://github.com/wedykej/CIS457-Group-Chat.git 
