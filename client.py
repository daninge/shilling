from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
#print(w3.eth.blockNumber)

import setup as s
import time

#deploys a contract requesting a proof of storage
receipt = s.deploy_contract(w3, "StorageProof", w3.eth.accounts[1], args=[69, 69])

#sets the contract location so other miners know where it is
#admittedly not decentralised but could potentially be
s.storage_proof_address = receipt['contractAddress']


my_contract = s.get_contract_instance(w3, receipt['contractAddress'], "StorageProof")
#print(my_contract.submitProof(b'abc', transact={'from': w3.eth.accounts[1]}))
while True: 
    proof = my_contract.getProof()
    if proof != b'':
        break
    time.sleep(1)
print("proof updated!!!")