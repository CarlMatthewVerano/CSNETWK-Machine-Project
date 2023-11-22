import socket
import threading

# Initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverIP = "127.0.0.1"
serverPort = 12345
server_socket.bind((serverIP, serverPort))

client_list = {}
client_list_address = []

def handle_client():
    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()

        if message.startswith("/join"):
            client_port = message.split()[1]
            client_list[addr] = {"port": client_port, "handle": "Anonymous"}
            print(f"Client from {addr} joined on port {client_port}.")

        elif message.startswith("/leave"):
            if addr in client_list:
                client_details = client_list[addr]
                print(f"Client {client_details['handle']} ({addr}) has left.")
                del client_list[addr]

        elif message.startswith("/register"):
            if len(message.split()) == 2:
                name = message.split()[1]
                if not any(client['handle'] == name for client in client_list.values()):
                    client_list[addr]["handle"] = name
                    server_socket.sendto(f"\nWelcome {name}!\n".encode('utf-8'), addr)
                else:
                    server_socket.sendto(f"\nError: Registration failed. Handle or alias already exists.\n".encode('utf-8'), addr)
            else:
                server_socket.sendto(f"\nError: Command parameters do not match or is not allowed.\n".encode('utf-8'), addr)

# Start client handling thread
client_thread = threading.Thread(target=handle_client)
client_thread.start()
