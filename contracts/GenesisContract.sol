pragma solidity ^0.4.17;

contract GenesisContract {
    address[] available_contracts;

    function getAvailableContracts() public view returns (address[]){
        return available_contracts;
    }

    function submitContract(address a) public {
        available_contracts.push(a);
    }
}