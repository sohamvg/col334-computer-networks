
# Import hashlib library (md5 method is part of it)
import hashlib

# File to check
file_name = 'out5.txt'

# Correct original md5 goes here
original_md5 = '70a4b9f4707d258f559f91615297a3ec'  

# Open,close, read file and calculate MD5 on its contents 
with open(file_name, 'rb') as file_to_check:
    # read contents of the file
    data = file_to_check.read()
    # pipe contents of the file through
    md5_returned = hashlib.md5(data).hexdigest()

# Finally compare original MD5 with freshly calculated
print(md5_returned)
if original_md5 == md5_returned:
    print ("MD5 verified.")
else:
    print ("MD5 verification failed!.")

# with open(file_name) as f:
#     counter = 1
#     for line in f:
#         counter += 1
#         if counter > 15 or line == "\r\n" or line =="\n":
#             break
#         print(counter, line)


# with open('file.txt', 'w') as fout:
#     fout.writelines(data[counter:])