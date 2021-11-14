from brownie import config, network, SimpleCollectible
from scripts.helpful_scripts import get_account

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"    #takes in the contract address and the token Id in the placeholders

def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(f"NFT successfully deployed you can view it on: {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}")  #simple_collectible.tokenCounter() - 1 get's us the current token id
    print("Please wait up to 20 minutes and hit the refresh metadata button.")
    return simple_collectible #This will be used in our unittest


def main():
    deploy_and_create()