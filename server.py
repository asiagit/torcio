import socket, socketserver, threading, os, sys

class Server(socketserver.ThreadingTCPServer):
    connections = []

class ConnectionHandler(socketserver.BaseRequestHandler):

    def handle(self):
        Server.connections.append(self)
        action = self.request.recv(1024)
        if action == 'listdir':
            self.listfiles()

    def listfiles(self, dirpath='files'):
        files_list = [elem for elem in os.listdir(dirpath) \
                if not elem.path.isdir()]
        self.request.sendall(len(files_list))
        self.request.recv(1024)
        for elem in file_list:
            self.request.sendall(elem)

    def sendfile(self, filepath):
        self.request.sendall('sendfile')
        self.request.recv(1024)
        self.request.sendall(os.path.split(filepath)[1])
        self.request.recv(1024)
        size = os.path.getsize(filepath)
        self.request.sendall(size)
        self.request.recv(1024)
        with open(filepath, 'rb') as bin_file:
            while True:
                bin_string = bin_file.read(1024)
                self.request.send(bin_string)
                if not bin_file: break


class Client:
    
    def __init__(self, host, port):
        self.request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request.connect((host, port))

    def recievefile(self, dirpath='files'):
        filename = self.request.recv(1024)
        self.request.sendall('filename recieved')
        size = self.request.recv(1024)
        size = int(size)
        self.request.sendall('size recieved')
        with open(os.path.join(dirname, filename), 'wb+') as bin_file:
            recv = 0
            while recv < size:
                bin_string = self.request.recv(1024)
                bin_file.write(bin_string)
                recv += len(bin_string)
        print(filename)
    
    def get_listfiles(self):
        list_len = int(self.request.recv(1024))
        files_list = []
        for elem in list_len:
            files_list.append(self.request.recv(1024))
        return files_list


PORT = 9001 + int(sys.argv[1])
if __name__ == '__main__':

    choice = input("server [s], client[c]")

    if choice == 'c':
        client = Client('localhost', PORT)
        l = client.get_listfiles()
        print(l)
    elif choice == 's':
        server = Server(('localhost', PORT), ConnectionHandler)
        server_thread = threading.Thread(target = server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
