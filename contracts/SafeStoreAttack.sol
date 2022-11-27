// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

import "./SafeStore.sol";

// This contract attempts to exploit SafeStore but will be reverted due to
// the safe guards set in place to prevent a re-entrancy attack
contract SafeStoreAttack {
    SafeStore public safeStore;
    address public owner;

    constructor(address _safeStoreAddress) {
        safeStore = SafeStore(_safeStoreAddress);
        owner = msg.sender;
    }

    // Fallback is called when EtherStore sends Ether to this contract.
    fallback() external payable {
        if (address(safeStore).balance >= 0.2 ether) {
            safeStore.withdraw(0.2 ether);
        }
    }

    function attack() external payable {
        require(msg.value >= 0.2 ether);
        safeStore.deposit{value: 0.2 ether}();
        safeStore.withdraw(0.2 ether);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "not contract owner");
        _;
    }

    function withdraw() public onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
    }

    // Helper function to check the balance of this contract
    function getAttackerBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
