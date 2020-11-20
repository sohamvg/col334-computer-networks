import socket
import os

def recvall(sock):
    fragments = []
    # c = -1
    while True:
        # c += 1
        # if c % 5 == 0:
        #     print(c)
        try:
            chunk = sock.recv(4096)
            if not chunk: 
                break
            fragments.append(chunk)
        except Exception as e:
            print("caught exception in receiving", e)
            # print("caught timeout")
            arr = b''.join(fragments)
            return arr
    arr = b''.join(fragments)
    return arr

# serverName = 'vayu.iitd.ac.in'
serverName = 'norvig.com'
serverPort = 80
# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# clientSocket = socket.create_connection((serverName, serverPort), 5)

# clientSocket.settimeout(10)
# clientSocket.connect((serverName,serverPort))
# clientSocket.settimeout(None)

content_length = 6488666
CHUNK_SIZE = 10000

total_chunks = int(content_length / CHUNK_SIZE) + 1

chunks = [None] * total_chunks
# for c in range(20):
#     bytes_range = str(c * CHUNK_SIZE) + "-" + str((c+1) * CHUNK_SIZE - 1)
#     GET_request = "GET /big.txt HTTP/1.1\r\nHost: " + serverName + "\r\nConnection: keep-alive\r\nRange: bytes=" + bytes_range + "\r\n\r\n"
#     clientSocket.sendall(GET_request.encode())
#     print(bytes_range)

# received_data = recvall(clientSocket)

# # for line in received_data.decode():
# #     print(line)
# # print(received_data.decode().splitlines())

# # print(received_data)

chunks_received = 0
# total_chunks = 40
while chunks_received < total_chunks:
    while True:
        try:
            clientSocket = socket.create_connection((serverName, serverPort), 15)
            print("Connected!")
            break
        except:
            print("Trying to connect...\r", end="")

    for c in range(chunks_received, total_chunks):
        bytes_range = str(c * CHUNK_SIZE) + "-" + str((c+1) * CHUNK_SIZE - 1)
        GET_request = "GET /big.txt HTTP/1.1\r\nHost: " + serverName + "\r\nConnection: keep-alive\r\nRange: bytes=" + bytes_range + "\r\n\r\n"
        clientSocket.sendall(GET_request.encode())
        print(bytes_range)

    data = recvall(clientSocket)
    while len(data) > 0:
        header_end = data.find(b"\r\n\r\n") + len(b"\r\n\r\n")
        for line in data[:header_end].decode().splitlines():
            if line.startswith("Content-Range: bytes "):
                content_range = line[len("Content-Range: bytes "):]
                chunk_index = int(int(content_range.split("-")[0]) / CHUNK_SIZE)
                print(chunk_index)
                chunk_data = data[header_end: header_end + CHUNK_SIZE]
                # chunk_data = data[:header_end + CHUNK_SIZE]
                if chunk_index != total_chunks -1 and len(data[:header_end + CHUNK_SIZE]) != header_end + CHUNK_SIZE:
                    break
                chunks[chunk_index] = chunk_data
                # chunks[chunk_index] = data[header_end: header_end + CHUNK_SIZE]
                chunks_received += 1
                
        data = data[header_end + CHUNK_SIZE:]
    
    print("chunks rec", chunks_received)
    clientSocket.close()


# with open('out3.txt', 'wb') as file:
#     file.write(received_data)

# clientSocket.close()

out_file = "out5.txt"
try:
    os.remove(out_file)
except OSError:
    pass
with open('out5.txt', 'ab') as file:
    for c in range(0, total_chunks):
        file.write(chunks[c])

print(total_chunks)
