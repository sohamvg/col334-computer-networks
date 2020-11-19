content_length = 6488666
CHUNK_SIZE = 10000

num_chunks = int(content_length / CHUNK_SIZE) + 1

chunks = [None] * num_chunks

#########################################

with open("out3.txt", 'rb') as file:
    data = file.read()

    while len(data) > 0:
        # print(data)
        header_end = data.find(b"\r\n\r\n") + len(b"\r\n\r\n")
        for line in data[:header_end].decode().splitlines():
            if line.startswith("Content-Range: bytes "):
                content_range = line[len("Content-Range: bytes "):]
                chunk_index = int(int(content_range.split("-")[0]) / CHUNK_SIZE)
                print(chunk_index)
                chunk_data = data[header_end: header_end + CHUNK_SIZE]
                print(len(chunk_data))
                chunks[chunk_index] = chunk_data
                # print(int(line[len("Content-Range: bytes "):].split("-")[0])/CHUNK_SIZE)
        # for line in data:
        #     print(line)
        # print(data[header_end + 10000:])
        
        data = data[header_end + CHUNK_SIZE:]

    # print(chunks[1])
    # print("\n------\n")
    # print(chunks[2])
