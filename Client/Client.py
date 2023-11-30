import socket
import os
import threading
import random
from time import sleep
from datetime import datetime

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientIP = '127.0.0.1'
clientPort = 12345

bufferSize = 1024
name = ""


def receive():
    global server_connected
    while server_connected:
        try:
            message = client_socket.recv(1024)
            if not message:  # Server has closed the connection
                print("Server has been disconnected.")
                server_connected = False  # Set the flag to indicate server disconnection
                break
            print(message.decode())
            return message.decode()
        except Exception as e:
            print("An error occurred:", e)
            server_connected = False
            break

def receive_file(client_socket, filename, name):
    data = client_socket.recv(819200)
    # Check if the first part of the data is the 'File not found.' message
    if data[:15].decode(errors='ignore') == "File not found.":
        print("File not found")
    else:
        file_path = os.path.join(f"./{name}", filename)
        with open(file_path, 'wb') as file:
            file.write(data)


def send_file_to_server(client_socket, filename, name):
    file_path = os.path.join(f"./{name}", filename)

    if os.path.exists(file_path):
        try:
            client_socket.sendall(f"/store {filename}".encode('utf-8'))

            with open(file_path, 'rb') as file:
                print(f'File uploading: {file_path}')
                file_content = file.read()
                client_socket.sendall(len(file_content).to_bytes(4, byteorder='big'))  

                while file_content:
                    client_socket.sendall(file_content)
                    file_content = file.read(8192)

                print(f"{name}<{get_current_time()}>: Uploaded {filename}")
        except Exception as e:
            print(f"Error sending file data: {e}")
    else:
        print("Error: File not found.")

def receive_dir():
    try:
        directory_data = client_socket.recv(1024)
        directory_listing = directory_data.decode()
        print("Directory listing from server:")
        print(directory_listing)
    except Exception as e:
        print("Error receiving directory listing:", e)

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def work():
    global name, server_connected
    server_connected = True
    user_registered = False
    user_joined = False
    while server_connected:
        user_input = input()
        if not server_connected:
            print("Server is not connected. Exiting.")
            break
        commandLen = user_input.split()

        if (user_input == "/?"):
            print("[1] /join <server_ip_add> <port>\t - Connect to the server application\n")
            print("[2] /leave\t\t\t\t - Disconnect from the server application\n")
            print("[3] /register <handle>\t\t\t - Register a unique handle or alias\n")
            print("[4] /store <filename>\t\t\t - Send file to server\n")
            print("[5] /dir <server_ip_add> <port>\t\t - Request directory file list from a server\n")
            print("[6] /get <filename> <port>\t\t - Fetch a file from a server\n")
            print("[7] /?\t\t\t\t\t - Request command help to output all Input Syntax commands for references\n")

        elif (user_input == "/leave"):
            if (user_joined == False):
                print("\nError: Disconnection failed. Please connect to the server first.")
            else:
                user_joined == False
                client_socket.send(f"/leave".encode('utf-8'))
                print("\nConnection closed. Thank you!")
                client_socket.close()
                break

        elif (user_input.startswith("/join")):

            if len(commandLen) <= 1:
                print("Error: Command parameters do not match or is not allowed.")

            elif (user_joined == False):

                client_details = user_input.split()

                if len(client_details) == 3:
                    serverIP, serverPort = client_details[1], client_details[2]

                    if serverIP != "127.0.0.1" or serverPort != "12345":
                        print(
                            "Error: Connection to the Server has failed! Please check IP Address and Port Number.")
                    else:
                        client_socket.connect((serverIP, int(serverPort)))
                        print("\nConnection to the Server is successful!")
                        client_socket.send(f"/join {serverPort}".encode('utf-8'))
                        user_joined = True

                        receive_thread = threading.Thread(target=receive)
                        receive_thread.start()
                else:
                    print("Error: Command parameters do not match or is not allowed.")
            else:
                print("Error: Failed to connect to Server. You are already connected.")
            
        elif (user_input.startswith("/register")):

            if len(commandLen) <= 1:
                print("Error: Command parameters do not match or is not allowed.")
            elif (user_joined == False):
                print("Error: Failed to register handle. Please connect to the server first.")
            else:
                if (user_registered == True):
                    print("Error: You are already registered!")
                else:
                    if len(user_input.split()) == 2:
                        name = user_input.split()[1]
                        client_socket.send(f"/register {name}".encode('utf-8'))
                        user_registered = True
                        # os.mkdir("../Client/{name}")
                        client_directory = f"./{name}"
                        os.makedirs(client_directory, exist_ok=True)
                        print(f"Directory for {name} created.")
                    else:
                        print("Error: Failed to register handle.")
        elif user_input.startswith("/get"):
            if user_joined:
                if user_registered:
                    filename = user_input.split()[1]
                    client_socket.send(f"/get {filename}".encode('utf-8'))
                    receive_file(client_socket, filename, name)
                else:
                    print("Register first before you're able to get files from the server.")
            else:
                print("Error: Please connect to the server first.")
        
        elif user_input.startswith("/store"):
            if user_joined:
                if user_registered:
                    filename = user_input.split()[1]
                    send_file_to_server(client_socket, filename, name)
                else:
                    print("Register first before you're able to store files to the server.")
            else:
                print("Error: Please connect to the server first.")

        elif (user_input == "/dir"):
            if server_connected:
                if user_registered:
                    client_socket.send("/dir".encode('utf-8'))
                    receive_dir()
                else:
                    print("Register first before you're able to see the files in the server.")
            else:
                print("Error: Server is not connected.")

        elif(user_input.startswith("/?")):
            print("----- USER COMMANDS -----")
            print("LEAVE CHATROOM: /leave")
            print("REGISTER HANDLE: /register <handle>")

        else:
            print("Command not found.")

        sleep(0.5)

work()