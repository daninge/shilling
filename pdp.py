from Crypto.Util import number
import rsa
import gensafeprime
import random
import hashlib
from fractions import gcd
from decimal import *
# pprime = None
# p = 2 * pprime + 1
# qprime = None
# q = 2* qprime + 1
# N = p * q



# def g() :

# (pubkey, privkey) = rsa.newkeys(2048)
# # print(pubkey)
# #print(privkey)

# print(privkey.n)
# print("//////////")
# print(privkey.p*privkey.q)

# p = privkey.p 
# q = privkey.q 
# N = privkey.n

prime_len = 512


# def g(n) : 
#     i = 1
#     while i < n:
#         r = i ** 2
#         if gcd(r + 1, n)==1 and gcd(r - 1, n)==1:
#             return r
#         else:
#             i += 1
#     return None

def g(p, q):
    a = random.randint(1, p * q)
    while not isGoodNumber(a, p, q):
        a = random.randint(1, p * q) 
    return a    

def isGoodNumber(a, p, q ): 
    aModP = a % p
    if aModP == 0 or aModP == 1 or aModP == (p-1):
        return False
    aModQ = a % q
    if aModQ == 0 or aModQ == 1 or aModQ == (q-1):
        return False
    return True


####################
#Usable functions below here

file = [1234, 5678, 9101, 1213]

def key_gen():
    (pubkey, privkey) = rsa.newkeys(512)
    #pk = (N, g)
    pk = (privkey.n, g(privkey.p, privkey.q))
    #sk = (e, d, v)
    sk = (privkey.e, privkey.d, random.getrandbits(512))
    return (pk, sk)

def tag_block(pk, sk, m, i):
    wi = str(sk[2] + (i << 512)).encode('utf-8')
    #print(wi)
    #print("///////////")
    h = hashlib.sha256()
    h.update(wi)
    hash_output = int(h.hexdigest(), 16) % pk[0]
    t = pow( (hash_output * (pk[1] ** m)), sk[1], pk[0])
    return (t, wi)

def get_challenge_blocks(k, c, f):
    random.seed(k)
    challenge_blocks = []
    for i in range(0, c):
        something = random.randrange(f)
        while something in challenge_blocks:
            something = random.randrange(f)
        challenge_blocks.append(something)  
    #return challenge_blocks
    return [0, 2]

def generate_coefficients(k ,c):
    random.seed(k)
    coefficients = []
    for i in range(0, c):
        coefficients.append(random.randint(0, 2000))
    #return coefficients
    return [5, 10]

def get_message(i):
    return file[i]

#f is number of avaliable blocks
def gen_proof(pk, f, chal, T):
    c, k1, k2, gs = chal
    
    #generate challenge blocks
    challenge_blocks = get_challenge_blocks(k1, c, f)
    
    print("raymond")
    #generate coefficients
    coefficients = generate_coefficients(k2, c)

    print("wfu")
    #Multiply challeneges
    big_t = 1

    temp = 0
    for i in range(0, c):
        temp += coefficients[i] * get_message(challenge_blocks[i])

    for i in range(0, c):
        wi = str(sk[2] + (challenge_blocks[i] << 512)).encode('utf-8')
        #print(wi)
        #print("///////////")
        h = hashlib.sha256()
        h.update(wi)
        hash_output = int(h.hexdigest(), 16) % pk[0]
        big_t *= (hash_output ** coefficients[i])
    big_t *= temp
    big_t = pow(big_t, sk[1], pk[0])
        #big_t *= T[challenge_blocks[i]][0] ** coefficients[i]
    
    print("john")
    h = hashlib.sha256()
    h.update(str(pow(gs, temp, pk[0])).encode('utf-8'))
    rho = int(h.hexdigest(), 16) % pk[0]
    print("rho")
    return (big_t, rho)

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
    challenge_blocks = get_challenge_blocks(k1, c, len(file))
    
    #generate coefficients
    coefficients = generate_coefficients(k2, c)
    print("initial +"+str(curvy_t))
    for i in range(0, c):
        wi = str(sk[2] + (challenge_blocks[i] << 512)).encode('utf-8')
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


tags = []
pk, sk = key_gen()

#print(sk)
#on the client
for i in range(0, len(file)):
    print("tagging block "+str(i))
    tag = tag_block(pk, sk, get_message(i), i)
    print(tag)
    tags.append(tag)

chal = (2, 2, 4, pk[1] ** 4)
#print(tags)
print("here")
#print("e "+)
proof = gen_proof(pk, len(file), chal, tags)
print("proof")
print(proof)
chal = (2, 2, 4, 4)

print(check_proof(pk, sk, chal, proof))