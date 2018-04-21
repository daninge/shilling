pragma solidity ^0.4.17;

contract StorageProof {
    address public requestor;
    address public storer;
    uint public fileId;
    uint public c;
    uint public k1;
    uint public k2;
    uint public gs;

    bytes proof;

    function StorageProof(address storerIn, uint fileIdIn, uint cIn, uint k1In, uint k2In, uint gsIn) public {
        requestor = msg.sender;
        storer = storerIn;
        fileId = fileIdIn;
    }

    function getStorer() view public returns (address) {
        return storer;
    }

    function getRequestor() view public returns (address) {
        return requestor;
    } 

    function getChallenge() view public returns (uint, uint, uint, uint) {
        return (c, k1, k2, gs);
    }

    function getProof() view public returns (bytes) {
        return proof;
    }

    function getFileId() view public returns (uint) {
        return fileId;
    }

    function submitProof(bytes proofIn) public {
        proof = proofIn;
    }
}