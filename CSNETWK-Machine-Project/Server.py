import socket
import threading

# Initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverIP = "127.0.0.1"
serverPort = 12345
server_socket.bind((serverIP, serverPort))
server_socket.listen()

client_list = []
client_list_address = []

def handle_client(client_socket, addr):
    while True:
        name = ''
        data = client_socket.recv(1024)
        message = data.decode()

        if message.startswith("/join"):
            # client_list_address[addr] = {"socket": client_socket}
            client_list_address.append({"address": addr})
            print(f"Client from {addr} joined.")
        elif message.startswith("/leave"):
            port_index = client_list_address.index({"address": addr})
            print(port_index)

            handle_index = client_list.index({"handle": name})
            print(handle_index)

            print(f"Client {client_list[port_index]} has left.")
            del client_list[port_index]
            del client_list_address[handle_index]
            break

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
    client_socket.close()
    
while True:
    client_socket, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
