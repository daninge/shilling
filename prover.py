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

def build_proof_chain(file_name, initial_challenge, chain_length):
    proofs = []
    chains = []
    chi = initial_challenge
    for i in range(0, chain_length):
        challenge_block = chi % sia.get_num_blocks(file_name)
        proofs += [(challenge_block, sia.generate_proof(challenge_block, file_name))]
        G = compute_posw(chi)
        chains += [G]
        chi = int(G.node[BinaryString(0, 0)]['label'])
    print(int(chi))
    print(proofs)
    print(chains)



build_proof_chain("somefile.txt", 5, 2)
#####################################################################
#Logic starts here

prover_id = w3.eth.accounts[5]

#Get the genesis contract
genesis_contract = s.get_contract_instance(w3, s.genesis_address, "GenesisContract")

print("Waiting for a contract:")

#print(genesis_contract.getAvailableContracts())

# print(s.genesis_address)

# print(genesis_contract.getContract())
#genesis_contract.submitContract(storer_id,transact={'from': storer_id})
#print(genesis_contract.getContract())
contract_address = genesis_contract.getOutsourcingContract()
while contract_address == None:
    #print(genesis_contract.getOutsourcingContract())
    time.sleep(1)
    contract_address = genesis_contract.getOutsourcingContract()

print("Accepting outsourcing contract at address "+str(contract_address))

#Get an instance of the contract at the accepted address
current_contract = s.get_contract_instance(w3, contract_address, "OutsourcingContract")
current_contract.setProvider(prover_id, transact={'from': prover_id})

exit()
while True:
    print(current_contract.getInitialChallenge())



