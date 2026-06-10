// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Voting {
    // Struct untuk menyimpan data kandidat
    struct Candidate {
        uint256 id;
        string name;
        uint256 voteCount;
    }

    // Mapping untuk menyimpan kandidat
    mapping(uint256 => Candidate) public candidates;

    // Mapping untuk tracking voter yang sudah vote
    mapping(address => bool) public hasVoted;

    // Jumlah kandidat
    uint256 public candidatesCount;

    // Address owner (admin)
    address public owner;

    // Status voting
    bool public votingOpen;

    // Events
    event CandidateAdded(uint256 indexed id, string name);
    event Voted(address indexed voter, uint256 indexed candidateId);
    event VotingStatusChanged(bool isOpen);

    // Modifier hanya owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Hanya owner yang bisa melakukan ini");
        _;
    }

    // Modifier voting harus aktif
    modifier whenVotingOpen() {
        require(votingOpen, "Voting belum dibuka atau sudah ditutup");
        _;
    }

    constructor() {
        owner = msg.sender;
        votingOpen = false;
    }

    // Fungsi untuk menambah kandidat (hanya owner)
    function addCandidate(string memory _name) public onlyOwner {
        require(bytes(_name).length > 0, "Nama tidak boleh kosong");

        candidatesCount++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);

        emit CandidateAdded(candidatesCount, _name);
    }

    // Fungsi untuk membuka/menutup voting
    function setVotingStatus(bool _status) public onlyOwner {
        votingOpen = _status;
        emit VotingStatusChanged(_status);
    }

    // Fungsi untuk vote
    function vote(uint256 _candidateId) public whenVotingOpen {
        require(!hasVoted[msg.sender], "Anda sudah melakukan voting");
        require(_candidateId > 0 && _candidateId <= candidatesCount, "Kandidat tidak valid");

        hasVoted[msg.sender] = true;
        candidates[_candidateId].voteCount++;

        emit Voted(msg.sender, _candidateId);
    }

    // Fungsi untuk mendapatkan semua kandidat
    function getAllCandidates() public view returns (Candidate[] memory) {
        Candidate[] memory allCandidates = new Candidate[](candidatesCount);

        for (uint256 i = 1; i <= candidatesCount; i++) {
            allCandidates[i - 1] = candidates[i];
        }

        return allCandidates;
    }

    // Fungsi untuk mendapatkan total votes
    function getTotalVotes() public view returns (uint256) {
        uint256 total = 0;
        for (uint256 i = 1; i <= candidatesCount; i++) {
            total += candidates[i].voteCount;
        }
        return total;
    }

    // Fungsi untuk cek apakah address sudah vote
    function checkIfVoted(address _voter) public view returns (bool) {
        return hasVoted[_voter];
    }
}
