import socket
import threading
import random
from time import sleep

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Client IP and random port
clientIP = '127.0.0.1'
clientPort = random.randint(8000, 10000)

# Function to receive messages from the server
def receive():
    while True:
        try:
            message, address = client_socket.recvfrom(1024)
            print(message.decode())
        except:
            pass

# Start a thread for receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

user_joined = False

while True:
    user_input = input()

    if user_input == "/leave":
        if not user_joined:
            print("\nError: Disconnection failed. Please connect to the server first.")
        else:
            client_socket.sendto(f"/leave".encode('utf-8'), (serverIP, int(serverPort)))
            print("\nConnection closed. Thank you!")
            client_socket.close()
            break

    elif user_input.startswith("/join"):
        if not user_joined:
            client_details = user_input.split()
            if len(client_details) == 3:
                serverIP = client_details[1]
                serverPort = client_details[2]
                client_socket.bind((clientIP, clientPort))
                client_socket.sendto(f"/join".encode('utf-8'), (serverIP, int(serverPort)))
                print("\nConnected to the server.")
                user_joined = True
            else:
                print("Error: Invalid command format.")
        else:
            print("Error: Already connected to a server.")

    elif user_input.startswith("/register"):
        if not user_joined:
            print("Error: Please connect to the server first.")
        else:
            name = user_input.split()[1]
            client_socket.sendto(f"/register {name}".encode('utf-8'), (serverIP, int(serverPort)))

    elif user_input.startswith("/?"):
        print("----- USER COMMANDS -----")
        print("LEAVE CHATROOM: /leave")
        print("REGISTER HANDLE: /register <handle>")

    else:
        print("Command not found.")

    sleep(0.75)
