import socket
import threading

# --- CONSTS ---
HOST = "127.0.0.1"  # כתובת השרת
PORT = 12345        # פורט השרת

# --- Functions ---

# Function to recieve message from server
def receive_messages(client_socket):
    try:
        while True:
            # Recieve message form server
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n{message}")
    except Exception as e:
        print(f"Error receiving messages: {e}")
    finally:
        print("Disconnected from server.")
        client_socket.close()


# --- Main ---
def run():
    # Make socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to server
        client_socket.connect((HOST, PORT))
        print("Connected to the server.")

        # Listen to message from server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()

        # Send message to server
        while True:
            message = input("")
            if message.lower() == "exit":
                print("Disconnecting...")
                break
            client_socket.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        
run()
