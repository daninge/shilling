from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
#print(w3.eth.blockNumber)

import setup as s
import time
import random
import pdp
import json

###################
#Client logic below here

file_name = 59

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
#time.sleep(5)
#print("Generating keys")
#generate keys
pk, sk = pdp.key_gen()

tags = []

# #generate tags
# for i in range(0, pdp.get_num_blocks(file_name)):
#     tags.append(pdp.tag_block(pk, sk, pdp.get_data(file_name, i), i))

# #print(tags)
# f = open(str(file_name)+"-tags.txt", 'w')
# f.write(json.dumps(tags))
# f.flush()

#request proofs regularly
while True:
    #time.sleep(5)
    print("Requesting proof of storage")

    #generate new challenge
    c = random.randint(0, 10) #TODO: this should be in range of num blocks in file

    #generate new proof request contract + push to network
    new_storage_proof = s.make_contract(w3, "StorageProof")
    tx_hash = new_storage_proof.constructor(storage_request.getRequestor(), storage_request.getStorer(), "somefile.txt", c).transact(transaction={'from': client_account})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    proof_request = s.get_contract_instance(w3, receipt['contractAddress'], "StorageProof")
    print("Challenge = " + str(proof_request.getChallenge()))

    #pulicise storage proof
    print("Publicising new proof request at "+receipt['contractAddress'])
    #time.sleep(7)
    storage_request.requestProof(receipt['contractAddress'], transact={'from': client_account})
    #time.sleep(3)
    print("Waiting for proof from"+str(storage_request.getStorer()))
    while True:
        #print(proof_request.getProof())
        time.sleep(1)
        if proof_request.getProof() != b'':
            break
    proof_received = json.loads(proof_request.getProof().decode('utf-8'))
    print("Proof Detected on Blockchain")

    #TODO: Verify proof here
    exit()




