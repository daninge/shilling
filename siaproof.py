import merkletools as m
import time
import os
import hashlib 

mt = m.MerkleTools(hash_type="md5")

def get_num_blocks(file_name):
    file_size = os.stat("files/"+str(file_name)).st_size
    return int(file_size / 100)

def sha(num):
    h = hashlib.sha256()
    h.update(num)
    return h.hexdigest()

def get_data(file_name, challenge_block):
   # return file[challenge_block]
    f = open("files/"+str(file_name), 'r')
    file_size = os.stat("files/"+str(file_name)).st_size
    #print("number of blocks = "+str(int(file_size / 1000)))
    f.seek(100 * challenge_block)
    #stuff = int.from_bytes(bytes(f.read(100)), byteorder='little')
    stuff = f.read(100)
    f.close()
    return stuff

def generate_proof(challenge, file_name):

    for i in range(0, get_num_blocks(file_name)):
        mt.add_leaf(get_data(file_name, i), True)

    mt.make_tree()

    while not mt.is_ready:
        print("Waiting")
        time.sleep(1)
    
    #print("merkle root "+mt.get_merkle_root())

    return (mt.get_merkle_root(), get_data(file_name, challenge), mt.get_proof(challenge))

def verify_proof(proof, data, merkle_root):
    h = hashlib.md5()
    h.update(str(data).encode('utf-8'))
    return mt.validate_proof(proof, h.hexdigest() ,merkle_root)


proof = generate_proof(4, "somefile.txt")
print(verify_proof(proof[2], proof[1], proof[0]))



