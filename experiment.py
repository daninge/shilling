from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
#print(w3.eth.blockNumber)

import setup as s
import time
# receipt = s.deploy_contract(w3, "StorageProof", w3.eth.accounts[1], args=[69, 69])
# print(receipt)
# my_contract = s.get_contract_instance(w3, receipt['contractAddress'], "StorageProof")
# print(my_contract.submitProof(b'abc', transact={'from': w3.eth.accounts[1]}))
# while 
# print(my_contract.getProof())

# while s.storage_proof_address == None:
#     continue

time.sleep(10)

s.get_contract_instance(w3, s.storage_proof_address, "StorageProof").setProof(b'maddy')

