import socket
import threading

# --- CONSTS ---

# HOST = "192.168.1.108"
HOST = "127.0.0.1"
PORT = 12345

# Listener                    IP Type(IPV4)   TCP Protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT)) # Connection between socket to IP:PORT 
server_socket.listen(5)
print(f"Test : {server_socket} , Server is running")



# --- Functions ---

# Function to handle a single client
def handle_client(client_socket, client_adress):
    print(f"Client {client_adress} connected.")
    try:
        while True:
            # Message from client, 1024 = size(bytes) ,utf-8 = Encoding 
            message = client_socket.recv(1024).decode('utf-8')
            if not message : # Empty? = Disconnect
                break
            print(f"Received from {client_adress}: {message}") # Print message
            
            # Respond to client
            response = f"Message received: {message}"
            client_socket.sendall(response.encode('utf-8'))
            
    except Exception as e:
        print(f"Error with client {client_adress}: {e}")
    finally:
        print(f"Closing connection with {client_adress}.")
        client_socket.close()
        
def run():
    try:
        while True:
            # Gain connection from new client
            client_socket, client_adress = server_socket.accept()
            print(f"New connection from {client_adress}")
            
            # Handle client VIA Thread (Multiclient)
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_adress))
            client_thread.start()
    except KeyboardInterrupt: # Ctrl+c to shutdown
        print("\nServer is shutting down.")
    finally:
        server_socket.close()



run()