# Blockchain Technology

Blockchain technology is a database mechanism that enables transparent information sharing within a business network by creating a decentralized, immutable system for recording transactions. This technology has been widely used across various sectors, including the creation of digital currencies such as Bitcoin and the Development of Smart Contracts. This course provides an understanding of the basic theories and concepts of Blockchain, Cryptocurrency, and Smart Contract technology. At the end of the lecture, students are expected to be able to implement Blockchain, Cryptocurrency, and Smart Contract technology.

## Course Learning Outcomes

1. Students are able to **design and implement the fundamental concepts of blockchain**, including distributed ledger architecture and cryptographic mechanisms that ensure data integrity
2. Students are able to **design and implement consensus mechanisms, cryptocurrency transaction structures, and network security mitigation strategies**
3. Students are able to **develop and deploy smart contracts on modern blockchain platforms** to automate business processes
4. Students are able to **integrate blockchain technology into real-world applications** (e.g., cybersecurity, supply chain, or finance) and develop a **prototype decentralized application (dApp)**

## Tools

- Python
- Solidity
- Remix IDE
- Hardhat 3 (dengan Hardhat Ignition)
- Ganache
- MetaMask
- Ethers.js v6

### Catatan Hardhat 3

Modul 09-11 dan 15 menggunakan **Hardhat 3** dengan sintaks terbaru:

| Fitur | Hardhat 2 | Hardhat 3 |
|-------|-----------|-----------|
| Config | `HardhatUserConfig` object | `defineConfig()` function |
| Plugins | `import "@plugin"` | `plugins: [plugin]` array |
| Test | `import { ethers } from "hardhat"` | `await network.create()` |
| Fixture | `loadFixture()` dari helpers | `networkHelpers.loadFixture()` |
| Deploy | `await Contract.deploy()` | `await ethers.deployContract()` |
| Env Vars | `process.env.VAR` | `configVariable("VAR")` |
| Deployment | Script manual | **Hardhat Ignition** (recommended) |

Untuk contoh lengkap, lihat [voting-dapp/README.md](voting-dapp/README.md).

## Topics

- Blockchain fundamentals
- Cryptocurrency
- Smart Contracts
- Wallet & dApp Integration

## Modules

| Module | Minggu | Title                               | Sub-CPMK | Link                         |
| ------ | ------ | ----------------------------------- | -------- | ---------------------------- |
| 1      | 1      | Introduction to Python              | 1.1      | [Go to module](module-01.md) |
| 2      | 2      | Blockchain Fundamentals             | 1.2      | [Go to module](module-02.md) |
| 3      | 3      | Advanced Blockchain Concepts        | 1.3      | [Go to module](module-03.md) |
| 4      | 4      | Blockchain Network dengan Flask API | 1.4      | [Go to module](module-04.md) |
| 5      | 5-6    | Cryptocurrency                      | 2.1      | [Go to module](module-05.md) |
| 6      | 5-6    | Advanced Cryptocurrency             | 2.1      | [Go to module](module-06.md) |
| -      | 7      | **Demo Proyek 1: Blockchain & Cryptocurrency** | 1.5, 2.2 | - |
| 7      | 8      | Smart Contracts (Python)            | 3.1      | [Go to module](module-07.md) |
| 8      | 8      | Smart Contract dengan Remix IDE     | 3.1      | [Go to module](module-08.md) |
| 9      | 9-10   | Hardhat Project Setup & Compile     | 3.2      | [Go to module](module-09.md) |
| 10     | 10     | Smart Contract Testing              | 3.3      | [Go to module](module-10.md) |
| 11     | 10     | Deployment & MetaMask Interaction   | 3.3      | [Go to module](module-11.md) |
| -      | 11     | **Demo Proyek 2: Smart Contract**   | 3.4      | - |
| 12     | 12     | Pengenalan dApp & Arsitektur Web3   | 4.1      | [Go to module](module-12.md) |
| 13     | 13     | Frontend Integration - Read Operations | 4.2   | [Go to module](module-13.md) |
| 14     | 14     | Frontend Integration - Write Operations | 4.3  | [Go to module](module-14.md) |
| 15     | 15     | dApp Advanced Features & Deployment | 4.4      | [Go to module](module-15.md) |
| -      | 16     | **Demo Proyek Akhir: dApp**         | 4.5      | - |
| 16     | -      | Smart Contract Security (Supplementary) | 3.x  | [Go to module](module-16.md) |

