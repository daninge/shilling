import os
from solc import compile_source
from web3.contract import ConciseContract

path = "/home/dinge/shilling-truffle/contracts/"

contracts = {}
contract_interfaces = {}

#import the source code
for file_name in os.listdir(path):
    file = open(path+file_name, 'r')
    contracts[file_name[:len(file_name) -4]] = file.read()

#print(contracts.keys())

#compile the contracts
for contract, src in contracts.items():
    #print(contract)
    contract_interfaces[contract] = compile_source(src)['<stdin>:'+contract]
    #print(compile_source(str(src)))
    #print(src)
    #break

def deploy_contract(w3, contract_name, sender, args=[1,1]):
    print(contract_name + " being deployed to network")
    # Instantiate and deploy contract
    contract = w3.eth.contract(abi=contract_interfaces[contract_name]['abi'], bytecode=contract_interfaces[contract_name]['bin'])
    # Get transaction hash from deployed contract
    tx_hash = contract.constructor(args = args).transact(transaction={'from': sender})
    # Get tx receipt to get contract address
    return w3.eth.waitForTransactionReceipt(tx_hash)

def get_contract_instance(w3, address, contract_name):
    return w3.eth.contract(abi=contract_interfaces[contract_name]['abi'], address=address, ContractFactoryClass=ConciseContract)

#print(contract_interfaces['StorageProof']['abi'])