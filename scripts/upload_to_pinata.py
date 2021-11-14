import os
from pathlib import Path
import requests
#pinata is an ipfs file management system they help you pin your files on their node so it's always available via ipfs
# if we used our system as a node then whenever our system is down our file becomes unavailable
PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS" 
filepath = "./images/pug.png"
filename = filepath.split('/')[-1]
#http headers for the post request
headers = {"pinata_api_key": os.getenv("PINATA_API_KEY"), "pinata_secret_api_key": os.getenv("PINATA_API_SECRET")}

#we can swap this with our upload to ipfs function in create metadata 
def main():
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(PINATA_BASE_URL + endpoint, files={"file": (filename, image_binary)}, headers=headers)
        print(response.json())