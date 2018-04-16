from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
#print(w3.eth.blockNumber)

import setup as s

receipt = s.deploy_contract(w3, "StorageProof", w3.eth.accounts[1], args=[69, 69])
print(receipt)
my_contract = s.get_contract_instance(w3, receipt['contractAddress'], "StorageProof")
print(my_contract.submitProof(b'abc', transact={'from': w3.eth.accounts[1]}))
print(my_contract.getProof())