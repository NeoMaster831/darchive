// SPDX-License-Identifier: MIT 

pragma solidity ^0.8.0;

import "./Ownable.sol";

contract DeArchive is Ownable {

    struct Archive {
        /* the sender is just nickname */
        uint256 sender;
        bytes data;
    }

    constructor(address _owner) Ownable(_owner) {}

    Archive[] public archives;

    function save(uint256 nickname, bytes memory _data) public returns (uint256) {
        archives.push(Archive(nickname, _data));
        return archives.length - 1; // return current index
    }

    function get(uint256 index) public view returns (uint256, bytes memory) {
        Archive storage archive = archives[index];
        return (archive.sender, archive.data);
    }

    function remove(uint256 index) public onlyOwner {
        delete archives[index];
    }
    
}