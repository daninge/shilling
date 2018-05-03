from web3 import Web3, HTTPProvider
import time
import setup as s
#import pdp
import json
import os
import siaproof as sia

w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

IS_OUTSOURCING_PROOFS = False

import sys
sys.path.append('./posw')
from posw.posw import *
from util import sha256H
N = 10

def build_proof_chain(file_name, initial_challenge, chain_length):
    proofs = []
    chains = []
    chi = initial_challenge
    for i in range(0, chain_length):
        challenge_block = chi % sia.get_num_blocks(file_name)
        p = sia.generate_proof(challenge_block, file_name)
        proofs += [p]
        chi = str(p)
        G = compute_posw(chi, n=N)
        gamma = opening_challenge(secure=False, s=420)
        chain = compute_open(chi, G, gamma)
        chains += [(G.node[BinaryString(0, 0)]['label'], chain)]
        chi = int(G.node[BinaryString(0, 0)]['label'])
    block_filter = w3.eth.filter('latest')
    print(w3.eth.getBlock('latest')['number'], w3.eth.getBlock('latest')['hash'])
    return (proofs, chains)

def verify_proof_chain(merkle_root, proofs, chains, initial_challenge):
    for i in range(0, len(proofs)):
        if not sia.verify_proof(proofs[i][2], proofs[i][1], proofs[i][0]):
            print("sia failed")
            return False
        chi = str(proofs[i])
        gamma = opening_challenge(secure=False, s=420)
        if not compute_verify(chi, chains[i][0], gamma, chains[i][1]):
            print("compute verify failed")
            return False
        chi = int(chains[i][0])
    return True
        



proofs, chains = build_proof_chain("somefile.txt", 5, 5)
print(verify_proof_chain(4,proofs, chains, 5))
exit()




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

    print(build_proof_chain("somefile.txt", current_contract.getInitialChallenge(), 3))



