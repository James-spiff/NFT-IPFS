from brownie import network
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
import pytest 
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import time

def test_can_create_advanced_collectible_integration():
    #Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #Act
    advanced_collectible, creation_tx = deploy_and_create()
    time.sleep(60)
    
    #Assert
    assert advanced_collectible.tokenCounter() > 0