## Concept Mapping

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    BLOCKCHAIN TECHNOLOGY (16 Minggu)                                   │
│                                                                                                        │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                      FASE 1: BLOCKCHAIN & CRYPTOCURRENCY (Minggu 1-7)                            │  │
│  │                                        CPMK-1 & CPMK-2                                           │  │
│  │                                                                                                  │  │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐    │  │
│  │   │  Module 01  │─►│  Module 02  │─►│  Module 03  │─►│  Module 04  │─►│   Module 05 & 06    │    │  │
│  │   │  Pengantar  │  │  Blockchain │  │  Advanced   │  │   Network   │  │   Cryptocurrency    │    │  │
│  │   │  (Minggu 1) │  │  (Minggu 2) │  │  (Minggu 3) │  │  (Minggu 4) │  │   (Minggu 5-6)      │    │  │
│  │   └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └──────────┬──────────┘    │  │
│  │                                                                                  │               │  │
│  │                                                                                  ▼               │  │
│  │                                                                       ╔═════════════════════╗   │  │
│  │                                                                       ║   DEMO PROYEK 1     ║   │  │
│  │                                                                       ║ Blockchain + Crypto ║   │  │
│  │                                                                       ║    (Minggu 7)       ║   │  │
│  │                                                                       ╚═════════════════════╝   │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                 │                                                      │
│                                                 ▼                                                      │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                          FASE 2: SMART CONTRACT DEVELOPMENT (Minggu 8-11)                        │  │
│  │                                           CPMK-3                                                 │  │
│  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ╔═════════════╗                       │  │
│  │   │ Module 07-08│───►│  Module 09  │───►│Module 10-11 │───►║  DEMO       ║                       │  │
│  │   │ Smart Contr.│    │  Hardhat    │    │Test+Deploy  │    ║  PROYEK 2   ║                       │  │
│  │   │  (Minggu 8) │    │  (Minggu 9) │    │ (Minggu 10) │    ║ (Minggu 11) ║                       │  │
│  │   └─────────────┘    └─────────────┘    └─────────────┘    ╚═════════════╝                       │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                 │                                                      │
│                                                 ▼                                                      │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                           FASE 3: dApp DEVELOPMENT (Minggu 12-16)                                │  │
│  │                                           CPMK-4                                                 │  │
│  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ╔═════════════╗    │  │
│  │   │  Module 12  │───►│  Module 13  │───►│  Module 14  │───►│  Module 15  │───►║  DEMO       ║    │  │
│  │   │ dApp+Web3   │    │ Read Ops    │    │ Write Ops   │    │ Advanced    │    ║  PROYEK 3   ║    │  │
│  │   │ (Minggu 12) │    │ (Minggu 13) │    │ (Minggu 14) │    │ (Minggu 15) │    ║ AKHIR (16)  ║    │  │
│  │   └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    ╚═════════════╝    │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1. Blockchain (Foundation)

| Topic                           | Sub-Topics                               | Module                 |
| ------------------------------- | ---------------------------------------- | ---------------------- |
| **Preparation**           | Python, VS Code Installation             | [Module 01](module-01.md) |
| **Data Structure**        | Block, Chain, Transaction                | [Module 02](module-02.md) |
| **Cryptography**          | Hash (SHA-256), Previous Hash            | [Module 02](module-02.md) |
| **Consensus**             | Proof of Work, Mining, Nonce, Difficulty | [Module 02](module-02.md) |
| **Validation**            | Chain Validation                         | [Module 02](module-02.md) |
| **Merkle Tree**           | Merkle Root, Merkle Proof                | [Module 03](module-03.md) |
| **Mining Reward**         | Coinbase Transaction, Halving            | [Module 03](module-03.md) |
| **Balance Tracking**      | UTXO vs Account Model                    | [Module 03](module-03.md) |
| **Mempool**               | Transaction Priority, Fee                | [Module 03](module-03.md) |
| **Difficulty Adjustment** | Target Block Time                        | [Module 03](module-03.md) |
| **P2P Network**           | Node, Decentralization                   | [Module 04](module-04.md) |
| **REST API**              | Flask, Endpoints                         | [Module 04](module-04.md) |
| **Consensus Algorithm**   | Longest Chain Rule                       | [Module 04](module-04.md) |

### 2. Cryptocurrency (Application)

