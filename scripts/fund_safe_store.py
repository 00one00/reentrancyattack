from brownie import SafeStore, accounts, network
from scripts.helpful_scripts import (
    get_account,
    deposit_value,
    convert_from_wei,
    TESTNET_ENVIRONMENTS,
)
from web3 import Web3


def owner_fund_contract():
    # Get appropriate account
    if network.show_active() in TESTNET_ENVIRONMENTS:
        account = get_account(id="metamask-goerli")
        try:
            # Verify if SafeStore is deployed
            safe_store = SafeStore[-1]
            print(f"Depositing {convert_from_wei} ether to SafeStore...")
            try:
                # If sufficient funds deposit to SafeStore
                safe_store.deposit({"value": deposit_value, "from": account})
                print("Deposit successful")
            except:
                ValueError
                print("Insufficient funds")
        except:
            IndexError
            print("No contract deployed please run deploy function")
    else:
        # Development chain
        account = accounts[0]
        safe_store = SafeStore.deploy({"from": account})
        print(f"Depositing {convert_from_wei} ether to SafeStore...")
        safe_store.deposit({"value": deposit_value, "from": account})
        print("Deposit successful")


def client_fund_contract():
    # Get appropriate accounts
    if network.show_active() in TESTNET_ENVIRONMENTS:
        account1 = get_account(id="test_acct_2")
        account2 = get_account(id="test_acct_3")
        try:
            # Verify if SafeStore is deployed
            safe_store = SafeStore[-1]
        except:
            IndexError
            print("No contract deployed please run deploy function")
    else:
        # Development chain
        account1 = accounts[1]
        account2 = accounts[2]
        try:
            # Verify if SafeStore is deployed on development network
            safe_store = SafeStore[-1]
        except:
            IndexError
            print("No contract deployed please run owner_fund_contract function")
    # The following try except blocks check if accounts have sufficient funds to deposit
    # and proceed with the deposits to the contract
    try:
        print("Account 1 depositing funds to contract")
        safe_store.deposit({"value": deposit_value, "from": account1})
    except:
        ValueError
        print("Insufficient funds")
    try:
        print("Account 2 depositing funds to contract")
        safe_store.deposit({"value": deposit_value, "from": account2})
    except:
        ValueError
        print("Insufficient funds")
    # Once all deposits are complete check balance of SafeStore contract
    safe_store_balance = Web3.fromWei(safe_store.balance(), "ether")
    print(
        f"Available funds successfully deposited - Contract balance: {safe_store_balance} ether"
    )


def main():
    owner_fund_contract()
    client_fund_contract()
