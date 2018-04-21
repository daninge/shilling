pragma solidity ^0.4.17;

contract GenesisContract {
    address[10] available_contracts;

    function getAvailableContracts() public view returns (address[10]){
        return available_contracts;
    }

    function submitContract(address a) public returns (int){
        for(uint i = 0; i < 10; i++){
            if(available_contracts[i] == 0){
                available_contracts[i] = a;
                return 1;
            }
        }
        return -1;
    }

    function getContract() public returns (address) {
        if(available_contracts.length == 0){
            return 0;
        }
        address to_return = available_contracts[available_contracts.length - 1];
        delete available_contracts[available_contracts.length - 1];  
        return to_return;
    }
}