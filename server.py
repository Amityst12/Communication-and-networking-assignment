import socket
import threading
# Reminders:  (Encode - תצפין Decode - תפצח) 

# --- CONSTS ---

# HOST = "192.168.1.108"
HOST = "127.0.0.1"
PORT = 12345

# Listener                    IP Type(IPV4)   TCP Protocol - TCP (Transmission Control Protocol)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT)) # Connection between socket to IP:PORT 
server_socket.listen(5)
print(f"Server is running, Test : {server_socket}")
clients = {} #Dic - holds in this format {"Name" : Socket }



# --- Functions ---
# Function to handle a single client
def handle_client(client_socket, client_adress):
    print(f"Client {client_adress} connected.")
    try:
        while True:
            client_socket.sendall("Enter your name: ".encode('utf-8')) # Assuming there is one name per person
            client_name = client_socket.recv(1024).decode('utf-8').strip()
            
            if not client_name: # Invalid name - empty
                client_socket.sendall("Invalid name.".encode('utf-8'))
                client_socket.close()
                continue # Ask again - reloop
            
            if client_name not in clients:
                clients[client_name] = client_socket # Add client to list
                print(f"Client {client_name} - connected from {client_adress}")
                client_socket.sendall("You are now connected!\nsend message in this format: '@Target_name (message).".encode('utf-8'))
                break
            else:
                client_socket.sendall("Name already taken, pick another.\n")
        
        while True:
            # Message from client, 1024 = size(bytes) ,utf-8 = Encoding 
            message = client_socket.recv(1024).decode('utf-8')
            if not message : # Empty? = Disconnect
                break
            print(f"Received from {client_adress}: {message}") # Print message
            
            if message.startswith('@'):
                target_name, msg = message[1:].split(' ',1) # Seperates the message - finds blank space with split
                if target_name == client_name:
                    client_socket.sendall(f"Why would you send a message to yourself? haha".encode('utf-8'))
                elif target_name in clients:
                    target_socket = clients[target_name]
                    target_socket.sendall(f"{client_name}: {msg}".encode('utf-8'))
                else:
                    client_socket.sendall(f"Client {target_name} not found.".encode('utf-8'))
            else: client_socket.sendall("Invalid format.\nSend message in this format: '@Target_name (message).".encode('utf-8'))
            
            # Respond to client
            response = f"Message received: {message}"
            client_socket.sendall(response.encode('utf-8'))
            
    except Exception as e:
        print(f"Error with client {client_adress}: {e}")
    finally:
        if client_name in clients:
            del clients[client_name]
        print(f"Closing connection with {client_adress}.")
        client_socket.close()
        
def run():
    try:
        while True:
            # Gain connection from new client
            client_socket, client_adress = server_socket.accept() # Returns conn and IP
            print(f"New connection from {client_adress}")
            
            # Handle client VIA Thread (Multiclient)
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_adress))
            client_thread.start()
    except KeyboardInterrupt: # Ctrl+c to shutdown
        print("\nServer is shutting down.")
    finally:
        server_socket.close()



run()