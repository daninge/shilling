pragma solidity ^0.4.17;

contract StorageProof {
    address public requestor;
    address public storer;
    uint public fileId;
    uint public challenge;

    bytes proof;

    function Migrations(address storerIn, uint fileIdIn) public {
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

    function getChallenge() view public returns (uint) {
        return challenge;
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