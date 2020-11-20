import socket
import os
import threading
import time
import sys
from matplotlib import pyplot as plt

CHUNK_SIZE = 10000
MAX_CHUNKS = 999999
chunks = [None] * MAX_CHUNKS

serverNames = ['vayu.iitd.ac.in', 'norvig.com']
serverName = 'norvig.com'
serverPort = 80
object_URL = '/big.txt'

def recvall(sock, progress):
    fragments = []
    while True:
        try:
            data_recv = sock.recv(4096)
            curr_time = time.time()
            if not data_recv:
                break
            fragments.append(data_recv)
            if len(progress) == 0:
                progress.append((curr_time, sys.getsizeof(data_recv)))
            else:
                progress.append((curr_time, progress[-1][1] + sys.getsizeof(data_recv)))
        except Exception as e:
            print("Caught exception in receiving", e)
            arr = b''.join(fragments)
            return arr
    arr = b''.join(fragments)
    return arr

def get_chunks(thread, start, end, progress):
    chunks_received = 0
    total_chunks_to_get = end - start + 1
    if thread % 2 == 0:
        serverName = serverNames[0]
    else:
        serverName = serverNames[1]

    while chunks_received < total_chunks_to_get:
        while True:
            try:
                clientSocket = socket.create_connection((serverName, serverPort), timeout=15)
                print(thread, "Connected!")
                break
            except:
                print(thread, "Trying to connect...\r", end="")

        for c in range(start + chunks_received, end + 1):
            bytes_range = str(c * CHUNK_SIZE) + "-" + str((c+1) * CHUNK_SIZE - 1)
            GET_request = "GET " + object_URL + " HTTP/1.1\r\nHost: " + serverName + "\r\nConnection: keep-alive\r\nRange: bytes=" + bytes_range + "\r\n\r\n"
            clientSocket.sendall(GET_request.encode())
            # print(bytes_range, threading.current_thread().name)

        data = recvall(clientSocket, progress)
        while len(data) > 0:
            header_end = data.find(b"\r\n\r\n") + len(b"\r\n\r\n")
            for line in data[:header_end].decode().splitlines():
                if line.startswith("Content-Range: bytes "):
                    content_range = line[len("Content-Range: bytes "):]
                    chunk_index = int(int(content_range.split("-")[0]) / CHUNK_SIZE)
                    # print(chunk_index, threading.current_thread().name)
                    chunk_data = data[header_end: header_end + CHUNK_SIZE]
                    if chunk_index != end and len(data[:header_end + CHUNK_SIZE]) != header_end + CHUNK_SIZE:
                        break
                    chunks[chunk_index] = chunk_data
                    chunks_received += 1
                    
            data = data[header_end + CHUNK_SIZE:]
        
        # print("chunks rec", chunks_received, threading.current_thread().name)
        clientSocket.close()


if __name__ == "__main__":

    while True:
        try:
            headerSocket = socket.create_connection((serverName, serverPort), timeout=15)
            break
        except:
            print("Trying to connect...\r", end="")
    HEAD_request = "HEAD " + object_URL + " HTTP/1.1\r\nHost: " + serverName + "\r\nConnection: keep-alive\r\n\r\n"
    headerSocket.sendall(HEAD_request.encode())
    header = recvall(headerSocket, [])
    headerSocket.close()
    content_length = 6488666

    for line in header.decode().splitlines():
        if line.startswith("Content-Length: "):
            content_length = int(line[len("Content-Length: "):])
            print("found content length", content_length)

    t0 = time.time()
    total_threads = 15
    sizes = [None] * total_threads

    total_chunks = int(content_length / CHUNK_SIZE) + 1

    zp = total_threads - (total_chunks % total_threads) 
    pp = total_chunks//total_threads
    for i in range(total_threads):
        if(i < zp):
            sizes[i] = pp
        else:
            sizes[i] = pp + 1

    t = [None] * total_threads
    progress = [[] for _ in range(total_threads)]
    start = 0
    for i in range(total_threads):
        # print("thr", i, sizes[i], start, start + sizes[i] - 1)
        t[i] = threading.Thread(target=get_chunks, name='t' + str(i), args=(i, start, start + sizes[i] - 1, progress[i]))
        start = start + sizes[i]

    # starting threads
    for i in range(total_threads):
        t[i].start()

    # wait until all threads finish 
    for i in range(total_threads):
        t[i].join()

    out_file = "out5.txt"
    try:
        os.remove(out_file)
    except OSError:
        pass
    with open(out_file, 'ab') as file:
        for c in range(0, total_chunks):
            try:
                file.write(chunks[c])
            except Exception as e:
                print(c, e)

    for i in range(total_threads):
        plt.plot([x[0] for x in progress[i]], [x[1] for x in progress[i]], label="thread-" + str(i))

    plt.xlabel("time (microseconds)")
    plt.ylabel("bytes")
    plt.title("Download progress for each connection")
    plt.legend()
    plt.show()
    # plt.savefig("conn.png")

    t1 = time.time()
    print("time", t1 - t0)

