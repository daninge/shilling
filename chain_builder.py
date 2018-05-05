from web3 import Web3, HTTPProvider
import time
import setup as s
import json
import os
import siaproof as sia
import pickle
import datetime

w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

IS_OUTSOURCING_PROOFS = False

import sys
sys.path.append('./posw')
from posw.posw import *
from posw.balloon import *
from util import sha256H


def build_proof_chain(file_name, initial_challenge, chain_length, t=None, tp=5, n=10):
    proofs = []
    chains = []
    chi = initial_challenge
    print("n = "+str(n))
    for i in range(0, chain_length):
        challenge_block = chi % sia.get_num_blocks(file_name)
        p = sia.generate_proof(challenge_block, file_name)
        proofs += [p]
        
        seed_string = ""
        #generate seed from all previous items in chain
        for j in range(0, len(proofs)):
            seed_string = seed_string + str(proofs[j])
        chi = seed_string

        G = compute_posw(chi, n=n)
        gamma = opening_challenge(secure=False, s=420, n=n, t=tp)
        chain = compute_open(chi, G, gamma)
        chains += [(G.node[BinaryString(0, 0)]['label'], chain)]
        chi = int(G.node[BinaryString(0, 0)]['label'])
    challenge_block = chi % sia.get_num_blocks(file_name)
    proofs += [sia.generate_proof(challenge_block, file_name)]
    block_filter = w3.eth.filter('latest')
    return (proofs, chains)


def verify_proof_chain(merkle_root, proofs, chains, initial_challenge, t=None, tp=5, n=10):
    for i in range(0, len(proofs) - 1):
        if not sia.verify_proof(proofs[i][2], proofs[i][1], proofs[i][0]):
            print("sia failed")
            return False
        seed_string = ""
        for j in range(0, i+1):
            seed_string = seed_string + str(proofs[j])
        chi = seed_string
        gamma = opening_challenge(secure=False, s=420, t=tp)
        if not compute_verify(chi, chains[i][0], gamma, chains[i][1]):
            print("compute verify failed")
            return False
        chi = int(chains[i][0])
    if not sia.verify_proof(proofs[-1][2], proofs[-1][1], proofs[-1][0]):
        return False
    else:
        return True



if __name__ == '__main__':
    proofs, chains = build_proof_chain("somefile.txt", 5,5)
    exit()