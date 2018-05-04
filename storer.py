from web3 import Web3, HTTPProvider
import time
import setup as s
#import pdp
import json
import os

w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

IS_OUTSOURCING_PROOFS = False

import sys
sys.path.append('./posw')
from posw.posw import *


def prove (address, account):
    print("Outsourcing proof")

    proof_request_contract = s.get_contract_instance(w3, address, "StorageProof")
    c = proof_request_contract.getChallenge()
    print(c)

    #request outsourcing
    new_outsource = s.make_contract(w3, "OutsourcingContract")
    tx_hash = new_outsource.constructor(requestorIn=address, fileIdIn=proof_request_contract.getFileId(), proofAddressIn=address).transact(transaction={'from': account})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    outsource_request = s.get_contract_instance(w3, receipt['contractAddress'], "OutsourcingContract")
    genesis_contract.submitOutsourcingContract(receipt['contractAddress'], transact={'from': account})
    print("Proof outsource requested")
    while outsource_request.getProvider() == None:
        time.sleep(1)
        print("Waiting for provider")

    prover_id = outsource_request.getProvider()
    print("Prover at "+str(prover_id)+" accepted contract")

    #TODO: verify proof here

    return True



#####################################################################
#Logic starts here

storer_id = w3.eth.accounts[0]

#Get the genesis contract
genesis_contract = s.get_contract_instance(w3, s.genesis_address, "GenesisContract")

print("Waiting for a contract:")

contract_address = genesis_contract.getContract()
while contract_address == None:
    print(genesis_contract.getContract())
    time.sleep(1)
    contract_address = genesis_contract.getContract()

print("Accepting storage contract at address "+str(contract_address))

#Get an instance of the contract at the accepted address
current_contract = s.get_contract_instance(w3, contract_address, "RequestStorageContract")
current_contract.setStorer(storer_id, transact={'from': storer_id})

#records the number of proofs we have submitted so far
num_proofs_so_far = 0

print("Waiting for proof requests")
#respond to requests for proofs of storage
while True:
    time.sleep(1)
    proof_request_list = current_contract.getProofs()
    print(proof_request_list)
    if len(proof_request_list) > num_proofs_so_far:
        print("Proof requested at address "+str(num_proofs_so_far))
        assert(prove(proof_request_list[num_proofs_so_far], storer_id))
        exit()


