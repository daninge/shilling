import os
from solc import compile_source
from web3.contract import ConciseContract
import sys
sys.path.append('./posw')
from posw.posw import *
import pickle

path = "contracts/"

contracts = {}
contract_interfaces = {}

genesis_address = None

try:
    f = open("genesis_address.txt", "r")
    genesis_address = f.read()
except:
    print("Failed to find genesis address file")

#import the source code
for file_name in os.listdir(path):
    file = open(path+file_name, 'r')
    contracts[file_name[:len(file_name) -4]] = file.read()


#compile the contracts
for contract, src in contracts.items():
    contract_interfaces[contract] = compile_source(src)['<stdin>:'+contract]

def make_contract(w3, contract_name):
    return w3.eth.contract(abi=contract_interfaces[contract_name]['abi'], bytecode=contract_interfaces[contract_name]['bin'])

#Gets a concise contract instance for this contract
def get_contract_instance(w3, address, contract_name):
    return w3.eth.contract(abi=contract_interfaces[contract_name]['abi'], address=address, ContractFactoryClass=ConciseContract)