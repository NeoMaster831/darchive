// SPDX-License-Identifier: MIT 

pragma solidity ^0.8.19;

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
        // We can safely use unchecked, because the length of the array will never be 0 if we successfully pushed an element
        // and pushing operation is checked, so.
        unchecked {
            return archives.length - 1;
        }
    }

    function get(uint256 index) public view returns (address, bytes memory) {
        Archive storage archive = archives[index];
        return (archive.sender, archive.data);
    }

    function remove(uint256 index) public onlyOwner {
        delete archives[index];
    }

}