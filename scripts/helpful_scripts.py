from brownie import accounts, network, config
from web3 import Web3

# Development environments that are torn down once script is finished executing
# You will not be able to see these transactions on etherscan
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["ganache-local", "development"]
# Forked mainnet environments
FORKED_ENVIRONMENTS = ["mainnet-fork-dev", "mainnet-fork"]
# Testnet environments on blockchains that you can view from block explorers
TESTNET_ENVIRONMENTS = ["goerli", "kovan", "polygon-test", "ftm-test", "avax-test"]
development_environments = [LOCAL_BLOCKCHAIN_ENVIRONMENTS, FORKED_ENVIRONMENTS]

# Toggle these values if you wish to use different amounts of ether in your contracts
deposit_value = Web3.toWei(0.2, "ether")
withdraw_value = Web3.toWei(0.2, "ether")

convert_from_wei = Web3.fromWei(deposit_value, "ether")

# account index = accounts[0], accounts[1]...
# account id = accounts imported into brownie using $ brownie accounts new "account name"
def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in development_environments:
        return accounts[0]
    # To use your own wallet without needing a password for every execution
    # you will need to add your private key into .env file
    return accounts.add(config["wallets"]["from_key"])
