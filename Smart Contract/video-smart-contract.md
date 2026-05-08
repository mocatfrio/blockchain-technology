# Rancangan Video Pembelajaran Smart Contract

## Pemetaan Video dengan Modul

| Video | Judul | Modul | Minggu |
|-------|-------|-------|--------|
| **Video 7** | Setup Project Smart Contract dengan Hardhat dan Compile Contract | [Module 09](../module-09.md) | 9 |
| **Video 8** | Unit Testing Smart Contract dengan Hardhat | [Module 10](../module-10.md) | 10 |
| **Video 9** | Deploy Smart Contract dan Interaksi Menggunakan MetaMask | [Module 11](../module-11.md) | 10 |

**Catatan:** Setelah menyelesaikan ketiga video dan modul ini, mahasiswa siap untuk **Demo Proyek 3: Smart Contract** di Minggu 11.

---

# Video 7 — Hardhat Project Setup + Compile

## Judul video

> **Video 7: Setup Project Smart Contract dengan Hardhat dan Compile Contract**

## Tujuan pembelajaran

Setelah video ini, mahasiswa mampu:

1. Membuat project Hardhat.
2. Memahami struktur folder project smart contract.
3. Memindahkan contract dari Remix ke project lokal.
4. Menjalankan compile.
5. Memahami output compile seperti ABI, bytecode, dan artifacts.

## Durasi ideal

**20–30 menit.**

Kalau angka “24” yang Bapak/Ibu tulis berarti durasi, maka video ini cocok dibuat sekitar  **24 menit** .

---

## Outline video

### 1. Pembuka dan konteks

Durasi: 2 menit.

Narasi:

```text
Pada pertemuan offline, kita sudah membahas konsep smart contract dan mencoba demo di Remix.
Di video ini, kita tidak mengulang konsep dasar Solidity.
Fokus kita adalah membuat project smart contract menggunakan Hardhat.
```

Tekankan:

```text
Remix cocok untuk belajar cepat.
Hardhat cocok untuk project yang lebih rapi, bisa ditest, dideploy, dan dikembangkan.
```

---

### 2. Persiapan tools

Durasi: 3–4 menit.

Yang perlu disebut:

```text
1. Node.js
2. npm
3. VS Code
4. Terminal
5. Hardhat
```

Contoh command:

```bash
node -v
npm -v
```

Lalu buat folder:

```bash
mkdir project2-smart-contract
cd project2-smart-contract
npm init -y
npm install --save-dev hardhat
npx hardhat --init
```

