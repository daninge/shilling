pragma solidity ^0.4.17;

contract RequestStorageContract {
    address public requestor;
    address public storer;
    uint public fileId;

    address[] proofs;

    function RequestStorageContract(address requestorIn, uint fileIdIn) public {
        requestor = requestorIn;
        fileId = fileIdIn;
    }

    function requestProof(address storageProof) public {
        proofs.push(storageProof);
    }

    function getRequestor() public view returns (address) {
        return requestor;
    }

    function getStorer() public view returns (address) {
        return storer;
    }

    function setStorer(address storerIn) public {
        storer = storerIn;
    }
    
    function getProofs() public view returns (address[]) {
        return proofs;
    }

    function getFileId() public view returns(uint) {
        return fileId;
    }

}