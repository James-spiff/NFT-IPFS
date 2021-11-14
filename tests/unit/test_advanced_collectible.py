from brownie import network
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
import pytest 
from scripts.advanced_collectible.deploy_and_create import deploy_and_create

def test_can_create_advanced_collectible():
    #Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #Act
    advanced_collectible, creation_tx = deploy_and_create()
    requestId = creation_tx.events["requestedCollectible"]["requestId"]    #an event we emitted in our smart contract
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": get_account()}
    )   #777 is just a random number
    #Assert
    assert advanced_collectible.tokenCounter() > 0
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3  #checks if the random number we generted for dogs is correct
