import setup as s

from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

genesis_id = w3.eth.accounts[0]

new = s.make_contract(w3, "GenesisContract")
tx_hash = new.constructor().transact(transaction={'from': genesis_id})
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
genesis_contract = s.get_contract_instance(w3, receipt['contractAddress'], "GenesisContract")

f= open("genesis_address.txt","w+")
f.write(receipt['contractAddress'])