| Topic                              | Sub-Topics                            | Module                 |
| ---------------------------------- | ------------------------------------- | ---------------------- |
| **Digital Signature**        | Asymmetric Cryptography, RSA          | [Module 05](module-05.md) |
| **Wallet**                   | Private Key, Public Key, Keypair      | [Module 05](module-05.md) |
| **Transaction Verification** | Sign, Verify                          | [Module 05](module-05.md) |
| **Multi-Node Network**       | Network Simulation                    | [Module 05](module-05.md) |
| **Double Spending**          | Prevention Mechanism                  | [Module 06](module-06.md) |
| **Transaction Broadcasting** | Propagation                           | [Module 06](module-06.md) |
| **Block Confirmation**       | Confirmation Count, Security Level    | [Module 06](module-06.md) |
| **UTXO Model**               | Input, Output, Change                 | [Module 06](module-06.md) |
| **ECDSA**                    | Elliptic Curve Digital Signature      | [Module 06](module-06.md) |
| **Address Format**           | Base58Check, Version Byte             | [Module 06](module-06.md) |
| **HD Wallet**                | BIP32, Derivation Path                | [Module 06](module-06.md) |
| **Mnemonic Phrase**          | BIP39, Seed Recovery                  | [Module 06](module-06.md) |
| **SPV**                      | Light Client, Simplified Verification | [Module 06](module-06.md) |

### 3. Smart Contract (Extension)

| Topic                         | Sub-Topics                                  | Module                                         |
| ----------------------------- | ------------------------------------------- | ---------------------------------------------- |
| **Basic Concepts**      | Definition, Vending Machine Analogy         | [Module 07](module-07.md), [Module 08](module-08.md) |
| **Remix IDE**           | File Explorer, Compiler, Deploy             | [Module 07](module-07.md)                         |
| **Solidity Basics**     | State Variable, Function, Constructor       | [Module 07](module-07.md)                         |
| **Access Control**      | msg.sender, require, Owner                  | [Module 07](module-07.md)                         |
| **Python Simulation**   | SmartContract Class, State                  | [Module 08](module-08.md)                         |
| **Contract Deployment** | Deploy to Blockchain                        | [Module 08](module-08.md)                         |
| **Contract Execution**  | Execute via Transaction                     | [Module 08](module-08.md)                         |
| **Use Case: Escrow**    | Fund Custody                                | [Module 08](module-08.md)                         |
| **Hardhat 3 Setup**     | defineConfig, Plugins, Compile              | [Module 09](module-09.md)                         |
| **Contract Testing**    | Fixture Pattern, loadFixture, Mocha, Chai   | [Module 10](module-10.md)                         |
| **Deployment**          | Hardhat Ignition, Deploy Script             | [Module 11](module-11.md)                         |
| **MetaMask**            | Wallet, dApp Connection                     | [Module 11](module-11.md)                         |
| **Security**            | Reentrancy, Access Control, DoS             | [Module 16](module-16.md)                         |

### 4. dApp Development (Integration)

| Topic                         | Sub-Topics                              | Module                                         |
| ----------------------------- | --------------------------------------- | ---------------------------------------------- |
| **Web3 Architecture**   | Decentralized Apps, Traditional vs Web3 | [Module 12](module-12.md)                       |
| **dApp Components**     | Frontend, Smart Contract, Wallet        | [Module 12](module-12.md)                       |
| **Provider Setup**      | Ethers.js v6 Provider, RPC Connection   | [Module 12](module-12.md)                       |
| **Wallet Integration**  | MetaMask Connection, Account Access     | [Module 12](module-12.md)                       |
| **Read Operations**     | Contract Instance, View Functions       | [Module 13](module-13.md)                       |
| **Data Display**        | React State, Blockchain Data            | [Module 13](module-13.md)                       |
| **Write Operations**    | Signer, State-Changing Functions        | [Module 14](module-14.md)                       |
| **Transaction Handling**| Confirmation, Receipt, Error Handling   | [Module 14](module-14.md)                       |
| **Event Listening**     | Real-time Updates, WebSocket            | [Module 15](module-15.md)                       |
| **UX Optimization**     | Loading States, Error Messages          | [Module 15](module-15.md)                       |
| **Testnet Deployment**  | Sepolia, Hardhat Ignition, Vercel       | [Module 15](module-15.md)                       |

### Learning Path

