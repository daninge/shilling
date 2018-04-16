from web3 import Web3, HTTPProvider
import time
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'));


def init():
    printed = w3.eth.blockNumber;
    while(True):
        time.sleep(1)
        while printed < w3.eth.blockNumber:
            printed+=1
            print("RECEIVED BLOCK "+str(printed))
            block_received(printed)

def process_transaction(transaction):
    #print("Processing t")
    print(transaction)

def block_received(block_number):
    block = w3.eth.getBlock(block_number);
    #print(block)
    for i in range(0, len(block.transactions)):
        print("Processing Transaction "+ str(i)+ " from block "+str(block_number))
        process_transaction(w3.eth.getTransactionFromBlock(block, i))

init();