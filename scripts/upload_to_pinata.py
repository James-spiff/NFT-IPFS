from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
import os
from pathlib import Path
import requests
import json 
#pinata is an ipfs file management system they help you pin your files on their node so it's always available via ipfs
# if we used our system as a node then whenever our system is down our file becomes unavailable
# PINATA_BASE_URL = "https://api.pinata.cloud/"
# endpoint = "pinning/pinFileToIPFS" 
# filepath = "./images/shiba-inu.png"
# filename = filepath.split('/')[-1]
# #http headers for the post request
# headers = {"pinata_api_key": os.getenv("PINATA_API_KEY"), "pinata_secret_api_key": os.getenv("PINATA_API_SECRET")}

#we can swap this with our upload to ipfs function in create metadata 
def main():
    # with Path(filepath).open("rb") as fp:
    #     image_binary = fp.read()
    #     response = requests.post(PINATA_BASE_URL + endpoint, files={"file": (filename, image_binary)}, headers=headers)
    #     print(response.json())
    upload_to_pinata()


#("metadata", metadata)
#To get better descriptions and stats create a file with them in it and call them by the breed name
def upload_to_pinata():
    PINATA_BASE_URL = "https://api.pinata.cloud/"
    endpoint = "pinning/pinFileToIPFS"
    headers = {"pinata_api_key": os.getenv("PINATA_API_KEY"), "pinata_secret_api_key": os.getenv("PINATA_API_SECRET")}
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        filepath = f"./images/{breed}.png"
        filename = filepath.split("/")[-1]
        metadata_path_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        metadata_filename = metadata_path_name.split("/")[-1]
        collectible_metadata = metadata_template
        collectible_metadata["name"] = breed
        collectible_metadata["description"] = "A thicc boi"


        with Path(filepath).open("rb") as fp:
            image_binary = fp.read()

        if Path(metadata_path_name).exists():
            print(f"{metadata_path_name} already exists! Delete it to overwrite")
        else:
            with open(metadata_path_name, 'w') as file:
                json.dump(collectible_metadata, file)
        
        with Path(metadata_path_name).open("rb") as fp:
            meta_binary = fp.read()
        
        response = requests.post(PINATA_BASE_URL + endpoint, files={"file": (filename, image_binary), "file": (metadata_filename, meta_binary)}, headers=headers)
        print(response.json())

#After this we upload it to an NFT marketplace like OpenSea in set_tokenuri.py
