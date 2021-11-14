//SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    constructor () public ERC721 ("Dogo", "DOG") { 
        tokenCounter = 0;
    }

    //this function creates/mints a new NFT whenever it's called
    //memory keyword stores data or a variable only in the function it belongs to
    function createCollectible(string memory tokenURI) public returns (uint256) {
        //creating a new NFT is just mapping a new tokenId to a new address/owner
        uint256 newTokenId = tokenCounter;
        //_safeMint is a function inherited from ERC721 standard
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI); //allows our NFT to have an image assosiated with it
        tokenCounter = tokenCounter + 1;
        return newTokenId;
    }
}