pragma solidity ^0.4.17;

contract GenesisContract {
    address available_contract;

    function submitContract(address a) public{
        // for(uint i = 0; i < 10; i++){
        //     if(available_contracts[i] == 0){
        //         available_contracts[i] =  a;
        //     }
        // }
        available_contract = a;
    }

    function getContract() public returns (address) {
        // for(uint i = 0; i < 10; i++){
        //     if(available_contracts[i] != 0){
        //         address to_return = available_contracts[i];
        //         available_contracts[i] = 0;
        //         return to_return;
        //     }
        // }
        return available_contract;
    }
}