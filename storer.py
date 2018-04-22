from web3 import Web3, HTTPProvider
import time
import setup as s
import pdp
import json

w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

IS_OUTSOURCING_PROOFS = False

file = [1234, 5678, 9101, 1213, 1234, 4321, 5678]

def get_tags(file_id):
    f = open(str(file_id)+"-tags.txt", 'r')
    tags = f.read()
    return json.loads(tags)

def get_data(file_name, challenge_block):
    return file[challenge_block]
    #return f.read()
    
def prove (address):
    print("prove")
    print(address)
    proof_request_contract = s.get_contract_instance(w3, address, "StorageProof")
    c, k1, k2, ss, N, g  = proof_request_contract.getChallenge()
    file_id = proof_request_contract.getFileId()
    #challege_data = get_data(file_id, challenge)
    challenge_blocks = pdp.get_challenge_blocks(k1, c, len(file))
    print("challenge blocks")
    print(challenge_blocks)
    data = []
    for index in challenge_blocks:
        data.append(get_data(60, index))

    #if proofs should be outsourced
    if IS_OUTSOURCING_PROOFS:
        print("is outsourcing proofs")
        #do shit here
    
    #generate proof here
    print("PROOF")
    print(pdp.gen_proof((N,g), len(file), (c, k1, k2, (g ** ss)), get_tags(60)))
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
    print(proof_request_list)
    if len(proof_request_list) > num_proofs_so_far:
        print("proof requested at address"+str(num_proofs_so_far))
        print(get_tags(60))
        prove(proof_request_list[num_proofs_so_far])
        num_proofs_so_far += 1
        print("proof successful, waiting for more proof requests")
        assert(False)


