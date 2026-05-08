# Module 11. Deployment & MetaMask Interaction

## Deskripsi

Modul ini membahas cara **deploy** smart contract ke local blockchain dan **berinteraksi** menggunakan MetaMask. Mahasiswa akan belajar menjalankan local blockchain, menulis deployment script, menghubungkan MetaMask, dan melakukan transaksi.

## Tujuan Pembelajaran

Setelah menyelesaikan modul ini, mahasiswa mampu:

1. Menjalankan local blockchain dengan Hardhat Node atau Ganache
2. Menulis deployment script
3. Deploy smart contract ke local network
4. Menghubungkan MetaMask ke local network
5. Import akun development ke MetaMask
6. Berinteraksi dengan smart contract menggunakan MetaMask
7. Memahami transaction hash dan perubahan state

## Prasyarat

- Sudah menyelesaikan Module 09 (Setup & Compile)
- Sudah menyelesaikan Module 10 (Testing)
- Contract sudah lolos semua test
- MetaMask sudah terinstall di browser

## List of Contents

- [Deskripsi](#deskripsi)
- [Tujuan Pembelajaran](#tujuan-pembelajaran)
- [Prasyarat](#prasyarat)
- [1. Dari Testing ke Deployment](#1-dari-testing-ke-deployment)
- [2. Local Blockchain](#2-local-blockchain)
- [3. Deployment Script](#3-deployment-script)
- [4. Deploy ke Local Network](#4-deploy-ke-local-network)
- [5. Setup MetaMask](#5-setup-metamask)
- [6. Import Akun Development](#6-import-akun-development)
- [7. Interaksi dengan Contract](#7-interaksi-dengan-contract)
- [8. Interaksi via Script](#8-interaksi-via-script)
- [9. Troubleshooting](#9-troubleshooting)
- [10. Latihan Tambahan](#10-latihan-tambahan)
- [Ringkasan](#ringkasan)
- [Tugas](#tugas)

---

## 1. Dari Testing ke Deployment

### 1.1 Workflow Development

```
┌─────────────────────────────────────────────────────────────────┐
│               SMART CONTRACT DEVELOPMENT WORKFLOW               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Module 09          Module 10          Module 11                │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐               │
│  │  Write   │─────►│   Test   │─────►│  Deploy  │               │
│  │ Contract │      │          │      │          │               │
│  └──────────┘      └──────────┘      └──────────┘               │ 
│       │                 │                 │                     │
│       ▼                 ▼                 ▼                     │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐               │
│  │ Compile  │      │ All Pass │      │ Interact │               │
│  │          │      │    ✓     │      │ MetaMask │               │
│  └──────────┘      └──────────┘      └──────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Perbedaan Test vs Deploy

| Aspek                 | Testing            | Deployment             |
| --------------------- | ------------------ | ---------------------- |
| **Network**     | Hardhat in-process | Hardhat Node / Ganache |
| **Persistence** | Reset setiap test  | State bertahan         |
| **Wallet**      | Tidak perlu        | MetaMask               |
| **Interaksi**   | Via script         | Via wallet / Remix     |

## 2. Local Blockchain

### 2.1 Opsi Local Blockchain

Ada dua opsi untuk menjalankan local blockchain:

| Opsi                   | Command/Action       | Port | Kelebihan                                |
| ---------------------- | -------------------- | ---- | ---------------------------------------- |
| **Hardhat Node** | `npx hardhat node` | 8545 | Terintegrasi dengan Hardhat, console.log |
| **Ganache**      | Buka aplikasi GUI    | 7545 | Visual, mudah dipahami, GUI              |

### 2.2 Hardhat Node

Buka terminal dan jalankan:

```bash
npx hardhat node
```

**Output:**

```text
Started HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545/

Accounts
========

WARNING: These accounts, and their private keys, are publicly known.
Any funds sent to them on Mainnet or any other live network WILL BE LOST.

Account #0: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 (10000 ETH)
Private Key: 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

Account #1: 0x70997970C51812dc3A010C7d01b50e0d17dc79C8 (10000 ETH)
Private Key: 0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d

Account #2: 0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC (10000 ETH)
Private Key: 0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a

...
```

**Penting:**

- Terminal ini harus tetap berjalan
- Jangan tutup terminal saat development
- Buka terminal baru untuk command lainnya

### 2.3 Ganache (Alternatif)

Jika menggunakan Ganache GUI:

1. Download dari https://trufflesuite.com/ganache/
2. Install dan buka aplikasi
3. Klik **Quickstart Ethereum**

```
┌─────────────────────────────────────────────────────────────────┐
│                        GANACHE GUI                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  RPC SERVER: HTTP://127.0.0.1:7545                              │
│  NETWORK ID: 1337                                               │
│                                                                 │
│  ACCOUNTS                                                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  0x627306090aB... │ 100.00 ETH │ [Show Keys] │            │  │
│  │  0xf17f52151EB... │ 100.00 ETH │ [Show Keys] │            │  │
│  │  0xC5fdf4076b8... │ 100.00 ETH │ [Show Keys] │            │  │
│  │  ...                                                      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  [BLOCKS]  [TRANSACTIONS]  [CONTRACTS]  [EVENTS]  [LOGS]        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 Perbandingan

| Aspek                 | Hardhat Node         | Ganache             |
| --------------------- | -------------------- | ------------------- |
| **Interface**   | CLI                  | GUI                 |
| **Akun**        | 20 akun × 10000 ETH | 10 akun × 100 ETH  |
| **Chain ID**    | 31337                | 1337                |
| **Port**        | 8545                 | 7545                |
| **Console.log** | Ya (Solidity)        | Tidak               |
| **Reset**       | Restart process      | Restart atau button |

## 3. Deployment Script

### 3.1 Buat Script Deploy

Buat file `scripts/deploy.js`:

```javascript
const hre = require("hardhat");

async function main() {
  console.log("Deploying CourseReward contract...");

  // Deploy dengan initial reward = 100
  const CourseReward = await hre.ethers.getContractFactory("CourseReward");
  const courseReward = await CourseReward.deploy(100);

  // Tunggu deployment selesai
  await courseReward.waitForDeployment();

  // Ambil address contract
  const address = await courseReward.getAddress();

  console.log(`CourseReward deployed to: ${address}`);
  console.log(`Initial reward amount: ${await courseReward.rewardAmount()}`);
  console.log(`Owner: ${await courseReward.owner()}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

### 3.2 Penjelasan Script

| Kode                                | Penjelasan                                       |
| ----------------------------------- | ------------------------------------------------ |
| `hre.ethers.getContractFactory()` | Mengambil contract yang sudah dicompile          |
| `CourseReward.deploy(100)`        | Deploy dengan parameter constructor              |
| `waitForDeployment()`             | Menunggu transaksi deployment dikonfirmasi       |
| `getAddress()`                    | Mendapatkan address contract yang sudah dideploy |

### 3.3 Struktur Deployment Script

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT SCRIPT FLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Import hardhat runtime environment                          │
│     const hre = require("hardhat");                             │
│                                                                 │
│  2. Get contract factory                                        │
│     const Contract = await hre.ethers.getContractFactory(...);  │
│                                                                 │
│  3. Deploy contract                                             │
│     const contract = await Contract.deploy(args);               │
│                                                                 │
│  4. Wait for deployment                                         │
│     await contract.waitForDeployment();                         │
│                                                                 │
│  5. Log contract address                                        │
│     console.log("Deployed to:", await contract.getAddress());   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 4. Deploy ke Local Network

### 4.1 Pastikan Local Blockchain Berjalan

Di terminal pertama, pastikan Hardhat Node atau Ganache sudah berjalan.

### 4.2 Deploy Contract

Buka terminal baru (jangan tutup terminal Hardhat Node) dan jalankan:

**Untuk Hardhat Node:**

```bash
npx hardhat run scripts/deploy.js --network localhost
```

**Untuk Ganache:**

```bash
npx hardhat run scripts/deploy.js --network ganache
```

### 4.3 Output Deploy

```text
Deploying CourseReward contract...
CourseReward deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3
Initial reward amount: 100
Owner: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
```

**Penting:** Catat **contract address** ini! Akan digunakan untuk interaksi.

### 4.4 Verifikasi di Hardhat Node

Di terminal Hardhat Node, akan muncul log transaksi:

```text
eth_chainId
eth_accounts
eth_blockNumber
eth_chainId (2)
eth_estimateGas
eth_getBlockByNumber
eth_feeHistory
eth_sendTransaction
  Contract deployment: CourseReward
  Contract address:    0x5fbdb2315678afecb367f032d93f642f64180aa3
  Transaction:         0x1234...
  From:                0xf39f...
  Value:               0 ETH
  Gas used:            298543 of 298543
  Block #1:            0xabcd...
```

### 4.5 Verifikasi di Ganache

Jika menggunakan Ganache GUI:

- Tab **Transactions** menampilkan transaksi deployment
- Tab **Blocks** menampilkan block baru
- Saldo ETH akun deployer berkurang sedikit (gas fee)

## 5. Setup MetaMask

### 5.1 Menambah Network Lokal

Buka MetaMask dan tambahkan network:

**Untuk Hardhat Node:**

| Field           | Value                 |
| --------------- | --------------------- |
| Network Name    | Hardhat Local         |
| RPC URL         | http://127.0.0.1:8545 |
| Chain ID        | 31337                 |
| Currency Symbol | ETH                   |

**Untuk Ganache:**

| Field           | Value                 |
| --------------- | --------------------- |
| Network Name    | Ganache Local         |
| RPC URL         | http://127.0.0.1:7545 |
| Chain ID        | 1337                  |
| Currency Symbol | ETH                   |

### 5.2 Langkah Menambah Network

```
┌─────────────────────────────────────────────────────────────────┐
│              MENAMBAH NETWORK DI METAMASK                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Klik dropdown network (pojok kiri atas)                     │
│                                                                 │
│  2. Klik "Add network" atau "Add a network manually"            │
│                                                                 │
│  3. Isi form:                                                   │
│     ┌─────────────────────────────────────────────────────────┐ │
│     │ Network name: Hardhat Local                             │ │
│     │ New RPC URL: http://127.0.0.1:8545                      │ │
│     │ Chain ID: 31337                                         │ │
│     │ Currency symbol: ETH                                    │ │
│     │ Block explorer URL: (kosongkan)                         │ │
│     └─────────────────────────────────────────────────────────┘ │
│                                                                 │
│  4. Klik "Save"                                                 │
│                                                                 │
│  5. Switch ke network yang baru ditambahkan                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Peringatan Keamanan

```
⚠️  PERINGATAN PENTING:
═══════════════════════════════════════════════════════════════
║  - Jangan gunakan wallet utama untuk development            ║
║  - Private key dari Hardhat/Ganache adalah PUBLIC           ║
║  - Jangan pernah kirim ETH asli ke akun development         ║
║  - Buat MetaMask profile terpisah untuk development         ║
═══════════════════════════════════════════════════════════════
```

## 6. Import Akun Development

### 6.1 Copy Private Key

Dari output Hardhat Node, copy salah satu private key:

```text
Account #0: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 (10000 ETH)
Private Key: 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
```

### 6.2 Import ke MetaMask

1. Klik icon akun di MetaMask
2. Pilih **Import account**
3. Pilih type: **Private Key**
4. Paste private key (tanpa `0x` prefix atau dengan, keduanya bisa)
5. Klik **Import**

### 6.3 Verifikasi

Setelah import:

- Akun baru muncul di MetaMask
- Balance: 10000 ETH (test ETH)
- Network: Hardhat Local

```
┌─────────────────────────────────────────┐
│              MetaMask                   │
├─────────────────────────────────────────┤
│  Network: Hardhat Local                 │
│                                         │
│  Account 2 (Imported)                   │
│  0xf39F...2266                          │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │         10000 ETH                │   │
│  │         (Test ETH)               │   │
│  └──────────────────────────────────┘   │
│                                         │
│  [Send] [Swap] [Bridge] [Buy]           │
└─────────────────────────────────────────┘
```

## 7. Interaksi dengan Contract

### 7.1 Opsi Interaksi

| Opsi                       | Keterangan            | Cocok untuk  |
| -------------------------- | --------------------- | ------------ |
| **Remix + MetaMask** | Visual, familiar      | Pembelajaran |
| **Hardhat Console**  | CLI interaktif        | Developer    |
| **Script**           | Automated, repeatable | Production   |

### 7.2 Interaksi via Remix + MetaMask

**Step 1: Buka Remix**

Akses https://remix.ethereum.org

**Step 2: Paste Contract**

1. Buat file baru: `CourseReward.sol`
2. Paste kode contract dari project Hardhat

**Step 3: Compile**

1. Buka tab **Solidity Compiler**
2. Pilih versi compiler yang sesuai (0.8.20)
3. Klik **Compile CourseReward.sol**

**Step 4: Connect MetaMask**

1. Buka tab **Deploy & Run Transactions**
2. Environment: pilih **Injected Provider - MetaMask**
3. MetaMask popup akan muncul - klik **Connect**

```
┌─────────────────────────────────────────────────────────────────┐
│               REMIX - DEPLOY & RUN                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Environment:                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Injected Provider - MetaMask                              ▼ ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  Account:                                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 0xf39F...2266 (10000 ether)                                 ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  Contract:                                                      │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ CourseReward                                              ▼ ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  At Address: [                              ] [At Address]      │
│              └── Masukkan contract address hasil deploy         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Step 5: Load Contract yang Sudah Deploy**

1. Masukkan contract address dari hasil deploy sebelumnya
2. Klik **At Address**
3. Contract akan muncul di bagian **Deployed Contracts**

**Step 6: Interaksi**

```
┌─────────────────────────────────────────────────────────────────┐
│  ▼ COURSEREWARD AT 0x5FbD...0aa3 (HARDHAT LOCAL)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  READ FUNCTIONS (Blue - No Gas):                                │
│  ┌──────────────────┐                                           │
│  │ rewardAmount     │ → 100                                     │
│  │ owner            │ → 0xf39F...2266                           │
│  │ getMyReward      │ → 0                                       │
│  │ hasClaimed [addr]│ → false                                   │
│  └──────────────────┘                                           │
│                                                                 │
│  WRITE FUNCTIONS (Orange - Requires Gas):                       │
│  ┌──────────────────┐                                           │
│  │ claimReward      │ [transact] ← Klik untuk claim             │
│  │ setRewardAmount  │ [200] [transact]                          │
│  └──────────────────┘                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 Demo: Claim Reward

1. Pastikan account di Remix adalah `student` (bukan owner)
2. Klik **claimReward**
3. MetaMask popup muncul untuk konfirmasi transaksi
4. Review gas fee
5. Klik **Confirm**
6. Tunggu transaksi selesai
7. Cek `hasClaimed` - sekarang `true`
8. Cek `rewards` - sekarang `100`

### 7.4 Memahami Transaction

Setelah transaksi berhasil, perhatikan:

| Info                       | Penjelasan                 |
| -------------------------- | -------------------------- |
| **Transaction Hash** | ID unik transaksi          |
| **From**             | Address pengirim transaksi |
| **To**               | Address contract           |
| **Gas Used**         | Jumlah gas yang digunakan  |
| **Status**           | Success / Failed           |

## 8. Interaksi via Script

### 8.1 Buat Script Interaksi

Untuk interaksi yang lebih programmatic, buat `scripts/interact.js`:

```javascript
const hre = require("hardhat");

async function main() {
  // Ganti dengan address contract hasil deploy
  const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

  // Ambil contract instance
  const CourseReward = await hre.ethers.getContractFactory("CourseReward");
  const courseReward = CourseReward.attach(contractAddress);

  // Ambil signers
  const [owner, student1, student2] = await hre.ethers.getSigners();

  console.log("=== CourseReward Interaction ===\n");

  // Baca state awal
  console.log("Owner:", await courseReward.owner());
  console.log("Reward Amount:", await courseReward.rewardAmount());
  console.log("Student1 hasClaimed:", await courseReward.hasClaimed(student1.address));

  // Student1 claim reward
  console.log("\n--- Student1 claiming reward ---");
  const tx = await courseReward.connect(student1).claimReward();
  await tx.wait();
  console.log("Transaction hash:", tx.hash);

  // Cek state setelah claim
  console.log("\n--- After claim ---");
  console.log("Student1 hasClaimed:", await courseReward.hasClaimed(student1.address));
  console.log("Student1 rewards:", await courseReward.rewards(student1.address));

  // Owner ubah reward amount
  console.log("\n--- Owner changing reward amount ---");
  const tx2 = await courseReward.setRewardAmount(200);
  await tx2.wait();
  console.log("New reward amount:", await courseReward.rewardAmount());

  console.log("\n=== Done ===");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

### 8.2 Jalankan Script

```bash
npx hardhat run scripts/interact.js --network localhost
```

**Output:**

```text
=== CourseReward Interaction ===

Owner: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
Reward Amount: 100
Student1 hasClaimed: false

--- Student1 claiming reward ---
Transaction hash: 0x1234567890abcdef...

--- After claim ---
Student1 hasClaimed: true
Student1 rewards: 100

--- Owner changing reward amount ---
New reward amount: 200

=== Done ===
```

### 8.3 Hardhat Console (Alternatif)

Untuk interaksi interaktif:

```bash
npx hardhat console --network localhost
```

Di dalam console:

```javascript
// Get contract
const CourseReward = await ethers.getContractFactory("CourseReward");
const reward = CourseReward.attach("0x5FbDB2315678afecb367f032d93F642f64180aa3");

// Read state
await reward.rewardAmount();
await reward.owner();

// Get signers
const [owner, student] = await ethers.getSigners();

// Claim reward
await reward.connect(student).claimReward();

// Check result
await reward.hasClaimed(student.address);

// Exit
.exit
```

## 9. Troubleshooting

### 9.1 Masalah Umum

| Masalah                      | Penyebab                      | Solusi                        |
| ---------------------------- | ----------------------------- | ----------------------------- |
| **Saldo tidak muncul** | Network salah                 | Cek RPC URL dan Chain ID      |
| **Transaksi gagal**    | Contract address salah        | Pastikan address benar        |
| **Nonce too high**     | Cache transaksi tidak sinkron | Reset account di MetaMask     |
| **Insufficient funds** | Gas tidak cukup               | Pastikan akun punya ETH       |
| **Network not found**  | Hardhat node tidak berjalan   | Jalankan `npx hardhat node` |

### 9.2 Reset MetaMask Account

Jika muncul error "Nonce too high":

1. Buka MetaMask Settings
2. Advanced
3. Clear activity tab data (atau Reset account)

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESET METAMASK                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Kapan perlu reset:                                             │
│  - Restart Hardhat node (nonce reset ke 0)                      │
│  - Error "nonce too high"                                       │
│  - Transaksi stuck                                              │
│                                                                 │
│  Cara reset:                                                    │
│  Settings → Advanced → Clear activity tab data                  │
│                                                                 │
│  ⚠️  Ini hanya clear history, tidak menghapus balance           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.3 Chain ID Error

Jika muncul error terkait Chain ID:

1. Pastikan Chain ID di MetaMask sesuai:
   - Hardhat: 31337
   - Ganache: 1337
2. Hapus network dan tambahkan ulang

---

## Tugas

### Tugas 1: Deploy Contract Anda

1. Buat deployment script untuk contract project Anda
2. Deploy ke Hardhat Node
3. Catat contract address

### Tugas 2: Setup MetaMask

1. Tambahkan network Hardhat Local ke MetaMask
2. Import minimal 2 akun dari Hardhat Node
3. Screenshot MetaMask dengan saldo test ETH

### Tugas 3: Interaksi via Remix

1. Load contract di Remix dengan "At Address"
2. Panggil minimal 3 function berbeda
3. Screenshot setiap transaksi yang berhasil

### Tugas 4: Script Interaksi

1. Buat script `interact.js` untuk contract Anda
2. Script harus mencakup:
   - Membaca state awal
   - Melakukan minimal 2 transaksi
   - Membaca state akhir
3. Screenshot output script

### Deliverable

Kumpulkan:

1. Screenshot Hardhat node berjalan
2. Screenshot hasil deployment (dengan contract address)
3. Screenshot MetaMask terhubung ke local network
4. Screenshot transaksi berhasil (minimal 2)
5. Screenshot state contract berubah
6. File `scripts/deploy.js` dan `scripts/interact.js`

---

## 10. Latihan Tambahan

### 10.1 Project: SimpleStorage

Sebagai latihan tambahan, buat contract sederhana untuk menyimpan dan membaca angka:

**contracts/SimpleStorage.sol:**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleStorage {
    uint256 private storedNumber;

    event NumberChanged(uint256 oldValue, uint256 newValue);

    function store(uint256 _number) public {
        uint256 oldValue = storedNumber;
        storedNumber = _number;
        emit NumberChanged(oldValue, _number);
    }

    function retrieve() public view returns (uint256) {
        return storedNumber;
    }
}
```

**Test:**

```javascript
const { expect } = require("chai");

describe("SimpleStorage", function () {
  it("should store and retrieve a number", async function () {
    const SimpleStorage = await ethers.getContractFactory("SimpleStorage");
    const storage = await SimpleStorage.deploy();

    await storage.store(42);
    expect(await storage.retrieve()).to.equal(42);
  });
});
```

### 10.2 Project: SimpleToken (Mini)

Contract token sederhana untuk latihan transfer:

**contracts/SimpleToken.sol:**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleToken {
    string public name = "SimpleToken";
    string public symbol = "STK";
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(uint256 _initialSupply) {
        totalSupply = _initialSupply;
        balanceOf[msg.sender] = _initialSupply;
    }

    function transfer(address _to, uint256 _value) public returns (bool) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
}
```

### 10.3 Langkah Latihan

1. Compile kedua contract
2. Tulis test untuk masing-masing (minimal 3 test case)
3. Deploy ke Hardhat Node
4. Interaksi via Remix + MetaMask
5. Screenshot bukti transaksi berhasil

## Referensi

- [Hardhat Network Documentation](https://hardhat.org/hardhat-network/docs/overview)
- [Hardhat Deploying Contracts](https://hardhat.org/tutorial/deploying-to-a-live-network)
- [MetaMask Development Network Guide](https://docs.metamask.io/wallet/how-to/run-devnet/)
- [Ganache Documentation](https://trufflesuite.com/docs/ganache/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts) - untuk pengembangan lanjutan
