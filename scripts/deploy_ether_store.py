from brownie import EtherStore, network, accounts, config
from scripts.helpful_scripts import get_account, TESTNET_ENVIRONMENTS


def deploy_ether_store():
    """
    Contract owner deploys contract
    """
    # Get appropriate account to deploy from. This will be the contract owner
    if network.show_active() in TESTNET_ENVIRONMENTS:
        account = get_account(id="metamask-goerli")
        print("Deploying EtherStore to testnet...")
    else:
        account = accounts[0]
        print("Deploying EtherStore to development network...")
    ether_store = EtherStore.deploy(
        {"from": account},
        # Verify the contract on etherscan if on Goerli
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"EtherStore deployed to {ether_store.address}")


def main():
    deploy_ether_store()
