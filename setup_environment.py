import setup as s

from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

genesis_id = w3.eth.accounts[0]

# new = s.make_contract(w3, "GenesisContract")
# result = s.deploy_contract(w3, new, w3.eth.accounts[0])
# contract = s.get_contract_instance(w3, result['contractAddress'], "GenesisContract")

new = s.make_contract(w3, "GenesisContract")
tx_hash = new.constructor().transact(transaction={'from': genesis_id})
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
genesis_contract = s.get_contract_instance(w3, receipt['contractAddress'], "GenesisContract")
# print(receipt['contractAddress'])
# print(genesis_contract.getContract())
# genesis_contract.submitContract(genesis_id, transact={'from':genesis_id})

# print(genesis_contract.getContract())
f= open("genesis_address.txt","w+")
f.write(receipt['contractAddress'])
# print(contract.getAvailableContracts())

# contract.submitContract(result['contractAddress'], transact={'from': w3.eth.accounts[0]});
# contract.submitContract(result['contractAddress'], transact={'from': w3.eth.accounts[0]});
# contract.submitContract(result['contractAddress'], transact={'from': w3.eth.accounts[0]});
# print(contract.getAvailableContracts())
#print(result)