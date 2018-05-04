from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
#print(w3.eth.blockNumber)

import sys
sys.path.append('./posw')

from posw.posw import *
from posw.balloon import *
from util import sha256H
from chain_builder import *

import setup as s
import time
import random
import json
import pickle
###################
#Client logic below here

file_id = sys.argv[-1]

try:
    f = open("files/"+str(file_id)+".txt", 'r')
except:
    print("No such file")
    exit()

#client_account
client_account = w3.eth.accounts[2]

#Get the genesis contract
genesis_contract = s.get_contract_instance(w3, s.genesis_address, "GenesisContract")

print("Requesting storer for file "+str(file_name))

#request storage
new_storage_request = s.make_contract(w3, "RequestStorageContract")
tx_hash = new_storage_request.constructor(fileIdIn=file_name, requestorIn=client_account).transact(transaction={'from': client_account})
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
storage_request = s.get_contract_instance(w3, receipt['contractAddress'], "RequestStorageContract")

print("Publicising available contract to mining pool")
print("Contract Address "+str(receipt['contractAddress']))
genesis_contract.submitContract(receipt['contractAddress'], transact={'from':client_account})

#wait for a miner to accept
print("Waiting for a storer to accept the contract")

while storage_request.getStorer() == None:
    # print(storage_request.getFileId())
    # print(storage_request.getStorer())
    # print(storage_request.getRequestor())
    print("Waiting for a storer to accept the contract")
    time.sleep(2)

#get the id of the storer 
storer_id = storage_request.getStorer()

print("Storer "+str(storer_id)+" accepted the contract!")

#transfer file to miner
##TODO: is this worth doing?

#request proofs regularly
while True:
    #time.sleep(5)
    print("Requesting proof of storage")

    #generate new challenge
    c = random.randint(0, 10) #TODO: this should be in range of num blocks in file

    #generate new proof request contract + push to network
    new_storage_proof = s.make_contract(w3, "StorageProof")
    tx_hash = new_storage_proof.constructor(storage_request.getRequestor(), storage_request.getStorer(), 59, c).transact(transaction={'from': client_account})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    proof_request = s.get_contract_instance(w3, receipt['contractAddress'], "StorageProof")
    print("Challenge = " + str(proof_request.getChallenge()))

    #pulicise storage proof
    print("Publicising new proof request at "+receipt['contractAddress'])
    storage_request.requestProof(receipt['contractAddress'], transact={'from': client_account})
    print("Waiting for proof from"+str(storage_request.getStorer()))
    while True:
        #print(proof_request.getProof())
        time.sleep(1)
        if proof_request.getProof() != b'':
            break
    proof_received = proof_request.getProof()
    reloaded = pickle.loads(proof_received)
    #print(reloaded)
    print("Proof Detected on Blockchain")
    print("Verifying Proof")
    if verify_proof_chain(None, reloaded[0], reloaded[1], proof_request.getChallenge()):
        print("Accept")
    else:
        print("Reject")
    exit()




