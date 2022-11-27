# Protect against a re-entrancy attack

Disclaimer: This program is only intended for educational purposes on how to safe-guard your smart contracts from re-entrancy attacks. Hacking with the intent of stealing money is illegal and unethical.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [API keys](#api-keys)
* [Brownie accounts setup](#brownie-accounts-setup)
* [How to use](#how-to-use)
* [EtherStore](#ether-store)
* [EtherStoreAttack](#ether-store-attack)
* [Protecting against re-entrancy attacks](#protecting-against-re-entrancy-attacks)
* [SafeStore](#safe-store)
* [SafeStoreAttack](#safe-store-attack)
* [Withdrawing funds from the contracts](#withdrawing-funds-from-the-contracts)

* [Links](#links)


## General info
This directory consists of two sets of contracts with each set containing two contracts of their own (a total of 4 contracts).
Set A contains contracts B and C where contract B(EtherStore) is a contract containing a vulnerability to a re-entrancy attack and contract C(EtherStoreAttack) exploits that vulnerability.
Set D contains contracts E and F where contract E(SafeStore) fixes the vulnerability that contract B contains and contract F(SafeStoreAttack) attempts to exploit E but fails.


## Technologies
Project is created with:
* pipx 1.1.0
* Solidity 0.8.13
* Python 3.11
* Brownie 1.19.0
* Web3py v5


## Setup
To run this project:

Download Python:

If you don't have Python installed on your machine, click the Python/downloads link provided in the links section and follow the prompts.

Download brownie:

Once you have Python installed on your machine you will need to install the Brownie development framework: a Python-based development and testing framework for smart contracts targeting the Ethereum Virtual Machine.
You can follow the instructions provided in the brownie documentation which is also in the "Links" section.

Since brownie needs pipx to be installed, start by installing pipx by running the two following commands in your terminal:

  $ python3 -m pip install --user pipx
  
  $ python3 -m pipx ensurepath

Note: You may need to restart your terminal after installing pipx

To install Brownie using pipx:

  $ pipx install eth-brownie

Once installation is complete, type brownie to verify that it worked:

  $ brownie

Brownie - Python development framework for Ethereum
Usage:  brownie <command> [<args>...] [options <args>]

Finally, install the web3py library if you haven't already. This installation is optional since we are only using the library to convert balances into a more readable format. Although it is optional, you will need to delete or comment out the lines of code utilizing this library if you choose not to run web3py.

  $ pip install web3


## API keys

You will need an API key to verify the contract on etherscan. If you do not wish to verify the contract go to the brownie-config.yaml file and under "networks" "goerli" change the True boolean to False
If you do wish to verify the contracts then follow the instructions in the etherscan docs which is provided in the links below.

Once you have the etherscan API key, the last API key you need is one that enables you to connect to an ethereum node. A node will allow you to talk to the blockchain through your scripts.
You can run your own node, but this option is often costly and time consuming. The easiest way is to use a third party service. The two most popular services are infura and alchemy, which I will provide links on API setup in the links below.

Note: When setting up your API key make sure to get the goerli testnet API and not the mainnet API.
You will not be able to deploy to the goerli testnet without a node API from infura or alchemy

Create a .env file and on the first line type:

* If you are using an Infura API: 
  
  export WEB3_INFURA_PROJECT_ID=<project_id>

* Or if you are using an Alchemy API: 
  
  export WEB3_ALCHEMY_PROJECT_ID=<project_id>

Then enter your etherscan API if you chose to verify your contracts:

  export ETHERSCAN_TOKEN=<etherscan_api>

Once finished, in your terminal type:

  $ source .env

## Brownie accounts setup

If you are running on a testnet or mainnet and want to utilize the get_account
function in helpful_scripts, you will need to make four of your own custom accounts within the brownie framework.
In your terminal run:

  $ brownie accounts new "Name of new account"
  
Note: You can name your accounts under the same names used in the scripts "metamask-goerli", "test_acct_2", "test_acct_3"... or name the accounts whatever you'd like. Just keep in mind that if you use a different name while creating these accounts you will need to go through and edit the names in each one of the scripts to whatever names you have chosen since brownie will not know what "metamask-goerli" is.

You will then be prompted to enter the accounts seed phrase followed by a password. If you are using metamask: You will first need to switch to the goerli network. To do this, ensure your metamask shows testnet networks by going to metamask Settings > Advanced and then toggling the "Show test networks" option. Once you have done that switch from "ethereum mainnet" at the top of your metamask dropdown and choose "goerli test network".

Next, create a new account: you can do this by opening your metamask extension and clicking the circle at the top right and then clicking on "create new account" and follow the prompts. You will need to create 4 seperate accounts. If you need more detail the link is included below. 

Since brownie requires you to enter your private key into the terminal to create new, secure accounts you will need to export the private key of each account by clicking the 3 vertical dots on the top right of the dropdown and then choose "account details". Next, hit "export private key". You will then be prompted to enter your metamask password. 
  
Finally, copy and paste the private key into your terminal. More details on exporting metamask private keys are also included in the links below.

Once you have created all four brownie accounts you can check them by running:

  $ brownie accounts list

If you have any problems with this step I have provided the link below to the brownie accounts documentation.


## How to use
The configuration file defaults us to automatically deploy to a development testnet, which you cannot view on etherscan and the transactions and history will be torn down as soon as the script is finished running. If you are looking to deploy to an actual testnet you will need to either set the default network in brownie-config.yaml to "goerli" or use the network flag in your terminal when running a script. If you are using goerli you will need goerli testnet eth, you can acquire this eth from a faucet for free, which i will provide the link to in the links section. If you do not have at least 0.8 goerli eth (0.2 goerli eth per test wallet) then you can change the amount to deposit and withdraw from the contracts in scripts/helpful_scripts.py - the amount can be as little as 0.02 goerli eth. Note the amounts should be the same for deposit_value and withdraw_value.

If you want to run on the default development network simply leave out the "--network goerli" flag.

Once you have the appropriate technologies installed on your machine, have four custom ID accounts added into brownie, have goerli eth and an API key set up from etherscan you're now ready to run the scripts so you can see first hand how smart contracts can be vulnerable to re-entrancy attacks and how you can guard against those attacks.

### EtherStore

EtherStore is the first contract we are going to deploy, it is the contract with the faulty code that leaves us susceptible to attacks.

Deploy this contract onto the goerli testnet by typing into your terminal:

  $ brownie run scripts/deploy_ether_store.py --network goerli

Again, if you want to run on the default development network simply leave out "--network goerli".

Now that the contract is deployed you need to fund it with the accounts you created by running:

  $ brownie run scripts/fund_ether_store.py --network goerli
  
Note: You can view your contract on the etherscan block explorer if you are using the goerli testnet. In your terminal you will see a print statement "EtherStore deployed to 'address'", copy the address, go to goerli.etherscan.io and paste the contract address into the search bar at the top. You will be able to view all transactions that happen within that contract, and once the attack is carried out you can investigate what happened under "Internal Txns". You can also view individual transactions.
  
This script is doing a few things: checking to see if the contract has already been deployed and if not it will deploy the contract for you. Next, it is funding the account through the contract owner (because they want to play too) and finally it is being funded by two innocent victims that have no idea what is about to happen. These will be the funds that are stolen.

Sweet! You have deployed a smart contract and have "clients" who have funded the contract and it is being utilized just as it was intended. What could go wrong? Run the attacker script to find out!

### EtherStoreAttack

To deploy EtherStoreAttack run:

  $ brownie run scripts/attack_ether_store.py --network goerli

This is where the meat and potatoes is. Here, we are deploying the contract(EtherStoreAttack) that will be targeting EtherStore with the goal of completely draining all of the funds out of it.
Once the attack contract is deployed the script will call the attack function that is written in the smart contract and then finally calling the withdraw function to get the funds out of EtherStoreAttack and into the attackers personal wallet.

* If you need to withdraw funds without using the attack_ether_store script run:
  
  $ brownie run scripts/withdraw_ether_store.py --network goerli

### Protecting against re-entrancy attacks

The contract that protects against the potential threats is essentially the same contract with a few minor updates:
* Within the withdraw function of the contract the users balance is updated before the function is actually executed. Therefore an attacker can't continuously call the same function over and over before it has been completed.
* Lastly, we have added a modifier to tack onto the withdraw function so that it locks the function from being called multiple times during its execution, which is what a re-entrancy attack is. In our case this modifier is called noReentrant.
Either one of these steps alone will work just fine but it is better to be extra diligent when it comes to handling other people's money.

### SafeStore

To deploy the upgraded anti-reentrancy contract, run:

  $ brownie run scripts/deploy_safe_store.py --network goerli

Fund the contract using the contract owner along with a couple of clients:

  $ brownie run scripts/fund_safe_store.py --network goerli

### SafeStoreAttack
  
Next, we will attempt to attack SafeStore and if it works as it should we will get a print statement letting us know that the attack has been reverted:

  $ brownie run scripts/attack_safe_store.py --network goerli

If the last line of your terminal is showing
"Funds still in SafeStore contract use withdraw script to get funds back"
then congratulations! You've just deployed a contract that is anti-reentrant and you can rest assured your users funds are safe and sound. 
  
### Withdrawing funds from the contracts

If you want your funds back after this test you will need to, well..use the withdraw script to get your funds back.
  
To withdraw funds from the SafeStore contract, run:

  $ brownie run scripts/withdraw_safe_store.py --network goerli
  
 If you want to withdraw funds from the EtherStore contract without carrying out the attack scripts, run:
  
  $ brownie run scripts/withdraw_ether_store.py --network goerli

All of the funds you used during this process should now be back in your wallet. But it is important to note that you should always play with free testnet eth on experiements like this and only deploy to mainnet when your app is ready to go into production.

I hope you found value in this and i am always open to feedback to improve my code: twitter @nonfungible_kid. If you would like to donate to my self-learning journey you can send eth to the address below. Good luck on your journey!
0x99F296Ff497E44f57ce58632652a2306e7Be4c3A


## Links
* Download Python:
  https://www.python.org/downloads/
  
* Install brownie framework:
  https://eth-brownie.readthedocs.io/en/stable/install.html
  
* Install web3py library:
  https://web3py.readthedocs.io/en/v5/quickstart.html
  
* Create custom accounts in brownie:
  https://eth-brownie.readthedocs.io/en/stable/core-accounts.html
  
* Create new accounts on metamask:
  https://metamask.zendesk.com/hc/en-us/articles/360015289452-How-to-create-an-additional-account-in-your-wallet
  
* Export metamask private key:
  https://metamask.zendesk.com/hc/en-us/articles/360015289632-How-to-export-an-account-s-private-key#:~:text=On%20the%20account%20page%2C%20click,click%20%E2%80%9CConfirm%E2%80%9D%20to%20proceed
  
* Goerli testnet eth faucet:
  https://goerlifaucet.com/
  
* Etherscan API key:
  https://docs.etherscan.io/getting-started/viewing-api-usage-statistics
  
* Get Alchemy API key to connect to node:
  https://docs.alchemy.com/docs/alchemy-quickstart-guide
  
* Get Infura API key to connect to node:
  https://docs.infura.io/infura/getting-started
  
* Etherscan block explorer for goerli testnet:
  https://goerli.etherscan.io
