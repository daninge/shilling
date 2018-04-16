from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

account_id = w3.eth.accounts[0]


print(account_id)
print(w3.eth.accounts)

#print statement
from solc import compile_source
from web3.contract import ConciseContract
import time 
# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.0;

contract StorageContract {
    int

    function StorageContract() {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() constant returns (string) {
        return greeting;
    }
}
'''

compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:Greeter']

print("****")
print(contract_interface['abi'])
print("//////")
# Instantiate and deploy contract
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 410000})

# Get tx receipt to get contract address
tx_receipt = None
while tx_receipt == None:
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    time.sleep(1)

contract_address = tx_receipt['contractAddress']
print("contract address = "+str(contract_address))
# Contract instance in concise mode
contract_instance = w3.eth.contract(abi=contract_interface['abi'], address=contract_address, ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object
print('Contract value: {}'.format(contract_instance.greet()))
contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[0]})
print('Setting value to: Nihao')
print('Contract value: {}'.format(contract_instance.greet()))