from Crypto.Util import number
import rsa
import gensafeprime
import random
import hashlib
from fractions import gcd
from decimal import *
import os 
import json
prime_len = 256



def g(p, q):
    a = random.randint(1, p * q)
    while not is_good_number(a, p, q):
        a = random.randint(1, p * q) 
    return a    

"""
Checks whether or not a, p, q work for our scheme. We want the following
    a =/= -1, 0, 1   (mod p)
    a =/= -1, 0, 1   (mod q)
"""
def is_good_number(a, p, q ): 
    aModP = a % p
    if aModP == 0 or aModP == 1 or aModP == (p-1):
        return False
    aModQ = a % q
    if aModQ == 0 or aModQ == 1 or aModQ == (q-1):
        return False
    return True

def get_tags(file_id):
    f = open(str(file_id)+"-tags.txt", 'r')
    tags = f.read()
    return json.loads(tags)

def get_data(file_name, challenge_block):
   # return file[challenge_block]
    f = open("files/kung.jpg", 'rb')
    file_size = os.stat("files/kung.jpg").st_size
    #print("number of blocks = "+str(int(file_size / 1000)))
    f.seek(1000 * challenge_block)
    stuff = int.from_bytes(bytes(f.read(1000)), byteorder='little')
    f.close()
    return stuff

def get_num_blocks(file_name):
    file_size = os.stat("files/kung.jpg").st_size
    return int(file_size / 1000)

####################
#Usable functions below here

#file = [1234, 5678, 9101, 1213,1234, 4321, 5678]

def sha(num):
    h = hashlib.sha256()
    h.update(str(num).encode('utf-8'))
    return int(h.hexdigest(), 16)

def key_gen():
    (pubkey, privkey) = rsa.newkeys(256)
    #pk = (N, g)
    pk = (privkey.n, g(privkey.p, privkey.q))
    #sk = (e, d, v)
    sk = (privkey.e, privkey.d, random.getrandbits(256))
    return (pk, sk)

def tag_block(pk, sk, m, i):
    wi = sk[2] + (i << 256)
    t = pow( (sha(wi) * pow(pk[1], m, pk[0])), sk[1], pk[0])
    return (t, wi)

def get_challenge_blocks(k, c, f):
    random.seed(k)
    challenge_blocks = []
    for i in range(0, c):
        something = random.randrange(f)
        while something in challenge_blocks:
            something = random.randrange(f)
        challenge_blocks.append(something)  
    return challenge_blocks
    #return [0, 2]

def generate_coefficients(k ,c):
    random.seed(k)
    coefficients = []
    for i in range(0, c):
        coefficients.append(random.randint(0, 2000))
    return coefficients
    #return [5, 10]

#f is number of avaliable blocks
def gen_proof(pk, f, chal, tags, actual_blocks):
    c, k1, k2, gs = chal
    
    #generate challenge blocks
    challenge_blocks = get_challenge_blocks(k1, c, f)
    
    print("raymond")
    #generate coefficients
    coefficients = generate_coefficients(k2, c)

    T = 1
    for i in range(0, c):
        #for every challenge
        block_num = challenge_blocks[i]
        coeff = coefficients[i]
        ti, wi = tags[block_num]
        T = T * pow(ti, coeff, pk[0])

    exponent = 0
    for i in range(0, c):
        block_num = challenge_blocks[i]
        coeff = coefficients[i]
        m = actual_blocks[i]
        exponent = exponent + (coeff * m)
    
    rho = sha(pow(gs, exponent, pk[0]))
    print("rho")
    return (T, rho)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def mod_inv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

#a/b mod m
def mod_divide(a, b, m):
    a = a % m
    inv = mod_inv(b, m)
    if inv == -1:
        print("oh no")
    else:
        return (inv * a) % m
    
def check_proof(pk, sk, chal, V):
    c, k1, k2, gs = chal
    print("before")
    # curvy_t = T * e
    curvy_t = pow(V[0], sk[0], pk[0])
    print("after")
    #generate challenge blocks
    challenge_blocks = get_challenge_blocks(k1, c, get_num_blocks(60))
    print(challenge_blocks)
    #generate coefficients
    coefficients = generate_coefficients(k2, c)
    print("initial +"+str(curvy_t))
    for i in range(0, c):
        wi = str(sk[2] + (challenge_blocks[i] << 256)).encode('utf-8')
        #print(wi)
        #print("///////////")
        h = hashlib.sha256()
        h.update(wi)
        hash_output = int(h.hexdigest(), 16) % pk[0]
        print("hmml")
        curvy_t = mod_divide(curvy_t, pow(hash_output, coefficients[i]), pk[0])
        #curvy_t = (curvy_t / pow(hash_output, coefficients[i])) % pk[0]
    #print("curvy t = "+str(curvy_t))

    h = hashlib.sha256()
    h.update(str(pow(curvy_t, chal[3], pk[0])).encode('utf-8'))
    hash_output = int(h.hexdigest(), 16) % pk[0]
    print(hash_output)
    if hash_output == V[1]:
        return True
    else:
        return False

my_file = "kung.jpg"

tags = []
pk, sk = key_gen()

#print(sk)
#on the client
for i in range(0, get_num_blocks(my_file)):
    print("tagging block "+str(i))
    tag = tag_block(pk, sk, get_data(my_file, i), i)
    print(tag)
    tags.append(tag)

chal = (2, 2, 4, pk[1] ** 4)
#print(tags)
print("here")
#print("e "+)

challenge_blocks = get_challenge_blocks(chal[1], chal[0], get_num_blocks(my_file))
print(challenge_blocks)
data = []
for index in challenge_blocks:
    data.append(get_data(my_file, index))

proof = gen_proof(pk, get_num_blocks(my_file), chal, tags, data)
print("proof")
print(proof)
chal = (2, 2, 4, 4)
print(check_proof(pk, sk, chal, proof))
