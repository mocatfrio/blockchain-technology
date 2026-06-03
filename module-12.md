# Modul 12. Pengenalan dApp & Arsitektur Web3

## Deskripsi

Modul ini membahas konsep dasar **Decentralized Application (dApp)**, arsitektur Web3, dan perbedaannya dengan aplikasi web tradisional. Mahasiswa akan memahami komponen-komponen yang diperlukan untuk membangun dApp dan bagaimana mereka saling terhubung.

## Tujuan Pembelajaran

Setelah menyelesaikan modul ini, mahasiswa mampu:

1. Memahami konsep dan karakteristik dApp
2. Membedakan arsitektur Web2 vs Web3
3. Menjelaskan komponen-komponen dApp (Frontend, Smart Contract, Wallet, Node/RPC)
4. Memahami flow interaksi user dengan dApp
5. Mengenal library dan tools untuk pengembangan dApp
6. Setup project dApp dengan React dan Vite

## Prasyarat

- Sudah menyelesaikan Module 09-11 (Hardhat Setup, Testing, Deployment)
- Memahami dasar HTML, CSS, JavaScript
- Memahami dasar React (opsional, akan dijelaskan singkat)
- Smart contract sudah berhasil deploy ke local network

## List of Contents

- [Deskripsi](#deskripsi)
- [Tujuan Pembelajaran](#tujuan-pembelajaran)
- [Prasyarat](#prasyarat)
- [1. Apa itu dApp?](#1-apa-itu-dapp)
- [2. Web2 vs Web3](#2-web2-vs-web3)
- [3. Arsitektur dApp](#3-arsitektur-dapp)
- [4. Komponen dApp](#4-komponen-dapp)
- [5. Flow Interaksi dApp](#5-flow-interaksi-dapp)
- [6. Tools dan Library](#6-tools-dan-library)
- [7. Setup Project dApp](#7-setup-project-dapp)
- [8. Struktur Project](#8-struktur-project)
- [9. Hands-on: Hello dApp](#9-hands-on-hello-dapp)
- [Ringkasan](#ringkasan)
- [Tugas](#tugas)

---

## 1. Apa itu dApp?

### 1.1 Definisi dApp

**dApp (Decentralized Application)** adalah aplikasi yang berjalan di atas jaringan blockchain terdesentralisasi, bukan di server terpusat. Backend logic-nya dijalankan oleh smart contract yang tersimpan di blockchain.

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEFINISI dApp                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  dApp = Decentralized Application                               │
│                                                                 │
│  ┌─────────────────┐     ┌─────────────────┐                    │
│  │    Frontend     │     │    Backend      │                    │
│  │  (Web/Mobile)   │────►│ (Smart Contract)│                    │
│  │                 │     │  on Blockchain  │                    │
│  └─────────────────┘     └─────────────────┘                    │
│                                 │                               │
│                                 ▼                               │
│                    ┌─────────────────────┐                      │
│                    │  Decentralized      │                      │
│                    │  - No single owner  │                      │
│                    │  - Transparent      │                      │
│                    │  - Immutable        │                      │
│                    │  - Trustless        │                      │
│                    └─────────────────────┘                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Karakteristik dApp

| Karakteristik           | Penjelasan                                                   |
| ----------------------- | ------------------------------------------------------------ |
| **Decentralized** | Tidak ada single point of failure, berjalan di banyak node   |
| **Open Source**   | Kode smart contract bisa diverifikasi oleh siapapun          |
| **Transparent**   | Semua transaksi tercatat dan bisa dilihat di blockchain      |
| **Tokenized**     | Sering menggunakan token untuk incentive dan governance      |
| **Autonomous**    | Berjalan sesuai logic yang sudah diprogram, tanpa intervensi |

### 1.3 Contoh dApp Populer

```
┌─────────────────────────────────────────────────────────────────┐
│                    KATEGORI dApp                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DeFi (Decentralized Finance)                                   │
│  ├── Uniswap      : Decentralized Exchange (DEX)                │
│  ├── Aave         : Lending & Borrowing                         │
│  ├── Compound     : Interest Rate Protocol                      │
│  └── MakerDAO     : Stablecoin (DAI)                            │
│                                                                 │
│  NFT & Gaming                                                   │
│  ├── OpenSea      : NFT Marketplace                             │
│  ├── Axie Infinity: Play-to-Earn Game                           │
│  └── Decentraland : Virtual World                               │
│                                                                 │
│  Social & Identity                                              │
│  ├── Lens Protocol: Decentralized Social                        │
│  ├── ENS          : Ethereum Name Service                       │
│  └── Mirror       : Decentralized Publishing                    │
│                                                                 │
│  Infrastructure                                                 │
│  ├── The Graph    : Indexing Protocol                           │
│  ├── Chainlink    : Oracle Network                              │
│  └── IPFS/Filecoin: Decentralized Storage                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.4 Kelebihan dan Kekurangan dApp

| Aspek              | Kelebihan                        | Kekurangan                        |
| ------------------ | -------------------------------- | --------------------------------- |
| **Control**  | User memiliki kontrol penuh      | User bertanggung jawab penuh      |
| **Trust**    | Trustless, kode adalah hukum     | Bug di smart contract berbahaya   |
| **Censorship** | Tahan sensor                     | Konten ilegal sulit dihapus       |
| **Cost**     | Tidak perlu server               | Gas fee untuk setiap transaksi    |
| **Speed**    | Tidak tergantung satu server     | Lebih lambat dari Web2            |
| **UX**       | Transparansi tinggi              | UX masih kompleks untuk pemula    |

---

## 2. Web2 vs Web3

### 2.1 Perbandingan Arsitektur

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEB2 ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   User                                                          │
│    │                                                            │
│    ▼                                                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │   Browser   │───►│   Server    │───►│  Database   │          │
│  │  (Frontend) │◄───│  (Backend)  │◄───│  (MySQL,    │          │
│  │             │    │  (Node.js,  │    │  MongoDB)   │          │
│  │             │    │   Django)   │    │             │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│                            │                                    │
│                     Single Company                              │
│                     Controls Everything                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    WEB3 ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   User                                                          │
│    │                                                            │
│    ▼                                                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │   Browser   │───►│   Wallet    │───►│  Blockchain │          │
│  │  (Frontend) │◄───│ (MetaMask)  │◄───│   Network   │          │
│  │  + Web3 Lib │    │             │    │  (1000s of  │          │
│  │             │    │             │    │   nodes)    │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│                                               │                 │
│                                        ┌──────┴──────┐          │
│                                        │Smart Contract│         │
│                                        │ (Backend)    │         │
│                                        └─────────────┘          │
│                                                                 │
│                     No Single Point of Control                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Perbandingan Detail

| Aspek                       | Web2                              | Web3                                     |
| --------------------------- | --------------------------------- | ---------------------------------------- |
| **Backend**           | Server (AWS, GCP)                 | Smart Contract on Blockchain             |
| **Database**          | MySQL, PostgreSQL, MongoDB        | Blockchain State                         |
| **Authentication**    | Username/Password, OAuth          | Wallet Signature (MetaMask)              |
| **Payment**           | Credit Card, PayPal               | Cryptocurrency                           |
| **Data Ownership**    | Company owns user data            | User owns their data                     |
| **Downtime**          | Server bisa down                  | Network selalu online (decentralized)    |
| **Update**            | Company bisa update kapan saja    | Perlu upgrade mechanism / governance     |
| **Cost Model**        | User gratis, company bayar server | User bayar gas fee per transaksi         |

### 2.3 Login/Authentication

```
┌─────────────────────────────────────────────────────────────────┐
│                 WEB2 vs WEB3 AUTHENTICATION                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WEB2: Username + Password                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. User masukkan email + password                      │    │
│  │  2. Server verifikasi di database                       │    │
│  │  3. Server kirim session/JWT token                      │    │
│  │  4. Browser simpan token untuk request selanjutnya      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  WEB3: Wallet Signature                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. User klik "Connect Wallet"                          │    │
│  │  2. MetaMask popup muncul                               │    │
│  │  3. User approve connection                             │    │
│  │  4. dApp dapat wallet address (public)                  │    │
│  │  5. Untuk verify ownership: sign message                │    │
│  │                                                         │    │
│  │  Tidak perlu password! Private key = identitas          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Arsitektur dApp

### 3.1 Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    dApp LAYER ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  PRESENTATION LAYER                     │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │    │
│  │  │    React    │  │    Vue      │  │   Mobile    │      │    │
│  │  │   Next.js   │  │   Nuxt.js   │  │ React Native│      │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  WEB3 LIBRARY LAYER                     │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │    │
│  │  │  Ethers.js  │  │   Web3.js   │  │    Viem     │      │    │
│  │  │  (Popular)  │  │  (Classic)  │  │   (Modern)  │      │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    WALLET LAYER                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │    │
│  │  │  MetaMask   │  │ WalletConnect│ │ Coinbase    │      │    │
│  │  │             │  │             │  │   Wallet    │      │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   NODE/RPC LAYER                        │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │    │
│  │  │   Alchemy   │  │   Infura    │  │ Local Node  │      │    │
│  │  │             │  │             │  │  (Hardhat)  │      │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  BLOCKCHAIN LAYER                       │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │    │
│  │  │  Ethereum   │  │   Polygon   │  │  Arbitrum   │      │    │
│  │  │             │  │             │  │             │      │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │    │
│  │                                                         │    │
│  │                  SMART CONTRACT                         │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │  contract MyContract {                          │    │    │
│  │  │    mapping(address => uint) public balances;    │    │    │
│  │  │    function deposit() public payable { ... }    │    │    │
│  │  │  }                                              │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    dApp DATA FLOW                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  READ (View Function - No Gas)                                  │
│  ════════════════════════════════════════════════════════════   │
│                                                                 │
│  Frontend ──► ethers.js ──► RPC Node ──► Blockchain             │
│     │                                         │                 │
│     │◄──────────── Data Response ◄────────────┘                 │
│     │                                                           │
│     │  Contoh: getBalance(), totalSupply()                      │
│     │  - Gratis (tidak bayar gas)                               │
│     │  - Instant response                                       │
│                                                                 │
│  WRITE (State-Changing Function - Requires Gas)                 │
│  ════════════════════════════════════════════════════════════   │
│                                                                 │
│  Frontend ──► ethers.js ──► MetaMask ──► User Signs ──►         │
│                                              │                  │
│                                              ▼                  │
│  Frontend ◄── Tx Hash ◄── RPC Node ◄── Broadcast to Network    │
│     │                                         │                 │
│     │         Wait for confirmation...        │                 │
│     │                                         ▼                 │
│     │◄─────── Tx Receipt ◄───── Block Mined ◄─┘                 │
│                                                                 │
│     Contoh: transfer(), mint(), claimReward()                   │
│     - Butuh gas fee                                             │
│     - Butuh user approval di wallet                             │
│     - Menunggu block confirmation                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Komponen dApp

### 4.1 Overview Komponen

```
┌─────────────────────────────────────────────────────────────────┐
│                    KOMPONEN dApp                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  1. FRONTEND                                             │   │
│  │     - User Interface (React, Vue, etc.)                  │   │
│  │     - Menampilkan data dari blockchain                   │   │
│  │     - Mengirim transaksi ke blockchain                   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  2. WEB3 LIBRARY (ethers.js / web3.js)                   │   │
│  │     - Bridge antara frontend dan blockchain              │   │
│  │     - Encode/decode data                                 │   │
│  │     - Sign transactions                                  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  3. WALLET (MetaMask)                                    │   │
│  │     - Menyimpan private key                              │   │
│  │     - Sign transaksi                                     │   │
│  │     - Manage multiple accounts                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  4. RPC NODE (Alchemy, Infura, Local)                    │   │
│  │     - Gateway ke blockchain network                      │   │
│  │     - Menjalankan read queries                           │   │
│  │     - Broadcast transactions                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  5. SMART CONTRACT                                       │   │
│  │     - Business logic di blockchain                       │   │
│  │     - State storage                                      │   │
│  │     - Immutable setelah deploy                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Frontend Framework Options

| Framework       | Kelebihan                    | Cocok untuk         |
| --------------- | ---------------------------- | ------------------- |
| **React**     | Ecosystem besar, banyak tutorial | General purpose     |
| **Next.js**   | SSR, SEO friendly            | Production dApp     |
| **Vue**       | Mudah dipelajari             | Tim kecil           |
| **Svelte**    | Performant, kompilasi optimal | Performa kritis     |

### 4.3 Web3 Library Comparison

| Library       | Kelebihan                          | Kekurangan           |
| ------------- | ---------------------------------- | -------------------- |
| **Ethers.js** | Modular, well-documented, TypeScript | Learning curve       |
| **Web3.js**   | Mature, banyak resource            | Bundle size besar    |
| **Viem**      | Modern, TypeScript-first, fast     | Relatif baru         |
| **Wagmi**     | React hooks, DX bagus              | React only           |

### 4.4 Node/RPC Provider

```
┌─────────────────────────────────────────────────────────────────┐
│                    RPC PROVIDER OPTIONS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Development (Local):                                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Hardhat Node    : npx hardhat node (port 8545)         │    │
│  │  Ganache         : GUI atau CLI (port 7545)             │    │
│  │  Anvil (Foundry) : Sangat cepat                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Testnet/Mainnet (Cloud):                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Alchemy         : Free tier generous, dashboard bagus  │    │
│  │  Infura          : Mature, reliable                     │    │
│  │  QuickNode       : Fast, multi-chain                    │    │
│  │  Public RPC      : Gratis tapi rate limited             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Flow Interaksi dApp

### 5.1 User Journey: Connect Wallet

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONNECT WALLET FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Step 1: User klik "Connect Wallet"                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  dApp Frontend                                          │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │                                                 │    │    │
│  │  │     Welcome to My dApp                          │    │    │
│  │  │                                                 │    │    │
│  │  │     [Connect Wallet] ◄── User clicks            │    │    │
│  │  │                                                 │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│  Step 2: MetaMask popup muncul                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  MetaMask Popup                                         │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │                                                 │    │    │
│  │  │  Connect to MyDApp?                             │    │    │
│  │  │                                                 │    │    │
│  │  │  This site is requesting access to view your   │    │    │
│  │  │  current account address.                      │    │    │
│  │  │                                                 │    │    │
│  │  │  Account: 0xf39F...2266                        │    │    │
│  │  │                                                 │    │    │
│  │  │     [Cancel]  [Connect] ◄── User approves      │    │    │
│  │  │                                                 │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│  Step 3: dApp mendapat address dan menampilkan UI               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  dApp Frontend (Connected)                              │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │                                                 │    │    │
│  │  │     Connected: 0xf39F...2266                    │    │    │
│  │  │     Balance: 100 Tokens                         │    │    │
│  │  │                                                 │    │    │
│  │  │     [Claim Reward]  [Transfer]                  │    │    │
│  │  │                                                 │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 User Journey: Send Transaction

```
┌─────────────────────────────────────────────────────────────────┐
│                    SEND TRANSACTION FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. User klik action button (misal: "Claim Reward")             │
│     │                                                           │
│     ▼                                                           │
│  2. Frontend membuat transaction object                         │
│     │  {                                                        │
│     │    to: contractAddress,                                   │
│     │    data: encodedFunctionCall                              │
│     │  }                                                        │
│     │                                                           │
│     ▼                                                           │
│  3. MetaMask popup untuk konfirmasi                             │
│     ┌───────────────────────────────────────┐                   │
│     │  Confirm Transaction                  │                   │
│     │                                       │                   │
│     │  Function: claimReward()              │                   │
│     │  Gas Fee: ~0.001 ETH                  │                   │
│     │                                       │                   │
│     │  [Reject]        [Confirm]            │                   │
│     └───────────────────────────────────────┘                   │
│     │                                                           │
│     ▼                                                           │
│  4. User sign transaction (private key digunakan)               │
│     │                                                           │
│     ▼                                                           │
│  5. Transaction broadcast ke network                            │
│     │                                                           │
│     ▼                                                           │
│  6. Frontend dapat transaction hash                             │
│     │  0x1234567890abcdef...                                    │
│     │                                                           │
│     ▼                                                           │
│  7. Menunggu block confirmation                                 │
│     │  "Transaction pending..."                                 │
│     │                                                           │
│     ▼                                                           │
│  8. Transaction confirmed!                                      │
│     │  "Reward claimed successfully!"                           │
│     │                                                           │
│     ▼                                                           │
│  9. UI update dengan data baru                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 State Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    dApp STATE DIAGRAM                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    ┌─────────────────┐                          │
│                    │   DISCONNECTED  │                          │
│                    │   (Initial)     │                          │
│                    └────────┬────────┘                          │
│                             │                                   │
│                    User clicks "Connect"                        │
│                             │                                   │
│                             ▼                                   │
│                    ┌─────────────────┐                          │
│                    │   CONNECTING    │                          │
│                    │   (Loading)     │                          │
│                    └────────┬────────┘                          │
│                             │                                   │
│             ┌───────────────┼───────────────┐                   │
│             │               │               │                   │
│        User rejects    User approves   Error/Timeout            │
│             │               │               │                   │
│             ▼               ▼               ▼                   │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│    │ DISCONNECTED│  │  CONNECTED  │  │    ERROR    │            │
│    └─────────────┘  └──────┬──────┘  └─────────────┘            │
│                            │                                    │
│                    User sends transaction                       │
│                            │                                    │
│                            ▼                                    │
│                    ┌─────────────────┐                          │
│                    │   TX PENDING    │                          │
│                    └────────┬────────┘                          │
│                             │                                   │
│             ┌───────────────┼───────────────┐                   │
│             │               │               │                   │
│        Tx Failed      Tx Success       User rejects             │
│             │               │               │                   │
│             ▼               ▼               ▼                   │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│    │  TX ERROR   │  │ TX SUCCESS  │  │  CONNECTED  │            │
│    └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Tools dan Library

### 6.1 Development Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    RECOMMENDED TECH STACK                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Frontend:                                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  React + Vite        : Fast development, modern tooling │    │
│  │  TailwindCSS         : Utility-first CSS                │    │
│  │  React Router        : Navigation                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Web3:                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  ethers.js v6        : Blockchain interaction           │    │
│  │  @metamask/sdk       : MetaMask integration (opsional)  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Smart Contract:                                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Hardhat             : Development framework            │    │
│  │  OpenZeppelin        : Secure contract templates        │    │
│  │  Solidity ^0.8.20    : Smart contract language          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Testing:                                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Hardhat Test        : Smart contract testing           │    │
│  │  Vitest              : Frontend testing                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Package Versions

Untuk modul ini, kita akan menggunakan:

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "ethers": "^6.9.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0"
  }
}
```

---

## 7. Setup Project dApp

### 7.1 Struktur Monorepo

Kita akan membuat struktur project dimana smart contract dan frontend berada dalam satu repository:

```
dapp-project/
├── contracts/              ← Hardhat project (dari Module 09-11)
│   ├── contracts/
│   ├── scripts/
│   ├── test/
│   └── hardhat.config.js
│
└── frontend/               ← React + Vite project (akan dibuat)
    ├── src/
    ├── public/
    ├── package.json
    └── vite.config.js
```

### 7.2 Step 1: Siapkan Folder Project

Pastikan Anda sudah memiliki project Hardhat dari modul sebelumnya. Jika belum, buat dulu:

```bash
# Buat folder utama
mkdir dapp-project
cd dapp-project

# Copy project Hardhat yang sudah ada, atau buat baru
mkdir contracts
cd contracts
npm init -y
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
npx hardhat init
# Pilih: Create a JavaScript project
```

### 7.3 Step 2: Setup Frontend dengan Vite

> **Apa yang akan kita lakukan?**
>
> Kita akan membuat aplikasi React menggunakan Vite (build tool modern yang sangat cepat). Vite akan menjadi "rumah" untuk frontend dApp kita, tempat user berinteraksi dengan smart contract.
>
> **Kenapa Vite?**
> - Lebih cepat dari Create React App
> - Hot Module Replacement (HMR) instan
> - Konfigurasi minimal

```bash
# Kembali ke folder utama
cd ..

# Buat project React dengan Vite
npm create vite@latest frontend -- --template react

# Masuk ke folder frontend
cd frontend

# Install dependencies
npm install

# Install ethers.js
npm install ethers
```

### 7.4 Step 3: Verifikasi Instalasi

```bash
# Di folder frontend
npm run dev
```

Buka browser di `http://localhost:5173` - Anda akan melihat halaman default Vite + React.

### 7.5 Step 4: Struktur Folder Frontend

Setelah setup, struktur folder frontend:

```
frontend/
├── node_modules/
├── public/
│   └── vite.svg
├── src/
│   ├── assets/
│   │   └── react.svg
│   ├── App.css
│   ├── App.jsx            ← Main component
│   ├── index.css
│   └── main.jsx           ← Entry point
├── .gitignore
├── index.html
├── package.json
├── package-lock.json
└── vite.config.js
```

---

## 8. Struktur Project

### 8.1 Recommended Folder Structure

Reorganisasi folder `src/` untuk dApp:

```
frontend/src/
├── components/            ← Reusable UI components
│   ├── ConnectButton.jsx
│   ├── Navbar.jsx
│   └── TransactionStatus.jsx
│
├── hooks/                 ← Custom React hooks
│   ├── useWallet.js
│   └── useContract.js
│
├── contracts/             ← ABI dan contract addresses
│   ├── CourseReward.json  ← Copy dari artifacts
│   └── addresses.js       ← Contract addresses per network
│
├── utils/                 ← Helper functions
│   ├── formatters.js
│   └── constants.js
│
├── pages/                 ← Page components (jika pakai routing)
│   └── Home.jsx
│
├── App.jsx
├── App.css
├── index.css
└── main.jsx
```

### 8.2 Copy ABI dari Hardhat

> **Apa itu ABI dan kenapa perlu di-copy?**
>
> ABI (Application Binary Interface) adalah "kamus" yang menjelaskan function apa saja yang ada di smart contract. Frontend butuh file ini untuk:
> - Tahu function mana yang bisa dipanggil
> - Tahu parameter apa yang dibutuhkan
> - Encode/decode data dengan benar
>
> **Lokasi file ABI:**
> Setelah `npx hardhat compile`, file ABI ada di:
> `contracts/artifacts/contracts/NamaContract.sol/NamaContract.json`

Setelah compile smart contract di Hardhat, copy file ABI ke frontend:

```bash
# Dari folder dapp-project
cp contracts/artifacts/contracts/CourseReward.sol/CourseReward.json frontend/src/contracts/
```

Atau buat script untuk otomatis copy:

**contracts/scripts/copy-abi.js:**
```javascript
const fs = require('fs');
const path = require('path');

const source = path.join(__dirname, '../artifacts/contracts/CourseReward.sol/CourseReward.json');
const dest = path.join(__dirname, '../../frontend/src/contracts/CourseReward.json');

// Buat folder jika belum ada
const destDir = path.dirname(dest);
if (!fs.existsSync(destDir)) {
  fs.mkdirSync(destDir, { recursive: true });
}

// Copy file
fs.copyFileSync(source, dest);
console.log('ABI copied to frontend!');
```

Jalankan:
```bash
cd contracts
node scripts/copy-abi.js
```

### 8.3 Contract Addresses File

> **Kenapa perlu file addresses.js?**
>
> Contract address berbeda di setiap network:
> - Deploy ke Hardhat local → address A
> - Deploy ke Sepolia testnet → address B
> - Deploy ke Ethereum mainnet → address C
>
> File ini menyimpan semua address dan memilih yang tepat berdasarkan chainId yang aktif.
>
> **Cara mendapatkan address:**
> Setiap kali deploy, catat address dari output terminal:
> ```
> CourseReward deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3
> ```
> Kemudian update file ini sesuai network-nya.

**frontend/src/contracts/addresses.js:**
```javascript
// Contract addresses per network
export const CONTRACT_ADDRESSES = {
  // Local development
  localhost: {
    courseReward: "0x5FbDB2315678afecb367f032d93F642f64180aa3" // Ganti dengan address hasil deploy
  },
  // Hardhat network
  hardhat: {
    courseReward: "0x5FbDB2315678afecb367f032d93F642f64180aa3"
  },
  // Sepolia testnet (nanti)
  sepolia: {
    courseReward: ""
  }
};

// Helper function
export function getContractAddress(contractName, chainId) {
  const networkMap = {
    31337: 'localhost',  // Hardhat
    1337: 'localhost',   // Ganache
    11155111: 'sepolia'  // Sepolia
  };

  const network = networkMap[chainId] || 'localhost';
  return CONTRACT_ADDRESSES[network]?.[contractName] || '';
}
```

---

## 9. Hands-on: Hello dApp

### 9.1 Membuat Komponen Sederhana

Mari buat dApp sederhana yang bisa connect ke MetaMask dan menampilkan alamat wallet.

> **Apa yang akan kita buat?**
>
> Sebuah halaman web sederhana dengan tombol "Connect Wallet" yang:
> 1. Memunculkan popup MetaMask saat diklik
> 2. Setelah user approve, menampilkan alamat wallet
> 3. Menampilkan saldo ETH wallet tersebut
>
> **Konsep penting yang digunakan:**
> - `window.ethereum` → objek yang disediakan MetaMask di browser
> - `eth_requestAccounts` → meminta izin akses ke wallet user
> - `BrowserProvider` → ethers.js wrapper untuk MetaMask
> - `useState` & `useEffect` → React hooks untuk state management
>
> **Cara kerja singkat:**
> ```
> User klik tombol → MetaMask popup → User approve → Dapat address → Tampilkan di UI
> ```

**frontend/src/App.jsx:**
```jsx
import { useState, useEffect } from 'react'
import { ethers } from 'ethers'
import './App.css'

function App() {
  // State
  const [account, setAccount] = useState(null)
  const [balance, setBalance] = useState(null)
  const [isConnecting, setIsConnecting] = useState(false)
  const [error, setError] = useState(null)

  // Check apakah MetaMask terinstall
  const isMetaMaskInstalled = () => {
    return typeof window.ethereum !== 'undefined'
  }

  // Connect wallet
  const connectWallet = async () => {
    if (!isMetaMaskInstalled()) {
      setError('MetaMask belum terinstall! Silakan install di metamask.io')
      return
    }

    setIsConnecting(true)
    setError(null)

    try {
      // Request akses ke accounts
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts'
      })

      if (accounts.length > 0) {
        setAccount(accounts[0])

        // Get balance
        const provider = new ethers.BrowserProvider(window.ethereum)
        const balance = await provider.getBalance(accounts[0])
        setBalance(ethers.formatEther(balance))
      }
    } catch (err) {
      console.error('Error connecting:', err)
      if (err.code === 4001) {
        setError('Koneksi ditolak oleh user')
      } else {
        setError('Gagal connect: ' + err.message)
      }
    } finally {
      setIsConnecting(false)
    }
  }

  // Disconnect wallet
  const disconnectWallet = () => {
    setAccount(null)
    setBalance(null)
  }

  // Listen untuk account changes
  useEffect(() => {
    if (isMetaMaskInstalled()) {
      window.ethereum.on('accountsChanged', (accounts) => {
        if (accounts.length > 0) {
          setAccount(accounts[0])
        } else {
          setAccount(null)
          setBalance(null)
        }
      })

      window.ethereum.on('chainChanged', () => {
        window.location.reload()
      })
    }

    // Cleanup
    return () => {
      if (isMetaMaskInstalled()) {
        window.ethereum.removeAllListeners('accountsChanged')
        window.ethereum.removeAllListeners('chainChanged')
      }
    }
  }, [])

  // Format address untuk display
  const formatAddress = (address) => {
    return `${address.slice(0, 6)}...${address.slice(-4)}`
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Hello dApp</h1>

        {!account ? (
          <button
            onClick={connectWallet}
            disabled={isConnecting}
            className="connect-btn"
          >
            {isConnecting ? 'Connecting...' : 'Connect Wallet'}
          </button>
        ) : (
          <div className="wallet-info">
            <span className="address">{formatAddress(account)}</span>
            <button onClick={disconnectWallet} className="disconnect-btn">
              Disconnect
            </button>
          </div>
        )}
      </header>

      <main className="main">
        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {account && (
          <div className="card">
            <h2>Wallet Connected!</h2>
            <p><strong>Address:</strong> {account}</p>
            <p><strong>Balance:</strong> {balance} ETH</p>
          </div>
        )}

        {!account && !error && (
          <div className="card">
            <h2>Welcome to My dApp</h2>
            <p>Connect your wallet to get started</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
```

### 9.2 Styling

> **Tips untuk pemula:**
>
> CSS ini memberikan tampilan modern dengan gradient background dan card design. Tidak perlu menghafal semua properti CSS - cukup copy paste dan modifikasi sesuai selera.
>
> **Poin penting:**
> - `.connect-btn` → styling untuk tombol connect
> - `.wallet-info` → container untuk info wallet setelah terhubung
> - `.error` → styling untuk pesan error (warna merah)

**frontend/src/App.css:**
```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  margin-bottom: 30px;
}

.header h1 {
  color: white;
  font-size: 1.5rem;
}

.connect-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.connect-btn:hover {
  background: #45a049;
  transform: translateY(-2px);
}

.connect-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
  transform: none;
}

.wallet-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.address {
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 8px;
  color: white;
  font-family: monospace;
}

.disconnect-btn {
  background: #ff5722;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.disconnect-btn:hover {
  background: #f4511e;
}

.main {
  padding: 20px;
}

.card {
  background: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.card h2 {
  color: #333;
  margin-bottom: 15px;
}

.card p {
  color: #666;
  margin-bottom: 10px;
  word-break: break-all;
}

.error {
  background: #ffebee;
  color: #c62828;
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #c62828;
}
```

### 9.3 Menjalankan dApp

1. **Terminal 1 - Jalankan Hardhat Node:**
```bash
cd contracts
npx hardhat node
```

2. **Terminal 2 - Jalankan Frontend:**
```bash
cd frontend
npm run dev
```

3. **Browser:**
   - Buka `http://localhost:5173`
   - Pastikan MetaMask sudah terinstall
   - Pastikan MetaMask terhubung ke network Hardhat Local (lihat Module 11)
   - Klik "Connect Wallet"

### 9.4 Testing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    TESTING HELLO dApp                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Buka http://localhost:5173                                  │
│     └─► Lihat "Welcome to My dApp"                              │
│                                                                 │
│  2. Klik "Connect Wallet"                                       │
│     └─► MetaMask popup muncul                                   │
│                                                                 │
│  3. Approve di MetaMask                                         │
│     └─► Address dan balance tampil                              │
│                                                                 │
│  4. Switch account di MetaMask                                  │
│     └─► dApp auto update address baru                           │
│                                                                 │
│  5. Switch network di MetaMask                                  │
│     └─► Page auto reload                                        │
│                                                                 │
│  6. Klik "Disconnect"                                           │
│     └─► Kembali ke state awal                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ringkasan

| Topik               | Poin Penting                                                          |
| ------------------- | --------------------------------------------------------------------- |
| **dApp**          | Aplikasi dengan backend di blockchain (smart contract)                |
| **Web3 vs Web2**  | Decentralized vs centralized, user-owned vs company-owned             |
| **Komponen dApp** | Frontend + Web3 Library + Wallet + RPC Node + Smart Contract          |
| **Tech Stack**    | React + Vite + ethers.js + MetaMask + Hardhat                         |
| **Flow**          | Connect wallet -> Read data -> Send transaction -> Wait confirmation  |

---

## Tugas

### Tugas 1: Setup Project dApp

1. Buat struktur monorepo dengan folder `contracts` dan `frontend`
2. Setup frontend dengan Vite + React
3. Install ethers.js
4. Screenshot struktur folder

### Tugas 2: Implementasi Hello dApp

1. Implementasikan Hello dApp sesuai tutorial
2. Pastikan bisa connect/disconnect wallet
3. Tampilkan address dan balance
4. Screenshot tampilan dApp saat connected

### Tugas 3: Tambah Fitur Network Info

1. Tambahkan tampilan informasi network yang sedang terkoneksi
2. Tampilkan: Network Name, Chain ID
3. Beri warning jika bukan network yang diharapkan

**Hint:** Gunakan `window.ethereum.request({ method: 'eth_chainId' })`

### Deliverable

Kumpulkan:
1. Screenshot struktur folder project
2. Screenshot dApp berjalan (disconnected state)
3. Screenshot dApp berjalan (connected state dengan address dan balance)
4. Screenshot fitur network info (Tugas 3)
5. File `App.jsx` yang sudah dimodifikasi

---

## Referensi

- [Ethereum Developer Documentation](https://ethereum.org/developers)
- [ethers.js Documentation](https://docs.ethers.org/v6/)
- [MetaMask Documentation](https://docs.metamask.io/)
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
