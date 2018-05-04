from web3 import Web3, HTTPProvider
import time
import setup as s
#import pdp
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


def build_proof_chain(file_name, initial_challenge, chain_length, t=None, tp=200, n=10):
    proofs = []
    chains = []
    #total_len = 0
    chi = initial_challenge
    for i in range(0, chain_length):
        challenge_block = chi % sia.get_num_blocks(file_name)
        p = sia.generate_proof(challenge_block, file_name)
        proofs += [p]
        chi = str(p)
        G = compute_posw(chi, n=n)
        gamma = opening_challenge(secure=False, s=420, t=tp)
        chain = compute_open(chi, G, gamma)
        #total_len += len(chain) * (len(chain[0]) * 32)
        chains += [(G.node[BinaryString(0, 0)]['label'], chain)]
        chi = int(G.node[BinaryString(0, 0)]['label'])
    #print("total len = " +str(total_len))
    block_filter = w3.eth.filter('latest')
    return (proofs, chains)

def verify_proof_chain(merkle_root, proofs, chains, initial_challenge, hash_function, t=None, tp=200):
    for i in range(0, len(proofs)):
        if not sia.verify_proof(proofs[i][2], proofs[i][1], proofs[i][0]):
            print("sia failed")
            return False
        chi = str(proofs[i])
        gamma = opening_challenge(secure=False, s=420, t=tp)
        if not compute_verify(chi, chains[i][0], gamma, chains[i][1], H=hash_function):
            print("compute verify failed")
            return False
        chi = int(chains[i][0])
    return True


# proofs, chains = build_proof_chain("somefile.txt", 5,5)
# exit()
# print("prover time = "+str(datetime.datetime.now() - time))
# time = 0
# verify_proof_chain(4,proofs, chains, 5)
# print("verifier time = "+str(datetime.datetime.now()))
# exit()




if __name__ == '__main__':
    #####################################################################
    #Logic starts here

    prover_id = w3.eth.accounts[5]

    #Get the genesis contract
    genesis_contract = s.get_contract_instance(w3, s.genesis_address, "GenesisContract")

    print("Waiting for a contract:")

    contract_address = genesis_contract.getOutsourcingContract()
    while contract_address == None:
        #print(genesis_contract.getOutsourcingContract())
        time.sleep(1)
        contract_address = genesis_contract.getOutsourcingContract()

    print("Accepting outsourcing contract at address "+str(contract_address))

    #Get an instance of the contract at the accepted address
    current_contract = s.get_contract_instance(w3, contract_address, "OutsourcingContract")
    current_contract.setProvider(prover_id, transact={'from': prover_id})

    address_of_storage_proof = current_contract.getProofAddress()

    print(build_proof_chain("somefile.txt", current_contract.getInitialChallenge(), 3))



