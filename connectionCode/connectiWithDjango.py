import socket

def getTendency_Keyword():
    # create a socket object
    print("waiting client connection...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        # get local machine name
        host = socket.gethostname()

        port = 8090

        # bind to the port
        serversocket.bind((host, port))

        # queue up to 5 requests
        serversocket.listen(5)


        # establish a connection
        clientsocket, addr = serversocket.accept()
        msg = clientsocket.recv(1024)
        result = msg.decode('utf8').split(',')
        print("Got a connection from %s" % str(addr))

        clientsocket.close()
        return (result[0],result[1])