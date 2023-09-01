# DFP (DIGITAL FORUM PROTOCOL)

![DFP Logo](https://your-image-url.com)

## 🚀 Project Overview

DFP is a cutting-edge application-level protocol for controlling digital forum interactions. This Python-based multi-threaded implementation handles basic application-level commands with finesse, creating a seamless experience for forum users.

🤖 **Client and Server Implementation**: Both client and server components have been meticulously crafted to ensure smooth communication.

🔐 **TCP-like Authentication**: DFP employs a secure authentication process involving tokens defined in DFP_CONSTS.py, akin to the robustness of TCP.

📂 **File Handling**: Users can effortlessly upload and delete files, enhancing the forum's versatility.

❤️ **Heartbeat Packet**: An ingenious heartbeat packet thread implementation ensures server stability, enabling smooth exits and shutdowns.

## 💻 Code Overview

The codebase is neatly organized into two major directories: `Client` and `Server`, each containing four essential files.

### Client-side:
- **client.py**: The entry point for client-server interaction. It establishes connections and initiates the communication process.
- **client_manager.py**: Implements the Client class, orchestrating authentication, forum interaction, and command execution.
- **client_process_commands.py**: Handles responses to various commands sent by the server.
- **DFP_CONSTS.py**: Stores crucial string constants and protocol details, the backbone of the DFP.

### Server-side:
- **server.py**: The server's nucleus, listening for connections and managing multiple clients with multithreading.
- **server_manager.py**: The counterpart of client_manager.py, managing server-side interactions.
- **server_process_commands.py**: Deals with command execution and responses.
- **DFP_CONSTS.py**: The heart of the protocol, containing vital constants and protocol specifications.

📝 **Note**: Maintain separate directories for the client and server when running the program, ensuring DFP_CONSTS.py is present in both.

## 📜 Application Layer Message Format

DFP relies on a combination of string constants and JSON for communication. String constants, defined in DFP_CONSTS.py, manage state transitions and interactions. JSON is used for more complex command functionalities like RDT (Read Data) and LST (List Files).

Notable Constants:
- **FORUM_START**: Marks the beginning of a forum interaction.
- **INVALID_COMMAND**: Indicates an invalid command.
- **COMMAND_FOUND**: Confirms a valid command.
- **PROCESS_COMMAND**: Signals the processing of a command.

## 💡 System Internals

The interaction begins with the server's launch, waiting for connections on 127.0.0.1:(Server_Port). Clients connect using `client.py <Server_IP> <Server_Port>`, with the server spawning a new thread for each connection.

An intriguing aspect is the use of an extra socket for heartbeat messages, enhancing robustness. This feature ensures clients are notified when the server exits (SHT command).

## 🔄 Design Trade-Offs

The project adopts multithreading for client sockets and parallel "I am alive" threads. Mutex locks ensure thread safety. Object-oriented programming is used for managing client and server states, enhancing code clarity.

## 🌟 Possible Improvements

While the project's current state is commendable, there's room for improvement. Consider these enhancements:
- Dynamic message generation instead of static string constants.
- Optimize thread creation using thread pools.
- Explore event-driven programming and `select` for efficient messaging.
- Implement file removal functionality.