```
FASE 1: BLOCKCHAIN & CRYPTOCURRENCY (Minggu 1-7) ─────────────────────────────────────────────────────────
                                                                                     CPMK-1 & CPMK-2
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ╔═══════════╗
     │  Module 01  │─►│  Module 02  │─►│  Module 03  │─►│  Module 04  │─►│Module 05-06 │─►║   DEMO    ║
     │  Pengantar  │  │  Blockchain │  │  Advanced   │  │   Network   │  │Cryptocurrency│  ║ PROYEK 1  ║
     │  Python     │  │  Struktur   │  │  PoW,Mining │  │  Flask API  │  │Wallet,Trans │  ║  (40%)    ║
     └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  ╚═══════════╝
        Minggu 1         Minggu 2         Minggu 3         Minggu 4        Minggu 5-6       Minggu 7
                                                    │
                                                    ▼
FASE 2: SMART CONTRACT (Minggu 8-11) ───────────────────────────────────────────────────────────────────
                                                                                          CPMK-3
     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ╔═════════════╗
     │ Module 07-08│────►│  Module 09  │────►│ Module 10-11│────►║   DEMO      ║
     │ Smart Contr.│     │  Hardhat 3  │     │Test+Ignition│     ║  PROYEK 2   ║
     │ Remix IDE   │     │  Setup      │     │ MetaMask    │     ║  (25%)      ║
     └─────────────┘     └─────────────┘     └─────────────┘     ╚═════════════╝
        Minggu 8            Minggu 9            Minggu 10           Minggu 11
                                                    │
                                                    ▼
FASE 3: dApp DEVELOPMENT (Minggu 12-16) ────────────────────────────────────────────────────────────────
                                                                                          CPMK-4
     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ╔═════════════╗
     │  Module 12  │────►│  Module 13  │────►│  Module 14  │────►│  Module 15  │────►║   DEMO      ║
     │ dApp+Web3   │     │  Read Ops   │     │ Write Ops   │     │ Advanced    │     ║  PROYEK 3   ║
     │ Arsitektur  │     │  Frontend   │     │ Transactions│     │ Deployment  │     ║AKHIR (25%)  ║
     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     ╚═════════════╝
        Minggu 12           Minggu 13           Minggu 14           Minggu 15           Minggu 16
```

### Tools by Category

| Fase | Category | Tools | Module | Minggu |
|------|----------|-------|--------|--------|
| 1 | **Blockchain & Cryptocurrency** | Python, Flask, Postman, RSA/ECDSA | Module 01-06 | 1-7 |
| 2 | **Smart Contract** | Remix IDE, Solidity, Hardhat 3, Ignition, MetaMask | Module 07-11 | 8-11 |
| 3 | **dApp Development** | React, Ethers.js v6, MetaMask, Vercel, Sepolia | Module 12-15 | 12-16 |

---

## Rancangan Pembelajaran Mingguan

### Fase 1: Blockchain & Cryptocurrency (Minggu 1-7) - CPMK-1 & CPMK-2

| Minggu | Sub-CPMK | Deskripsi Sub-CPMK | Topik | Module | Aktivitas | Asesmen |
|--------|----------|-------------------|-------|--------|-----------|---------|
| 1 | **Sub-CPMK-1.1** | Mahasiswa mampu menjelaskan konsep dasar blockchain, distributed ledger, dan membandingkan blockchain dengan database tradisional | Pengantar Blockchain: Konsep dasar, distributed ledger, blockchain vs database tradisional | [Module 01](module-01.md) | Install tools (VS Code, Python), diskusi use cases | Partisipasi Kelas |
| 2 | **Sub-CPMK-1.2** | Mahasiswa mampu mengimplementasikan struktur block sederhana dengan hashing dan validasi chain menggunakan Python | Arsitektur Blockchain: Struktur block, hashing, validasi chain, immutability | [Module 02](module-02.md) | Hands-on: Implementasi blockchain sederhana (Python) | Partisipasi Kelas |
| 3 | **Sub-CPMK-1.3** | Mahasiswa mampu mengimplementasikan digital signatures, mining, dan mekanisme Proof of Work dengan block reward | Implementasi Blockchain: Digital signatures, mining, Proof of Work, block reward | [Module 03](module-03.md) | Sharing dan diskusi, implementasi PoW | Partisipasi Kelas |
| 4 | **Sub-CPMK-1.4** | Mahasiswa mampu mengembangkan simulasi blockchain multi-node menggunakan Flask API dan Postman | Blockchain Network: Multi-node, Flask API, Postman untuk simulasi | [Module 04](module-04.md) | Hands-on: Simulasi multi-node | Partisipasi Kelas |
| 5-6 | **Sub-CPMK-2.1** | Mahasiswa mampu mengimplementasikan struktur transaksi, wallet, verifikasi transaksi, dan menangani masalah double-spending | Transaksi Cryptocurrency: Struktur transaksi, wallets, verifikasi, double-spending | [Module 05](module-05.md), [Module 06](module-06.md) | Hands-on: Simulasi transaksi cryptocurrency | Partisipasi Kelas |
| 7 | **Sub-CPMK-2.2** | Mahasiswa mampu mempresentasikan dan mendemonstrasikan sistem blockchain & cryptocurrency yang telah dikembangkan | **Demo Proyek 1: Blockchain & Cryptocurrency** | - | Presentasi dan demonstrasi | **Proyek 1 (40%)** |

