from brownie import network
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest 
from scripts.simple_collectible.deploy_and_create import deploy_and_create

def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #Arrange/Act
    simple_collectible = deploy_and_create()
    #Assert
    assert simple_collectible.ownerOf(0) == get_account()
    
