import io
from socket import *
import sys
CACHED_FILE_PREFIX="c_"

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
serverAddr = sys.argv[1]  # Listen to any address
serverPort = 8887
tcpSerSock.bind((serverAddr, serverPort))
tcpSerSock.listen(1)
# Fill in end.
i = 0
while i < 30:
    i += 1
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    # Fill in start.
    message = tcpCliSock.recv(4096).decode()
    # Fill in end.
    print(f"request:\n {message}")

    # Extract the filename from the given message
    requestUrl = (message.split()[1]).partition("/")[2]
    print(f"request URL: {requestUrl}")
    cachedFilename = CACHED_FILE_PREFIX + requestUrl
    fileExist = "false"

    try:
        # Check whether the file exist in the cache
        f = open(cachedFilename, "r")
        outputData = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")
        # Fill in start.
        tcpCliSock.send(outputData)
        # Fill in end.
        print('Read from cache')
        # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxy server
            # Fill in start.
            c = socket(AF_INET, SOCK_STREAM)
            # Fill in end.
            resqFilename = "/".join(requestUrl.split("/")[1:])
            print(f"Request File: {resqFilename}")
            hostn = (requestUrl.split("/")[0]).replace("www.", "", 1)
            print(f"hostname: {hostn}")
            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((hostn, 443))
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileObj = c.makefile('wr', 1)
                fileObj.write("GET " + resqFilename + " HTTP / 1.1\n\n")
                # Read the response into buffer
                # Fill in start.
                resp = fileObj.readlines()
                print(f"Response: \n{resp}")
                #
                # # Fill in end.
                # # Create a new file in the cache for the requested file.
                # # Also send the response in the buffer to client socket and the corresponding file in the cache
                # tmpFile = open("./" + filename, "wb")
                #
                # # Fill in start.
                # tcpCliSock.sendall(tmpFile.readlines())
                #
                # # Fill in end
            except Exception as e:
                print(e)
                print("Illegal request")
        else:
            # HTTP response message for file not found
            # Fill in start.
            tcpCliSock.send("HTTP/1.0 404 NOT FOUND\r\n")
            # Fill in end.
    # Close the client and the server sockets
    tcpCliSock.close()
# Fill in start.
tcpSerSock.close()
# Fill in end.
