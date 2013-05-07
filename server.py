import socket, threading, os, sys
import SocketServer as socketserver

class ConnectionHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            action = self.request.recv(1024)
            if action == 'listdir':
                self.listfiles()
            elif action == 'sendfile':
                self.sendfile()

    def listfiles(self, dirpath='files'):
        files_list = [elem for elem in os.listdir(dirpath) \
                if not os.path.isdir(elem)]
        self.request.sendall('|'.join(files_list))
        self.request.recv(1024)

    def sendfile(self):
        self.request.sendall('ready')
        file_name = self.request.recv(1024)
        filepath = os.path.join('files', file_name)
        size = os.path.getsize(filepath)
        self.request.sendall(str(size))
        self.request.recv(1024)
        with open(filepath, 'rb') as bin_file:
            while True:
                bin_string = bin_file.read(1024)
                self.request.send(bin_string)
                if not bin_file: break


class Client:

    def __init__(self, host, port):
        self.host, self.port = host, port
        self.request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request.connect((host, port))
        self.files_list = []

    def recievefile(self, filename):
        self.request.sendall('sendfile')
        self.request.recv(1024)
        self.request.sendall(filename)
        size = self.request.recv(1024)
        print size
        size = int(size)
        self.request.sendall('size recieved')
        with open(os.path.join('files', filename), 'wb+') as bin_file:
            recv = 0
            while recv < size:
                bin_string = self.request.recv(1024)
                bin_file.write(bin_string)
                recv += len(bin_string)
        print(filename)

    def get_listfiles(self):
        if not self.files_list:
            self.request.sendall('listdir')
            self.files_list = self.request.recv(4096).split('|')
            self.request.sendall('ok')
        return self.files_list

    def getinfo(self):
        return "%s:%d" % (self.host, self.port)

PORT = 9001 + int(sys.argv[1])
if __name__ == '__main__':

    #choice = raw_input("server [s], client[c]")
    server = socketserver.ThreadingTCPServer(('', PORT), ConnectionHandler)
    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    clients = []
    while True:
        choice = raw_input("Wylistuj [ls], pobierz plik [pp], dodaj clienta [dc]: ")
        if choice == 'dc':
            ip = raw_input('podaj ip: ')
            port = int(raw_input('podaj port: '))
            clients.append(Client(ip, port))
        elif choice == 'ls':
            for nr, elem in enumerate(clients):
                print(nr, elem.getinfo())
            nr = int(raw_input("podaj nr klienta do listowania: "))
            l = clients[nr].get_listfiles()
            print(l)
        elif choice == 'pp':
            for nr, elem in enumerate(clients):
                print(nr, elem.getinfo())
            nr = int(raw_input("podaj nr klienta, by pobrac od niego plik: "))
            print(clients[nr].get_listfiles())
            file_name = raw_input("Podaj dokladna nazwe pliku: ")
            clients[nr].recievefile(file_name)
