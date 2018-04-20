from Crypto.Util import number
import rsa
import gensafeprime
import random
import hashlib
from fractions import gcd
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
def key_gen():
    (pubkey, privkey) = rsa.newkeys(2048)
    pk = (privkey.n, g(privkey.p, privkey.q))
    sk = (privkey.e, privkey.d, random.getrandbits(2048))
    return (pk, sk)

def tag_block(pk, sk, m, i):
    wi = sk[2] + (i << 2048)
    t = (hashlib.sha256(wi) * (g ** m)) ** sk[1]
    return (t, wi)

#f is number of avaliable blocks
def gen_proof(pk, f, chal, T):
    c, k1, k2, gs = chal
    
    #generate challenge blocks
    random.seed(k1)
    challenge_blocks = []
    for i in range(0, c):
        something = random.randrange(f)
        while something not in challenge_blocks:
            something = random.randrange(f)
        challenge_blocks.append(something)
    
    #generate coefficients
    random.seed(k2)
    coefficients = []
    for i in range(0, c):
        coefficients.append(random.randint(0, 2000))

    #Multiply challeneges
    big_t = 1
    for challenge in challenge_blocks:
        big_t *= T[challenge][0]

    temp = 0
    for i in range(0, c):
        temp += coefficients[i] * get_message(challenge_blocks[i])
    
    rho = hashlib.sha256((gs ** temp) % pk[0])

    return (big_t, rho)



        



    
