pragma solidity ^0.4.17;

contract RequestStorageContract {
    address public requestor;
    address public storer;
    uint public fileId;

    address[] proofs;

    function RequestStorageContract(address requestorIn, address storerIn, uint fileIdIn) public {
        requestor = requestorIn;
        storer = storerIn;
        fileId = fileIdIn;
    }

    function requestProof(address storageProof) public {
        proofs.push(storageProof);
    }

    function getProofs() public view returns (address[]) {
        return proofs;
    }

    function getFileId() public view returns(uint) {
        return fileId;
    }

}