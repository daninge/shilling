pragma solidity ^0.4.17;

contract StorageProof {
    address public client;
    address public storer;
    uint public fileId;
    uint public challenge;

    bytes proof;

    function StorageProof(address clientIn, address storerIn, uint fileIdIn, uint challengeIn) public {
        client = clientIn;
        storer = storerIn;
        fileId = fileIdIn;
        challenge = challengeIn;
    }

    function getClient() view public returns (address) {
        return client;
    }

    function getStorer() view public returns (address) {
        return storer;
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