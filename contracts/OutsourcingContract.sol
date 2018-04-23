pragma solidity ^0.4.17;

contract OutsourcingContract {
    address public requestor;
    address public provider;
    uint public fileId;

    bytes proof;

    function OutsourcingContract(address requestorIn, uint fileIdIn) public {
        requestor = requestorIn;
        fileId = fileIdIn;
    }

    function setRequestor(address rin) public {
        requestor = rin;
    }

    function requestProof(bytes storageProof) public {
        proof = storageProof;
    }

    function getRequestor() public view returns (address) {
        return requestor;
    }
    
    function getProof() public view returns (bytes) {
        return proof;
    }

    function getFileId() public view returns(uint) {
        return fileId;
    }

}