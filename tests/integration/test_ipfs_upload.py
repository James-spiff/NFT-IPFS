from brownie import config, AdvancedCollectible, network
from scripts.advanced_collectible.create_metadata import upload_to_ipfs
from scripts.helpful_scripts import get_breed

dog_image_dict = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png"
} 

dog_metadata_dict = {
    "PUG": "https://ipfs.io/ipfs/QmUsQYZiss6trnbbFyvb8X7Rcn59ukp76BVduehBKTMbDN?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmeN438cbxLEjGFPdLt8f9mvDFvKGSpeVPLSDnk4KBam5J?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUaKthjKkBpvZKkpA9tMi1BFb4QnvpbBUkxCKqGyFoXfw?filename=2-ST_BERNARD.json"
}

def test_ipfs_upload():
    #Arrange
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    #Act
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        image_path = "./images/" + breed.lower().replace("_", "-") + ".png"
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        image_uri = upload_to_ipfs(image_path)
        metadata_uri = upload_to_ipfs(metadata_file_name)
        #Assert
        assert image_uri in dog_image_dict[breed]
        assert metadata_uri in dog_metadata_dict[breed]   