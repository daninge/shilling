from prover import *
import sys
from posw.balloon import *
import time

#order of args tb, tp, n, is_verify
# tb = int(sys.argv[-4])
# tp = int(sys.argv[-3])
# n = int(sys.argv[-2])
# is_verify = int(sys.argv[-1])
tb = 20
tp = 1
n = 10



def my_custom_hash_function(nonce, arg, ti):
    return balloon_hash(nonce, arg, space=1, time=ti)

while True:
    print("tp = "+str(tp))
    ti = time.time()
    proofs, chains = build_proof_chain("somefile.txt", 5, 1, lambda x, y: my_custom_hash_function(x, y, tb), tp=tp)
    proof_time = time.time() - ti
    ti = time.time()
    verify_proof_chain(4,proofs, chains, 20, lambda x, y: my_custom_hash_function(x, y, tb), tp=tp)
    verify_time = time.time() - ti
    tp += 2

