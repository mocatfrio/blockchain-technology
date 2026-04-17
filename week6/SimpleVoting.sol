// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleVoting {
    address public owner;
    uint public yesCount;
    uint public noCount;
    bool public openVoting;
    mapping(address => bool) public hasVoted;

    constructor() {
        owner = msg.sender;
    }

    function voteOpen() public {
        require(msg.sender == owner, "Only owner can do this");
        openVoting = true;
    }

    function voteClose() public {
        require(msg.sender == owner, "Only owner can do this");
        openVoting = false;
    }

    function voteYes() public {
        require(openVoting, "Voting perlu dibuka");
        require(!hasVoted[msg.sender], "You have already voted");
        hasVoted[msg.sender] = true;
        yesCount += 1;
    }

    function voteNo() public {
        require(openVoting, "Voting perlu dibuka");
        require(!hasVoted[msg.sender], "You have already voted");
        hasVoted[msg.sender] = true;
        noCount += 1;
    }

    function resetVoting() public {
        require(msg.sender == owner, "Only owner can reset voting");
        yesCount = 0;
        noCount = 0;
    }

    function totalVote() public view returns (uint total, uint yes, uint no) {
        uint currentTotal = yesCount+noCount;
        return (currentTotal, yesCount, noCount);
    }

    function viewStatus() public view returns (string memory) {
        if (openVoting == true) {
            return ("Voting is open");
        } else {
            return ("Voting is closed");
        }
    }
}