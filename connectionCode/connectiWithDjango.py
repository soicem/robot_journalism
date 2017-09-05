import socket

def getTendency_Keyword():
    # create a socket object
    print("waiting client connection...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        # get local machine name
        host = socket.gethostname()
        port = 8084

        # bind to the port
        try :
            serversocket.bind((host, port))
        except(OSError):
            print("again")
        finally:
            serversocket.listen(5)

        # queue up to 5 requests
        # serversocket.listen(5)

        # establish a connection
        clientsocket, addr = serversocket.accept()
        msg = clientsocket.recv(1024)
        result = msg.decode('utf8').split(',')
        print("Got a connection from %s" % str(addr))

        clientsocket.close()
        return (result[0],result[1])

class socket_Django:
    def __init__(self):
        print("waiting client connection...")
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # get local machine name
        host = socket.gethostname()
        port = 8084

        # bind to the port
        self.serversocket.bind((host, port))

        # queue up to 5 requests
        self.serversocket.listen(5)

        # establish a connection
        self.clientsocket, self.addr = self.serversocket.accept()

    def getTendency_Keyword(self):
        # create a socket object

        msg = self.clientsocket.recv(1024)
        result = msg.decode('utf8').split(',')
        print("Got a connection from %s" % str(self.addr))

        return (result[0], result[1])

    def send_Newdata(self, titles, summarized_articles, imgUrls):

        send_data=''
        send_titles =""
        send_articles="*"
        send_imgUrls="*"
        for i in range(len(titles)):
            send_titles += "## "+ titles[i]
            send_articles += "## "+ summarized_articles[i]
            send_imgUrls += "## "+ imgUrls[i]
        send_titles += send_articles + send_imgUrls
        # print(send_titles)
        self.clientsocket.send(send_titles.encode('utf8'))

    def socketClose(self):
        self.clientsocket.close()
        self.serversocket.close()