Catatan: di versi Hardhat terbaru, dokumentasi resminya memakai inisialisasi project dengan `npx hardhat --init`. ([hardhat.org](https://hardhat.org/hardhat-runner/docs/getting-started?utm_source=chatgpt.com "Getting started with Hardhat | Ethereum development ..."))

Pilih opsi saat init:

```text
? What do you want to do? Create a JavaScript project
? Hardhat project root: (tekan Enter)
? Do you want to add a .gitignore? Yes
? Do you want to install this sample project's dependencies with npm? Yes
```

### 3. Jelaskan struktur project

Durasi: 4–5 menit.

Tampilkan struktur folder:

```text
project2-smart-contract/
├── contracts/
│   └── CourseReward.sol
├── test/
├── ignition/ atau scripts/
├── hardhat.config.js
├── package.json
└── README.md
```

Penjelasan singkat:

| Folder/File                | Fungsi                                   |
| -------------------------- | ---------------------------------------- |
| `contracts/`             | Tempat file smart contract Solidity      |
| `test/`                  | Tempat unit test smart contract          |
| `scripts/`/`ignition/` | Tempat script atau module deployment     |
| `hardhat.config.js`      | Konfigurasi Hardhat                      |
| `artifacts/`             | Hasil compile, termasuk ABI dan bytecode |

Jangan terlalu teoritis. Cukup tekankan bahwa struktur ini akan dipakai sampai Project 3.

---

### 3b. Jelaskan hardhat.config.js

Durasi: 2-3 menit.

Tampilkan file `hardhat.config.js`:

```javascript
require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.20",
  networks: {
    localhost: {
      url: "http://127.0.0.1:8545"
    },
    // Untuk Ganache (opsional)
    ganache: {
      url: "http://127.0.0.1:7545",
      chainId: 1337
    }
  }
};
```

Jelaskan singkat:

| Bagian | Fungsi |
|--------|--------|
| `solidity` | Versi compiler Solidity |
| `networks` | Daftar blockchain yang bisa diakses |
| `localhost` | Hardhat Network (port 8545) |
| `ganache` | Ganache GUI (port 7545) |

---

### 4. Masukkan smart contract

Durasi: 5–6 menit.

Gunakan contract sederhana yang sudah nyambung dengan materi sebelumnya.

Contoh nama:

```text
CourseReward.sol
```

Fitur contract:

```text
1. Owner/dosen
2. Reward amount
3. Mahasiswa bisa claim reward
4. Mahasiswa hanya bisa claim sekali
5. Owner bisa mengubah reward amount
6. Event saat reward diklaim
```

Struktur minimal:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CourseReward {
    address public owner;
    uint256 public rewardAmount;

    mapping(address => uint256) public rewards;
    mapping(address => bool) public hasClaimed;

    event RewardClaimed(address indexed student, uint256 amount);
    event RewardAmountChanged(uint256 newAmount);

    constructor(uint256 _rewardAmount) {
        owner = msg.sender;
        rewardAmount = _rewardAmount;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    function claimReward() public {
        require(!hasClaimed[msg.sender], "Reward already claimed");

        rewards[msg.sender] += rewardAmount;
        hasClaimed[msg.sender] = true;

        emit RewardClaimed(msg.sender, rewardAmount);
    }

    function setRewardAmount(uint256 _newAmount) public onlyOwner {
        rewardAmount = _newAmount;
        emit RewardAmountChanged(_newAmount);
    }

    function getMyReward() public view returns (uint256) {
        return rewards[msg.sender];
    }
}
```

Narasi:

```text
Kita tidak akan membahas semua syntax dari awal, karena konsepnya sudah dibahas offline.
Sekarang fokus kita adalah bagaimana contract ini dikelola di project Hardhat.
```

---

### 5. Compile contract

Durasi: 4–5 menit.

Command:

```bash
npx hardhat compile
```

Jelaskan output:

```text
Compiled successfully
```

Lalu buka folder:

```text
artifacts/contracts/CourseReward.sol/CourseReward.json
```

Jelaskan singkat:

| Output    | Arti                                                   |
| --------- | ------------------------------------------------------ |
| ABI       | Interface agar aplikasi/script bisa memanggil contract |
| Bytecode  | Kode yang akan dideploy ke blockchain                  |
| Artifacts | File hasil compile dari Hardhat                        |

---

### 6. Error compile umum

Durasi: 3–4 menit.

Tampilkan contoh error kecil:

```text
1. Salah nama file
2. Salah versi Solidity
3. Kurang titik koma
4. Typo nama function
5. Contract name tidak sesuai
```

Tujuannya agar mahasiswa tidak panik saat error.

---

## Output akhir Video 7

Mahasiswa harus punya:

```text
1. Project Hardhat berhasil dibuat
2. File CourseReward.sol ada di folder contracts/
3. Compile berhasil
4. Folder artifacts muncul
```

## Tugas setelah Video 7

Mahasiswa mengumpulkan:

```text
1. Screenshot hasil npx hardhat compile
2. Screenshot struktur folder project
3. Commit awal ke GitHub
```

---

# Video 8 — Smart Contract Testing

## Judul video

> **Video 8: Unit Testing Smart Contract dengan Hardhat**

## Tujuan pembelajaran

Setelah video ini, mahasiswa mampu:

1. Menulis test untuk smart contract.
2. Menguji skenario berhasil.
3. Menguji skenario gagal.
4. Menguji access control.
5. Membuktikan bahwa contract benar, bukan hanya “bisa jalan”.

## Durasi ideal

**30–40 menit.**

Video ini sebaiknya sedikit lebih panjang daripada Video 7 karena testing adalah kompetensi penting Project 2.

---

## Outline video

### 1. Pembuka: kenapa testing penting?

Durasi: 3 menit.

Narasi:

```text
Di Remix, kita biasanya klik function satu per satu.
Masalahnya, cara manual sulit diulang dan mudah lupa.
Dengan Hardhat test, kita bisa membuat skenario otomatis untuk membuktikan smart contract berjalan sesuai aturan.
```

Tekankan:

```text
Smart contract harus diuji sebelum dideploy, karena bug smart contract bisa sulit diperbaiki setelah berada di blockchain.
```

Hardhat menyediakan dukungan testing sebagai bagian inti dari tutorial resminya, termasuk menulis dan menjalankan test untuk contract yang sudah dicompile. ([hardhat.org](https://hardhat.org/docs/tutorial/writing-and-testing?utm_source=chatgpt.com "Writing and testing a Solidity contract"))

---

### 2. Buat file test

Durasi: 3–4 menit.

Buat file:

```text
test/CourseReward.js
```

Struktur awal:

```javascript
const { expect } = require("chai");

describe("CourseReward", function () {
  // test akan ditulis di sini
});
```

Jelaskan:

| Bagian         | Fungsi                        |
| -------------- | ----------------------------- |
| `describe`   | Kelompok test                 |
| `it`         | Satu test case                |
| `expect`     | Assertion/pengecekan hasil    |
| `beforeEach` | Setup ulang sebelum tiap test |

---

### 3. Setup deployment di dalam test

Durasi: 5 menit.

Contoh:

```javascript
const { expect } = require("chai");

describe("CourseReward", function () {
  let reward;
  let owner;
  let student1;
  let student2;

  beforeEach(async function () {
    [owner, student1, student2] = await ethers.getSigners();

    const CourseReward = await ethers.getContractFactory("CourseReward");
    reward = await CourseReward.deploy(100);
  });

  it("should deploy successfully", async function () {
    expect(await reward.rewardAmount()).to.equal(100);
  });
});
```

Jelaskan:

```text
getSigners() memberi kita beberapa akun testing.
owner adalah akun pertama.
student1 dan student2 digunakan untuk simulasi user berbeda.
```

---

### 4. Test deployment dan owner

Durasi: 5 menit.

Test:

```javascript
it("should set the correct owner", async function () {
  expect(await reward.owner()).to.equal(owner.address);
});
```

Jelaskan:

```text
Ketika contract dideploy, msg.sender di constructor adalah owner.
```

---

### 5. Test fungsi utama: claimReward

Durasi: 5–6 menit.

Test:

```javascript
it("should allow student to claim reward", async function () {
  await reward.connect(student1).claimReward();

  expect(await reward.rewards(student1.address)).to.equal(100);
  expect(await reward.hasClaimed(student1.address)).to.equal(true);
});
```

Jelaskan:

```text
connect(student1) berarti transaksi dikirim dari wallet student1, bukan dari owner.
```

---

### 6. Test skenario gagal: tidak boleh claim dua kali

Durasi: 5 menit.

Test:

```javascript
it("should not allow student to claim twice", async function () {
  await reward.connect(student1).claimReward();

  await expect(
    reward.connect(student1).claimReward()
  ).to.be.revertedWith("Reward already claimed");
});
```

Jelaskan:

```text
Test yang baik tidak hanya mengecek skenario sukses, tetapi juga skenario gagal.
```

---

### 7. Test access control

Durasi: 5 menit.

Test owner boleh mengubah reward:

```javascript
it("should allow owner to change reward amount", async function () {
  await reward.setRewardAmount(200);
  expect(await reward.rewardAmount()).to.equal(200);
});
```

Test non-owner tidak boleh:

```javascript
it("should reject non-owner changing reward amount", async function () {
  await expect(
    reward.connect(student1).setRewardAmount(200)
  ).to.be.revertedWith("Only owner can call this function");
});
```

---

### 8. Test event

Durasi: 4–5 menit.

Jika waktu cukup, tambahkan:

```javascript
it("should emit RewardClaimed event", async function () {
  await expect(reward.connect(student1).claimReward())
    .to.emit(reward, "RewardClaimed")
    .withArgs(student1.address, 100);
});
```

Ini bagus karena mengajarkan bahwa event bisa dipakai untuk mencatat aktivitas penting.

---

### 9. Jalankan test

Durasi: 2–3 menit.

Command:

```bash
npx hardhat test
```

Output yang diharapkan:

```text
6 passing
```

---

### 10. Test coverage (opsional)

Durasi: 2-3 menit.

Jika waktu cukup, tunjukkan cara cek test coverage:

```bash
npx hardhat coverage
```

Output:

```text
------------------|----------|----------|----------|----------|
File              |  % Stmts | % Branch |  % Funcs |  % Lines |
------------------|----------|----------|----------|----------|
 CourseReward.sol |      100 |      100 |      100 |      100 |
------------------|----------|----------|----------|----------|
All files         |      100 |      100 |      100 |      100 |
------------------|----------|----------|----------|----------|
```

Jelaskan:

```text
Coverage menunjukkan berapa persen kode yang sudah diuji.
Target ideal adalah 80-100% coverage.
```

---

## Test case wajib mahasiswa

Minimal mahasiswa harus punya 5 test:

| No | Test Case                         | Wajib |
| -: | --------------------------------- | ----: |
|  1 | Contract berhasil deploy          |    Ya |
|  2 | Owner benar                       |    Ya |
|  3 | Student bisa claim reward         |    Ya |
|  4 | Student tidak bisa claim dua kali |    Ya |
|  5 | Non-owner tidak bisa ubah reward  |    Ya |
|  6 | Event muncul saat claim           | Bonus |

---

## Output akhir Video 8

Mahasiswa harus punya:

```text
1. File test/CourseReward.js
2. Minimal 5 test case
3. Semua test lulus
4. Screenshot hasil npx hardhat test
```

## Tugas setelah Video 8

Mahasiswa mengumpulkan:

```text
1. Screenshot hasil test
2. File test yang sudah dibuat
3. Tambahan minimal 1 test case buatan sendiri
```

---

# Video 9 — Deployment + Interaksi dengan MetaMask

## Judul video

> **Video 9: Deploy Smart Contract dan Interaksi Menggunakan MetaMask**

## Tujuan pembelajaran

Setelah video ini, mahasiswa mampu:

1. Menjalankan local blockchain dengan Hardhat.
2. Deploy contract ke local network.
3. Menghubungkan MetaMask ke local network.
4. Import akun development.
5. Melakukan transaksi smart contract menggunakan wallet.
6. Memahami transaction hash dan perubahan state.

## Durasi ideal

**30–40 menit.**

---

## Outline video

### 1. Pembuka: dari testing ke deployment

Durasi: 2 menit.

Narasi:

```text
Di Video 8, kita sudah membuktikan contract berjalan dengan test.
Sekarang kita akan menjalankan blockchain lokal, deploy contract, lalu mencoba transaksi menggunakan MetaMask.
```

Tekankan:

```text
Project 2 belum membuat frontend dApp.
Frontend dApp akan masuk ke Project 3.
Di sini MetaMask dipakai untuk memahami transaksi dan wallet signing.
```

---

### 2. Jalankan local blockchain

Durasi: 5–6 menit.

Ada 2 opsi local blockchain:

| Opsi | Command | Port | Kelebihan |
|------|---------|------|-----------|
| **Hardhat Node** | `npx hardhat node` | 8545 | Terintegrasi dengan Hardhat |
| **Ganache** | Buka aplikasi GUI | 7545 | Visual, mudah dipahami |

**Opsi A: Hardhat Node**

```bash
npx hardhat node
```

Output:

```text
Started HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545/

Accounts
========
Account #0: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 (10000 ETH)
Private Key: 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
...
```

**Opsi B: Ganache (Alternatif)**

```text
1. Buka aplikasi Ganache
2. Klik Quickstart Ethereum
3. Lihat daftar 10 akun dengan masing-masing 100 ETH
4. Catat RPC Server: HTTP://127.0.0.1:7545
```

Tampilan Ganache:

```text
┌─────────────────────────────────────────────────────────────┐
│  GANACHE                                                    │
│  RPC SERVER: HTTP://127.0.0.1:7545                          │
│  NETWORK ID: 1337                                           │
├─────────────────────────────────────────────────────────────┤
│  ACCOUNTS                                                   │
│  0x... (100 ETH)  [Show Keys]                               │
│  0x... (100 ETH)  [Show Keys]                               │
│  ...                                                        │
└─────────────────────────────────────────────────────────────┘
```

Jelaskan:

```text
Hardhat node atau Ganache menjalankan blockchain lokal di komputer kita.
Akun-akun testing dan private key akan muncul.
ETH yang muncul adalah test ETH lokal, bukan ETH asli.
```

Hardhat Network memang disediakan sebagai local Ethereum network untuk deploy, testing, dan debugging di mesin lokal. ([hardhat.org](https://hardhat.org/hardhat-network?utm_source=chatgpt.com "Hardhat Network | Ethereum development environment for ..."))

---

### 3. Buat deployment script

Durasi: 6–8 menit.

Buat file:

```text
scripts/deploy.js
```

Contoh:

```javascript
const hre = require("hardhat");

async function main() {
  const CourseReward = await hre.ethers.getContractFactory("CourseReward");
  const reward = await CourseReward.deploy(100);

  await reward.waitForDeployment();

  console.log("CourseReward deployed to:", await reward.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

Jelaskan:

| Baris                   | Makna                                   |
| ----------------------- | --------------------------------------- |
| `getContractFactory`  | Mengambil contract yang sudah dicompile |
| `deploy(100)`         | Deploy contract dengan reward awal 100  |
| `waitForDeployment()` | Menunggu deployment selesai             |
| `getAddress()`        | Mengambil address contract              |

---

### 4. Deploy ke local network

Durasi: 4–5 menit.

Buka terminal kedua, lalu jalankan:

**Jika pakai Hardhat Node:**

```bash
npx hardhat run scripts/deploy.js --network localhost
```

**Jika pakai Ganache:**

```bash
npx hardhat run scripts/deploy.js --network ganache
```

Output:

```text
CourseReward deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3
```

Mahasiswa wajib mencatat:

```text
Contract address
```

Karena address ini akan dipakai untuk interaksi.

**Di Ganache GUI:**

Jika menggunakan Ganache, tunjukkan bahwa:

```text
1. Tab "Transactions" menampilkan transaksi deployment
2. Tab "Blocks" menampilkan block baru
3. Saldo ETH akun deployer berkurang sedikit (gas fee)
```

---

### 5. Hubungkan MetaMask ke local network

Durasi: 6–8 menit.

Di MetaMask, tambahkan network lokal:

**Jika pakai Hardhat Node:**

```text
Network Name : Hardhat Local
RPC URL      : http://127.0.0.1:8545
Chain ID     : 31337
Currency     : ETH
```

**Jika pakai Ganache:**

```text
Network Name : Ganache Local
RPC URL      : http://127.0.0.1:7545
Chain ID     : 1337
Currency     : ETH
```

MetaMask memiliki panduan resmi untuk menghubungkan MetaMask ke Hardhat development network, termasuk penggunaan RPC lokal `http://127.0.0.1:8545/` dan seed phrase khusus development. ([MetaMask](https://docs.metamask.io/metamask-connect/evm/guides/best-practices/run-devnet/?utm_source=chatgpt.com "Run a Development Network - MetaMask Connect"))

Tekankan keamanan:

```text
Jangan gunakan wallet utama.
Jangan gunakan seed phrase asli.
Private key dari Hardhat hanya untuk development lokal.
```

MetaMask secara eksplisit menyarankan seed phrase khusus development yang terpisah dari wallet yang menyimpan aset bernilai. ([MetaMask](https://docs.metamask.io/metamask-connect/evm/guides/best-practices/run-devnet/?utm_source=chatgpt.com "Run a Development Network - MetaMask Connect"))

---

### 6. Import akun Hardhat ke MetaMask

Durasi: 4–5 menit.

Langkah:

```text
1. Copy salah satu private key dari terminal Hardhat node
2. Buka MetaMask
3. Import account
4. Paste private key
5. Pastikan saldo test ETH muncul
```

Jelaskan:

```text
Akun ini berasal dari Hardhat local node.
Saldo ETH yang muncul adalah saldo testing lokal.
```

---

### 7. Interaksi dengan contract

Karena belum masuk Project 3 dApp, ada 3 opsi interaksi:

| Opsi                               | Keterangan                       |
| ---------------------------------- | -------------------------------- |
| Hardhat console                    | Developer-oriented               |
| Script interact.js                 | Rapi dan bisa diulang            |
| Remix + Injected Provider MetaMask | Visual dan mudah untuk mahasiswa |

Untuk video ini, saya sarankan gunakan:

```text
Deploy pakai Hardhat
Interaksi visual pakai Remix + MetaMask
```

Alasannya: mahasiswa sudah familiar dengan Remix dari sesi offline.

---

## Opsi interaksi yang direkomendasikan: Remix + MetaMask

Durasi: 8–10 menit.

Langkah:

```text
1. Buka Remix
2. Paste contract CourseReward.sol
3. Compile dengan versi Solidity yang sesuai
4. Di Deploy & Run Transactions, pilih Injected Provider - MetaMask
5. Pastikan network MetaMask adalah Hardhat Local
6. Masukkan contract address hasil deploy
7. Klik At Address
8. Panggil function contract
```

Demo function:

```text
1. rewardAmount()
2. getMyReward()
3. claimReward()
4. hasClaimed(address)
5. rewards(address)
```

Saat `claimReward()` dipanggil:

```text
1. MetaMask menampilkan konfirmasi transaksi
2. User klik Confirm
3. Transaksi diproses
4. State contract berubah
```

Tampilkan transaction hash dari MetaMask.

---

### 7b. Alternatif: Interaksi dengan Script (Opsional)

Durasi: 5-7 menit (jika waktu cukup).

Jika ingin menunjukkan cara developer, buat file `scripts/interact.js`:

```javascript
const hre = require("hardhat");

async function main() {
  // Ganti dengan address contract hasil deploy
  const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

  // Ambil contract instance
  const CourseReward = await hre.ethers.getContractFactory("CourseReward");
  const reward = CourseReward.attach(contractAddress);

  // Ambil signers (akun)
  const [owner, student1] = await hre.ethers.getSigners();

  console.log("=== CourseReward Interaction ===\n");

  // Baca state awal
  console.log("Owner:", await reward.owner());
  console.log("Reward Amount:", await reward.rewardAmount());

  // Student1 claim reward
  console.log("\nStudent1 claiming reward...");
  const tx = await reward.connect(student1).claimReward();
  await tx.wait();

  // Cek hasil
  console.log("Student1 reward:", await reward.rewards(student1.address));
  console.log("Student1 hasClaimed:", await reward.hasClaimed(student1.address));

  console.log("\n=== Done ===");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

Jalankan:

```bash
npx hardhat run scripts/interact.js --network localhost
```

Output:

```text
=== CourseReward Interaction ===

Owner: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
Reward Amount: 100

Student1 claiming reward...
Student1 reward: 100
Student1 hasClaimed: true

=== Done ===
```

Jelaskan:

```text
Script ini berguna untuk automasi atau testing cepat.
Di Project 3 nanti, logika ini akan dipindah ke frontend React.
```

---

### 8. Troubleshooting singkat

Durasi: 3–4 menit.

Masalah umum:

| Masalah                       | Solusi                                          |
| ----------------------------- | ----------------------------------------------- |
| Saldo tidak muncul            | Cek network RPC dan chain ID                    |
| Transaksi gagal               | Pastikan contract address benar                 |
| MetaMask nonce error          | Reset account di MetaMask                       |
| Salah network                 | Pindah ke Hardhat Local                         |
| Contract tidak bisa dipanggil | Pastikan ABI/contract sama dengan yang dideploy |

Catatan khusus: Hardhat pernah mendokumentasikan isu chain ID dengan MetaMask dan memberi solusi konfigurasi jika muncul error terkait EIP-155 atau chain ID. ([hardhat.org](https://hardhat.org/hardhat-network/docs/metamask-issue?utm_source=chatgpt.com "MetaMask chainId issue | Ethereum development ..."))

---

## Output akhir Video 9

Mahasiswa harus punya:

```text
1. Hardhat node berjalan
2. Contract berhasil dideploy ke localhost
3. Contract address tercatat
4. MetaMask terhubung ke Hardhat Local
5. Akun Hardhat berhasil diimport
6. Transaksi claimReward berhasil
7. Transaction hash muncul
8. State rewards berubah
```

## Tugas setelah Video 9

Mahasiswa mengumpulkan:

```text
1. Screenshot Hardhat node berjalan
2. Screenshot hasil deployment contract
3. Screenshot MetaMask terhubung ke Hardhat Local
4. Screenshot transaksi berhasil
5. Screenshot hasil state berubah, misalnya hasClaimed = true atau rewards = 100
```

---

# Ringkasan 3 Video

| No | Video                           | Fokus                                              | Output                       |
| -: | ------------------------------- | -------------------------------------------------- | ---------------------------- |
|  7 | Hardhat project setup + compile | Membuat project lokal dan compile contract         | Project Hardhat siap         |
|  8 | Smart Contract Testing          | Membuktikan logic contract dengan unit test        | Semua test lulus             |
|  9 | Deployment + MetaMask           | Deploy ke local network dan transaksi pakai wallet | Contract bisa diinteraksikan |

---

# Deliverable Project 2 Setelah 3 Video

Setelah menyelesaikan Video 7–9, mahasiswa sudah siap submit Project 2 dengan isi:

```text
project2-smart-contract/
├── contracts/
│   └── CourseReward.sol
├── test/
│   └── CourseReward.js
├── scripts/
│   └── deploy.js
├── hardhat.config.js
├── package.json
└── README.md
```

Yang dikumpulkan:

| Deliverable         | Keterangan               |
| ------------------- | ------------------------ |
| GitHub repository   | Berisi project Hardhat   |
| Smart contract      | Minimal 1 contract utama |
| Unit test           | Minimal 5 test case      |
| Deployment script   | Bisa deploy ke localhost |
| Screenshot compile  | Bukti Video 7            |
| Screenshot test     | Bukti Video 8            |
| Screenshot deploy   | Bukti Video 9            |
| Screenshot MetaMask | Bukti interaksi wallet   |
| README              | Cara menjalankan project |

---

# Narasi Benang Merah untuk Mahasiswa

Bapak/Ibu bisa membuka seri ini dengan kalimat:

```text
Pada Project 1, kita membuat blockchain sederhana dengan Python.
Pada sesi offline, kita sudah mengenal smart contract dan Remix.
Sekarang di Project 2, kita belajar workflow developer smart contract yang lebih profesional:
menulis contract, compile, testing, deploy, dan transaksi menggunakan MetaMask.
Frontend dApp belum kita buat sekarang, karena itu akan menjadi Project 3.
```

Dengan rancangan ini, Project 2 tetap fokus pada  **smart contract engineering** , bukan frontend.
