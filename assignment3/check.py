
import hashlib

file_name = 'output/download2.txt'

original_md5 = '70a4b9f4707d258f559f91615297a3ec'  

with open(file_name, 'rb') as file_to_check:
    data = file_to_check.read()
    md5_returned = hashlib.md5(data).hexdigest()

print(md5_returned)
if original_md5 == md5_returned:
    print ("MD5 verified.")
else:
    print ("MD5 verification failed!.")
