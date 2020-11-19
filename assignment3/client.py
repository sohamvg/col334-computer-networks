import socket

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    c = 0
    while True:
        part = sock.recv(BUFF_SIZE)
        c += 1
        print(c, len(part))
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

def recvall2(sock):
    fragments = []

    c = 0
    while True:
        c += 1
        if c % 5000 == 0:
            print(c) 
        chunk = sock.recv(4096)
        if not chunk: 
            break
        fragments.append(chunk)
    arr = b''.join(fragments)
    return arr

serverName = 'vayu.iitd.ac.in'
serverPort = 80
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.getaddrinfo(serverName, serverPort)
clientSocket.connect((serverName,serverPort))
clientSocket.sendall("GET /big.txt HTTP/1.1\r\nHost: vayu.iitd.ac.in\r\n\r\n".encode())
# modifiedSentence = clientSocket.recv(6488666 * 1024)
modifiedSentence = recvall2(clientSocket)
with open('text2.txt', 'wb') as file:
    file.write(modifiedSentence)
clientSocket.close()
