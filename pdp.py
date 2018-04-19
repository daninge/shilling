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
def key_gen(key_size):
    # p = gensafeprime.generate(prime_len)
    # pdash = (p - 1)/2
    # q = gensafeprime.generate(prime_len)
    # qdash = (q - 1)/2
    # N = p * q
    
    # #find e and d
    # v = random.getrandbits(key_size)
    



def tag_block(pk, sk, m, i):
    print("erdsafji\n")
