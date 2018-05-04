pragma solidity ^0.4.17;

contract OutsourcingContract {
    address public requestor;
    address public provider;
    uint public fileId;
    address public proofAddress;

    function OutsourcingContract(address requestorIn, uint fileIdIn, address proofAddressIn) public {
        requestor = requestorIn;
        fileId = fileIdIn;
        proofAddress = proofAddressIn;
    }
    
    function setProvider(address pIn) public {
        provider = pIn;
    }

    function getProvider() public view returns (address) {
        return provider;
    }

    function setRequestor(address rin) public {
        requestor = rin;
    }

    function getRequestor() public view returns (address) {
        return requestor;
    }

    function getProofAddress() public view returns (address) {
        return proofAddress;
    }

    function getFileId() public view returns(uint) {
        return fileId;
    }

}