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
from chain_builder import *


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
    storage_proof = s.get_contract_instance(w3, address_of_storage_proof, "StorageProof")
    proof_chain = build_proof_chain(str(storage_proof.getFileId())+".txt", storage_proof.getChallenge(), 3)
    
    
    storage_proof.submitProof(pickle.dumps(proof_chain), transact={'from': prover_id, 'gas':2000000000})
    print("Proof submited for verification")



