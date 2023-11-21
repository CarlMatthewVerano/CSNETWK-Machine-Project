import socket
import os

def main():
    sServerAddress = input("Enter server address: ")
    nPort = int(input("Enter port number: "))

    try:
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

    except Exception as e:
        print(e)
    finally:
        print("Client: Connection is terminated.")

if __name__ == "__main__":
    main()