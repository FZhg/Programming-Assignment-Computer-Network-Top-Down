# import socket module
import os
import time
from socket import *


def getContentSize(contentLineList):
    length = 0
    crcnLen = len("\r\n".encode())
    for i in range(0, len(contentLineList)):
        length += len(contentLineList[i].encode())
        length += crcnLen
    return length


def sendLineSocket(lineList, cnSocket):
    for i in range(0, len(lineList)):
        print(lineList[i])
        cnSocket.send(lineList[i].encode())
        cnSocket.send("\r\n".encode())


serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
# Fill in start
serverAddr = ""  # listen to all addresses
serverPort = 6788
serverSocket.bind((serverAddr, serverPort))
serverSocket.listen(1)
# Fill in end
while True:
    # Establish the connection
    print('Ready to serve...')
    # Fill in start
    connectionSocket, addr = serverSocket.accept()
    # Fill in end
    try:
        # Fill in start
        message = connectionSocket.recv(4096)

        # Fill in end
        filename = message.split()[1][1:]
        # /HelloWorld.html -> HelloWorld.html

        f = open(filename)

        # Fill in start
        # get the files as the lines
        outputData = f.readlines()

        # Fill in end

        # Fill in start
        # Example
        # HTTP/1.1 200 OK
        # Connection: close
        # Date: Tue, 18 Aug 2015 15:44:04 GMT
        # Server: Apache/2.2.3 (CentOS)
        # Last-Modified: Tue, 18 Aug 2015 15:11:03 GMT
        # Content-Length: 6821
        # Content-Type: text/html

        headerLines = [
            "HTTP/1.1 200 OK",
            "Connection: close",
            "Date: " + time.asctime(time.gmtime(time.time())),
            "Server: Python",
            "Last-Modified: " + time.asctime(time.gmtime(os.path.getmtime(filename))),
            # "Content-Length: " + str(getContentSize(outputData)),
            "Content-Type: " + "text/html"  # TODO: add other types
        ]

        sendLineSocket(headerLines, connectionSocket)
        # Fill in end
        # Send the content of the requested file to the client

        sendLineSocket(outputData, connectionSocket)

        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        # Fill in start
        headerLines = [
            "HTTP/1.1 404 Not Found",
            "Connection: close",
            "Date" + time.asctime(time.gmtime(time.time())),
            "Server: Python"
        ]

        sendLineSocket(headerLines, connectionSocket)
        # Fill in end
        # Close client socket
        # Fill in start
        connectionSocket.close()
        # Fill in end
    # serverSocket.close()
    # sys.exit()  # Terminate the program after sending the corresponding data
