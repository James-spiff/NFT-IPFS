//SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol"; //to get a random number

//Here we make an NFT contract where the token URI can be one of 3 different dog images it will be randomly selected

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD} //the 3 different breed of dogs a user can randomly get
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;
    //it is considered best practice to emit an event whenever we update a mapping
    event requestedCollectible(bytes32 indexed requestId, address requester); //requestId is indexed so we can easily search for the event
    event breedAssigned(uint256 indexed tokenId, Breed dog_breed);

    constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public VRFConsumerBase(_vrfCoordinator, _linkToken) ERC721("Dogo", "DOG") {
        tokenCounter = 0;   //tokenCounter counts all the tokens you have deployed under this contract
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee); //creates our randomness requeest to get a random breed from our dogs
        requestIdToSender[requestId] = msg.sender; //a mapping that keeps track of the sender in order for us to use it in our fulfillRandomness function
        //emit event after we update a mapping
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        Breed dog_breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = dog_breed; //set's the token id to our randomly selected dog
        //emit event after we update a mapping
        emit breedAssigned(newTokenId, dog_breed);
        //by default in this our msg.sender isn't the user but instead the VRFCoordinator for us to acces the user we have to store a mapping of users in our createCollectible function
        address owner = requestIdToSender[requestId]; //get's the user's address from the mapping we created 
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    //_setTokenURI(newTokenId, tokenURI); //allows our NFT to have an image assosiated with it
    //To be able to randomly select a tokenURI we need to create a setTokenURI function that adapts the one provided by the ERC721 protocol
    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        //only the owner of the tokenId can update the tokenURI
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not owner or approved"); //_isApprovedOrOwner is an openZeppelin function that checks if an address is an owner or approved
        _setTokenURI(tokenId, _tokenURI);
    }
}

