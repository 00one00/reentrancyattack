from brownie import EtherStore, network, accounts
from scripts.helpful_scripts import get_account, deposit_value, TESTNET_ENVIRONMENTS


def assert_contract_is_deployed():
    # Get appropriate account
    if network.show_active() in TESTNET_ENVIRONMENTS:
        account = get_account(id="metamask-goerli")
    else:
        account = accounts[0]
    # Assert EtherStore is deployed
    if len(EtherStore) >= 1:
        print("Fetching deployed contract")
        EtherStore[-1]
    else:
        print("Deploying EtherStore...")
        EtherStore.deploy({"from": account})
    print("EtherStore deployed")


def owner_fund_contract():
    # Get appropriate account
    if network.show_active() in TESTNET_ENVIRONMENTS:
        account = get_account(id="metamask-goerli")
    else:
        account = accounts[0]
    try:
        # Fetch deployed EtherStore
        ether_store = EtherStore[-1]
        try:
            # If sufficient funds deposit to EtherStore
            print(f"{account.address} depositing funds to contract...")
            ether_store.deposit({"value": deposit_value, "from": account})
            print("Deposit successful")
        except:
            ValueError
            print("Insufficient funds")
    except:
        print("Contract not deployed")


def client1_fund_contract():
    """
    Client1 interacting with the contract. Each client represents a victim to the attack
    """
    # Get appropriate account
    if network.show_active() in TESTNET_ENVIRONMENTS:
        account = get_account(id="test_acct_2")
        if len(EtherStore) > 0:
            # Fetch deployed EtherStore
            ether_store = EtherStore[-1]
            try:
                # If sufficient funds deposit to EtherStore
                print(f"{account.address} depositing funds to contract...")
                ether_store.deposit({"from": account, "value": deposit_value})
                print(f"Contract successfully funded by {account.address}")
            except:
                ValueError
                print("Insufficient funds")
        else:
            print("Please deploy contract using the deploy_ether_store function")
    else:
        account = accounts[1]
    try:
        ether_store = EtherStore[-1]
        ether_store.deposit({"from": account, "value": deposit_value})
    except:
        IndexError
        print("Please deploy contract using the deploy_ether_store function")


def client2_fund_contract():
    """
    Client2 interacting with the contract. Each client represents a victim to the attack
    """
    # Get appropriate account
    if network.show_active() in TESTNET_ENVIRONMENTS:
        account = get_account(id="test_acct_3")
        if len(EtherStore) > 0:
            # Fetch deployed EtherStore
            ether_store = EtherStore[-1]
            ether_store.deposit({"from": account, "value": deposit_value})
            print(f"Contract successfully funded by {account.address}")
        else:
            print("Please deploy contract using the deploy_ether_store function")
    else:
        account = accounts[1]
    try:
        # Assert EtherStore on development chain
        ether_store = EtherStore[-1]
        try:
            # If sufficient funds deposit to EtherStore
            print(f"{account.address} depositing funds to contract...")
            ether_store.deposit({"from": account, "value": deposit_value})
            print(f"Contract successfully funded by {account.address}")
        except:
            ValueError
            print("Insufficient funds")
    except:
        IndexError
        print("Please deploy contract using the deploy_ether_store function")


def main():
    assert_contract_is_deployed()
    owner_fund_contract()
    client1_fund_contract()
    client2_fund_contract()
