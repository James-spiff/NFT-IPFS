from brownie import (
    accounts, 
    network, 
    config,
    interface,
    LinkToken,
    MockV3Aggregator,
    VRFCoordinatorMock,
    Contract,
)
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "ganache"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"    #takes in the contract address and the token Id in the placeholders

BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}

def get_breed(breed_number):
    return BREED_MAPPING[breed_number]  #we use this function in our create_metadata to get the breed from the token_id

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


contracts_to_mock = {
    "link_token": LinkToken,
    "vrf_coordinator": VRFCoordinatorMock,
}

def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config if defined otherwise,
    it will deploy a mock version of the contract and return the mock contract.
        Args:
            contract_name (string)
        returns:
            The most recently deployed version of this contract.
    
    """

    contract_type = contracts_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract


def deploy_mocks(decimals=18, initial_value=2000):
    """
    Use this script if you want to deploy mocks to a testnet
    """
    account = get_account()
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("Deploying Mock VRF Coordinator...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRF Coordinator deployed to {vrf_coordinator.address}")


def fund_with_link(contract_address, account=None, link_token=None, amount=Web3.toWei(1, 'ether')):
    account = account if account else get_account() #if an account isn't passed as an argument use the get_account function
    link_token = link_token if link_token else get_contract("link_token")
    funding_tx = interface.LinkTokenInterface(link_token).transfer(contract_address, amount, {"from": account})
    funding_tx.wait(1)
    print(f"Funded {contract_address}")
    return funding_tx