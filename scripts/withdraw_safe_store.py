from brownie import SafeStore, network, accounts
from scripts.helpful_scripts import (
    get_account,
    deposit_value,
    withdraw_value,
    TESTNET_ENVIRONMENTS,
)


def withdraw():
    if network.show_active() in TESTNET_ENVIRONMENTS:
        # Get all accounts with potential funds on contract
        account_owner = get_account(id="metamask-goerli")
        account2 = get_account(id="test_acct_2")
        account3 = get_account(id="test_acct_3")
        account4 = get_account(id="test_acct_4")
        # Fetch deployed EtherStore contract
        safe_store = SafeStore[-1]
        print("Withdrawing from testnet contract...")
        # The following try except blocks check if each account has funds on contract
        # if they do it will withdraw the available funds back into the account
        try:
            safe_store.withdraw(withdraw_value, {"from": account_owner})
            print(f"{account_owner.address} withdraw successful")
        except:
            print(f"Insufficient amount for withdraw from {account_owner.address}")
        try:
            safe_store.withdraw(withdraw_value, {"from": account2})
            print(f"{account2} withdraw successful")
        except:
            print(f"Insufficient amount for withdraw from {account2.address}")
        try:
            safe_store.withdraw(withdraw_value, {"from": account3})
            print(f"{account3} withdraw successful")
        except:
            print(f"Insufficient amount for withdraw from {account3.address}")
        try:
            safe_store.withdraw(withdraw_value, {"from": account4})
            print(f"{account4} withdraw successful")
        except:
            print(f"Insufficient amount for withdraw from {account4.address}")
        print("Available funds successfully withdrawn")

    else:  # development environments
        account = accounts[0]
        safe_store = SafeStore.deploy({"from": account})
        print("Depositing funds to SafeStore...")
        safe_store.deposit({"value": deposit_value, "from": account})
        print("Deposit successful")
        print("Withdrawing funds from SafeStore...")
        safe_store.withdraw(withdraw_value, {"from": account})
        print("Withdraw successful")


def main():
    withdraw()