### Fase 2: Smart Contract Development (Minggu 8-11) - CPMK-3

| Minggu | Sub-CPMK | Deskripsi Sub-CPMK | Topik | Module | Aktivitas | Asesmen |
|--------|----------|-------------------|-------|--------|-----------|---------|
| 8 | **Sub-CPMK-3.1** | Mahasiswa mampu menulis smart contract dasar menggunakan Solidity dengan variabel, fungsi, tipe data, dan visibility yang tepat | Smart Contract Basics: Konsep, Solidity, variabel, fungsi, visibility | [Module 07](module-07.md), [Module 08](module-08.md) | Hands-on: Remix IDE, Simple Storage, Voting Contract | Partisipasi Kelas |
| 9 | **Sub-CPMK-3.2** | Mahasiswa mampu mengkonfigurasi Hardhat 3 dengan defineConfig() dan memahami fixture pattern untuk testing | Hardhat 3 Setup: defineConfig, plugins, fixture pattern | [Module 09](module-09.md) | Hands-on: Setup Hardhat 3 project | Partisipasi Kelas |
| 10 | **Sub-CPMK-3.3** | Mahasiswa mampu men-deploy smart contract menggunakan Hardhat 3 dan Hardhat Ignition pada local blockchain | Development Environment: Testing dengan loadFixture, Deployment, MetaMask | [Module 10](module-10.md), [Module 11](module-11.md) | Hands-on: Testing, deploy dengan Ignition, interaksi MetaMask | Partisipasi Kelas |
| 11 | **Sub-CPMK-3.4** | Mahasiswa mampu mempresentasikan smart contract yang telah dikembangkan dengan mempertimbangkan aspek keamanan | **Demo Proyek 2: Smart Contract** | - | Presentasi smart contract dengan aspek keamanan | **Proyek 2 (25%)** |

### Fase 3: dApp Development (Minggu 12-16) - CPMK-4

| Minggu | Sub-CPMK | Deskripsi Sub-CPMK | Topik | Module | Aktivitas | Asesmen |
|--------|----------|-------------------|-------|--------|-----------|---------|
| 12 | **Sub-CPMK-4.1** | Mahasiswa mampu memahami arsitektur Web3 dan komponen-komponen dApp | Pengenalan dApp: Konsep Web3, arsitektur dApp, komponen-komponen | [Module 12](module-12.md) | Hands-on: Setup project dApp, integrasi MetaMask | Partisipasi Kelas |
| 13 | **Sub-CPMK-4.2** | Mahasiswa mampu membaca data dari smart contract menggunakan frontend React dan Ethers.js | Frontend Integration Read: Provider, contract instance, view functions | [Module 13](module-13.md) | Hands-on: Read operations dari smart contract | Partisipasi Kelas |
| 14 | **Sub-CPMK-4.3** | Mahasiswa mampu mengirim transaksi ke smart contract dan menangani state-changing operations | Frontend Integration Write: Signer, transactions, event handling | [Module 14](module-14.md) | Hands-on: Write operations dan transaction handling | Partisipasi Kelas |
| 15 | **Sub-CPMK-4.4** | Mahasiswa mampu mengimplementasikan fitur lanjutan dan men-deploy dApp ke testnet menggunakan Hardhat Ignition | dApp Advanced: Real-time events, optimasi UX, Hardhat Ignition, deployment ke Sepolia | [Module 15](module-15.md) | Hands-on: Event listening, deployment dengan Ignition ke Sepolia | Partisipasi Kelas |
| 16 | **Sub-CPMK-4.5** | Mahasiswa mampu mempresentasikan dApp lengkap yang mengintegrasikan smart contract, wallet, dan frontend | **Demo Proyek 3: dApp** | - | Presentasi dApp lengkap | **Proyek 3 (25%)** |

