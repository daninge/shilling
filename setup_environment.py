import setup as s

from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

result = s.deploy_contract(w3, "GenesisContract",w3.eth.accounts[0], None)
contract = s.get_contract_instance(w3, result['contractAddress'], "GenesisContract")

f= open("genesis_address.txt","w+")
f.write(result['contractAddress'])
# print(contract.getAvailableContracts())

# contract.submitContract(result['contractAddress'], transact={'from': w3.eth.accounts[0]});
# contract.submitContract(result['contractAddress'], transact={'from': w3.eth.accounts[0]});
# contract.submitContract(result['contractAddress'], transact={'from': w3.eth.accounts[0]});
# print(contract.getAvailableContracts())
#print(result)