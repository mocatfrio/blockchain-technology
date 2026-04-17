# Module 07. Smart Contract dengan Remix IDE

## Deskripsi

Modul ini merupakan panduan hands-on untuk memahami dasar-dasar smart contract menggunakan Remix IDE. Fokus modul ini adalah **pemahaman konsep dan logika**, bukan menulis kode dari nol.

**Tools:** Browser, Remix Ethereum IDE
**Prasyarat:** Paham dasar blockchain, transaksi, wallet, dan konsep address secara umum

## Tujuan Pembelajaran

Setelah mengikuti modul ini, peserta diharapkan mampu:

1. Menjelaskan apa itu smart contract
2. Mengenali bagian dasar kode Solidity
3. Menjalankan smart contract sederhana di Remix
4. Membedakan function, state, dan constructor
5. Memahami `require`, `msg.sender`, dan owner-only access
6. Menguji skenario transaksi berhasil dan gagal

## List of Contents

- [Deskripsi](#deskripsi)
- [Tujuan Pembelajaran](#tujuan-pembelajaran)
- [List of Contents](#list-of-contents)
- [1. Konsep Dasar Smart Contract](#1-konsep-dasar-smart-contract)
 - [1.1 Apa itu Smart Contract?](#11-apa-itu-smart-contract)
 - [1.2 Perbedaan dengan Program Biasa](#12-perbedaan-dengan-program-biasa)
 - [1.3 Istilah Penting](#13-istilah-penting)
- [2. Mengenal Remix IDE](#2-mengenal-remix-ide)
 - [2.1 Apa itu Remix?](#21-apa-itu-remix)
 - [2.2 Komponen Utama Remix](#22-komponen-utama-remix)
- [3. Contoh Contract: Simple Voting](#3-contoh-contract-simple-voting)
 - [3.1 Kode Smart Contract](#31-kode-smart-contract)
   - [License dan Pragma](#license-dan-pragma)
   - [State Variables](#state-variables)
   - [Constructor](#constructor)
   - [Function voteYes()](#function-voteyes)
   - [Function resetVoting()](#function-resetvoting)
- [4. Langkah Praktik di Remix](#4-langkah-praktik-di-remix)
 - [4.1 Membuka Remix](#41-membuka-remix)
 - [4.2 Membuat File Contract](#42-membuat-file-contract)
 - [4.3 Compile Contract](#43-compile-contract)
 - [4.4 Deploy Contract](#44-deploy-contract)
 - [4.5 Berinteraksi dengan Contract](#45-berinteraksi-dengan-contract)
- [5. Modifikasi Lanjutan](#5-modifikasi-lanjutan)
 - [Modifikasi 1: Tambah Vote "No"](#modifikasi-1-tambah-vote-no)
 - [Modifikasi 2: Total Vote](#modifikasi-2-total-vote)
 - [Modifikasi 3: Voting Open/Close](#modifikasi-3-voting-openclose)
 - [Modifikasi 4: Event](#modifikasi-4-event)

## 1. Konsep Dasar Smart Contract

### 1.1 Apa itu Smart Contract?

**Smart contract** adalah program yang berjalan di blockchain untuk menjalankan aturan secara otomatis. Bayangkan seperti mesin penjual otomatis (vending machine):

```
┌─────────────────────────────────────────────────────────────┐
│                    VENDING MACHINE                          │
│                                                             │
│  1. Masukkan uang ──────► Cek jumlah uang                   │
│  2. Pilih minuman  ──────► Cek ketersediaan                 │
│  3. Jika valid     ──────► Keluarkan minuman + kembalian    │
│  4. Jika tidak     ──────► Batalkan transaksi               │
│                                                             │
│  Tidak ada manusia yang mengoperasikan!                     │
└─────────────────────────────────────────────────────────────┘
```

Smart contract bekerja dengan cara yang sama:
- **Input:** Data/perintah dari pengguna
- **Logic:** Aturan yang sudah terprogram
- **Output:** Hasil eksekusi (perubahan state atau penolakan)

### 1.2 Perbedaan dengan Program Biasa

| Aspek | Program Biasa | Smart Contract |
|-------|---------------|----------------|
| **Lokasi** | Server/komputer tertentu | Blockchain (terdistribusi) |
| **Kontrol** | Pemilik server | Tidak ada yang bisa mengubah |
| **Eksekusi** | Satu mesin | Semua node di jaringan |
| **Kepercayaan** | Perlu trust ke pemilik | Trustless (kode adalah hukum) |
| **Perubahan** | Bisa diubah kapan saja | Immutable (tidak bisa diubah) |

### 1.3 Istilah Penting

| Istilah | Penjelasan | Analogi |
|---------|------------|---------|
| **State Variable** | Data yang disimpan oleh contract | Variabel di database |
| **Function** | Aksi yang bisa dijalankan pada contract | Method/fungsi program |
| **Constructor** | Function khusus yang berjalan sekali saat contract dibuat | Setup awal |
| **msg.sender** | Address yang sedang memanggil function | "Siapa yang login?" |
| **require** | Syarat yang harus dipenuhi, jika tidak transaksi gagal | if-else dengan auto-reject |
| **revert** | Keadaan saat transaksi dibatalkan | Rollback transaction |
| **owner** | Address pemilik contract (biasanya pembuat) | Admin sistem |

## 2. Mengenal Remix IDE

### 2.1 Apa itu Remix?

**Remix IDE** adalah Integrated Development Environment berbasis web untuk menulis, compile, deploy, dan menguji smart contract Ethereum.

**URL:** https://remix.ethereum.org

Kelebihan Remix:
- Tidak perlu instalasi
- Gratis dan open source
- Mendukung simulasi blockchain (Remix VM)
- Cocok untuk belajar dan prototyping

### 2.2 Komponen Utama Remix

```
┌─────────────────────────────────────────────────────────────────┐
│                        REMIX IDE                                │
├─────────────┬───────────────────────────────────────────────────┤
│             │                                                   │
│   SIDEBAR   │              EDITOR AREA                          │
│             │                                                   │
│  ┌───────┐  │  ┌─────────────────────────────────────────────┐  │
│  │ Files │  │  │ // SPDX-License-Identifier: MIT             │  │
│  │       │  │  │ pragma solidity ^0.8.20;                    │  │
│  │ ────  │  │  │                                             │  │
│  │ ────  │  │  │ contract SimpleVoting {                     │  │
│  │ ────  │  │  │     address public owner;                   │  │
│  └───────┘  │  │     ...                                     │  │
│             │  └─────────────────────────────────────────────┘  │
│  ┌───────┐  ├───────────────────────────────────────────────────┤
│  │Compile│  │              TERMINAL / OUTPUT                    │
│  └───────┘  │  ┌─────────────────────────────────────────────┐  │
│             │  │ [Transaction Log]                           │  │
│  ┌───────┐  │  │ [Compile Status]                            │  │
│  │Deploy │  │  │ [Error Messages]                            │  │
│  └───────┘  │  └─────────────────────────────────────────────┘  │
└─────────────┴───────────────────────────────────────────────────┘
```

**Komponen yang perlu diperhatikan:**

1. **File Explorer** (icon folder)
   - Tempat menyimpan dan mengelola file contract
   - Bisa membuat folder dan file baru

2. **Solidity Compiler** (icon S)
   - Compile kode Solidity menjadi bytecode
   - Menampilkan error jika ada kesalahan syntax

3. **Deploy & Run Transactions** (icon Ethereum)
   - Deploy contract ke blockchain (VM atau testnet)
   - Menjalankan function pada contract
   - Mengatur account dan environment

4. **Deployed Contracts**
   - Daftar contract yang sudah di-deploy
   - Tempat untuk berinteraksi dengan contract

## 3. Contoh Contract: Simple Voting

### 3.1 Kode Smart Contract

Salin dan gunakan kode berikut di Remix:

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleVoting {
    address public owner;              
    uint public yesCount;              
    mapping(address => bool) public hasVoted;  

    constructor() {
        owner = msg.sender;  // Pembuat contract menjadi owner
    }

    function voteYes() public {
        require(!hasVoted[msg.sender], "You have already voted");
        hasVoted[msg.sender] = true;
        yesCount += 1;
    }

    function resetVoting() public {
        require(msg.sender == owner, "Only owner can reset voting");
        yesCount = 0;
    }
}
```

#### License dan Pragma

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
```

- `SPDX-License-Identifier`: Lisensi kode (MIT = open source)
- `pragma solidity`: Versi compiler yang digunakan

#### State Variables

```sol
address public owner;
uint public yesCount;
mapping(address => bool) public hasVoted;
```

| Variable | Tipe | Fungsi |
|----------|------|--------|
| `owner` | `address` | Menyimpan address pemilik contract |
| `yesCount` | `uint` | Menyimpan jumlah vote "yes" |
| `hasVoted` | `mapping` | Mencatat apakah address sudah vote |

> **Kata kunci `public`:** Membuat variable dapat dibaca dari luar contract

#### Constructor

```sol
constructor() {
    owner = msg.sender;
}
```

- Dijalankan **sekali saja** saat contract dibuat
- `msg.sender` = address yang men-deploy contract
- Menjadikan deployer sebagai `owner`

#### Function voteYes()

```sol
function voteYes() public {
    require(!hasVoted[msg.sender], "You have already voted");
    hasVoted[msg.sender] = true;
    yesCount += 1;
}
```

**Alur kerja:**

```
┌────────────────────────────────────────────────────────────┐
│                   voteYes() dipanggil                      │
└─────────────────────────┬──────────────────────────────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │ hasVoted[msg.sender] == true?│
            └──────────────┬──────────────┘
                   ┌───────┴───────┐
                   │               │
                  YES             NO
                   │               │
                   ▼               ▼
            ┌──────────┐    ┌────────────────────┐
            │  REVERT  │    │ hasVoted = true    │
            │  (gagal) │    │ yesCount += 1      │
            └──────────┘    │ (berhasil)         │
                            └────────────────────┘
```

#### Function resetVoting()

```sol
function resetVoting() public {
    require(msg.sender == owner, "Only owner can reset voting");
    yesCount = 0;
}
```

**Access Control:**
- Hanya `owner` yang bisa menjalankan function ini
- Jika bukan owner, transaksi akan revert

## 4. Langkah Praktik di Remix

### 4.1 Membuka Remix

1. Buka browser (Chrome/Firefox recommended)
2. Akses https://remix.ethereum.org
3. Tunggu sampai IDE selesai loading
   
![1776435668140](image/module-07/1776435668140.png)

### 4.2 Membuat File Contract

1. Klik icon **File Explorer** di sidebar
2. Klik icon **Create New File** (atau klik kanan → New File)
3. Beri nama: `SimpleVoting.sol`
4. Salin kode contract ke file tersebut

### 4.3 Compile Contract

1. Klik icon **Solidity Compiler** di sidebar
2. Pastikan versi compiler sesuai (0.8.x)
3. Klik tombol **Compile SimpleVoting.sol**
4. Jika berhasil, akan muncul centang hijau

**Jika ada error:**
- Baca pesan error dengan teliti
- Biasanya typo atau versi tidak sesuai

### 4.4 Deploy Contract

1. Klik icon **Deploy & Run Transactions** di sidebar
2. Pengaturan:
   - **Environment:** `Remix VM (Cancun)` atau `Remix VM (Shanghai)`
   - **Account:** Pilih salah satu (ada 10 test account dengan 100 ETH masing-masing)
   - **Contract:** Pastikan `SimpleVoting` terpilih
3. Klik tombol **Deploy**
4. Contract akan muncul di bagian **Deployed Contracts**

### 4.5 Berinteraksi dengan Contract

Setelah deploy, di bagian **Deployed Contracts** akan muncul:

```
▼ SIMPLEVOTING AT 0x...
   ├── owner          [button]  ← Baca owner address
   ├── yesCount       [button]  ← Baca jumlah vote
   ├── hasVoted       [input]   ← Cek apakah address sudah vote
   ├── voteYes        [button]  ← Berikan vote
   └── resetVoting    [button]  ← Reset voting (owner only)
```

**Warna tombol:**
- **Biru:** Function read-only (gratis, tidak mengubah state)
- **Orange:** Function yang mengubah state (membutuhkan transaksi)

## 5. Modifikasi Lanjutan

Jika peserta sudah paham, coba modifikasi berikut:

### Modifikasi 1: Tambah Vote "No"

```sol
uint public noCount;

function voteNo() public {
    require(!hasVoted[msg.sender], "You have already voted");
    hasVoted[msg.sender] = true;
    noCount += 1;
}
```

### Modifikasi 2: Total Vote

```sol
function getTotalVotes() public view returns (uint) {
    return yesCount + noCount;
}
```

### Modifikasi 3: Voting Open/Close

```sol
bool public votingOpen = true;

modifier onlyWhenOpen() {
    require(votingOpen, "Voting is closed");
    _;
}

function voteYes() public onlyWhenOpen {
    // ... kode vote
}

function closeVoting() public {
    require(msg.sender == owner, "Only owner");
    votingOpen = false;
}
```

### Modifikasi 4: Event

```sol
event VoteCasted(address indexed voter, bool vote);

function voteYes() public {
    require(!hasVoted[msg.sender], "Already voted");
    hasVoted[msg.sender] = true;
    yesCount += 1;
    emit VoteCasted(msg.sender, true);  // Emit event
}
```

**Next Steps:**
- Pelajari [Module 06](module-06.md) untuk konsep cryptocurrency lanjutan
- Eksplorasi dokumentasi Solidity: https://docs.soliditylang.org
- Coba deploy ke testnet (Sepolia) menggunakan MetaMask
