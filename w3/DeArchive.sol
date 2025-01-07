// SPDX-License-Identifier: MIT 

pragma solidity ^0.8.0;

import "./Ownable.sol";

contract DeArchive is Ownable {

    struct Archive {
        address sender;
        bytes data;
    }

    constructor(address _owner) Ownable(_owner) {}

    Archive[] public archives;

    function save(bytes memory _data) public returns (uint256) {
        archives.push(Archive(msg.sender, _data));
        return archives.length - 1;
    }

    function get(uint256 index) public view returns (address, bytes memory) {
        Archive storage archive = archives[index];
        return (archive.sender, archive.data);
    }

    function remove(uint256 index) public onlyOwner {
        delete archives[index];
    }

}