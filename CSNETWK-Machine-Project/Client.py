import socket
import os
import threading
import random
from time import sleep

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clientIP = '127.0.0.1'
clientPort = random.randint(8000, 10000)

bufferSize = 1024

def receive():

    while True:
        try:
            message, address = client_socket.recvfrom(1024)
            print(message.decode())
        except:
            pass

receive_thread = threading.Thread(target=receive)
receive_thread.start()

user_registered = False
user_joined = False

while True:
    user_input = input()

    if (user_input == "/leave"):
        if (user_joined == False):
            print("\nError: Disconnection failed. Please connect to the server first.")
        else:
            client_socket.sendto(f"/leave".encode('utf-8'), (serverIP, int(serverPort)))
            print("\nConnection closed. Thank you!")
            client_socket.close()
            break

    elif (user_input.startswith("/join")):

        if (user_joined == False):

            client_details = user_input.split()

            if len(client_details) == 3:
                serverIP, serverPort = client_details[1], client_details[2]

                if serverIP != "127.0.0.1" or serverPort != "12345":
                    print(
                        "Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                else:
                    client_socket.bind((clientIP, clientPort))
                    bufferSize = 1024
                    print("\nConnection to the Message Board Server is successful!")
                    client_socket.sendto(f"/join {clientPort}".encode('utf-8'), (serverIP, int(serverPort)))
                    user_joined = True
            else:
                print("Error: Command parameters do not match or is not allowed.")
        else:
            print("Error: Failed to connect to Message Board Server. You are already connected.")
        
    elif (user_input.startswith("/register")):
        if (user_joined == False):
            print("Error: Failed to register handle. Please connect to the server first.")
        else:
            if (user_registered == True):
                print("Error: You are already registered!")
            else:
                if (user_joined == True):
                    if len(user_input.split()) == 2:
                        name = user_input.split()[1]
                        client_socket.sendto(f"/register {name}".encode('utf-8'), (serverIP, int(serverPort)))
                        response, _ = client_socket.recvfrom(1024)
                        response = response.decode()
                        if response == "Name already taken. Please choose another.":
                            print(response)
                            break
                        elif response == "Name registered successfully.":
                            user_registered = True
                            print(response)
                    else:
                        print("Error: Failed to register handle. Don't add spaces to your handle.")

    elif(user_input.startswith("/?")):
        print("----- USER COMMANDS -----")
        print("LEAVE CHATROOM: /leave")
        print("REGISTER HANDLE: /register <handle>")

    else:
        print("Command not found.")

    sleep(0.75)