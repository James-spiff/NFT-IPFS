from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import get_breed, get_account, OPENSEA_URL

dog_metadata_dict = {
    "PUG": "https://ipfs.io/ipfs/QmUsQYZiss6trnbbFyvb8X7Rcn59ukp76BVduehBKTMbDN?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmeN438cbxLEjGFPdLt8f9mvDFvKGSpeVPLSDnk4KBam5J?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUaKthjKkBpvZKkpA9tMi1BFb4QnvpbBUkxCKqGyFoXfw?filename=2-ST_BERNARD.json"
}

def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id)) 
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dict[breed])


#Here we make our NFT visible in an NFT marketplace   
def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(f"NFT deployed! You can now view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}")
    print("Please wait up to 20 minutes and hit the refresh metadata button")