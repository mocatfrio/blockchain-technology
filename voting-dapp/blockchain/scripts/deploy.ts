import { network } from "hardhat";

const { ethers } = await network.create();

console.log("Deploying Voting contract...");

// Deploy contract menggunakan Ethers.js
const voting = await ethers.deployContract("Voting");
const contractAddress = await voting.getAddress();

console.log(`Voting contract deployed to: ${contractAddress}`);

// Tambahkan beberapa kandidat untuk testing
console.log("\nAdding sample candidates...");

await voting.addCandidate("Budi Santoso");
console.log("- Added: Budi Santoso");

await voting.addCandidate("Siti Rahayu");
console.log("- Added: Siti Rahayu");

await voting.addCandidate("Ahmad Wijaya");
console.log("- Added: Ahmad Wijaya");

// Buka voting
await voting.setVotingStatus(true);
console.log("\nVoting is now OPEN!");

console.log("\n========================================");
console.log("CONTRACT ADDRESS:", contractAddress);
console.log("========================================");
console.log("\nSave this address for frontend configuration!");
