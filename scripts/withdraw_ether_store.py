from brownie import accounts, network, EtherStore
from scripts.helpful_scripts import (
    get_account,
    deposit_value,
    withdraw_value,
    TESTNET_ENVIRONMENTS,
)


def withdraw_funds():
    """
    Use this function only if you want to withdraw funds manually through
    client addresses and not using the Attacker contract to do so
    """
    # Get all accounts with potential funds on contract
    if network.show_active() in TESTNET_ENVIRONMENTS:
        account_owner = get_account(id="metamask-goerli")
        account2 = get_account(id="test_acct_2")
        account3 = get_account(id="test_acct_3")
        # Fetch deployed EtherStore contract
        ether_store = EtherStore[-1]
        print("Withdrawing from testnet contract...")
        # The following try except blocks check if each account has funds on contract
        # if they do it will withdraw the available funds back into the account
        try:
            ether_store.withdraw({"from": account_owner})
            print(f"{account_owner.address} withdraw successful")
        except:
            print(f"Insufficient amount for withdraw from {account_owner.address}")
        try:
            ether_store.withdraw({"from": account2})
            print(f"{account2} withdraw successful")
        except:
            print(f"Insufficient amount for withdraw from {account2.address}")
        try:
            ether_store.withdraw({"from": account3})
            print(f"{account3} withdraw successful")
        except:
            print(f"Insufficient amount for withdraw from {account3.address}")
        print("Available funds successfully withdrawn")
    else:  # development environments
        account = accounts[0]
        ether_store = EtherStore.deploy({"from": account})
        print("Depositing funds to EtherStore...")
        ether_store.deposit({"value": deposit_value, "from": account})
        print("Deposit successful")
        print("Withdrawing funds from EtherStore...")
        ether_store.withdraw({"from": account})
        print("Withdraw successful")


def main():
    withdraw_funds()
