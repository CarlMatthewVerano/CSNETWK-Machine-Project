import socket
import threading
import os
from datetime import datetime

global name

# Initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverIP = "127.0.0.1"
serverPort = 12345
server_socket.bind((serverIP, serverPort))
server_socket.listen()

client_list = []
client_list_address = []

print("Welcome to the serber")
server_directory = f"./Server/SerDir"
os.makedirs(server_directory, exist_ok=True)
print(f"Directory for Server created.")

def send_file(client_socket, filename):
    file_path = os.path.join(server_directory, filename)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            data = file.read(819200)
            # while data:
            client_socket.sendall(data)
                # data = file.read(1024)
            # client_socket.sendall(f"\nFILE SENT!\n".encode('utf-8'))
    else:
        client_socket.send("File not found.".encode('utf-8'))

def receive_file_from_client(client_socket, filename):
    file_path = os.path.join(server_directory, filename)
    print(f"Receiving file to: {file_path}")

    try:
        with open(file_path, 'wb') as file:
            print('File incoming...')
            
            file_size_bytes = client_socket.recv(4)
            file_size = int.from_bytes(file_size_bytes, byteorder='big')
            print(f"Expecting {file_size} bytes of data")

            received_bytes = 0
            while received_bytes < file_size:
                data = client_socket.recv(8192)
                if not data:
                    break
                file.write(data)
                received_bytes += len(data)
                print(f"Received {received_bytes} bytes of data")

        print(f"File received and stored: {filename}")
    except Exception as e:
        print(f"Error receiving file: {e}")

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def handle_client(client_socket, addr):
    while True:
        name = ''
        data = client_socket.recv(1024)
        print(f"Received data: {data}")
        message = data.decode()
        print(f"Decoded message: {message}")

        if message.startswith("/join"):
            # client_list_address[addr] = {"socket": client_socket}
            client_list_address.append({"address": addr})
            print(f"Client from {addr} joined.")
        
        elif message.startswith("/leave"):

            print("NAME:", name)
            print("ADDR:", addr)
            print("CLIENT_LIST_ADDR:", client_list_address)
            port_index = client_list_address.index({"address": addr})
            print("PORT INDEX:", port_index)
            print(client_list)

            indeces = next((i for i, item in enumerate(client_list_address) if item["address"] == addr), None)
            
            # handle_index = client_list.index({"handle": name})
            # print("HANDLE INDEX", handle_index)
            try:
                print(f"Client {client_list[indeces]} has left.")
                client_directory = f"./Client/{client_list[indeces]['handle']}"
                os.rmdir(client_directory)
                del client_list[indeces]
            except:
                print("Client has left")
            
            finally:
                del client_list_address[indeces]

        elif message.startswith("/register"):
            name = message.split()[1]
            if not any(d['handle'] == name for d in client_list):
                print("Not here")
                client_socket.sendall(f"\nWelcome {name}!\n".encode('utf-8'))
                client_list.append({"handle": name})

            else:
                print("Here")
                client_socket.sendall(f"\nError: Registration failed. Handle or alias already exists.\n".encode('utf-8'))
            # if (name != client[1] for client in client_list):
            #     print("testing")
            #     print(name)
            #     print(client_list)
            #     print(type(client_list))
            #     client_list.append({"handle": name})
            #     # print(client_list)
            #     client_socket.send(f"\nWelcome {name}!\n".encode('utf-8'))
            #     print(type(client_list[0]))
            #     print(client_list[0]['handle'])
            #     print(client_list)
            # else:
            #     print("dasdasda")
            #     client_socket.send(f"\nError: Registration failed. Handle or alias already exists.\n".encode('utf-8'))
        
        elif message.startswith("/store"):
                _, filename = message.split()
                print(f"Received file data: {data}")
                receive_file_from_client(client_socket, filename)
                print(f"{name}<{get_current_time()}>: Stored {filename}")
        
        elif message.startswith("/get"):
            filename = message.split()[1]
            send_file(client_socket, filename)
            
    client_socket.close()
    
while True:
    client_socket, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
