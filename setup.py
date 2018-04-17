import os
from solc import compile_source
from web3.contract import ConciseContract

path = "contracts/"

contracts = {}
contract_interfaces = {}

storage_proof_address = None

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

#Gets a concise contract instance for this contract
def get_contract_instance(w3, address, contract_name):
    return w3.eth.contract(abi=contract_interfaces[contract_name]['abi'], address=address, ContractFactoryClass=ConciseContract)

def block_received(block_number):
    block = w3.eth.getBlock(block_number);
    print(block)
    for i in range(0, len(block.transactions)):
        print("Processing Transaction "+ str(i)+ " from block "+str(block_number))
        transaction = (w3.eth.getTransactionFromBlock(block.number, i))

#Returns when a transaction occurs on this contract
def monitor_contract(w3, address, beginning_block): #beginning block is the first block to search
    printed = w3.eth.blockNumber #starting from now (i.e. don't print the whole chain every time)
    while(True):
        while printed < w3.eth.blockNumber:
            printed+=1
            print("RECEIVED BLOCK "+str(printed))
            block_received(printed)