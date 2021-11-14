from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_account, get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json

#we want to create the metadata for all our tokens
def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))  #get's the id reps breed from our smart contract
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"  #file name of the metadata which is in a folder named after the network we are on e.g rinkeby and has a name consisting of the token_id and breed
        #print(metadata_file_name)
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating metadata file {metadata_file_name}")
            #filling up the metadata
            collectible_metadata["name"] = breed 
            collectible_metadata["description"] = f"A chubby {breed}"
            #print(collectible_metadata)
            image_path = "./images/" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_path)  #uploads our image_uri to ipfs
            collectible_metadata["image"] = image_uri
            #dump collectible_metadata into it's own file
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_file_name)  #this uploads our file metadata to ipfs


    #function that uploads our image to IPFS
def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:   #rb: read binary used for image files
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"  #gotten from the ipfs command line
        endpoint = "/api/v0/add"    #the api end point for the post request
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})   #we send a post request with the url and our image file to ipfs
        ipfs_hash = response.json()["Hash"] #after we upload our image ipfs returns a hash as a response we use this hash in our image_uri to access our file metadata on ipfs
        filename = filepath.split("/")[-1:][0]  # this takes a string like "./images/PUG.png" and returns PUG.png
        #filename = filepath.split("/")[-1]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
