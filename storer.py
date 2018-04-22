from web3 import Web3, HTTPProvider
import time
import setup as s
import pdp

w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

IS_OUTSOURCING_PROOFS = False


def get_data(file_name, challenge_block):
    f = open("files/"+str(file_name)+".txt", r)
    return f.read()
    
def prove (address):
    proof_request_contract = s.get_contract_instance(w3, address, "StorageProof")
    challenge  = proof_request_contract.getChallenge()
    file_id = proof_request_contract.getFileId()
    challege_data = get_data(file_id, challenge)

    #if proofs should be outsourced
    if IS_OUTSOURCING_PROOFS:
        print("is outsourcing proofs")
        #do shit here
    
    #generate proof here
    print("generating a local proof")


#####################################################################
#Logic starts here

storer_id = w3.eth.accounts[0]

#Get the genesis contract
genesis_contract = s.get_contract_instance(w3, s.genesis_address, "GenesisContract")

print("Waiting for a contract:")

#print(genesis_contract.getAvailableContracts())

# print(s.genesis_address)

# print(genesis_contract.getContract())
#genesis_contract.submitContract(storer_id,transact={'from': storer_id})
#print(genesis_contract.getContract())
contract_address = genesis_contract.getContract()
while contract_address == None:
    print(genesis_contract.getContract())
    time.sleep(1)
    contract_address = genesis_contract.getContract()

print("Accepting storage contract at address "+str(contract_address))

#Get an instance of the contract at the accepted address
current_contract = s.get_contract_instance(w3, contract_address, "RequestStorageContract")
current_contract.setStorer(storer_id, transact={'from': storer_id})

#records the number of proofs we have submitted so far
num_proofs_so_far = 0

print("waiting for proof requests")
#respond to requests for proofs of storage
while True:
    print("waiting for proof requests")
    time.sleep(1)
    proof_request_list = current_contract.getProofs()
    print(current_contract.getProofs())
    if len(proof_request_list) > num_proofs_so_far:
        num_proofs_so_far += 1
        print("proof requested at address"+str(num_proofs_so_far))
        prove(proof_request_list[num_proofs_so_far])
        print("proof successful, waiting for more proof requests")


