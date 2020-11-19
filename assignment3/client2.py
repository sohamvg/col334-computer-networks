import socket

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    c = 0
    while True:
        part = sock.recv(BUFF_SIZE)
        c += 1
        print(c, len(part))
        if not part:
            break

        data += part
        # if len(part) < BUFF_SIZE:
        #     # either 0 or end of data
        #     break
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
# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.getaddrinfo(serverName, serverPort)
# clientSocket.connect((serverName,serverPort))

while True:
    try:
        clientSocket = socket.create_connection((serverName, serverPort), 20)
        break
    except:
        print("retrying\r", end="")

with open("get-01.txt", 'rb') as f:
    data = f.read()
    clientSocket.sendall(data)
# modifiedSentence = clientSocket.recv(6488666 * 1024)
modifiedSentence = recvall(clientSocket)
# modifiedSentence = clientSocket.recv(1024 * 6488666)
print(modifiedSentence)

# with open('client2_out.txt', 'wb') as file:
#     file.write(modifiedSentence)
clientSocket.close()