---

## Pemetaan Module ke Minggu

| Minggu | Module | Judul Module |
|--------|--------|--------------|
| 1 | 01 | Introduction to Python |
| 2 | 02 | Blockchain Fundamentals |
| 3 | 03 | Advanced Blockchain Concepts |
| 4 | 04 | Blockchain Network dengan Flask API |
| 5-6 | 05, 06 | Cryptocurrency, Advanced Cryptocurrency |
| 7 | - | **Demo Proyek 1: Blockchain & Cryptocurrency** |
| 8 | 07, 08 | Smart Contracts (Python), Smart Contract dengan Remix IDE |
| 9 | 09 | Hardhat Project Setup & Compile |
| 10 | 10, 11 | Smart Contract Testing, Deployment & MetaMask Interaction |
| 11 | - | **Demo Proyek 2: Smart Contract** |
| 12 | 12 | Pengenalan dApp & Arsitektur Web3 |
| 13 | 13 | Frontend Integration - Read Operations |
| 14 | 14 | Frontend Integration - Write Operations |
| 15 | 15 | dApp Advanced Features & Deployment |
| 16 | - | **Demo Proyek 3: dApp** |

### Modul Tambahan (Supplementary)

| Minggu | Module | Judul Module |
|--------|--------|--------------|
| - | 16 | Smart Contract Security (dapat dipelajari setelah Module 10) |

---

## Penilaian

| No | Jenis Penilaian | CPMK | Bobot | Tenggat |
|----|-----------------|------|-------|---------|
| 1 | Partisipasi Kelas | 1-4 | 10% | - |
| 2 | Proyek 1: Blockchain & Cryptocurrency | 1, 2 | 40% | Minggu 7 |
| 3 | Proyek 2: Smart Contract | 3 | 25% | Minggu 11 |
| 4 | Proyek 3: dApp | 4 | 25% | Minggu 16 |

---

## Panduan Proyek

| Proyek | Deskripsi | Link |
|--------|-----------|------|
| **Proyek 1** | Blockchain & Cryptocurrency | [Lihat Panduan](projects/project-01-blockchain-cryptocurrency.md) |
| **Proyek 2** | Smart Contract Development | [Lihat Panduan](projects/project-02-smart-contract.md) |

### Proyek 1: Blockchain & Cryptocurrency (Minggu 7)

| Fitur | Deskripsi |
|-------|-----------|
| Block Structure | index, timestamp, transactions, proof, previous_hash |
| Proof of Work | Mining dengan difficulty |
| Chain Validation | Validasi integritas chain |
| Multi-Node Network | Flask API, consensus |
| Wallet | Private/public key pair |
| Digital Signature | Sign & verify transaksi |
| Balance Tracking | Hitung saldo per address |
| Double-Spending Prevention | Cegah penggunaan ganda |

### Proyek 2: Smart Contract (Minggu 11)

| Pilihan | Deskripsi | Fitur Utama |
|---------|-----------|-------------|
| Course Reward | Sistem reward untuk mahasiswa | claim, setAmount, tracking |
| Simple Voting | Sistem voting untuk pemilihan | createProposal, vote, tally |
| Todo List | Todo list on-chain | addTodo, complete, delete |
| Simple Escrow | Layanan escrow transaksi aman | deposit, release, refund |
| Simple Token | Token cryptocurrency sederhana | transfer, mint, balance |
| Crowdfunding | Platform penggalangan dana | createCampaign, donate, withdraw |

### Proyek 3: dApp (Minggu 16)

| Pilihan | Deskripsi | Komponen |
|---------|-----------|----------|
| Token Launchpad | Platform untuk launch dan distribusi token | Token factory + claim UI |
| NFT Minting Site | Website untuk mint NFT collection | NFT contract + minting UI |
| Decentralized Voting | Aplikasi voting untuk organisasi | Voting contract + dashboard |
| Crowdfunding Platform | Platform donasi dengan target | Campaign contract + donor UI |
| Simple DEX | Token swap sederhana | Swap contract + trading UI |
