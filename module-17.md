# Modul 17. dApp pada Bitcoin vs Ethereum: Perbandingan Platform

## Deskripsi

Modul ini membahas perbedaan fundamental antara **dApp (Decentralized Application)** yang dibangun di atas blockchain **Bitcoin** versus **Ethereum** dan platform sejenis. Mahasiswa akan memahami mengapa sebagian besar dApp dibangun di Ethereum, bagaimana Bitcoin juga bisa mendukung dApp melalui layer-2 solutions, serta perbandingan ekosistem dApp di berbagai public blockchain.

## Tujuan Pembelajaran

Setelah menyelesaikan modul ini, mahasiswa mampu:

1. Memahami perbedaan arsitektur Bitcoin vs Ethereum untuk pengembangan dApp
2. Menjelaskan keterbatasan Bitcoin sebagai platform dApp dan solusinya
3. Membandingkan smart contract capability di berbagai blockchain
4. Mengidentifikasi use case yang cocok untuk masing-masing platform
5. Mengenal ekosistem dApp di Bitcoin (Lightning, Stacks, RSK) dan Ethereum (Layer-2)

## Prasyarat

- Sudah menyelesaikan Module 02-06 (Blockchain & Cryptocurrency Fundamentals)
- Memahami konsep dasar blockchain, transaksi, dan konsensus
- Memahami konsep smart contract (Module 07-08)

## List of Contents

