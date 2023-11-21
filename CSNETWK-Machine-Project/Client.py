import socket
import os

def userInput(userCommand):
    print(userCommand)
    specCommand = userCommand.split()

    if specCommand[0] == "/join":
        print("User in")
        try:
            fileTransferConnection(specCommand[1], int(specCommand[2]))
        except:
            print("Error: Connection to the Server has failed! Please check IP Address and Port Number.")
        finally:
            print("Client: Connection is terminated.")

    elif specCommand[0] == "/leave":
        print("Error: Disconnection failed. Please connect to the server first.")

    elif specCommand[0] == "/register":
        print("Error: Registration failed. Please connect to the server first.")

    elif specCommand[0] == "/store":
        print("Error: Store failed. Please connect to the server first.")

    elif specCommand[0] == "/dir":
        print("Error: Request failed. Please connect to the server first.")

    elif specCommand[0] == "/get":
        print("Error: Fetch failed. Please connect to the server first.")

    elif specCommand[0] == "/?":
        print("[1] /join <server_ip_add> <port>\t - Connect to the server application\n")
        print("[2] /leave\t\t\t\t - Disconnect from the server application\n")
        print("[3] /register <handle>\t\t\t - Register a unique handle or alias\n")
        print("[4] /store <filename>\t\t\t - Send file to server\n")
        print("[5] /dir <server_ip_add> <port>\t\t - Request directory file list from a server\n")
        print("[6] /get <filename> <port>\t\t - Fetch a file from a server\n")
        print("[7] /?\t\t\t\t\t - Request command help to output all Input Syntax commands for references\n")

    else:
        print("Error: Command not found.")

def fileTransferConnection(sServerAddress, nPort):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientEndpoint:
            clientEndpoint.connect((sServerAddress, nPort))
            print("Client: Connected to server at", clientEndpoint.getpeername())

            with clientEndpoint.makefile('wb') as dosWriter:
                dosWriter.write(("Client: Hello from client" + str(clientEndpoint.getsockname())).encode('utf-8'))

            with clientEndpoint.makefile('rb') as disReader:
                file_size = int(disReader.readline().decode('utf-8'))

                server_hello_message = disReader.readline().decode('utf-8')
                print(server_hello_message.strip())
                with open("Received.txt", 'wb') as fileOutputStream:
                    received_size = 0
                    while received_size < file_size:
                        buffer_size = min(4096, file_size - received_size)
                        buffer = clientEndpoint.recv(buffer_size)
                        if not buffer:
                            break
                        fileOutputStream.write(buffer)
                        received_size += len(buffer)

            print("Client: Downloaded file Received.txt")

def main():
    userCommand = input("Enter command: ")
    userInput(userCommand)

if __name__ == "__main__":
    main()