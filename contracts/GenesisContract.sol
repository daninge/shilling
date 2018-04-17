pragma solidity ^0.4.17;

contract GenesisContract {
    address[] available_contracts;

    function getAvailableContracts() public view returns (address[]){
        return available_contracts;
    }

    function submitContract(address a) public {
        available_contracts.push(a);
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