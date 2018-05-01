pragma solidity ^0.4.17;

contract GenesisContract {
    address available_contract;
    address outsourcing_contract;

    function submitOutsourcingContract(address a) public{
        outsourcing_contract = a;
    }

    function getOutsourcingContract() public returns (address) {
        address to_return = outsourcing_contract;

        return to_return;
    }

    function submitContract(address a) public{
        available_contract = a;
    }

    function getContract() public returns (address) {
        address to_return = available_contract;
        return to_return;
    }
}