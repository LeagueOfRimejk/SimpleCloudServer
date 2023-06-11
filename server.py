import socket

from app import Application


class Server:
    HOST = "192.168.1.7"
    PORT = 5000
    SERVER_ADDR = HOST, PORT
    DEFAULT_ENCODING = "UTF-8"

    def __init__(self, application):
        self.application = application()

    def create(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.SERVER_ADDR)
        return server_socket
    
    def send_file(self, client_socket, file, buffer_size=1024):
        # Send the file data in fixed sized chunks
        chunk_size = buffer_size

        # Ensure that there is any bytes chunks left by adding 1
        num_chunks = (len(file) // chunk_size) + 1

        # i in for loop represents the pointer for subsequent chunk
        for i in range(num_chunks):
            start = i * chunk_size
            end = (i + 1) * chunk_size
            chunk = file[start:end]
            client_socket.sendall(chunk)

    def start(self):
        # Create server socket
        server_socket = self.create()

        # Listen for incomming connections
        server_socket.listen(1)
        print(f"\tServer stars listening on {self.HOST}:{self.PORT}\r\n")

        running = True
        while running:
            client_socket, client_addr = server_socket.accept()

            print("\r\n" + 100 * "=" + "\r\n")
            print(f"\t -- New Connection from {client_addr[0]}:{client_addr[1]}\r\n")
            request = client_socket.recv(1024).decode(self.DEFAULT_ENCODING)

            print(request)
            print("\r\n" + 100 * "=" + "\r\n")

            # Unpack the result and check if it contains file
            response, file = self.application.handle_request(request)
            if file:
                client_socket.send(response.encode(self.DEFAULT_ENCODING))
                self.send_file(client_socket, file, buffer_size=1024)
            else:
                # Send response without file
                client_socket.send(response.encode(self.DEFAULT_ENCODING))

            # Close connection
            client_socket.close()


server = Server(Application)
if __name__ == "__main__":
    server.start()
