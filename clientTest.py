import socket

HOST = "127.0.0.1"  # כתובת השרת (ודא שהיא תואמת לשרת שלך)
PORT = 12345        # פורט השרת

# יצירת Socket לקוח
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # התחברות לשרת
    client_socket.connect((HOST, PORT))
    print("Connected to the server.")

    while True:
        # שליחת הודעה לשרת
        message = input("Enter a message to send (or type 'exit' to disconnect): ")
        if message.lower() == 'exit':
            print("Disconnecting from the server.")
            break

        client_socket.sendall(message.encode('utf-8'))

        # קבלת תשובה מהשרת
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")
finally:
    client_socket.close()
    print("Client socket closed.")
