from web3 import Web3, HTTPProvider
import time
import pprint

pp = pprint.PrettyPrinter(indent = 4)

w3 = Web3(HTTPProvider('http://127.0.0.1:7545'));


def init():
   # abi = '[{'stateMutability': 'nonpayable', 'type': 'function', 'payable': False, 'inputs': [{'type': 'string', 'name': '_greeting'}], 'outputs': [], 'constant': False, 'name': 'setGreeting'}, {'stateMutability': 'view', 'type': 'function', 'payable': False, 'inputs': [], 'outputs': [{'type': 'string', 'name': ''}], 'constant': True, 'name': 'greet'}, {'stateMutability': 'view', 'type': 'function', 'payable': False, 'inputs': [], 'outputs': [{'type': 'string', 'name': ''}], 'constant': True, 'name': 'greeting'}, {'stateMutability': 'nonpayable', 'inputs': [], 'payable': False, 'type': 'constructor'}]'
    # contract = w3.eth.contract(address='0x99E6EE18a8064aEf39e7fD87686458a9Ec5d0571')
    # print(contract.functions.__str__())
    printed = w3.eth.blockNumber
    while(True):
        time.sleep(1)
        while printed < w3.eth.blockNumber:
            printed+=1
            print("RECEIVED BLOCK "+str(printed))
            block_received(printed)

def process_transaction(transaction):
    #print("Processing t")
    #pp.pprint(transaction)
    #ascii = Web3.toAscii(transaction.input)
    print(transaction)

def block_received(block_number):
    block = w3.eth.getBlock(block_number);
    print(block)
    for i in range(0, len(block.transactions)):
        print("Processing Transaction "+ str(i)+ " from block "+str(block_number))
        process_transaction(w3.eth.getTransactionFromBlock(block.number, i))

init();