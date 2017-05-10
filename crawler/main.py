import Article
import asyncio
import socket

from example_code.clockdeco_param import clock

@clock('{name}({args}) dt={elapsed:0.3f}s')
def main(tendency,keyword):
    ar2 = Article.Article(tendency, keyword)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ar2.gathering(loop))

def getTendency_Keyword():
    # create a socket object
    print("waiting client connection...")
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

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
    print("soicem")
    #msg = str(msg.decode('unicode'), 'utf-8')
    result = msg.decode('ascii').split(',')
    # result = msg.split(',')
    print("Got a connection from %s" % str(addr))

    clientsocket.close()
    return (result[0],result[1])

if __name__=="__main__":
    result = getTendency_Keyword()
    keyword, tendency = result
    print(result)
    # tendency = input("tendency : ")
    # keyword = input("keyword : ")
    # main(tendency,keyword)


