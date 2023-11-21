import socket
import os

def main():
    nPort = int(input("Enter port number: "))
    print("Server: Listening on port", nPort, "...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
            serverSocket.bind(('localhost', nPort))
            serverSocket.listen(1)
            print("Server: Waiting for a client to connect...")

            serverEndpoint, clientAddress = serverSocket.accept()
            print("Server: New client connected:", clientAddress)

            # Receiving a message from the client
            client_message = serverEndpoint.recv(4096).decode('utf-8')
            print(client_message)

            # Sending file details and content
            file_size = os.path.getsize("Download.txt")
            serverEndpoint.sendall((str(file_size) + '\n').encode('utf-8'))
            serverEndpoint.sendall("Server: Hello World!\n".encode('utf-8'))

            with open("Download.txt", 'rb') as fileInputStream:
                buffer = fileInputStream.read(4096)
                while buffer:
                    serverEndpoint.sendall(buffer)
                    buffer = fileInputStream.read(4096)
            
            print("Server: File sent!")

    except Exception as e:
        print(e)
    finally:
        print("Server: Connection is terminated.")

if __name__ == "__main__":
    main()
