# Tutorial Membuat dApp Sederhana (Voting dApp)

**Final Project - Mata Kuliah Teknologi Blockchain**

Tutorial ini akan memandu Anda membuat aplikasi terdesentralisasi (dApp) sederhana berupa sistem voting menggunakan Ethereum blockchain.

## Daftar Isi

1. [Pendahuluan](#1-pendahuluan)
2. [Prerequisites](#2-prerequisites)
3. [Tech Stack](#3-tech-stack)
4. [Setup Project](#4-setup-project)
5. [Membuat Smart Contract](#5-membuat-smart-contract)
6. [Testing Smart Contract](#6-testing-smart-contract)
7. [Deploy ke Local Blockchain](#7-deploy-ke-local-blockchain)
8. [Membuat Frontend](#8-membuat-frontend)
9. [Integrasi Frontend dengan Smart Contract](#9-integrasi-frontend-dengan-smart-contract)
10. [Deploy ke Testnet (Opsional)](#10-deploy-ke-testnet-opsional)
11. [Demo: Membuka Voting &amp; Multiple Voters](#11-demo-membuka-voting--multiple-voters)
12. [Pengembangan Lebih Lanjut](#12-pengembangan-lebih-lanjut)
    - [12.1 Fitur Tambahan Smart Contract](#121-fitur-tambahan-untuk-smart-contract)
    - [12.2 Teknologi &amp; Arsitektur Lanjutan](#122-teknologi--arsitektur-lanjutan)
    - [12.3 Keamanan &amp; Best Practices](#123-keamanan--best-practices)
    - [12.4 Fitur Frontend Lanjutan](#124-fitur-frontend-lanjutan)
    - [12.5 Integrasi Teknologi Lain](#125-integrasi-teknologi-lain)
    - [12.6 Alternatif dApp Project Ideas](#126-alternatif-dapp-project-ideas)
    - [12.7 Tools &amp; Resources Tambahan](#127-tools--resources-tambahan)

## 1. Pendahuluan

### Apa itu dApp?

**dApp (Decentralized Application)** adalah aplikasi yang berjalan di jaringan blockchain terdesentralisasi, bukan di server terpusat. Komponen utama dApp:

- **Smart Contract**: Program yang berjalan di blockchain (backend)
- **Frontend**: Antarmuka pengguna (web/mobile)
- **Wallet**: Untuk autentikasi dan transaksi (MetaMask)

### Mengapa Voting dApp?

- Transparan: Semua vote tercatat di blockchain
- Immutable: Tidak bisa dimanipulasi
- Trustless: Tidak perlu pihak ketiga

## 2. Prerequisites

Pastikan sudah terinstall:

- **Node.js** (v18 atau lebih baru): https://nodejs.org/
- **Git**: https://git-scm.com/
- **Code Editor** (VS Code direkomendasikan)
- **MetaMask** browser extension: https://metamask.io/

Cek instalasi:

```bash
node --version   # Harus v18+
npm --version    # Harus v9+
git --version
```

## 3. Tech Stack

| Komponen              | Teknologi        |
| --------------------- | ---------------- |
| Smart Contract        | Solidity         |
| Development Framework | Hardhat 3        |
| Web3 Library          | Ethers.js        |
| Frontend              | React + Vite     |
| Wallet                | MetaMask         |
| Testing               | Mocha + Chai     |
| Deployment            | Hardhat Ignition |

## 4. Setup Project

### Step 4.1: Buat Direktori Project

```bash
mkdir voting-dapp
cd voting-dapp
```

### Step 4.2: Inisialisasi Hardhat Project

```bash
mkdir blockchain
cd blockchain

npm init -y
npm install --save-dev hardhat
npx hardhat init
```

Pilih: **Create a TypeScript project (with Mocha + Ethers.js)**

![image](/Users/mocatfrio/Projects/blockchain-technology/voting-dapp/image/README/1781030655043.png)

Hardhat 3 akan otomatis menginstall dependencies yang diperlukan:

- `@nomicfoundation/hardhat-toolbox` - Plugin lengkap (Ethers.js, Chai, dll)
- `ethers` - Library untuk interaksi blockchain
- `typescript` - TypeScript compiler
- `@nomicfoundation/hardhat-ignition` - Deployment framework
- `chai` - Assertion library untuk testing

### Step 4.3: Struktur Folder

```
voting-dapp/
├── blockchain/              # Smart contract (Hardhat 3)
│   ├── contracts/           # File Solidity (.sol)
│   ├── ignition/            # Hardhat Ignition modules
│   │   └── modules/         # Deployment modules
│   ├── scripts/             # Script deploy (.ts)
│   ├── test/                # Unit tests (.ts)
│   ├── hardhat.config.ts    # Konfigurasi Hardhat (TypeScript)
│   ├── package.json
│   └── tsconfig.json        # Konfigurasi TypeScript
├── frontend/                # React app
│   ├── src/
│   └── ...
└── README.md
```

## 5. Membuat Smart Contract

### Step 5.1: Buat File Smart Contract

Buat file `blockchain/contracts/Voting.sol`:

```solidity
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
```

### Step 5.2: Penjelasan Smart Contract

| Komponen             | Penjelasan                                            |
| -------------------- | ----------------------------------------------------- |
| `struct Candidate` | Struktur data untuk menyimpan info kandidat           |
| `mapping`          | Penyimpanan key-value di blockchain                   |
| `modifier`         | Kondisi yang harus dipenuhi sebelum fungsi dijalankan |
| `event`            | Log yang bisa dibaca oleh frontend                    |
| `view`             | Fungsi yang hanya membaca data (gratis)               |
| `public`           | Bisa dipanggil dari luar contract                     |

## 6. Testing Smart Contract

### Step 6.1: Buat File Test

Buat file `blockchain/test/Voting.ts`:

> **Catatan Hardhat 3**: Menggunakan `network.create()` untuk mendapatkan `ethers` dan `networkHelpers`

```typescript
import { expect } from "chai";
import { network } from "hardhat";

// Buat network connection (top-level await di Hardhat 3)
const { ethers, networkHelpers } = await network.create();

describe("Voting Contract", function () {
  // Fixture untuk deploy contract (di-cache oleh loadFixture)
  async function deployVotingFixture() {
    const [owner, voter1, voter2] = await ethers.getSigners();
    const voting = await ethers.deployContract("Voting");
    return { voting, owner, voter1, voter2 };
  }

  describe("Deployment", function () {
    it("Harus set owner dengan benar", async function () {
      const { voting, owner } = await networkHelpers.loadFixture(deployVotingFixture);
      const contractOwner = await voting.owner();
      expect(contractOwner).to.equal(owner.address);
    });

    it("Voting harus tertutup di awal", async function () {
      const { voting } = await networkHelpers.loadFixture(deployVotingFixture);
      const isOpen = await voting.votingOpen();
      expect(isOpen).to.equal(false);
    });

    it("Jumlah kandidat awal harus 0", async function () {
      const { voting } = await networkHelpers.loadFixture(deployVotingFixture);
      const count = await voting.candidatesCount();
      expect(count).to.equal(0n);
    });
  });

  describe("Add Candidate", function () {
    it("Owner bisa menambah kandidat", async function () {
      const { voting } = await networkHelpers.loadFixture(deployVotingFixture);
      await voting.addCandidate("Kandidat A");

      const candidate = await voting.candidates(1);
      expect(candidate.name).to.equal("Kandidat A");
      expect(candidate.voteCount).to.equal(0n);
    });

    it("Non-owner tidak bisa menambah kandidat", async function () {
      const { voting, voter1 } = await networkHelpers.loadFixture(deployVotingFixture);
      await expect(
        voting.connect(voter1).addCandidate("Kandidat B")
      ).to.be.revertedWith("Hanya owner yang bisa melakukan ini");
    });

    it("Nama kandidat tidak boleh kosong", async function () {
      const { voting } = await networkHelpers.loadFixture(deployVotingFixture);
      await expect(
        voting.addCandidate("")
      ).to.be.revertedWith("Nama tidak boleh kosong");
    });
  });

  describe("Voting", function () {
    // Fixture dengan kandidat sudah ditambahkan
    async function deployWithCandidatesFixture() {
      const { voting, owner, voter1, voter2 } = await deployVotingFixture();
      await voting.addCandidate("Kandidat A");
      await voting.addCandidate("Kandidat B");
      await voting.setVotingStatus(true);
      return { voting, owner, voter1, voter2 };
    }

    it("Voter bisa melakukan voting", async function () {
      const { voting, voter1 } = await networkHelpers.loadFixture(deployWithCandidatesFixture);
      await voting.connect(voter1).vote(1);

      const candidate = await voting.candidates(1);
      expect(candidate.voteCount).to.equal(1n);

      const hasVoted = await voting.hasVoted(voter1.address);
      expect(hasVoted).to.equal(true);
    });

    it("Voter tidak bisa vote 2 kali", async function () {
      const { voting, voter1 } = await networkHelpers.loadFixture(deployWithCandidatesFixture);
      await voting.connect(voter1).vote(1);

      await expect(
        voting.connect(voter1).vote(2)
      ).to.be.revertedWith("Anda sudah melakukan voting");
    });

    it("Tidak bisa vote jika voting ditutup", async function () {
      const { voting, voter1 } = await networkHelpers.loadFixture(deployWithCandidatesFixture);
      await voting.setVotingStatus(false);

      await expect(
        voting.connect(voter1).vote(1)
      ).to.be.revertedWith("Voting belum dibuka atau sudah ditutup");
    });

    it("Tidak bisa vote kandidat yang tidak ada", async function () {
      const { voting, voter1 } = await networkHelpers.loadFixture(deployWithCandidatesFixture);
      await expect(
        voting.connect(voter1).vote(99)
      ).to.be.revertedWith("Kandidat tidak valid");
    });
  });

  describe("Get Candidates", function () {
    it("Harus mengembalikan semua kandidat", async function () {
      const { voting } = await networkHelpers.loadFixture(deployVotingFixture);
      await voting.addCandidate("Kandidat A");
      await voting.addCandidate("Kandidat B");
      await voting.addCandidate("Kandidat C");

      const candidates = await voting.getAllCandidates();
      expect(candidates.length).to.equal(3);
      expect(candidates[0].name).to.equal("Kandidat A");
      expect(candidates[1].name).to.equal("Kandidat B");
      expect(candidates[2].name).to.equal("Kandidat C");
    });
  });

  describe("Total Votes", function () {
    it("Harus menghitung total votes dengan benar", async function () {
      const { voting, voter1, voter2 } = await networkHelpers.loadFixture(deployVotingFixture);
      await voting.addCandidate("Kandidat A");
      await voting.addCandidate("Kandidat B");
      await voting.setVotingStatus(true);

      await voting.connect(voter1).vote(1);
      await voting.connect(voter2).vote(2);

      const totalVotes = await voting.getTotalVotes();
      expect(totalVotes).to.equal(2n);
    });
  });
});
```

**Penjelasan sintaks Hardhat 3 (Mocha + Chai + Ethers.js):**

| Komponen                          | Penjelasan                                  |
| --------------------------------- | ------------------------------------------- |
| `network.create()`              | Membuat koneksi network (mengganti `hre`) |
| `networkHelpers.loadFixture()`  | Menjalankan fixture dengan caching          |
| `ethers.getSigners()`           | Mendapatkan daftar test accounts            |
| `ethers.deployContract()`       | Deploy contract                             |
| `expect().to.equal()`           | Assertion untuk kesamaan nilai              |
| `expect().to.be.revertedWith()` | Assertion untuk error smart contract        |
| `contract.connect(signer)`      | Menjalankan fungsi sebagai signer lain      |

### Step 6.2: Jalankan Test

```bash
cd blockchain
npx hardhat test
```

Output yang diharapkan:

```
Running Solidity tests


Running Mocha tests


  Voting Contract
    Deployment
      ✔ Harus set owner dengan benar (43ms)
      ✔ Voting harus tertutup di awal
      ✔ Jumlah kandidat awal harus 0
    Add Candidate
      ✔ Owner bisa menambah kandidat
      ✔ Non-owner tidak bisa menambah kandidat
      ✔ Nama kandidat tidak boleh kosong
    Voting
      ✔ Voter bisa melakukan voting
      ✔ Voter tidak bisa vote 2 kali
      ✔ Tidak bisa vote jika voting ditutup
      ✔ Tidak bisa vote kandidat yang tidak ada
    Get Candidates
      ✔ Harus mengembalikan semua kandidat
    Total Votes
      ✔ Harus menghitung total votes dengan benar


  12 passing (91ms)


12 passing (12 mocha)
```

## 7. Deploy ke Local Blockchain

### Step 7.1: Buat Script Deploy

Buat file `blockchain/scripts/deploy.ts`:

> **Catatan Hardhat 3**: Menggunakan `network.create()` untuk mendapatkan `ethers`

```typescript
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
```

**Alternatif: Menggunakan Hardhat Ignition (Recommended untuk Hardhat 3)**

Hardhat 3 merekomendasikan penggunaan **Ignition** untuk deployment. Buat file `blockchain/ignition/modules/Voting.ts`:

```typescript
import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const VotingModule = buildModule("VotingModule", (m) => {
  const voting = m.contract("Voting");

  return { voting };
});

export default VotingModule;
```

Deploy dengan Ignition:

```bash
npx hardhat ignition deploy ignition/modules/Voting.ts --network localhost
```

### Step 7.2: Konfigurasi Hardhat

Edit file `blockchain/hardhat.config.ts`:

> **Catatan Hardhat 3**: Menggunakan `defineConfig` dan format plugin baru

```typescript
import hardhatToolboxMochaEthersPlugin from "@nomicfoundation/hardhat-toolbox-mocha-ethers";
import { configVariable, defineConfig } from "hardhat/config";

export default defineConfig({
  plugins: [hardhatToolboxMochaEthersPlugin],
  solidity: {
    profiles: {
      default: {
        version: "0.8.28",
      },
      production: {
        version: "0.8.28",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200,
          },
        },
      },
    },
  },
  networks: {
    hardhatMainnet: {
      type: "edr-simulated",
      chainType: "l1",
    },
    // Untuk deploy ke testnet (opsional)
    sepolia: {
      type: "http",
      chainType: "l1",
      url: configVariable("SEPOLIA_RPC_URL"),
      accounts: [configVariable("SEPOLIA_PRIVATE_KEY")],
    },
  },
});
```

**Penjelasan konfigurasi Hardhat 3:**

| Komponen                         | Penjelasan                           |
| -------------------------------- | ------------------------------------ |
| `defineConfig()`               | Fungsi konfigurasi Hardhat 3         |
| `plugins: []`                  | Array plugin (format baru)           |
| `hardhat-toolbox-mocha-ethers` | Plugin untuk Mocha + Ethers.js       |
| `solidity.profiles`            | Profil compiler (default/production) |
| `type: "edr-simulated"`        | Network simulator Hardhat 3          |
| `configVariable()`             | Membaca environment variable         |

### Step 7.3: Jalankan Local Blockchain

Buka terminal baru dan jalankan:

```bash
cd blockchain
npx hardhat node
```

Biarkan terminal ini tetap berjalan. Anda akan melihat daftar accounts dengan 10000 ETH masing-masing.

### Step 7.4: Deploy Contract

Di terminal lain:

```bash
cd blockchain
npx hardhat run scripts/deploy.ts --network localhost
```

**PENTING**: Catat CONTRACT ADDRESS yang muncul!

## 8. Membuat Frontend

### Step 8.1: Setup React dengan Vite

```bash
cd ..  # Kembali ke root folder voting-dapp
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install ethers
```

> **Catatan**: Tutorial ini menggunakan **JavaScript**. Untuk penjelasan perbedaan JavaScript vs TypeScript, lihat **Module 12 Section 6.3**.

> **Catatan**: Frontend menggunakan **ethers.js** yang sama dengan backend Hardhat. Ini memudahkan development karena sintaks konsisten di seluruh project.

### Step 8.2: Buat File Konfigurasi Contract

Buat file `frontend/src/config/contract.js`:

```javascript
// Ganti dengan address contract hasil deploy
export const CONTRACT_ADDRESS = "PASTE_CONTRACT_ADDRESS_DISINI";

// ABI (Application Binary Interface) dari smart contract
// Copy dari blockchain/artifacts/contracts/Voting.sol/Voting.json
export const CONTRACT_ABI = [
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "id",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "name",
        "type": "string"
      }
    ],
    "name": "CandidateAdded",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "voter",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "candidateId",
        "type": "uint256"
      }
    ],
    "name": "Voted",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "bool",
        "name": "isOpen",
        "type": "bool"
      }
    ],
    "name": "VotingStatusChanged",
    "type": "event"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "_name",
        "type": "string"
      }
    ],
    "name": "addCandidate",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "candidates",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "id",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "name",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "voteCount",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "candidatesCount",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_voter",
        "type": "address"
      }
    ],
    "name": "checkIfVoted",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getAllCandidates",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "id",
            "type": "uint256"
          },
          {
            "internalType": "string",
            "name": "name",
            "type": "string"
          },
          {
            "internalType": "uint256",
            "name": "voteCount",
            "type": "uint256"
          }
        ],
        "internalType": "struct Voting.Candidate[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getTotalVotes",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "hasVoted",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bool",
        "name": "_status",
        "type": "bool"
      }
    ],
    "name": "setVotingStatus",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_candidateId",
        "type": "uint256"
      }
    ],
    "name": "vote",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "votingOpen",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
];
```

### Step 8.3: Buat Komponen React

Ganti isi file `frontend/src/App.jsx`:

```jsx
import { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { CONTRACT_ADDRESS, CONTRACT_ABI } from './config/contract';
import './App.css';

function App() {
  const [account, setAccount] = useState(null);
  const [contract, setContract] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [hasVoted, setHasVoted] = useState(false);
  const [votingOpen, setVotingOpen] = useState(false);
  const [isOwner, setIsOwner] = useState(false);
  const [loading, setLoading] = useState(false);
  const [totalVotes, setTotalVotes] = useState(0);

  // Connect ke MetaMask
  const connectWallet = async () => {
    try {
      if (!window.ethereum) {
        alert('MetaMask tidak terdeteksi! Silakan install MetaMask.');
        return;
      }

      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts'
      });

      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      const votingContract = new ethers.Contract(
        CONTRACT_ADDRESS,
        CONTRACT_ABI,
        signer
      );

      setAccount(accounts[0]);
      setContract(votingContract);

      // Cek apakah user adalah owner
      const owner = await votingContract.owner();
      setIsOwner(owner.toLowerCase() === accounts[0].toLowerCase());

    } catch (error) {
      console.error('Error connecting wallet:', error);
    }
  };

  // Load data dari contract
  const loadContractData = async () => {
    if (!contract || !account) return;

    try {
      setLoading(true);

      // Get semua kandidat
      const allCandidates = await contract.getAllCandidates();
      const formattedCandidates = allCandidates.map(c => ({
        id: Number(c.id),
        name: c.name,
        voteCount: Number(c.voteCount)
      }));
      setCandidates(formattedCandidates);

      // Cek status voting
      const isOpen = await contract.votingOpen();
      setVotingOpen(isOpen);

      // Cek apakah user sudah vote
      const voted = await contract.checkIfVoted(account);
      setHasVoted(voted);

      // Get total votes
      const total = await contract.getTotalVotes();
      setTotalVotes(Number(total));

    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Vote untuk kandidat
  const voteForCandidate = async (candidateId) => {
    if (!contract) return;

    try {
      setLoading(true);
      const tx = await contract.vote(candidateId);
      await tx.wait();

      alert('Vote berhasil!');
      await loadContractData();
    } catch (error) {
      console.error('Error voting:', error);
      alert('Gagal vote: ' + (error.reason || error.message));
    } finally {
      setLoading(false);
    }
  };

  // Toggle status voting (owner only)
  const toggleVoting = async () => {
    if (!contract) return;

    try {
      setLoading(true);
      const tx = await contract.setVotingStatus(!votingOpen);
      await tx.wait();

      await loadContractData();
    } catch (error) {
      console.error('Error toggling voting:', error);
      alert('Gagal mengubah status voting');
    } finally {
      setLoading(false);
    }
  };

  // Load data ketika contract atau account berubah
  useEffect(() => {
    if (contract && account) {
      loadContractData();
    }
  }, [contract, account]);

  // Listen untuk perubahan account
  useEffect(() => {
    if (window.ethereum) {
      window.ethereum.on('accountsChanged', (accounts) => {
        if (accounts.length > 0) {
          setAccount(accounts[0]);
        } else {
          setAccount(null);
          setContract(null);
        }
      });
    }
  }, []);

  return (
    <div className="app">
      <header>
        <h1>Voting dApp</h1>
        <p>Sistem Voting Berbasis Blockchain</p>
      </header>

      <main>
        {!account ? (
          <div className="connect-section">
            <p>Silakan connect wallet untuk mulai voting</p>
            <button onClick={connectWallet} className="btn-primary">
              Connect MetaMask
            </button>
          </div>
        ) : (
          <div className="voting-section">
            <div className="info-box">
              <p><strong>Connected:</strong> {account.slice(0, 6)}...{account.slice(-4)}</p>
              <p><strong>Status Voting:</strong> {votingOpen ? '🟢 Dibuka' : '🔴 Ditutup'}</p>
              <p><strong>Total Votes:</strong> {totalVotes}</p>
              {hasVoted && <p className="voted-badge">Anda sudah melakukan voting</p>}
            </div>

            {isOwner && (
              <div className="admin-panel">
                <h3>Admin Panel</h3>
                <button
                  onClick={toggleVoting}
                  disabled={loading}
                  className={votingOpen ? 'btn-danger' : 'btn-success'}
                >
                  {votingOpen ? 'Tutup Voting' : 'Buka Voting'}
                </button>
              </div>
            )}

            <h2>Daftar Kandidat</h2>

            {loading ? (
              <p>Loading...</p>
            ) : (
              <div className="candidates-grid">
                {candidates.map((candidate) => (
                  <div key={candidate.id} className="candidate-card">
                    <h3>{candidate.name}</h3>
                    <p className="vote-count">{candidate.voteCount} votes</p>
                    <div className="progress-bar">
                      <div
                        className="progress"
                        style={{
                          width: totalVotes > 0
                            ? `${(candidate.voteCount / totalVotes) * 100}%`
                            : '0%'
                        }}
                      />
                    </div>
                    <button
                      onClick={() => voteForCandidate(candidate.id)}
                      disabled={hasVoted || !votingOpen || loading}
                      className="btn-vote"
                    >
                      {hasVoted ? 'Sudah Vote' : 'Vote'}
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>

      <footer>
        <p>Final Project - Teknologi Blockchain</p>
      </footer>
    </div>
  );
}

export default App;
```

### Step 8.4: Styling

Ganti isi file `frontend/src/App.css`:

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  min-height: 100vh;
  color: #fff;
}

.app {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

header {
  text-align: center;
  padding: 40px 0;
}

header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  background: linear-gradient(90deg, #00d9ff, #00ff88);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

header p {
  color: #888;
  font-size: 1.1rem;
}

main {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 30px;
  backdrop-filter: blur(10px);
}

.connect-section {
  text-align: center;
  padding: 50px 0;
}

.connect-section p {
  margin-bottom: 20px;
  color: #aaa;
}

.btn-primary {
  background: linear-gradient(90deg, #00d9ff, #00ff88);
  color: #1a1a2e;
  border: none;
  padding: 15px 40px;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 217, 255, 0.3);
}

.info-box {
  background: rgba(0, 217, 255, 0.1);
  border: 1px solid rgba(0, 217, 255, 0.3);
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 30px;
}

.info-box p {
  margin: 5px 0;
}

.voted-badge {
  color: #00ff88;
  font-weight: bold;
  margin-top: 10px !important;
}

.admin-panel {
  background: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 30px;
}

.admin-panel h3 {
  margin-bottom: 15px;
  color: #ffc107;
}

.btn-success {
  background: #00ff88;
  color: #1a1a2e;
  border: none;
  padding: 10px 25px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

.btn-danger {
  background: #ff4757;
  color: #fff;
  border: none;
  padding: 10px 25px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

h2 {
  margin-bottom: 20px;
  color: #00d9ff;
}

.candidates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.candidate-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 25px;
  text-align: center;
  transition: transform 0.2s, border-color 0.2s;
}

.candidate-card:hover {
  transform: translateY(-5px);
  border-color: #00d9ff;
}

.candidate-card h3 {
  margin-bottom: 15px;
  font-size: 1.3rem;
}

.vote-count {
  font-size: 1.5rem;
  color: #00ff88;
  font-weight: bold;
  margin-bottom: 15px;
}

.progress-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 20px;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #00d9ff, #00ff88);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.btn-vote {
  background: linear-gradient(90deg, #00d9ff, #00ff88);
  color: #1a1a2e;
  border: none;
  padding: 12px 30px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: opacity 0.2s;
  width: 100%;
}

.btn-vote:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

footer {
  text-align: center;
  padding: 30px 0;
  color: #666;
}

@media (max-width: 600px) {
  header h1 {
    font-size: 1.8rem;
  }

  .candidates-grid {
    grid-template-columns: 1fr;
  }
}
```

Hapus file yang tidak diperlukan:

```bash
rm frontend/src/index.css
```

Edit `frontend/src/main.`

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

## 9. Integrasi Frontend dengan Smart Contract

### Step 9.1: Setup MetaMask untuk Local Network

1. Buka MetaMask
2. Klik network dropdown → **Add Network** → **Add network manually**
3. Isi:
   - Network Name: `Hardhat Local`
   - RPC URL: `http://127.0.0.1:8545`
   - Chain ID: `31337`
   - Currency Symbol: `ETH`
4. Save

### Step 9.2: Import Account Test ke MetaMask

Dari output `npx hardhat node`, copy private key dari Account #0:

```
Account #0: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
Private Key: 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
```

Di MetaMask:

1. Klik icon account → **Import Account**
2. Paste private key
3. Import

### Step 9.3: Update Contract Address

Edit `frontend/src/config/contract.js`:

- Ganti `PASTE_CONTRACT_ADDRESS_DISINI` dengan address contract hasil deploy

### Step 9.4: Jalankan Frontend

```bash
cd frontend
npm run dev
```

Buka browser di `http://localhost:5173`

---

## 10. Deploy ke Testnet (Opsional)

### Step 10.1: Dapatkan Sepolia ETH

1. Buat akun di https://www.alchemy.com/
2. Buat App untuk Sepolia testnet
3. Dapatkan test ETH dari faucet: https://sepoliafaucet.com/

### Step 10.2: Setup Environment Variables

Buat file `blockchain/.env`:

```env
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
PRIVATE_KEY=your_wallet_private_key
```

Install dotenv:

```bash
cd blockchain
npm install dotenv
```

Konfigurasi sudah ada di `hardhat.config.ts`. Pastikan environment variables sudah diset:

```bash
# Di file .env atau export langsung
export SEPOLIA_RPC_URL="https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY"
export SEPOLIA_PRIVATE_KEY="your_wallet_private_key"
```

Hardhat 3 menggunakan `configVariable()` untuk membaca environment variables yang sudah dikonfigurasi di `hardhat.config.ts`.

### Step 10.3: Deploy ke Sepolia

**Opsi 1: Menggunakan script**

```bash
npx hardhat run scripts/deploy.ts --network sepolia
```

**Opsi 2: Menggunakan Hardhat Ignition (Recommended)**

```bash
npx hardhat ignition deploy ignition/modules/Voting.ts --network sepolia
```

---

## 11. Demo: Membuka Voting & Multiple Voters

Tutorial ini menunjukkan cara menggunakan fitur **Open/Close Voting** dan simulasi **beberapa voter** melakukan voting.

### Step 11.1: Persiapan

Pastikan:

1. Hardhat node berjalan di terminal 1: `npx hardhat node`
2. Contract sudah di-deploy: `npx hardhat run scripts/deploy.ts --network localhost`
3. Frontend berjalan: `cd frontend && npm run dev`

### Step 11.2: Import Multiple Accounts ke MetaMask

Dari output `npx hardhat node`, Anda akan melihat 20 test accounts. Import beberapa account ke MetaMask:

```
Account #0: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 (Owner/Admin)
Private Key: 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

Account #1: 0x70997970C51812dc3A010C7d01b50e0d17dc79C8 (Voter 1)
Private Key: 0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d

Account #2: 0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC (Voter 2)
Private Key: 0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a

Account #3: 0x90F79bf6EB2c4f870365E785982E1f101E93b906 (Voter 3)
Private Key: 0x7c852118294e51e653712a81e05800f419141751be58f605c371e15141b007a6
```

**Cara import ke MetaMask:**

1. Klik icon account → **Import Account**
2. Paste private key
3. Klik **Import**
4. Ulangi untuk account lain (beri nama: "Voter 1", "Voter 2", dll)

### Step 11.3: Skenario Demo

```
┌─────────────────────────────────────────────────────────────────┐
│                     SKENARIO DEMO VOTING                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Owner deploy contract        → Voting TERTUTUP              │
│  2. Owner menambah kandidat      → 3 kandidat ditambahkan       │
│  3. Owner MEMBUKA voting         → Status: OPEN                 │
│  4. Voter 1 vote Kandidat A      → Vote count: 1                │
│  5. Voter 2 vote Kandidat B      → Vote count: 1                │
│  6. Voter 3 vote Kandidat A      → Vote count: 2                │
│  7. Voter 1 coba vote lagi       → DITOLAK (sudah vote)         │
│  8. Owner MENUTUP voting         → Status: CLOSED               │
│  9. Voter baru coba vote         → DITOLAK (voting ditutup)     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Step 11.4: Demo via Frontend

#### A. Login sebagai Owner (Account #0)

1. Buka MetaMask, pilih **Account #0** (Owner)
2. Buka `http://localhost:5173`
3. Klik **Connect MetaMask**
4. Anda akan melihat **Admin Panel** (karena Anda owner)

#### B. Membuka Voting

1. Di Admin Panel, klik tombol **"Buka Voting"**
2. Konfirmasi transaksi di MetaMask
3. Status berubah dari 🔴 **Ditutup** → 🟢 **Dibuka**

```
┌─────────────────────────────────────────┐
│            Admin Panel                  │
├─────────────────────────────────────────┤
│  Status Voting: 🟢 Dibuka               │
│                                         │
│  [  Tutup Voting  ]                     │
└─────────────────────────────────────────┘
```

#### C. Voter 1 Melakukan Voting

1. Di MetaMask, **switch account** ke **Voter 1** (Account #1)
2. Refresh halaman atau klik **Connect** lagi
3. Pilih kandidat yang diinginkan, klik **Vote**
4. Konfirmasi transaksi di MetaMask
5. Vote count kandidat bertambah

```
┌─────────────────────────────────────────┐
│  Kandidat A                             │
│  ████████████████░░░░░░░░░  1 votes     │
│  [    Vote    ]                         │
├─────────────────────────────────────────┤
│  Kandidat B                             │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░  0 votes     │
│  [    Vote    ]                         │
└─────────────────────────────────────────┘
```

#### D. Voter 2 dan Voter 3 Melakukan Voting

1. Switch ke **Voter 2**, vote untuk Kandidat B
2. Switch ke **Voter 3**, vote untuk Kandidat A

**Hasil akhir:**

```
┌─────────────────────────────────────────┐
│  Kandidat A                             │
│  ████████████████████████░░  2 votes    │
├─────────────────────────────────────────┤
│  Kandidat B                             │
│  ████████████░░░░░░░░░░░░░  1 vote      │
├─────────────────────────────────────────┤
│  Kandidat C                             │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░  0 votes     │
├─────────────────────────────────────────┤
│  Total Votes: 3                         │
└─────────────────────────────────────────┘
```

#### E. Test: Voter Tidak Bisa Vote 2 Kali

1. Switch kembali ke **Voter 1**
2. Coba klik **Vote** lagi
3. Akan muncul error: **"Anda sudah melakukan voting"**

#### F. Menutup Voting

1. Switch ke **Owner** (Account #0)
2. Di Admin Panel, klik **"Tutup Voting"**
3. Status berubah dari 🟢 **Dibuka** → 🔴 **Ditutup**

#### G. Test: Tidak Bisa Vote Setelah Ditutup

1. Import **Account #4** sebagai voter baru
2. Switch ke account tersebut
3. Coba klik **Vote**
4. Akan muncul error: **"Voting belum dibuka atau sudah ditutup"**

### Step 11.5: Demo via Hardhat Console (Alternatif)

Jika ingin demo tanpa frontend, gunakan Hardhat console:

```bash
cd blockchain
npx hardhat console --network localhost
```

```javascript
// Get contract instance
const Voting = await ethers.getContractFactory("Voting");
const voting = await Voting.attach("PASTE_CONTRACT_ADDRESS");

// Get signers (accounts)
const [owner, voter1, voter2, voter3] = await ethers.getSigners();

// Cek status awal
await voting.votingOpen();  // false

// Owner membuka voting
await voting.setVotingStatus(true);
await voting.votingOpen();  // true

// Voter 1 vote untuk kandidat 1
await voting.connect(voter1).vote(1);

// Voter 2 vote untuk kandidat 2
await voting.connect(voter2).vote(2);

// Voter 3 vote untuk kandidat 1
await voting.connect(voter3).vote(1);

// Cek hasil
const kandidatA = await voting.candidates(1);
console.log("Kandidat A votes:", kandidatA.voteCount.toString());  // 2

const kandidatB = await voting.candidates(2);
console.log("Kandidat B votes:", kandidatB.voteCount.toString());  // 1

// Total votes
const total = await voting.getTotalVotes();
console.log("Total votes:", total.toString());  // 3

// Voter 1 coba vote lagi (akan error)
await voting.connect(voter1).vote(2);  // Error: Anda sudah melakukan voting

// Owner tutup voting
await voting.setVotingStatus(false);

// Voter baru coba vote (akan error)
const [,,,, voter4] = await ethers.getSigners();
await voting.connect(voter4).vote(1);  // Error: Voting belum dibuka atau sudah ditutup
```

### Step 11.6: Ringkasan Fitur Voting

| Fitur                      | Fungsi                    | Siapa yang bisa              |
| -------------------------- | ------------------------- | ---------------------------- |
| `setVotingStatus(true)`  | Membuka voting            | Owner saja                   |
| `setVotingStatus(false)` | Menutup voting            | Owner saja                   |
| `vote(candidateId)`      | Melakukan voting          | Semua orang (1x per address) |
| `addCandidate(name)`     | Menambah kandidat         | Owner saja                   |
| `getAllCandidates()`     | Melihat semua kandidat    | Semua orang                  |
| `getTotalVotes()`        | Melihat total votes       | Semua orang                  |
| `checkIfVoted(address)`  | Cek sudah vote atau belum | Semua orang                  |

### Step 11.7: Error yang Mungkin Muncul

| Error Message                            | Penyebab                     | Solusi                       |
| ---------------------------------------- | ---------------------------- | ---------------------------- |
| "Hanya owner yang bisa melakukan ini"    | Bukan owner yang menjalankan | Switch ke account owner      |
| "Anda sudah melakukan voting"            | Address sudah pernah vote    | Tidak bisa vote lagi         |
| "Voting belum dibuka atau sudah ditutup" | Status voting = false        | Owner harus buka voting dulu |
| "Kandidat tidak valid"                   | ID kandidat tidak ada        | Gunakan ID 1, 2, atau 3      |
| "Nama tidak boleh kosong"                | Menambah kandidat tanpa nama | Isi nama kandidat            |

---



## 12. Pengembangan Lebih Lanjut

Berikut adalah ide-ide fitur dan teknologi yang dapat ditambahkan untuk mengembangkan Voting dApp menjadi lebih kompleks dan fungsional.

### 12.1 Fitur Tambahan untuk Smart Contract

#### A. Whitelist Voter

Hanya address yang terdaftar yang boleh voting.

```solidity
// Tambahkan di smart contract
mapping(address => bool) public registeredVoters;
uint256 public registeredVotersCount;

function registerVoter(address _voter) public onlyOwner {
    require(!registeredVoters[_voter], "Voter sudah terdaftar");
    registeredVoters[_voter] = true;
    registeredVotersCount++;
}

modifier onlyRegisteredVoter() {
    require(registeredVoters[msg.sender], "Anda tidak terdaftar sebagai voter");
    _;
}
```

#### B. Time-Based Voting

Voting dengan batas waktu otomatis.

```solidity
uint256 public votingStartTime;
uint256 public votingEndTime;

function setVotingPeriod(uint256 _startTime, uint256 _endTime) public onlyOwner {
    require(_endTime > _startTime, "End time harus lebih besar dari start time");
    votingStartTime = _startTime;
    votingEndTime = _endTime;
}

modifier withinVotingPeriod() {
    require(block.timestamp >= votingStartTime, "Voting belum dimulai");
    require(block.timestamp <= votingEndTime, "Voting sudah berakhir");
    _;
}
```

#### C. Multiple Elections

Mendukung beberapa sesi voting/pemilu berbeda.

```solidity
struct Election {
    string name;
    uint256 startTime;
    uint256 endTime;
    bool active;
    uint256[] candidateIds;
}

mapping(uint256 => Election) public elections;
uint256 public electionsCount;
```

#### D. Delegated Voting

Voter bisa mendelegasikan suaranya ke voter lain.

```solidity
mapping(address => address) public delegations;

function delegate(address _to) public {
    require(_to != msg.sender, "Tidak bisa delegate ke diri sendiri");
    require(!hasVoted[msg.sender], "Anda sudah vote");
    delegations[msg.sender] = _to;
}
```

#### E. Vote Weight / Staking

Bobot suara berdasarkan jumlah token yang di-stake.

```solidity
mapping(address => uint256) public stakedAmount;
uint256 public minimumStake = 1 ether;

function stake() public payable {
    require(msg.value >= minimumStake, "Stake kurang dari minimum");
    stakedAmount[msg.sender] += msg.value;
}

function voteWithWeight(uint256 _candidateId) public {
    uint256 weight = stakedAmount[msg.sender] / minimumStake;
    candidates[_candidateId].voteCount += weight;
}
```

### 12.2 Teknologi & Arsitektur Lanjutan

#### A. IPFS untuk Data Off-Chain

Simpan data kandidat (foto, bio, visi misi) di IPFS.

| Komponen              | Fungsi                             |
| --------------------- | ---------------------------------- |
| **IPFS**        | Penyimpanan file terdesentralisasi |
| **Pinata**      | IPFS pinning service               |
| **NFT.Storage** | Alternatif gratis untuk IPFS       |

```solidity
struct Candidate {
    uint256 id;
    string name;
    string ipfsHash;  // CID untuk metadata di IPFS
    uint256 voteCount;
}
```

```javascript
// Upload ke IPFS menggunakan Pinata
const pinataSDK = require('@pinata/sdk');
const pinata = new pinataSDK('apiKey', 'apiSecret');

const metadata = {
    name: "Budi Santoso",
    photo: "ipfs://Qm...",
    bio: "Kandidat terbaik untuk memajukan...",
    visiMisi: ["Poin 1", "Poin 2"]
};

const result = await pinata.pinJSONToIPFS(metadata);
// result.IpfsHash -> simpan di smart contract
```

#### B. The Graph untuk Indexing

Query data blockchain lebih efisien dengan GraphQL.

```graphql
# schema.graphql
type Candidate @entity {
  id: ID!
  name: String!
  voteCount: BigInt!
  voters: [Vote!]! @derivedFrom(field: "candidate")
}

type Vote @entity {
  id: ID!
  voter: Bytes!
  candidate: Candidate!
  timestamp: BigInt!
}
```

```javascript
// Query dengan Apollo Client
const GET_CANDIDATES = gql`
  query GetCandidates {
    candidates(orderBy: voteCount, orderDirection: desc) {
      id
      name
      voteCount
    }
  }
`;
```

#### C. Layer 2 Solutions

Kurangi gas fee dengan deploy ke Layer 2.

| Network            | Keunggulan              | Gas Fee |
| ------------------ | ----------------------- | ------- |
| **Polygon**  | EVM compatible, murah   | ~$0.01  |
| **Arbitrum** | Optimistic rollup       | ~$0.10  |
| **Optimism** | Optimistic rollup       | ~$0.10  |
| **Base**     | Coinbase L2, murah      | ~$0.01  |
| **zkSync**   | ZK rollup, sangat murah | ~$0.05  |

```typescript
// Di hardhat.config.ts untuk Polygon
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config: HardhatUserConfig = {
  solidity: "0.8.19",
  networks: {
    polygon: {
      url: "https://polygon-rpc.com",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 137
    }
  }
};

export default config;
```

#### D. Multi-Wallet Support

Selain MetaMask, dukung wallet lain dengan Web3Modal atau RainbowKit.

```bash
npm install @rainbow-me/rainbowkit wagmi viem
```

```jsx
import { RainbowKitProvider, ConnectButton } from '@rainbow-me/rainbowkit';

function App() {
  return (
    <RainbowKitProvider>
      <ConnectButton />
      {/* ... */}
    </RainbowKitProvider>
  );
}
```

### 12.3 Keamanan & Best Practices

#### A. Access Control dengan OpenZeppelin

```bash
npm install @openzeppelin/contracts
```

```solidity
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract Voting is Ownable, Pausable, ReentrancyGuard {
    // Contract yang lebih aman
}
```

#### B. Upgradeable Contracts

Gunakan proxy pattern untuk upgrade contract tanpa kehilangan data.

```solidity
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

contract VotingV1 is Initializable, UUPSUpgradeable {
    function initialize() public initializer {
        // Setup awal
    }
}
```

#### C. Gas Optimization

```solidity
// Gunakan uint256 daripada uint8 untuk efisiensi
// Pack struct untuk hemat storage
struct Candidate {
    uint128 id;        // Pack dalam 1 slot
    uint128 voteCount; // dengan voteCount
    string name;       // Slot terpisah
}

// Gunakan events untuk data yang tidak perlu on-chain
event VoteDetails(address voter, uint256 candidateId, uint256 timestamp);
```

### 12.4 Fitur Frontend Lanjutan

#### A. Real-time Updates dengan Events

```javascript
// Frontend (React) - menggunakan ethers.js
// Listen ke events dari smart contract
contract.on("Voted", (voter, candidateId, event) => {
    console.log(`${voter} voted for candidate ${candidateId}`);
    loadContractData(); // Refresh data
});

contract.on("VotingStatusChanged", (isOpen) => {
    setVotingOpen(isOpen);
});
```

> **Catatan**: Kode di atas menggunakan ethers.js yang konsisten dengan backend Hardhat.

#### B. Chart & Visualisasi

```bash
npm install recharts
```

```jsx
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

const VotingChart = ({ candidates }) => {
    const data = candidates.map(c => ({
        name: c.name,
        value: c.voteCount
    }));

    return (
        <PieChart width={400} height={400}>
            <Pie data={data} dataKey="value" nameKey="name" />
            <Tooltip />
            <Legend />
        </PieChart>
    );
};
```

#### C. Notifikasi & Toast

```bash
npm install react-hot-toast
```

```jsx
import toast from 'react-hot-toast';

// Saat vote berhasil
toast.success('Vote berhasil dicatat di blockchain!');

// Saat error
toast.error('Gagal melakukan voting');

// Loading state
toast.promise(contract.vote(candidateId), {
    loading: 'Memproses vote...',
    success: 'Vote berhasil!',
    error: 'Vote gagal'
});
```

#### D. PWA (Progressive Web App)

Buat dApp bisa diinstall di mobile.

```bash
npm install vite-plugin-pwa -D
```

### 12.5 Integrasi Teknologi Lain

#### A. Chainlink Oracle

Dapatkan data eksternal (misalnya verifikasi identitas).

```solidity
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

// Contoh: Batasi voting berdasarkan harga ETH
AggregatorV3Interface internal priceFeed;

function vote(uint256 _candidateId) public {
    (, int256 price, , , ) = priceFeed.latestRoundData();
    require(price > 2000 * 10**8, "ETH harga terlalu rendah");
    // ... logic voting
}
```

#### B. ENS (Ethereum Name Service)

Tampilkan nama ENS instead of address panjang.

```javascript
const provider = new ethers.BrowserProvider(window.ethereum);
const ensName = await provider.lookupAddress(address);
// "vitalik.eth" instead of "0x..."
```

#### C. Zero-Knowledge Proofs

Voting anonim tapi tetap verifiable.

| Library             | Kegunaan                |
| ------------------- | ----------------------- |
| **snarkjs**   | ZK-SNARK implementation |
| **circom**    | ZK circuit compiler     |
| **semaphore** | Anonymous signaling     |

```bash
npm install snarkjs circom
```

#### D. Multi-chain Support

Deploy ke beberapa blockchain sekaligus.

```javascript
const NETWORKS = {
    ethereum: { chainId: 1, contract: "0x..." },
    polygon: { chainId: 137, contract: "0x..." },
    arbitrum: { chainId: 42161, contract: "0x..." }
};
```

### 12.6 Alternatif dApp Project Ideas

Selain Voting, berikut ide dApp lain untuk final project:

| Project                            | Deskripsi                         | Tingkat Kesulitan |
| ---------------------------------- | --------------------------------- | ----------------- |
| **Todo List**                | Task management on-chain          | Mudah             |
| **Crowdfunding**             | Platform penggalangan dana        | Sedang            |
| **NFT Marketplace**          | Jual-beli NFT                     | Sedang            |
| **Token (ERC-20)**           | Buat cryptocurrency sendiri       | Mudah             |
| **NFT Collection**           | Mint NFT dengan metadata          | Sedang            |
| **DAO Governance**           | Voting untuk keputusan organisasi | Sulit             |
| **DeFi Staking**             | Stake token dapat reward          | Sulit             |
| **Supply Chain**             | Tracking produk                   | Sedang            |
| **Certificate Verification** | Verifikasi ijazah/sertifikat      | Sedang            |
| **Escrow Service**           | Pembayaran dengan perantara       | Sedang            |
| **Lottery**                  | Undian dengan random number       | Sedang            |
| **Auction**                  | Lelang terdesentralisasi          | Sedang            |

### 12.7 Tools & Resources Tambahan

#### Development Tools

| Tool                | Fungsi                                       |
| ------------------- | -------------------------------------------- |
| **Hardhat**   | Framework utama (TypeScript, Ethers.js)      |
| **Foundry**   | Alternatif Hardhat (Rust-based, lebih cepat) |
| **Tenderly**  | Debugging & monitoring                       |
| **Slither**   | Security analysis                            |
| **Mythril**   | Smart contract security                      |
| **Remix IDE** | Online Solidity IDE                          |

#### Testing & Debugging

```bash
# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Fuzz testing dengan Foundry
forge test --fuzz-runs 1000
```

#### Monitoring & Analytics

| Service                  | Kegunaan                   |
| ------------------------ | -------------------------- |
| **Etherscan**      | Block explorer             |
| **Dune Analytics** | On-chain data analysis     |
| **Nansen**         | Wallet tracking            |
| **Alchemy**        | Node provider + monitoring |

## Referensi

- [Solidity Documentation](https://docs.soliditylang.org/)
- [Hardhat Documentation](https://hardhat.org/docs)
- [Hardhat Toolbox](https://hardhat.org/hardhat-runner/plugins/nomicfoundation-hardhat-toolbox)
- [Hardhat Ignition](https://hardhat.org/ignition/docs/getting-started)
- [Ethers.js v6 Documentation](https://docs.ethers.org/v6/)
- [Chai Assertion Library](https://www.chaijs.com/)
- [Mocha Test Framework](https://mochajs.org/)
- [MetaMask Documentation](https://docs.metamask.io/)
- [React Documentation](https://react.dev/)
