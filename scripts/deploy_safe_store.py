from brownie import SafeStore, network, config, accounts
from scripts.helpful_scripts import get_account, TESTNET_ENVIRONMENTS


def deploy_contract():
    # Get appropriate account to deploy from. This will be the contract owner
    if network.show_active() in TESTNET_ENVIRONMENTS:
        account = get_account(id="metamask-goerli")
        print("Deploying SafeStore to testnet...")
    else:
        account = accounts[0]
        print("Deploying SafeStore to development network...")
    safe_store = SafeStore.deploy(
        {"from": account},
        # Verify the contract on etherscan if on Goerli
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"SafeStore deployed to {safe_store.address}")


def main():
    deploy_contract()
