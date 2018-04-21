from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
#print(w3.eth.blockNumber)

import setup as s
import time
import random
import pdp

file = [1234, 5678, 9101, 1213, 1234, 4321, 5678]

###################
#Client logic below here


file_id = 60

#client_account
client_account = w3.eth.accounts[2]

#Get the genesis contract
genesis_contract = s.get_contract_instance(w3, s.genesis_address, "GenesisContract")

print("Requesting storage for file "+str(file_id))

#request storage
new_storage_request = s.make_contract(w3, "RequestStorageContract")
tx_hash = new_storage_request.constructor(fileIdIn=file_id, requestorIn=client_account).transact(transaction={'from': client_account})
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
storage_request = s.get_contract_instance(w3, receipt['contractAddress'], "StorageProof")

print("Publicising available contract to mining pool")
print("contract Address "+str(receipt['contractAddress']))
genesis_contract.submitContract(receipt['contractAddress']).transact(transaction={'from': client_account})

#wait for a miner to accept
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

print("Generating keys")
#generate keys
pk, sk = pdp.key_gen()

#request proofs regularly
while True:
    time.sleep(5)
    print("Requesting proof of storage")

    #generate new challenge
    c = random.randint(0, len(file))
    k1 = random.randint(0, 10000)
    k2 = random.randint(0, 10000)
    s = random.randint(0, pk[0])

    #generate new proof request contract + push to network
    new_storage_proof = s.make_contract(w3, "StorageProof")
    tx_hash = new_storage_proof.constructor(storerIn=storer_id, fileIdIn=file_id, cIn = c, k1In = k1, k2In = k2, gsIn = (pk[1] ** s) ).transact(transaction={'from': client_account})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    proof_request = s.get_contract_instance(w3, receipt['contractAddress'], "StorageProof")

    #request proof
    storage_request.requestProof(receipt['contractAddress'])



