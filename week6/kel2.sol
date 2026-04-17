// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RentAll{
    address public owner;

    struct Item {
        string name;
        uint price;
        uint quantity;
    }

    Item[] public items;
    mapping(uint => mapping(address => uint)) public userRentals;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require (msg.sender == owner, "Hanya owner bisa edit");
        _;
    }

    function addItem(string memory _name, uint _price, uint _qty) public onlyOwner{
        items.push(Item(_name, _price, _qty));
    }

    function rentItem(uint _itemID) public payable {
        require(_itemID < items.length);
        item storage = items[_itemID];

        require(item.quantity > 0);
        require(msg.value == item.price);

        item.quantity -=1;
        
    }

}
