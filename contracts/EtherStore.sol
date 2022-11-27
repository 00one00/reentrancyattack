// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

/* This contract is vulnerable to re-entrancy attacks.
It is a simple contract that allows users to deposit and withdraw funds.
The vulnerability lies within the withdraw function
where the user balance is not updated until after the transfer is complete.
This allows a bad actor to take advantage by depositing funds and then withdrawing 
those funds as a normal user would, except the attacker will run the function repeatedly
until all funds are drained from the contract.
*/

contract EtherStore {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint256 bal = balances[msg.sender];
        require(bal > 0);

        (bool sent, ) = msg.sender.call{value: bal}("");
        require(sent, "Failed to send ether");

        balances[msg.sender] = 0; // line responsible for exploit,
        // should be moved above function call
    }

    // Helper function to check the balance of this contract
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
