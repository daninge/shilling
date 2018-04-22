pragma solidity ^0.4.17;

contract StorageProof {
    address public requestor;
    address public storer;
    uint public fileId;
    uint public c;
    uint public k1;
    uint public k2;
    uint public gs;
    uint public N;
    uint public g;

    bytes proof;

    function StorageProof(address storerIn, uint fileIdIn, uint cIn, uint k1In, uint k2In, uint gsIn, uint NIn, uint gIn) public {
        requestor = msg.sender;
        storer = storerIn;
        fileId = fileIdIn;
        c = cIn;
        k1 = k1In;
        k2 = k2In;
        gs = gsIn;
        N = NIn;
        g = gIn;
    }

    function getStorer() view public returns (address) {
        return storer;
    }

    function getRequestor() view public returns (address) {
        return requestor;
    } 

    function getChallenge() view public returns (uint, uint, uint, uint, uint, uint) {
        return (c, k1, k2, gs, N, g);
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