- [1. Mengapa Ada Perbedaan?](#1-mengapa-ada-perbedaan)
- [2. Bitcoin: Digital Gold vs Programmable Money](#2-bitcoin-digital-gold-vs-programmable-money)
- [3. Ethereum: World Computer](#3-ethereum-world-computer)
- [4. Perbandingan Arsitektur](#4-perbandingan-arsitektur)
- [5. dApp di Ekosistem Bitcoin](#5-dapp-di-ekosistem-bitcoin)
- [6. dApp di Ekosistem Ethereum](#6-dapp-di-ekosistem-ethereum)
- [7. Platform Blockchain Lainnya](#7-platform-blockchain-lainnya)
- [8. Perbandingan Komprehensif](#8-perbandingan-komprehensif)
- [9. Memilih Platform yang Tepat](#9-memilih-platform-yang-tepat)
- [Ringkasan](#ringkasan)
- [Tugas](#tugas)

---

## 1. Mengapa Ada Perbedaan?

### 1.1 Filosofi Desain yang Berbeda

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FILOSOFI DESAIN: BITCOIN vs ETHEREUM                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  BITCOIN (2009)                        ETHEREUM (2015)                      │
│  ┌─────────────────────────┐          ┌─────────────────────────┐          │
│  │                         │          │                         │          │
│  │  "Peer-to-peer          │          │  "World Computer"       │          │
│  │   electronic cash       │          │                         │          │
│  │   system"               │          │  "Programmable          │          │
│  │                         │          │   blockchain"           │          │
│  │  Tujuan: Uang digital   │          │                         │          │
│  │  yang terdesentralisasi │          │  Tujuan: Platform       │          │
│  │                         │          │  untuk aplikasi         │          │
│  │  Fokus:                 │          │  terdesentralisasi      │          │
│  │  - Keamanan             │          │                         │          │
│  │  - Stabilitas           │          │  Fokus:                 │          │
│  │  - Kesederhanaan        │          │  - Programmability      │          │
│  │                         │          │  - Fleksibilitas        │          │
│  │  Dibuat oleh:           │          │  - Ekosistem            │          │
│  │  Satoshi Nakamoto       │          │                         │          │
│  │                         │          │  Dibuat oleh:           │          │
│  └─────────────────────────┘          │  Vitalik Buterin        │          │
│                                       │                         │          │
│                                       └─────────────────────────┘          │
│                                                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│                                                                             │
│  Analogi:                                                                   │
│  ┌─────────────────────────┐          ┌─────────────────────────┐          │
│  │  BITCOIN = Kalkulator   │          │  ETHEREUM = Komputer    │          │
│  │                         │          │                         │          │
│  │  Sangat baik untuk      │          │  Bisa menjalankan       │          │
│  │  satu fungsi: hitung    │          │  berbagai program       │          │
│  │                         │          │                         │          │
│  │  Sederhana, aman,       │          │  Kompleks, fleksibel,   │          │
│  │  terpercaya             │          │  powerful               │          │
│  └─────────────────────────┘          └─────────────────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Pertanyaan Umum yang Membingungkan

> **"Kenapa tidak semua dApp dibangun di Bitcoin saja? Bukankah Bitcoin lebih terkenal dan aman?"**

Jawaban singkat: **Bitcoin tidak didesain untuk itu.**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MISKONSEPSI UMUM                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ SALAH: "Bitcoin dan Ethereum sama saja, cuma beda nama"                 │
│                                                                             │
│  ✅ BENAR: Bitcoin dan Ethereum adalah blockchain dengan                    │
│            tujuan dan kemampuan yang SANGAT BERBEDA                         │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  ❌ SALAH: "Semua blockchain bisa menjalankan smart contract"               │
│                                                                             │
│  ✅ BENAR: Tidak semua blockchain memiliki kemampuan smart contract.        │
│            Bitcoin memiliki scripting SANGAT TERBATAS.                      │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  ❌ SALAH: "dApp hanya bisa dibangun di Ethereum"                           │
│                                                                             │
│  ✅ BENAR: dApp bisa dibangun di berbagai platform, termasuk               │
│            di atas Bitcoin menggunakan layer-2 solutions                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Bitcoin: Digital Gold vs Programmable Money

### 2.1 Bitcoin Script: Bahasa Scripting Terbatas

Bitcoin memiliki bahasa scripting sendiri yang disebut **Bitcoin Script**, tapi sangat terbatas dibandingkan smart contract Ethereum.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BITCOIN SCRIPT                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Karakteristik Bitcoin Script:                                              │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  1. TIDAK TURING COMPLETE                                           │   │
│  │     - Tidak ada loop (for, while)                                   │   │
│  │     - Tidak ada rekursi                                             │   │
│  │     - Eksekusi selalu berhenti (tidak bisa infinite loop)           │   │
│  │                                                                     │   │
│  │  2. STACK-BASED                                                     │   │
│  │     - Operasi berbasis stack sederhana                              │   │
│  │     - Seperti kalkulator Reverse Polish Notation (RPN)              │   │
│  │                                                                     │   │
│  │  3. LIMITED OPCODES                                                 │   │
│  │     - Hanya ~100 opcodes                                            │   │
│  │     - Banyak yang disabled untuk keamanan                           │   │
│  │                                                                     │   │
│  │  4. STATELESS                                                       │   │
│  │     - Tidak menyimpan state                                         │   │
│  │     - Setiap script independen                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Contoh Bitcoin Script sederhana (P2PKH):                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ScriptPubKey (Locking Script):                                     │   │
│  │  OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG          │   │
│  │                                                                     │   │
│  │  ScriptSig (Unlocking Script):                                      │   │
│  │  <signature> <publicKey>                                            │   │
│  │                                                                     │   │
│  │  Artinya: "Buktikan kamu pemilik private key dari address ini"      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Apa yang BISA Dilakukan Bitcoin Script?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    KEMAMPUAN BITCOIN SCRIPT                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ✅ BISA:                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  1. Pay-to-Public-Key-Hash (P2PKH)                                  │   │
│  │     └── Transfer Bitcoin ke address biasa                          │   │
│  │                                                                     │   │
│  │  2. Multi-Signature (MultiSig)                                      │   │
│  │     └── Membutuhkan M dari N tanda tangan                          │   │
│  │     └── Contoh: 2-of-3 multisig untuk corporate wallet             │   │
│  │                                                                     │   │
│  │  3. Time-Locked Transactions                                        │   │
│  │     └── CLTV (CheckLockTimeVerify): Lock sampai waktu tertentu     │   │
│  │     └── CSV (CheckSequenceVerify): Lock sampai N block             │   │
│  │                                                                     │   │
│  │  4. Hash Time-Locked Contracts (HTLC)                               │   │
│  │     └── Dasar dari Lightning Network                               │   │
│  │     └── Atomic Swaps antar blockchain                              │   │
│  │                                                                     │   │
│  │  5. Pay-to-Script-Hash (P2SH)                                       │   │
│  │     └── Script kompleks yang di-hash                               │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ❌ TIDAK BISA:                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  1. Loop atau iterasi                                               │   │
│  │     └── Tidak bisa: for, while, recursion                          │   │
│  │                                                                     │   │
│  │  2. Menyimpan state kompleks                                        │   │
│  │     └── Tidak ada storage seperti Ethereum                         │   │
│  │                                                                     │   │
│  │  3. Memanggil script lain                                           │   │
│  │     └── Tidak ada composability                                    │   │
│  │                                                                     │   │
│  │  4. Kalkulasi kompleks                                              │   │
│  │     └── Tidak bisa: AMM, lending protocols, complex DeFi           │   │
│  │                                                                     │   │
│  │  5. NFT native                                                      │   │
│  │     └── Perlu workaround (Ordinals, Inscriptions)                  │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Mengapa Bitcoin Dibuat Terbatas?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ALASAN KETERBATASAN BITCOIN                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Design Decision oleh Satoshi Nakamoto:                                     │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  1. KEAMANAN > FITUR                                                │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │  "Lebih sedikit fitur = lebih sedikit attack surface"   │    │   │
│  │     │                                                         │    │   │
│  │     │  Bitcoin Script yang terbatas berarti:                  │    │   │
│  │     │  - Tidak ada bug infinite loop                          │    │   │
│  │     │  - Lebih mudah di-audit                                 │    │   │
│  │     │  - Lebih predictable                                    │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  │  2. TUJUAN SPESIFIK: UANG DIGITAL                                   │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │  Bitcoin dibuat untuk SATU tujuan:                      │    │   │
│  │     │  Transfer nilai secara peer-to-peer                     │    │   │
│  │     │                                                         │    │   │
│  │     │  Tidak perlu:                                           │    │   │
│  │     │  - DeFi protocols                                       │    │   │
│  │     │  - NFT marketplace                                      │    │   │
│  │     │  - Gaming                                               │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  │  3. IMMUTABILITY & CONSERVATISM                                     │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │  Perubahan di Bitcoin sangat LAMBAT dan HATI-HATI       │    │   │
│  │     │                                                         │    │   │
│  │     │  - SegWit butuh bertahun-tahun untuk diadopsi           │    │   │
│  │     │  - Taproot upgrade memakan waktu lama                   │    │   │
│  │     │  - Komunitas sangat konservatif terhadap perubahan      │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Hasilnya:                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Bitcoin = Paling aman, paling terdesentralisasi, paling stabil    │   │
│  │            TAPI tidak fleksibel untuk dApp kompleks                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Ethereum: World Computer

### 3.1 Ethereum Virtual Machine (EVM)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ETHEREUM VIRTUAL MACHINE (EVM)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Karakteristik EVM:                                                         │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  1. TURING COMPLETE                                                 │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │  - Bisa menjalankan SEMUA jenis komputasi               │    │   │
│  │     │  - Loop, rekursi, conditional logic                     │    │   │
│  │     │  - Sama powerful seperti komputer biasa                 │    │   │
│  │     │                                                         │    │   │
│  │     │  Tapi ada batasan: GAS LIMIT                            │    │   │
│  │     │  - Setiap operasi butuh gas                             │    │   │
│  │     │  - Gas habis = eksekusi berhenti                        │    │   │
│  │     │  - Mencegah infinite loop                               │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  │  2. STATEFUL                                                        │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │  - Smart contract menyimpan STATE di blockchain         │    │   │
│  │     │  - mapping, arrays, structs                             │    │   │
│  │     │  - State persisten dan bisa diubah                      │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  │  3. COMPOSABLE                                                      │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │  - Contract bisa memanggil contract lain                │    │   │
│  │     │  - "Money Legos" - building blocks                      │    │   │
│  │     │  - DeFi protocols saling terintegrasi                   │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  │  4. DETERMINISTIC                                                   │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │  - Semua node mendapat hasil yang SAMA                  │    │   │
│  │     │  - Tidak ada randomness native                          │    │   │
│  │     │  - Predictable execution                                │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Smart Contract: Program di Blockchain

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SMART CONTRACT ETHEREUM                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Apa yang membuat Ethereum berbeda:                                         │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  BITCOIN TRANSACTION:                                               │   │
│  │  ┌───────────────────────────────────────────────────────────────┐ │   │
│  │  │  "Transfer 1 BTC dari Alice ke Bob"                           │ │   │
│  │  │                                                               │ │   │
│  │  │  Input: Alice's UTXO                                          │ │   │
│  │  │  Output: Bob's Address                                        │ │   │
│  │  │                                                               │ │   │
│  │  │  Hanya ITU. Tidak ada logic tambahan.                         │ │   │
│  │  └───────────────────────────────────────────────────────────────┘ │   │
│  │                                                                     │   │
│  │  vs                                                                 │   │
│  │                                                                     │   │
│  │  ETHEREUM SMART CONTRACT:                                           │   │
│  │  ┌───────────────────────────────────────────────────────────────┐ │   │
│  │  │  contract Escrow {                                            │ │   │
│  │  │      address buyer;                                           │ │   │
│  │  │      address seller;                                          │ │   │
│  │  │      uint256 amount;                                          │ │   │
│  │  │      bool delivered;                                          │ │   │
│  │  │                                                               │ │   │
│  │  │      function deposit() { ... }                               │ │   │
│  │  │      function confirmDelivery() { ... }                       │ │   │
│  │  │      function releaseFunds() { ... }                          │ │   │
│  │  │      function refund() { ... }                                │ │   │
│  │  │  }                                                            │ │   │
│  │  │                                                               │ │   │
│  │  │  Logic kompleks, state management, multiple functions         │ │   │
│  │  └───────────────────────────────────────────────────────────────┘ │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Solidity: Bahasa Smart Contract

```solidity
// Contoh Smart Contract Ethereum (Solidity)
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title SimpleToken
 * @dev Contoh token sederhana - TIDAK MUNGKIN di Bitcoin native
 */
contract SimpleToken {
    // STATE VARIABLES - disimpan di blockchain
    string public name = "MyToken";
    string public symbol = "MTK";
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    // EVENTS - untuk tracking
    event Transfer(address indexed from, address indexed to, uint256 amount);

    // CONSTRUCTOR - dijalankan sekali saat deploy
    constructor(uint256 _initialSupply) {
        totalSupply = _initialSupply;
        balanceOf[msg.sender] = _initialSupply;
    }

    // FUNCTIONS - logic yang bisa dipanggil
    function transfer(address to, uint256 amount) public returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");

        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;

        emit Transfer(msg.sender, to, amount);
        return true;
    }
}

// Hal-hal di atas TIDAK BISA dilakukan di Bitcoin Script:
// 1. mapping (key-value storage)
// 2. State yang bisa diubah
// 3. Events
// 4. Complex functions dengan multiple operations
// 5. String storage
```

---

## 4. Perbandingan Arsitektur

### 4.1 Tabel Perbandingan Teknis

| Aspek                      | Bitcoin          | Ethereum             |
| -------------------------- | ---------------- | -------------------- |
| **Tahun Lahir**      | 2009             | 2015                 |
| **Pembuat**          | Satoshi Nakamoto | Vitalik Buterin      |
| **Bahasa Script**    | Bitcoin Script   | Solidity, Vyper, dll |
| **Turing Complete**  | Tidak            | Ya                   |
| **State Management** | Stateless (UTXO) | Stateful (Account)   |
| **Smart Contract**   | Sangat terbatas  | Fully programmable   |
| **Block Time**       | ~10 menit        | ~12 detik            |
| **Konsensus**        | Proof of Work    | Proof of Stake       |
| **TPS (native)**     | ~7 tx/s          | ~15-30 tx/s          |
| **Gas/Fee Model**    | Satoshi per byte | Gas per computation  |
| **Native Token**     | BTC              | ETH                  |
| **Token Standard**   | Tidak ada native | ERC-20, ERC-721, dll |

### 4.2 Diagram Arsitektur

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ARSITEKTUR: BITCOIN vs ETHEREUM                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  BITCOIN ARCHITECTURE                                                       │
│  ════════════════════                                                       │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         BITCOIN BLOCKCHAIN                          │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐               │   │
│  │  │ Block 1 │──│ Block 2 │──│ Block 3 │──│ Block N │               │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘               │   │
│  │       │            │            │            │                      │   │
│  │       ▼            ▼            ▼            ▼                      │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │                    TRANSACTIONS (UTXO)                      │   │   │
│  │  │  Input (spent) ──► Output (unspent) ──► Input ──► Output    │   │   │
│  │  │                                                             │   │   │
│  │  │  Setiap UTXO hanya bisa digunakan SEKALI                    │   │   │
│  │  │  Tidak ada state yang disimpan                              │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ETHEREUM ARCHITECTURE                                                      │
│  ═════════════════════                                                      │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        ETHEREUM BLOCKCHAIN                          │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐               │   │
│  │  │ Block 1 │──│ Block 2 │──│ Block 3 │──│ Block N │               │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘               │   │
│  │       │            │            │            │                      │   │
│  │       ▼            ▼            ▼            ▼                      │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │                      WORLD STATE                            │   │   │
│  │  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │   │   │
│  │  │  │   Account 1   │  │   Account 2   │  │  Contract A   │   │   │   │
│  │  │  │  Balance: 5   │  │  Balance: 10  │  │  Code: ...    │   │   │   │
│  │  │  │  Nonce: 3     │  │  Nonce: 7     │  │  Storage:     │   │   │   │
│  │  │  └───────────────┘  └───────────────┘  │  - var1: 100  │   │   │   │
│  │  │                                        │  - var2: 200  │   │   │   │
│  │  │                                        │  - mapping... │   │   │   │
│  │  │                                        └───────────────┘   │   │   │
│  │  │                                                             │   │   │
│  │  │  State berubah setiap block                                 │   │   │
│  │  │  Smart contracts menyimpan data kompleks                    │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 UTXO vs Account Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UTXO MODEL vs ACCOUNT MODEL                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  BITCOIN: UTXO (Unspent Transaction Output)                                 │
│  ═════════════════════════════════════════                                  │
│                                                                             │
│  Analogi: Seperti UANG TUNAI                                                │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Alice punya:                                                       │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐                                │   │
│  │  │ 2 BTC  │  │ 3 BTC  │  │ 1 BTC  │   Total: 6 BTC                 │   │
│  │  │ (UTXO) │  │ (UTXO) │  │ (UTXO) │                                │   │
│  │  └────────┘  └────────┘  └────────┘                                │   │
│  │                                                                     │   │
│  │  Alice kirim 4 BTC ke Bob:                                          │   │
│  │  - Gunakan UTXO 2 BTC + 3 BTC = 5 BTC (input)                       │   │
│  │  - Output: 4 BTC ke Bob, 1 BTC kembali ke Alice (change)            │   │
│  │  - UTXO lama "burned", UTXO baru dibuat                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Kelebihan UTXO:                                                            │
│  + Privacy lebih baik (banyak address)                                      │
│  + Parallel transaction processing                                          │
│  + Tidak ada nonce race condition                                           │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  ETHEREUM: ACCOUNT MODEL                                                    │
│  ═══════════════════════                                                    │
│                                                                             │
│  Analogi: Seperti REKENING BANK                                             │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Alice's Account:                                                   │   │
│  │  ┌─────────────────────────────────────┐                           │   │
│  │  │  Address: 0xAlice...                │                           │   │
│  │  │  Balance: 6 ETH                     │                           │   │
│  │  │  Nonce: 5                           │                           │   │
│  │  └─────────────────────────────────────┘                           │   │
│  │                                                                     │   │
│  │  Alice kirim 4 ETH ke Bob:                                          │   │
│  │  - Alice.balance -= 4                                               │   │
│  │  - Bob.balance += 4                                                 │   │
│  │  - Alice.nonce += 1                                                 │   │
│  │                                                                     │   │
│  │  Sederhana dan intuitif!                                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Kelebihan Account:                                                         │
│  + Lebih mudah dipahami                                                     │
│  + Cocok untuk smart contract dengan state                                  │
│  + Hemat space (tidak perlu reference ke UTXO)                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. dApp di Ekosistem Bitcoin

### 5.1 Solusi Layer-2 Bitcoin

Meskipun Bitcoin tidak mendukung smart contract kompleks secara native, ada beberapa solusi untuk membangun dApp:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BITCOIN LAYER-2 SOLUTIONS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                           ┌─────────────────────┐                           │
│                           │   BITCOIN LAYER 1   │                           │
│                           │   (Base Layer)      │                           │
│                           │   - Keamanan        │                           │
│                           │   - Settlement      │                           │
│                           │   - Store of Value  │                           │
│                           └──────────┬──────────┘                           │
│                                      │                                      │
│            ┌─────────────────────────┼─────────────────────────┐            │
│            │                         │                         │            │
│            ▼                         ▼                         ▼            │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐       │
│  │   LIGHTNING     │     │     STACKS      │     │      RSK        │       │
│  │   NETWORK       │     │   (ex-Blockstack)│    │  (Rootstock)    │       │
│  │                 │     │                 │     │                 │       │
│  │  Payment        │     │  Smart Contract │     │  EVM-Compatible │       │
│  │  Channels       │     │  Platform       │     │  Sidechain      │       │
│  │                 │     │                 │     │                 │       │
│  │  - Micropayments│     │  - Clarity Lang │     │  - Solidity     │       │
│  │  - Instant      │     │  - DeFi         │     │  - Port ETH dApps│      │
│  │  - Low fees     │     │  - NFTs         │     │  - 2-way peg    │       │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘       │
│            │                         │                         │            │
│            ▼                         ▼                         ▼            │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐       │
│  │    LIQUID       │     │    ORDINALS     │     │    RGB          │       │
│  │   NETWORK       │     │  & INSCRIPTIONS │     │   PROTOCOL      │       │
│  │                 │     │                 │     │                 │       │
│  │  Federated      │     │  NFTs on Bitcoin│     │  Smart Contracts│       │
│  │  Sidechain      │     │  (2023+)        │     │  on Lightning   │       │
│  │                 │     │                 │     │                 │       │
│  │  - Fast settle  │     │  - BRC-20 tokens│     │  - Client-side  │       │
│  │  - Confidential │     │  - Digital art  │     │    validation   │       │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Lightning Network

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LIGHTNING NETWORK                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Apa itu Lightning Network?                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Layer-2 payment protocol di atas Bitcoin                           │   │
│  │  - Pembayaran instan (milidetik)                                    │   │
│  │  - Fee sangat rendah (< 1 satoshi)                                  │   │
│  │  - Jutaan transaksi per detik (teoritis)                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Cara Kerja:                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  1. OPEN CHANNEL                                                    │   │
│  │     ┌─────┐         On-chain TX          ┌─────┐                   │   │
│  │     │Alice│ ──────────────────────────── │ Bob │                   │   │
│  │     └─────┘    "Lock 0.1 BTC in          └─────┘                   │   │
│  │                 multisig channel"                                   │   │
│  │                                                                     │   │
│  │  2. OFF-CHAIN TRANSACTIONS                                          │   │
│  │     ┌─────┐  ───── 0.01 BTC ─────►  ┌─────┐                        │   │
│  │     │Alice│  ◄──── 0.02 BTC ──────  │ Bob │   (Instant, free!)     │   │
│  │     └─────┘  ───── 0.005 BTC ────►  └─────┘                        │   │
│  │                                                                     │   │
│  │     Transaksi terjadi OFF-CHAIN                                     │   │
│  │     Tidak perlu konfirmasi blockchain                               │   │
│  │                                                                     │   │
│  │  3. CLOSE CHANNEL                                                   │   │
│  │     ┌─────┐         On-chain TX          ┌─────┐                   │   │
│  │     │Alice│ ──────────────────────────── │ Bob │                   │   │
│  │     └─────┘    "Settle final balance"    └─────┘                   │   │
│  │                                                                     │   │
│  │     Alice: 0.045 BTC, Bob: 0.055 BTC                                │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  dApp di Lightning Network:                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Wallet: Muun, Phoenix, BlueWallet                                │   │
│  │  - Payment: Strike, Cash App (LN support)                           │   │
│  │  - Micropayments: Podcasting 2.0, pay-per-article                   │   │
│  │  - Gaming: Zebedee games                                            │   │
│  │  - Social: Nostr + Lightning tips                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Keterbatasan:                                                              │
│  - Bukan smart contract platform (hanya payment)                            │
│  - Channel liquidity terbatas                                               │
│  - Kompleks untuk user awam                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Stacks (Smart Contract di Bitcoin)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STACKS BLOCKCHAIN                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Apa itu Stacks?                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Smart contract platform yang "anchored" ke Bitcoin                 │   │
│  │  - Menggunakan Bitcoin sebagai settlement layer                     │   │
│  │  - Punya native token: STX                                          │   │
│  │  - Bahasa: Clarity (bukan Solidity)                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Arsitektur:                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  ┌──────────────────────────────────────────────────────────────┐  │   │
│  │  │                    STACKS BLOCKCHAIN                         │  │   │
│  │  │  ┌────────────────────────────────────────────────────────┐  │  │   │
│  │  │  │  Smart Contracts (Clarity)                             │  │  │   │
│  │  │  │  - DeFi: ALEX, Arkadiko                                │  │  │   │
│  │  │  │  - NFTs: Gamma, StacksArt                              │  │  │   │
│  │  │  │  - DAOs: ExecutorDAO                                   │  │  │   │
│  │  │  └────────────────────────────────────────────────────────┘  │  │   │
│  │  │                          │                                   │  │   │
│  │  │                          │ Proof of Transfer (PoX)           │  │   │
│  │  │                          │ "Anchors" ke Bitcoin              │  │   │
│  │  │                          ▼                                   │  │   │
│  │  └──────────────────────────┼───────────────────────────────────┘  │   │
│  │                             │                                      │   │
│  │  ┌──────────────────────────▼───────────────────────────────────┐  │   │
│  │  │                    BITCOIN BLOCKCHAIN                        │  │   │
│  │  │  - Security & finality dari Bitcoin PoW                      │  │   │
│  │  │  - Stacks block hash di-commit ke Bitcoin                    │  │   │
│  │  └──────────────────────────────────────────────────────────────┘  │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Clarity Language (berbeda dari Solidity):                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ;; Contoh Clarity smart contract                                   │   │
│  │  (define-data-var counter uint u0)                                  │   │
│  │                                                                     │   │
│  │  (define-public (increment)                                         │   │
│  │    (begin                                                           │   │
│  │      (var-set counter (+ (var-get counter) u1))                     │   │
│  │      (ok (var-get counter))))                                       │   │
│  │                                                                     │   │
│  │  (define-read-only (get-counter)                                    │   │
│  │    (ok (var-get counter)))                                          │   │
│  │                                                                     │   │
│  │  Kelebihan Clarity:                                                 │   │
│  │  - Decidable (bisa dianalisis sebelum eksekusi)                     │   │
│  │  - Tidak ada reentrancy attack                                      │   │
│  │  - Lebih aman dari Solidity                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.4 Ordinals & BRC-20 (NFT/Token di Bitcoin)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ORDINALS & INSCRIPTIONS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Apa itu Ordinals? (2023)                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Protokol untuk memberi "identitas" ke setiap satoshi               │   │
│  │  - 1 BTC = 100,000,000 satoshi                                      │   │
│  │  - Setiap satoshi bisa di-track dan diberi nomor urut               │   │
│  │  - Satoshi bisa di-"inscribe" dengan data (gambar, teks, dll)       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Cara Kerja:                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  1. ORDINAL THEORY                                                  │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │  Satoshi #0 → Satoshi #1 → ... → Satoshi #N             │    │   │
│  │     │                                                         │    │   │
│  │     │  Setiap satoshi punya "ordinal number" unik             │    │   │
│  │     │  Bisa di-track melalui UTXO                             │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  │  2. INSCRIPTION                                                     │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │  Data (image, text, code) di-embed ke witness data      │    │   │
│  │     │  dari transaksi Bitcoin (SegWit/Taproot)                │    │   │
│  │     │                                                         │    │   │
│  │     │  ┌─────────────────┐                                    │    │   │
│  │     │  │  Inscription    │                                    │    │   │
│  │     │  │  ───────────    │                                    │    │   │
│  │     │  │  Content-Type:  │                                    │    │   │
│  │     │  │  image/png      │                                    │    │   │
│  │     │  │                 │                                    │    │   │
│  │     │  │  [Image Data]   │                                    │    │   │
│  │     │  │                 │                                    │    │   │
│  │     │  │  Attached to    │                                    │    │   │
│  │     │  │  Satoshi #X     │                                    │    │   │
│  │     │  └─────────────────┘                                    │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  BRC-20 Tokens:                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Token standard di Bitcoin menggunakan inscriptions                 │   │
│  │                                                                     │   │
│  │  Deploy token:                                                      │   │
│  │  {"p":"brc-20","op":"deploy","tick":"ORDI","max":"21000000"}        │   │
│  │                                                                     │   │
│  │  Mint token:                                                        │   │
│  │  {"p":"brc-20","op":"mint","tick":"ORDI","amt":"1000"}              │   │
│  │                                                                     │   │
│  │  Transfer:                                                          │   │
│  │  {"p":"brc-20","op":"transfer","tick":"ORDI","amt":"100"}           │   │
│  │                                                                     │   │
│  │  Catatan: Ini BUKAN smart contract!                                 │   │
│  │  - Hanya JSON data di inscription                                   │   │
│  │  - Indexer eksternal yang interpret                                 │   │
│  │  - Tidak ada on-chain logic                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Kontroversi Ordinals:                                                      │
│  + Pro:  Membawa NFT dan tokens ke Bitcoin                                  │
│  + Pro:  Meningkatkan fee untuk miners                                      │
│  - Kontra: "Spam" di blockchain Bitcoin                                     │
│  - Kontra: Bukan use case yang dimaksud Satoshi                             │
│  - Kontra: Meningkatkan block size dan fee                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. dApp di Ekosistem Ethereum

### 6.1 Kategori dApp Ethereum

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EKOSISTEM dApp ETHEREUM                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DeFi (Decentralized Finance)                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  DEX (Decentralized Exchange)                                       │   │
│  │  ├── Uniswap      : AMM terbesar, swap tokens                       │   │
│  │  ├── SushiSwap    : Fork Uniswap dengan rewards                     │   │
│  │  ├── Curve        : Optimized untuk stablecoin swaps                │   │
│  │  └── 1inch        : DEX aggregator                                  │   │
│  │                                                                     │   │
│  │  Lending/Borrowing                                                  │   │
│  │  ├── Aave         : Money market protocol                           │   │
│  │  ├── Compound     : Interest rate protocol                          │   │
│  │  └── MakerDAO     : CDP dan stablecoin DAI                          │   │
│  │                                                                     │   │
│  │  Derivatives                                                        │   │
│  │  ├── dYdX         : Perpetual trading                               │   │
│  │  ├── Synthetix    : Synthetic assets                                │   │
│  │  └── GMX          : Decentralized perpetuals                        │   │
│  │                                                                     │   │
│  │  Yield Aggregator                                                   │   │
│  │  ├── Yearn Finance: Auto-compound yields                            │   │
│  │  └── Convex       : Boost Curve yields                              │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  NFT & Gaming                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  Marketplace                                                        │   │
│  │  ├── OpenSea      : NFT marketplace terbesar                        │   │
│  │  ├── Blur         : Pro trader NFT marketplace                      │   │
│  │  └── LooksRare    : Community-owned marketplace                     │   │
│  │                                                                     │   │
│  │  Gaming                                                             │   │
│  │  ├── Axie Infinity: Play-to-earn pioneer                            │   │
│  │  ├── Gods Unchained: Trading card game                              │   │
│  │  └── Loot         : On-chain generative items                       │   │
│  │                                                                     │   │
│  │  Virtual Worlds                                                     │   │
│  │  ├── Decentraland : Virtual land and experiences                    │   │
│  │  └── The Sandbox  : User-created gaming                             │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Infrastructure                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  ├── The Graph    : Indexing & querying blockchain data             │   │
│  │  ├── Chainlink    : Oracle network (off-chain data)                 │   │
│  │  ├── ENS          : Decentralized domain names                      │   │
│  │  └── IPFS/Filecoin: Decentralized storage                           │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Social & Identity                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  ├── Lens Protocol: Decentralized social graph                      │   │
│  │  ├── Mirror       : Web3 publishing platform                        │   │
│  │  └── POAP         : Proof of attendance protocol                    │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Ethereum Layer-2 Solutions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ETHEREUM LAYER-2 SCALING                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Mengapa perlu Layer-2?                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Ethereum L1 terbatas:                                              │   │
│  │  - ~15-30 TPS                                                       │   │
│  │  - Gas fee tinggi saat congestion ($50-$500 per tx!)                │   │
│  │  - Tidak scalable untuk mass adoption                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Types of Layer-2:                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  1. OPTIMISTIC ROLLUPS                                              │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │  - Assume transaksi valid, challenge jika fraud          │    │   │
│  │     │  - 7 hari withdrawal period (untuk dispute)              │    │   │
│  │     │  - EVM compatible (mudah port dApps)                     │    │   │
│  │     │                                                          │    │   │
│  │     │  Examples:                                               │    │   │
│  │     │  ├── Optimism (OP): DeFi, social                        │    │   │
│  │     │  ├── Arbitrum: Largest by TVL                           │    │   │
│  │     │  └── Base (Coinbase): Consumer apps                     │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  │  2. ZK ROLLUPS (Zero-Knowledge)                                     │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │  - Validity proof untuk setiap batch                     │    │   │
│  │     │  - Instant finality (tidak perlu dispute period)         │    │   │
│  │     │  - Lebih kompleks secara teknis                          │    │   │
│  │     │                                                          │    │   │
│  │     │  Examples:                                               │    │   │
│  │     │  ├── zkSync Era: General purpose zkEVM                  │    │   │
│  │     │  ├── Starknet: Cairo language, gaming focus             │    │   │
│  │     │  ├── Polygon zkEVM: EVM equivalent                      │    │   │
│  │     │  └── Scroll: EVM equivalent zkRollup                    │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  │  3. SIDECHAINS                                                      │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │  - Blockchain terpisah dengan bridge ke Ethereum         │    │   │
│  │     │  - Punya consensus sendiri                               │    │   │
│  │     │  - Kurang decentralized tapi lebih cepat                 │    │   │
│  │     │                                                          │    │   │
│  │     │  Examples:                                               │    │   │
│  │     │  └── Polygon PoS: Paling populer, cheap & fast          │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Perbandingan Layer-2:                                                      │
│  ┌──────────────┬─────────────┬──────────────┬─────────────┬─────────────┐ │
│  │              │   Optimism  │   Arbitrum   │   zkSync    │  Polygon PoS│ │
│  ├──────────────┼─────────────┼──────────────┼─────────────┼─────────────┤ │
│  │ TPS          │   ~2,000    │   ~4,000     │   ~2,000    │   ~7,000    │ │
│  │ Avg Fee      │   $0.01-0.1 │   $0.01-0.1  │   $0.01-0.1 │   $0.001    │ │
│  │ Withdrawal   │   7 days    │   7 days     │   Minutes   │   ~3 hours  │ │
│  │ EVM Compat   │   Full      │   Full       │   Near-full │   Full      │ │
│  │ Security     │   ETH L1    │   ETH L1     │   ETH L1    │   Own PoS   │ │
│  └──────────────┴─────────────┴──────────────┴─────────────┴─────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Token Standards

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ETHEREUM TOKEN STANDARDS                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ERC-20: Fungible Token                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  interface IERC20 {                                                 │   │
│  │      function totalSupply() external view returns (uint256);        │   │
│  │      function balanceOf(address account) external view;             │   │
│  │      function transfer(address to, uint256 amount) external;        │   │
│  │      function approve(address spender, uint256 amount) external;    │   │
│  │      function transferFrom(address from, address to, uint256);      │   │
│  │  }                                                                  │   │
│  │                                                                     │   │
│  │  Use cases: USDC, USDT, LINK, UNI, AAVE, dan ribuan token lainnya   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ERC-721: Non-Fungible Token (NFT)                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  interface IERC721 {                                                │   │
│  │      function ownerOf(uint256 tokenId) external view;               │   │
│  │      function safeTransferFrom(address from, address to, uint256);  │   │
│  │      function approve(address to, uint256 tokenId) external;        │   │
│  │      function tokenURI(uint256 tokenId) external view;              │   │
│  │  }                                                                  │   │
│  │                                                                     │   │
│  │  Use cases: CryptoPunks, BAYC, art NFTs, gaming items               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ERC-1155: Multi-Token Standard                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Kombinasi fungible + non-fungible dalam satu contract            │   │
│  │  - Batch transfers (hemat gas)                                      │   │
│  │  - Cocok untuk gaming (multiple item types)                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Ini TIDAK ADA di Bitcoin native!                                           │
│  Bitcoin tidak punya token standard. Solusi seperti BRC-20 adalah          │
│  workaround menggunakan inscriptions, bukan smart contract.                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Platform Blockchain Lainnya

### 7.1 EVM-Compatible Chains

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EVM-COMPATIBLE BLOCKCHAINS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Apa itu EVM-Compatible?                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Blockchain yang menjalankan Ethereum Virtual Machine (EVM)         │   │
│  │  - Bisa deploy smart contract Solidity tanpa modifikasi             │   │
│  │  - Bisa pakai tools yang sama: Hardhat, MetaMask, Ethers.js         │   │
│  │  - Migrasi dApp relatif mudah                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Popular EVM Chains:                                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  BNB Chain (ex-BSC)                                                 │   │
│  │  ├── Oleh: Binance                                                  │   │
│  │  ├── Konsensus: Proof of Staked Authority                           │   │
│  │  ├── TPS: ~160                                                      │   │
│  │  ├── Fee: ~$0.10                                                    │   │
│  │  └── Use: PancakeSwap, Venus, gaming                                │   │
│  │                                                                     │   │
│  │  Avalanche (C-Chain)                                                │   │
│  │  ├── Konsensus: Avalanche consensus                                 │   │
│  │  ├── TPS: ~4,500                                                    │   │
│  │  ├── Fee: ~$0.01-0.10                                               │   │
│  │  └── Use: Trader Joe, AAVE, gaming                                  │   │
│  │                                                                     │   │
│  │  Fantom                                                             │   │
│  │  ├── Konsensus: Lachesis (aBFT)                                     │   │
│  │  ├── TPS: ~25,000 (teoritis)                                        │   │
│  │  ├── Fee: <$0.01                                                    │   │
│  │  └── Use: SpookySwap, DeFi                                          │   │
│  │                                                                     │   │
│  │  Cronos                                                             │   │
│  │  ├── Oleh: Crypto.com                                               │   │
│  │  └── Use: DeFi, NFT dari Crypto.com ecosystem                       │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Non-EVM Smart Contract Platforms

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NON-EVM SMART CONTRACT PLATFORMS                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Solana                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Language: Rust, C, C++                                             │   │
│  │  Konsensus: Proof of History + Proof of Stake                       │   │
│  │  TPS: ~65,000 (teoritis), ~3,000 (praktek)                          │   │
│  │  Fee: <$0.001                                                       │   │
│  │  Block time: ~400ms                                                 │   │
│  │                                                                     │   │
│  │  Kelebihan:                                                         │   │
│  │  + Sangat cepat dan murah                                           │   │
│  │  + Single global state                                              │   │
│  │                                                                     │   │
│  │  Kekurangan:                                                        │   │
│  │  - Learning curve tinggi (Rust)                                     │   │
│  │  - Outages yang sering                                              │   │
│  │  - Tidak EVM compatible                                             │   │
│  │                                                                     │   │
│  │  dApps: Raydium, Orca, Magic Eden, Marinade                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Cardano                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Language: Plutus (Haskell-based), Marlowe                          │   │
│  │  Konsensus: Ouroboros (Proof of Stake)                              │   │
│  │  Model: Extended UTXO (eUTXO)                                       │   │
│  │                                                                     │   │
│  │  Kelebihan:                                                         │   │
│  │  + Peer-reviewed research                                           │   │
│  │  + Formal verification friendly                                     │   │
│  │                                                                     │   │
│  │  Kekurangan:                                                        │   │
│  │  - Development lambat                                               │   │
│  │  - eUTXO kompleks untuk DeFi                                        │   │
│  │  - Ekosistem masih kecil                                            │   │
│  │                                                                     │   │
│  │  dApps: SundaeSwap, Minswap, JPG Store                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Cosmos                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Language: CosmWasm (Rust), SDK (Go)                                │   │
│  │  Konsensus: Tendermint BFT                                          │   │
│  │  Model: App-specific blockchains                                    │   │
│  │                                                                     │   │
│  │  Kelebihan:                                                         │   │
│  │  + Build your own blockchain                                        │   │
│  │  + IBC (Inter-Blockchain Communication)                             │   │
│  │  + Sovereignty per chain                                            │   │
│  │                                                                     │   │
│  │  Chains: Osmosis, Juno, Secret Network, Terra                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Polkadot                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Language: ink! (Rust), Substrate                                   │   │
│  │  Konsensus: Nominated Proof of Stake                                │   │
│  │  Model: Parachains (parallel chains)                                │   │
│  │                                                                     │   │
│  │  Kelebihan:                                                         │   │
│  │  + Shared security dari Relay Chain                                 │   │
│  │  + Cross-chain messaging (XCM)                                      │   │
│  │  + Customizable parachains                                          │   │
│  │                                                                     │   │
│  │  Parachains: Acala, Moonbeam, Astar                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Perbandingan Komprehensif

### 8.1 Feature Comparison Matrix

| Feature                    | Bitcoin         | Bitcoin L2 (Stacks) | Ethereum      | Ethereum L2   | Solana    |
| -------------------------- | --------------- | ------------------- | ------------- | ------------- | --------- |
| **Smart Contract**   | Tidak           | Ya (Clarity)        | Ya (Solidity) | Ya (Solidity) | Ya (Rust) |
| **dApp Support**     | Minimal         | Ya                  | Penuh         | Penuh         | Penuh     |
| **TPS**              | ~7              | ~50                 | ~15-30        | ~2,000-4,000  | ~3,000    |
| **Block Time**       | 10 menit        | 10 menit*           | 12 detik      | 2 detik       | 400ms     |
| **Fee (avg)**        | $1-50 | $0.01-1 | $1-100 | $0.01-0.1  | <$0.001       |               |           |
| **Token Standard**   | Tidak ada       | SIP-010             | ERC-20/721    | ERC-20/721    | SPL       |
| **DeFi TVL**         | $1B* | $100M    | $50B+ | $10B+       | $1B           |               |           |
| **NFT**              | Ordinals*       | Ya                  | Ya            | Ya            | Ya        |
| **Security**         | Tertinggi       | Bitcoin-backed      | Tinggi        | Inherit ETH   | Medium    |
| **Decentralization** | Tertinggi       | Medium              | Tinggi        | Varies        | Medium    |

*Data indikatif, dapat berubah

### 8.2 Kapan Menggunakan Masing-Masing?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DECISION MATRIX: MEMILIH PLATFORM                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  BITCOIN (L1)                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  ✅ Gunakan untuk:                                                  │    │
│  │  - Store of value (HODLing)                                         │   │
│  │  - Large value transfers                                            │   │
│  │  - Maximum security & decentralization                              │   │
│  │  - Treasury/reserve asset                                           │   │
│  │                                                                     │   │
│  │  ❌ Jangan gunakan untuk:                                           │   │
│  │  - Complex smart contracts                                          │   │
│  │  - DeFi applications                                                │   │
│  │  - NFT marketplaces                                                 │   │
│  │  - High-frequency trading                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  LIGHTNING NETWORK                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ✅ Gunakan untuk:                                                  │   │
│  │  - Micropayments (streaming money)                                  │   │
│  │  - Point of sale payments                                           │   │
│  │  - Instant Bitcoin transfers                                        │   │
│  │  - Tipping & content monetization                                   │   │
│  │                                                                     │   │
│  │  ❌ Jangan gunakan untuk:                                           │   │
│  │  - Smart contracts                                                  │   │
│  │  - Long-term storage                                                │   │
│  │  - Large value (channel limits)                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  STACKS (Bitcoin L2)                                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ✅ Gunakan untuk:                                                  │   │
│  │  - Smart contracts dengan Bitcoin security                          │   │
│  │  - Bitcoin-native DeFi                                              │   │
│  │  - NFTs backed by Bitcoin                                           │   │
│  │                                                                     │   │
│  │  ❌ Jangan gunakan untuk:                                           │   │
│  │  - EVM compatibility needed                                         │   │
│  │  - High-speed trading (block time lambat)                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ETHEREUM (L1)                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ✅ Gunakan untuk:                                                  │   │
│  │  - High-value DeFi (large TVL)                                      │   │
│  │  - Maximum liquidity                                                │   │
│  │  - Protocol deployment (canonical version)                          │   │
│  │  - Blue-chip NFTs                                                   │   │
│  │                                                                     │   │
│  │  ❌ Jangan gunakan untuk:                                           │   │
│  │  - Low-value transactions (fee > value)                             │   │
│  │  - Gaming (terlalu lambat & mahal)                                  │   │
│  │  - High-frequency operations                                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ETHEREUM L2 (Arbitrum, Optimism, zkSync)                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ✅ Gunakan untuk:                                                  │   │
│  │  - DeFi dengan fee rendah                                           │   │
│  │  - Gaming (lebih cepat & murah)                                     │   │
│  │  - Frequent transactions                                            │   │
│  │  - Retail users (affordable)                                        │   │
│  │                                                                     │   │
│  │  ❌ Jangan gunakan untuk:                                           │   │
│  │  - Need instant L1 settlement                                       │   │
│  │  - Bridge risk not acceptable                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  SOLANA                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ✅ Gunakan untuk:                                                  │   │
│  │  - High-speed trading                                               │   │
│  │  - Gaming (real-time)                                               │   │
│  │  - Consumer apps (low fee crucial)                                  │   │
│  │  - NFTs dengan high volume                                          │   │
│  │                                                                     │   │
│  │  ❌ Jangan gunakan untuk:                                           │   │
│  │  - Maximum decentralization needed                                  │   │
│  │  - 100% uptime critical                                             │   │
│  │  - EVM compatibility needed                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Memilih Platform yang Tepat

### 9.1 Flowchart Pemilihan Platform

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FLOWCHART: MEMILIH BLOCKCHAIN PLATFORM                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                              START                                          │
│                                │                                            │
│                                ▼                                            │
│                    ┌───────────────────────┐                               │
│                    │ Apakah butuh smart    │                               │
│                    │ contract kompleks?    │                               │
│                    └───────────┬───────────┘                               │
│                                │                                            │
│                    ┌───────────┴───────────┐                               │
│                    │                       │                               │
│                   TIDAK                   YA                               │
│                    │                       │                               │
│                    ▼                       ▼                               │
│     ┌─────────────────────┐   ┌───────────────────────┐                    │
│     │ Hanya transfer      │   │ Butuh EVM             │                    │
│     │ value?              │   │ compatibility?        │                    │
│     └──────────┬──────────┘   └───────────┬───────────┘                    │
│                │                          │                                 │
│      ┌─────────┴─────────┐      ┌─────────┴─────────┐                      │
│      │                   │      │                   │                      │
│     YA                  TIDAK  YA                 TIDAK                    │
│      │                   │      │                   │                      │
│      ▼                   ▼      ▼                   ▼                      │
│  ┌────────┐    ┌────────────┐ ┌────────────┐   ┌────────────┐              │
│  │BITCOIN │    │ LIGHTNING  │ │ Low fee    │   │ Need max   │              │
│  │(store  │    │ NETWORK    │ │ penting?   │   │ speed?     │              │
│  │of value)│   │(payments)  │ └──────┬─────┘   └──────┬─────┘              │
│  └────────┘    └────────────┘        │                │                    │
│                                      │                │                    │
│                            ┌─────────┴──────┐   ┌─────┴─────┐              │
│                            │                │   │           │              │
│                           YA               TIDAK YA        TIDAK           │
│                            │                │   │           │              │
│                            ▼                ▼   ▼           ▼              │
│                    ┌────────────┐   ┌────────┐ ┌──────┐ ┌────────┐         │
│                    │ ETH L2     │   │ ETH L1 │ │SOLANA│ │CARDANO │         │
│                    │ Arbitrum   │   │        │ │      │ │COSMOS  │         │
│                    │ Optimism   │   │        │ │      │ │etc     │         │
│                    │ zkSync     │   │        │ │      │ │        │         │
│                    └────────────┘   └────────┘ └──────┘ └────────┘         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Pertimbangan untuk Developer

| Pertimbangan             | Bitcoin Ecosystem       | Ethereum Ecosystem           | Solana        |
| ------------------------ | ----------------------- | ---------------------------- | ------------- |
| **Learning Curve** | Tinggi (Script/Clarity) | Medium (Solidity)            | Tinggi (Rust) |
| **Documentation**  | Terbatas                | Sangat lengkap               | Baik          |
| **Tooling**        | Basic                   | Excellent (Hardhat, Foundry) | Baik (Anchor) |
| **Community**      | Kecil untuk dev         | Sangat besar                 | Growing       |
| **Job Market**     | Kecil                   | Terbesar                     | Growing       |
| **Composability**  | Terbatas                | Excellent                    | Good          |

### 9.3 Kesimpulan untuk Mahasiswa

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    REKOMENDASI UNTUK PEMBELAJARAN                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  UNTUK MEMULAI:                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  1. PELAJARI ETHEREUM DULU                                          │   │
│  │     - Dokumentasi paling lengkap                                    │   │
│  │     - Komunitas developer terbesar                                  │   │
│  │     - Tools paling mature                                           │   │
│  │     - Skill transferable ke EVM chains lain                         │   │
│  │     - Job market terbesar                                           │   │
│  │                                                                     │   │
│  │  2. PAHAMI KONSEP BITCOIN                                           │   │
│  │     - Fondasi semua cryptocurrency                                  │   │
│  │     - Memahami UTXO model                                           │   │
│  │     - Mengerti mengapa ada keterbatasan                             │   │
│  │                                                                     │   │
│  │  3. EKSPLORASI LAYER-2                                              │   │
│  │     - Real-world scalability solutions                              │   │
│  │     - Deploy dApp di Arbitrum/Optimism                              │   │
│  │                                                                     │   │
│  │  4. KEMUDIAN EKSPLORASI LAINNYA                                     │   │
│  │     - Solana jika tertarik high-performance                         │   │
│  │     - Stacks jika tertarik Bitcoin ecosystem                        │   │
│  │     - Cosmos/Polkadot jika tertarik multi-chain                     │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  PRIORITAS SKILLS:                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  1. Solidity + EVM fundamentals                                     │   │
│  │  2. Web3.js / Ethers.js                                             │   │
│  │  3. React + dApp frontend                                           │   │
│  │  4. Testing & Security                                              │   │
│  │  5. L2 deployment                                                   │   │
│  │  6. (Optional) Rust untuk Solana/Stacks                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Ringkasan

### Key Takeaways

| Topik                 | Poin Utama                                                                          |
| --------------------- | ----------------------------------------------------------------------------------- |
| **Bitcoin**     | Didesain sebagai uang digital, bukan platform dApp. Smart contract sangat terbatas. |
| **Ethereum**    | "World Computer" dengan full smart contract support. Ekosistem dApp terbesar.       |
| **Bitcoin L2**  | Lightning (payments), Stacks (smart contracts), Ordinals (NFTs) memperluas Bitcoin. |
| **Ethereum L2** | Arbitrum, Optimism, zkSync memberikan scalability dengan security Ethereum.         |
| **Pemilihan**   | Pilih platform berdasarkan kebutuhan: security, speed, cost, ecosystem.             |

### Comparison Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  BITCOIN                         ETHEREUM                                   │
│  ════════                        ════════                                   │
│  "Digital Gold"                  "World Computer"                           │
│                                                                             │
│  ┌───────────────────┐          ┌───────────────────┐                       │
│  │ ✓ Store of value  │          │ ✓ Smart contracts │                       │
│  │ ✓ Most secure     │          │ ✓ DeFi, NFTs      │                       │
│  │ ✓ Most decentralized│        │ ✓ Large ecosystem │                       │
│  │ ✗ No smart contract│         │ ✗ High fees (L1)  │                       │
│  │ ✗ Slow & expensive │         │ ✗ Slower than L2  │                       │
│  └───────────────────┘          └───────────────────┘                       │
│                                                                             │
│  Layer-2 Solutions:              Layer-2 Solutions:                         │
│  - Lightning: Payments           - Arbitrum, Optimism: Rollups              │
│  - Stacks: Smart contracts       - zkSync, Polygon: Fast & cheap            │
│  - Ordinals: NFTs                                                           │
│                                                                             │
│  ════════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  UNTUK dApp DEVELOPMENT → MULAI DENGAN ETHEREUM                             │
│  UNTUK STORE OF VALUE → BITCOIN                                             │
│  UNTUK PAYMENTS → LIGHTNING NETWORK                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tugas

### Tugas 1: Research dan Perbandingan

1. Pilih SATU dApp populer (misal: Uniswap, OpenSea, atau Aave)
2. Analisis mengapa dApp tersebut dibangun di Ethereum, bukan Bitcoin
3. Jelaskan fitur-fitur apa yang membutuhkan smart contract
4. Diskusikan apakah dApp tersebut bisa dibangun di Bitcoin (dengan atau tanpa L2)

### Tugas 2: Eksplorasi Layer-2

1. Bandingkan Lightning Network dengan Ethereum L2 (pilih salah satu: Arbitrum/Optimism)
2. Buat tabel perbandingan: TPS, fee, use case, cara kerja
3. Jelaskan trade-off masing-masing solusi

### Tugas 3: Hands-on Exploration

1. Install wallet untuk Bitcoin (Muun/Phoenix untuk Lightning)
2. Install MetaMask dan tambahkan network Arbitrum atau Optimism
3. Screenshot kedua wallet dan bandingkan UX-nya
4. Tulis refleksi: mana yang lebih mudah untuk pengguna awam?

### Deliverable

Kumpulkan laporan (2-3 halaman) yang berisi:

1. Jawaban Tugas 1 dengan analisis mendalam
2. Tabel perbandingan Tugas 2
3. Screenshot dan refleksi Tugas 3
4. Kesimpulan pribadi: platform mana yang menurut Anda paling berpotensi untuk mass adoption dan mengapa?

---

## Referensi

- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf) - Satoshi Nakamoto
- [Ethereum Whitepaper](https://ethereum.org/whitepaper/) - Vitalik Buterin
- [Lightning Network Paper](https://lightning.network/lightning-network-paper.pdf)
- [Stacks Documentation](https://docs.stacks.co/)
- [L2Beat - Layer 2 Comparison](https://l2beat.com/)
- [DeFi Llama - TVL Tracker](https://defillama.com/)
- [Ordinals Documentation](https://docs.ordinals.com/)
