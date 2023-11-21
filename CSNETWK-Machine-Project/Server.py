import socket
import threading

# Initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverIP = "127.0.0.1"
serverPort = 12345
server_socket.bind((serverIP, serverPort))

client_list = {}  # Dictionary for client details

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
            handle = message.split()[1]
            if any(client['handle'] == handle for client in client_list.values()):
                server_socket.sendto("Name already taken. Please choose another.".encode(), addr)
            else:
                client_list[addr]['handle'] = handle
                print(f"Client {addr} registered as {handle}.")
                server_socket.sendto("Name registered successfully.".encode(), addr)

# Start client handling thread
client_thread = threading.Thread(target=handle_client)
client_thread.start()
