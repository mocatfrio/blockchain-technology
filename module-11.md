# Module 11. Hands-on MetaMask

## Deskripsi

Modul ini merupakan panduan praktis (hands-on) untuk menggunakan **MetaMask**, wallet cryptocurrency paling populer untuk berinteraksi dengan blockchain Ethereum dan jaringan EVM-compatible lainnya. MetaMask menjadi jembatan antara browser dengan dunia Web3.

Topik yang dibahas pada modul ini:

1. **Konsep Wallet** - Memahami peran wallet dalam ekosistem blockchain
2. **Instalasi MetaMask** - Setup wallet di browser
3. **Manajemen Akun** - Membuat dan mengelola multiple accounts
4. **Seed Phrase & Security** - Memahami recovery phrase dan best practices keamanan
5. **Networks** - Menghubungkan ke berbagai jaringan (Mainnet, Testnet, Custom)
6. **Testnet Faucet** - Mendapatkan ETH gratis untuk testing
7. **Transaksi** - Mengirim dan menerima cryptocurrency
8. **Integrasi Remix IDE** - Deploy smart contract menggunakan MetaMask
9. **dApp Connection** - Menghubungkan wallet ke aplikasi terdesentralisasi

## Prasyarat

Sebelum mempelajari modul ini, pastikan telah:

1. Memahami konsep dasar blockchain ([Module 02](module-02.md))
2. Memahami konsep wallet dan digital signature ([Module 05](module-05.md))
3. Browser modern (Chrome, Firefox, atau Brave)
4. Koneksi internet yang stabil

## List of Contents

- [Deskripsi](#deskripsi)
- [Prasyarat](#prasyarat)
- [List of Contents](#list-of-contents)
- [1. Konsep Wallet](#1-konsep-wallet)
  - [1.1 Apa itu Cryptocurrency Wallet?](#11-apa-itu-cryptocurrency-wallet)
  - [1.2 Jenis-jenis Wallet](#12-jenis-jenis-wallet)
  - [1.3 Mengapa MetaMask?](#13-mengapa-metamask)
- [2. Instalasi MetaMask](#2-instalasi-metamask)
  - [2.1 Download Extension](#21-download-extension)
  - [2.2 Membuat Wallet Baru](#22-membuat-wallet-baru)
  - [2.3 Import Wallet yang Sudah Ada](#23-import-wallet-yang-sudah-ada)
- [3. Memahami Seed Phrase](#3-memahami-seed-phrase)
  - [3.1 Apa itu Seed Phrase?](#31-apa-itu-seed-phrase)
  - [3.2 Cara Kerja Seed Phrase](#32-cara-kerja-seed-phrase)
  - [3.3 Best Practices Keamanan](#33-best-practices-keamanan)
- [4. Anatomi MetaMask](#4-anatomi-metamask)
  - [4.1 Antarmuka Utama](#41-antarmuka-utama)
  - [4.2 Account Management](#42-account-management)
  - [4.3 Menambah Akun Baru](#43-menambah-akun-baru)
- [5. Networks di MetaMask](#5-networks-di-metamask)
  - [5.1 Mainnet vs Testnet](#51-mainnet-vs-testnet)
  - [5.2 Daftar Network Populer](#52-daftar-network-populer)
  - [5.3 Mengganti Network](#53-mengganti-network)
  - [5.4 Menambah Custom Network](#54-menambah-custom-network)
- [6. Mendapatkan Testnet ETH](#6-mendapatkan-testnet-eth)
  - [6.1 Apa itu Faucet?](#61-apa-itu-faucet)
  - [6.2 Langkah Mendapatkan Sepolia ETH](#62-langkah-mendapatkan-sepolia-eth)
  - [6.3 Faucet Alternatif](#63-faucet-alternatif)
- [7. Melakukan Transaksi](#7-melakukan-transaksi)
  - [7.1 Menerima Cryptocurrency](#71-menerima-cryptocurrency)
  - [7.2 Mengirim Cryptocurrency](#72-mengirim-cryptocurrency)
  - [7.3 Memahami Gas Fee](#73-memahami-gas-fee)
  - [7.4 Melihat Riwayat Transaksi](#74-melihat-riwayat-transaksi)
- [8. Integrasi dengan Remix IDE](#8-integrasi-dengan-remix-ide)
  - [8.1 Menghubungkan MetaMask ke Remix](#81-menghubungkan-metamask-ke-remix)
  - [8.2 Deploy Contract ke Testnet](#82-deploy-contract-ke-testnet)
  - [8.3 Berinteraksi dengan Contract](#83-berinteraksi-dengan-contract)
- [9. Menghubungkan ke dApp](#9-menghubungkan-ke-dapp)
  - [9.1 Cara Kerja dApp Connection](#91-cara-kerja-dapp-connection)
  - [9.2 Permission dan Security](#92-permission-dan-security)
  - [9.3 Memutuskan Koneksi dApp](#93-memutuskan-koneksi-dapp)
- [10. Tips Keamanan MetaMask](#10-tips-keamanan-metamask)
- [Latihan](#latihan)

---

## 1. Konsep Wallet

### 1.1 Apa itu Cryptocurrency Wallet?

**Cryptocurrency wallet** adalah perangkat lunak atau perangkat keras yang menyimpan **private key** dan memungkinkan pengguna untuk berinteraksi dengan blockchain.

```
┌─────────────────────────────────────────────────────────────────┐
│                    CRYPTOCURRENCY WALLET                         │
│                                                                  │
│  ┌─────────────────┐     ┌─────────────────┐                     │
│  │   Private Key   │────►│   Public Key    │────► Address        │
│  │  (rahasia)      │     │  (bisa dibagi)  │     (identitas)     │
│  └─────────────────┘     └─────────────────┘                     │
│                                                                  │
│  Wallet TIDAK menyimpan cryptocurrency!                          │
│  Wallet menyimpan KUNCI untuk mengakses aset di blockchain.      │
└─────────────────────────────────────────────────────────────────┘
```

**Analogi:**

- **Private Key** = Kunci rumah (harus dijaga, jangan dibagikan)
- **Public Key** = Alamat rumah (bisa dibagikan untuk menerima paket)
- **Wallet** = Dompet yang menyimpan kunci

> **Penting:** Cryptocurrency tidak disimpan di wallet. Aset tetap ada di blockchain. Wallet hanya menyimpan kunci untuk mengaksesnya.

### 1.2 Jenis-jenis Wallet

| Jenis                      | Contoh                       | Kelebihan               | Kekurangan                       |
| -------------------------- | ---------------------------- | ----------------------- | -------------------------------- |
| **Hot Wallet**       | MetaMask, Trust Wallet       | Mudah digunakan, gratis | Terhubung internet (risiko hack) |
| **Cold Wallet**      | Ledger, Trezor               | Sangat aman, offline    | Harga mahal, kurang praktis      |
| **Paper Wallet**     | Cetak QR code                | Offline, gratis         | Mudah hilang/rusak               |
| **Custodial Wallet** | Exchange (Binance, Coinbase) | Tidak perlu manage key  | Bukan pemilik sebenarnya         |

```
Tingkat Keamanan:

Cold Wallet ████████████████████ Tertinggi
Paper Wallet ███████████████░░░░░ Tinggi (jika disimpan dengan baik)
Hot Wallet █████████░░░░░░░░░░░ Sedang
Custodial ███░░░░░░░░░░░░░░░░░ Rendah (trust pihak ketiga)
```

### 1.3 Mengapa MetaMask?

**MetaMask** adalah hot wallet berbasis browser extension yang paling populer di ekosistem Ethereum.

**Kelebihan MetaMask:**

| Fitur                             | Penjelasan                                                      |
| --------------------------------- | --------------------------------------------------------------- |
| **Browser Integration**     | Terintegrasi langsung dengan browser (Chrome, Firefox, Brave)   |
| **Multi-Network**           | Mendukung Ethereum, Polygon, BSC, Arbitrum, dan network lainnya |
| **dApp Compatible**         | Bisa connect ke ribuan aplikasi Web3                            |
| **Free & Open Source**      | Gratis dan kode sumbernya terbuka                               |
| **User Friendly**           | Interface yang mudah digunakan                                  |
| **Hardware Wallet Support** | Bisa dihubungkan dengan Ledger/Trezor                           |

**Statistik MetaMask (2024):**

- 30+ juta pengguna aktif bulanan
- Mendukung 10+ jaringan blockchain
- Tersedia di Chrome, Firefox, Brave, Edge, dan mobile

---

## 2. Instalasi MetaMask

### 2.1 Download Extension

1. Buka website resmi: https://metamask.io
2. Klik **Download**
3. Pilih browser yang digunakan

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOWNLOAD METAMASK                             │
│                                                                  │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│    │  Chrome  │  │ Firefox  │  │  Brave   │  │   Edge   │       │
│    │    ✓     │  │    ✓     │  │    ✓     │  │    ✓     │       │
│    └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                  │
│    ⚠️  HANYA download dari metamask.io atau store resmi!        │
│    ⚠️  Hati-hati dengan website palsu (phishing)!               │
└─────────────────────────────────────────────────────────────────┘
```

4. Klik **Add to Chrome** (atau browser lainnya)
5. Konfirmasi dengan klik **Add Extension**
6. MetaMask icon (rubah) akan muncul di toolbar browser

### 2.2 Membuat Wallet Baru

Setelah extension terinstall:

**Langkah 1: Memulai Setup**

```
┌─────────────────────────────────────────┐
│         Welcome to MetaMask!             │
│                                          │
│   ┌─────────────────────────────────┐   │
│   │      Create a new wallet        │   │ ← Pilih ini
│   └─────────────────────────────────┘   │
│                                          │
│   ┌─────────────────────────────────┐   │
│   │   Import an existing wallet     │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Langkah 2: Membuat Password**

- Buat password yang kuat (minimal 8 karakter)
- Password ini untuk unlock MetaMask di browser
- **Catatan:** Password ini BERBEDA dengan seed phrase

**Langkah 3: Backup Seed Phrase**

- MetaMask akan menampilkan 12 kata (Secret Recovery Phrase)
- **CATAT DAN SIMPAN DI TEMPAT AMAN!**
- Jangan screenshot atau simpan di cloud

**Langkah 4: Konfirmasi Seed Phrase**

- MetaMask akan meminta konfirmasi dengan menyusun kata-kata
- Pastikan urutan benar

**Langkah 5: Selesai**

- Wallet siap digunakan
- Address Ethereum pertama sudah tersedia

### 2.3 Import Wallet yang Sudah Ada

Jika sudah memiliki seed phrase dari wallet lain:

1. Pilih **Import an existing wallet**
2. Masukkan 12/24 kata seed phrase
3. Buat password baru untuk MetaMask
4. Selesai - wallet akan ter-restore dengan semua akun

```
┌─────────────────────────────────────────────────────────────────┐
│                    IMPORT WALLET                                 │
│                                                                  │
│  Secret Recovery Phrase:                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ abandon ability able about above absent absorb abstract ... ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ⚠️  Pastikan tidak ada orang lain yang melihat!               │
│  ⚠️  MetaMask tidak pernah meminta seed phrase via email!       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Memahami Seed Phrase

### 3.1 Apa itu Seed Phrase?

**Seed phrase** (atau Secret Recovery Phrase / Mnemonic) adalah 12 atau 24 kata yang merepresentasikan master key wallet Anda.

```
Contoh Seed Phrase (12 kata):

┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ abandon │ │ ability │ │  able   │ │  about  │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
    1            2           3           4

┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│  above  │ │ absent  │ │ absorb  │ │abstract │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
    5            6           7           8

┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ absurd  │ │  abuse  │ │ access  │ │accident │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
    9           10          11          12
```

### 3.2 Cara Kerja Seed Phrase

Seed phrase menggunakan standar **BIP39** untuk mengkonversi kata-kata menjadi master key.

```
Seed Phrase (12 kata)
        │
        ▼
   [BIP39 Process]
        │
        ▼
   Master Seed (512 bit)
        │
        ▼
   [BIP32 Derivation]
        │
   ┌────┴────┬────────┬────────┐
   ▼         ▼        ▼        ▼
Account 1  Account 2  ...  Account N
(m/44'/60'/0'/0/0)  (m/44'/60'/0'/0/1)
```

Dari satu seed phrase, bisa di-derive **unlimited accounts**.

### 3.3 Best Practices Keamanan

**DO (Lakukan):**

| Praktik               | Alasan                            |
| --------------------- | --------------------------------- |
| Tulis di kertas       | Tidak bisa di-hack secara digital |
| Simpan di brankas     | Aman dari pencurian fisik         |
| Buat beberapa salinan | Backup jika satu hilang           |
| Gunakan metal backup  | Tahan air dan api                 |

**DON'T (Jangan):**

| Praktik               | Risiko                              |
| --------------------- | ----------------------------------- |
| Screenshot            | Bisa di-sync ke cloud, mudah dicuri |
| Simpan di notes/email | Bisa di-hack jika akun dibobol      |
| Share ke siapapun     | Kehilangan akses permanen           |
| Input di website lain | Phishing attack                     |

```
⚠️  PERINGATAN PENTING:
═══════════════════════════════════════════════════════════════
║  Siapa yang memiliki seed phrase = Pemilik wallet           ║
║  MetaMask/Ethereum TIDAK BISA reset atau recover seed       ║
║  Jika hilang = Aset hilang SELAMANYA                        ║
═══════════════════════════════════════════════════════════════
```

---

## 4. Anatomi MetaMask

### 4.1 Antarmuka Utama

```
┌─────────────────────────────────────────────────────────────────┐
│  ┌─────────────────┐                    ┌─────────────────┐     │
│  │ Ethereum Mainnet│ ◄── Network       │     ≡ Menu      │     │
│  └─────────────────┘     Selector      └─────────────────┘     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│        ┌──────────────────────────────────────┐                 │
│        │         🦊 Account 1                  │                 │
│        │    0x742d...3Fe9 [Copy] [QR]         │ ◄── Address     │
│        └──────────────────────────────────────┘                 │
│                                                                  │
│            ┌──────────────────────────┐                         │
│            │       0.5 ETH            │                         │
│            │      $1,250.00           │ ◄── Balance             │
│            └──────────────────────────┘                         │
│                                                                  │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│    │   Buy    │  │   Send   │  │   Swap   │  │  Bridge  │       │
│    └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  [Tokens]  [NFTs]  [Activity]                                    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  ETH                                          0.5 ETH       ││
│  │  USDT                                      100.00 USDT      ││
│  │  + Import tokens                                            ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

**Komponen Utama:**

| Komponen                   | Fungsi                                            |
| -------------------------- | ------------------------------------------------- |
| **Network Selector** | Pilih jaringan blockchain (Mainnet, Testnet, dll) |
| **Account**          | Nama akun dan address wallet                      |
| **Balance**          | Saldo cryptocurrency                              |
| **Buy**              | Beli crypto dengan kartu/bank                     |
| **Send**             | Kirim crypto ke address lain                      |
| **Swap**             | Tukar antar token                                 |
| **Bridge**           | Transfer ke chain lain                            |
| **Tokens**           | Daftar token yang dimiliki                        |
| **NFTs**             | Koleksi NFT                                       |
| **Activity**         | Riwayat transaksi                                 |

### 4.2 Account Management

MetaMask mendukung multiple accounts dalam satu wallet.

```
┌─────────────────────────────────────────┐
│            My Accounts                   │
├─────────────────────────────────────────┤
│  ✓ Account 1                             │
│    0x742d35Cc6634C0532925a3b844Bc454e... │
│    0.5 ETH                               │
├─────────────────────────────────────────┤
│    Account 2 (Savings)                   │
│    0x8Ba1f109551bD432803012645Ac136dda... │
│    2.0 ETH                               │
├─────────────────────────────────────────┤
│    Account 3 (Trading)                   │
│    0x1234...                              │
│    0.1 ETH                               │
├─────────────────────────────────────────┤
│  + Add account or hardware wallet        │
└─────────────────────────────────────────┘
```

### 4.3 Menambah Akun Baru

1. Klik icon account (lingkaran) di pojok kanan atas
2. Klik **+ Add account or hardware wallet**
3. Pilih **Add a new account**
4. Beri nama akun
5. Klik **Create**

Setiap akun baru akan memiliki address berbeda tetapi masih dari seed phrase yang sama.

---

## 5. Networks di MetaMask

### 5.1 Mainnet vs Testnet

| Aspek                       | Mainnet                     | Testnet              |
| --------------------------- | --------------------------- | -------------------- |
| **Nilai**             | Real value (uang asli)      | Tidak bernilai       |
| **Tujuan**            | Production, transaksi nyata | Development, testing |
| **Cara mendapat ETH** | Beli dengan uang            | Gratis dari faucet   |
| **Contoh**            | Ethereum Mainnet            | Sepolia, Goerli      |

```
Mainnet                          Testnet
┌─────────────────┐              ┌─────────────────┐
│ ETH = $2,500    │              │ ETH = $0        │
│ Real money      │              │ Test only       │
│ Production      │              │ Development     │
└─────────────────┘              └─────────────────┘
```

### 5.2 Daftar Network Populer

| Network           | Chain ID | Keterangan             |
| ----------------- | -------- | ---------------------- |
| Ethereum Mainnet  | 1        | Network utama Ethereum |
| Sepolia Testnet   | 11155111 | Testnet resmi terbaru  |
| Polygon           | 137      | Layer 2, fee murah     |
| Arbitrum One      | 42161    | Layer 2, fee murah     |
| Optimism          | 10       | Layer 2, fee murah     |
| BSC               | 56       | Binance Smart Chain    |
| Avalanche C-Chain | 43114    | Avalanche network      |

### 5.3 Mengganti Network

1. Klik dropdown network di pojok kiri atas
2. Pilih network yang diinginkan
3. Jika network belum ada, tambahkan secara manual

```
┌─────────────────────────────────────────┐
│            Select a network              │
├─────────────────────────────────────────┤
│  ✓ Ethereum Mainnet                      │
│    Sepolia test network                  │
│    Linea Mainnet                         │
├─────────────────────────────────────────┤
│  + Add network                           │
│  Show test networks ○                    │
└─────────────────────────────────────────┘
```

**Untuk menampilkan Testnet:**

1. Klik **Show test networks** toggle
2. Testnet seperti Sepolia akan muncul

### 5.4 Menambah Custom Network

Untuk menambah network yang tidak ada di daftar default:

1. Klik **+ Add network**
2. Isi data network:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Add a network manually                        │
├─────────────────────────────────────────────────────────────────┤
│  Network name:                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Polygon Mainnet                                             ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  New RPC URL:                                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ https://polygon-rpc.com                                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Chain ID:                                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 137                                                         ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Currency symbol:                                                │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ MATIC                                                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Block explorer URL (Optional):                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ https://polygonscan.com                                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│                      [Save]                                      │
└─────────────────────────────────────────────────────────────────┘
```

**Data Network Populer:**

| Network   | RPC URL                               | Chain ID | Symbol |
| --------- | ------------------------------------- | -------- | ------ |
| Polygon   | https://polygon-rpc.com               | 137      | MATIC  |
| BSC       | https://bsc-dataseed.binance.org      | 56       | BNB    |
| Arbitrum  | https://arb1.arbitrum.io/rpc          | 42161    | ETH    |
| Avalanche | https://api.avax.network/ext/bc/C/rpc | 43114    | AVAX   |

---

## 6. Mendapatkan Testnet ETH

### 6.1 Apa itu Faucet?

**Faucet** adalah layanan yang memberikan cryptocurrency testnet secara gratis untuk keperluan development dan testing.

```
┌─────────────────────────────────────────────────────────────────┐
│                         FAUCET                                   │
│                                                                  │
│   Developer ──────► Input Address ──────► Receive Test ETH      │
│                                                                  │
│   Batasan:                                                       │
│   - Hanya testnet (tidak bernilai)                              │
│   - Limit request per hari/minggu                               │
│   - Beberapa memerlukan verifikasi                              │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Langkah Mendapatkan Sepolia ETH

**Step 1: Pastikan MetaMask di Sepolia Network**

- Klik network selector
- Pilih **Sepolia test network**
- Jika tidak ada, aktifkan "Show test networks"

**Step 2: Copy Address MetaMask**

- Klik address untuk copy ke clipboard
- Address dimulai dengan `0x...`

**Step 3: Kunjungi Faucet**

Beberapa faucet Sepolia yang tersedia:

| Faucet              | URL                                                               | Persyaratan          |
| ------------------- | ----------------------------------------------------------------- | -------------------- |
| Google Cloud Faucet | https://cloud.google.com/application/web3/faucet/ethereum/sepolia | Login Google         |
| Alchemy Faucet      | https://sepoliafaucet.com                                         | Login Alchemy (free) |
| Infura Faucet       | https://www.infura.io/faucet/sepolia                              | Login Infura (free)  |
| QuickNode           | https://faucet.quicknode.com/ethereum/sepolia                     | Login QuickNode      |

**Step 4: Request ETH**

1. Paste address MetaMask
2. Klik **Request** atau **Send**
3. Tunggu beberapa detik

**Step 5: Verifikasi di MetaMask**

- Balance akan bertambah (biasanya 0.5 - 2 ETH)
- Cek tab **Activity** untuk melihat transaksi masuk

### 6.3 Faucet Alternatif

Jika faucet utama tidak berfungsi:

1. **PoW Faucet** - https://sepolia-faucet.pk910.de

   - Mining di browser untuk mendapat ETH
   - Tidak perlu login
2. **Chainlink Faucet** - https://faucets.chain.link/sepolia

   - Memberikan ETH dan LINK token
   - Perlu login dengan wallet
3. **Community Faucet** - Cari di Discord developer communities

---

## 7. Melakukan Transaksi

### 7.1 Menerima Cryptocurrency

Untuk menerima crypto, cukup bagikan address:

1. Klik address di MetaMask untuk copy
2. Atau klik icon QR code untuk menampilkan QR
3. Bagikan address/QR ke pengirim

```
┌─────────────────────────────────────────┐
│              Receive ETH                 │
├─────────────────────────────────────────┤
│         ┌───────────────────┐           │
│         │    ██████████    │           │
│         │    ██      ██    │           │
│         │    ██  QR  ██    │           │
│         │    ██      ██    │           │
│         │    ██████████    │           │
│         └───────────────────┘           │
│                                          │
│   0x742d35Cc6634C0532925a3b844Bc454e4438f44e │
│                [Copy]                     │
└─────────────────────────────────────────┘
```

### 7.2 Mengirim Cryptocurrency

**Langkah-langkah:**

1. Klik tombol **Send**
2. Masukkan address tujuan atau pilih dari kontak
3. Masukkan jumlah yang akan dikirim
4. Review gas fee
5. Klik **Confirm**

```
┌─────────────────────────────────────────────────────────────────┐
│                         Send ETH                                 │
├─────────────────────────────────────────────────────────────────┤
│  To:                                                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 0x8Ba1f109551bD432803012645Ac136dda...                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Amount:                                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 0.1 ETH                                          [Max]      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Estimated fee: 0.0021 ETH (~$5.25)                             │
│                                                                  │
│  Total: 0.1021 ETH                                              │
│                                                                  │
│              [Cancel]              [Next]                        │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 Memahami Gas Fee

**Gas** adalah biaya untuk memproses transaksi di blockchain Ethereum.

```
┌─────────────────────────────────────────────────────────────────┐
│                        GAS FEE                                   │
│                                                                  │
│  Transaction Fee = Gas Limit × Gas Price                        │
│                                                                  │
│  Gas Limit: Jumlah maksimum gas yang digunakan                  │
│  Gas Price: Harga per unit gas (dalam Gwei)                     │
│                                                                  │
│  Contoh:                                                         │
│  Gas Limit: 21,000 (transfer ETH standard)                      │
│  Gas Price: 30 Gwei                                             │
│  Fee = 21,000 × 30 Gwei = 630,000 Gwei = 0.00063 ETH           │
└─────────────────────────────────────────────────────────────────┘
```

**Pengaturan Gas di MetaMask:**

| Mode                 | Penjelasan                           |
| -------------------- | ------------------------------------ |
| **Low**        | Murah tapi lambat (menit sampai jam) |
| **Market**     | Harga rata-rata (biasanya < 1 menit) |
| **Aggressive** | Mahal tapi cepat (detik)             |
| **Advanced**   | Atur gas sendiri                     |

### 7.4 Melihat Riwayat Transaksi

1. Klik tab **Activity** di MetaMask
2. Klik transaksi untuk detail
3. Klik **View on block explorer** untuk detail lengkap di Etherscan

```
┌─────────────────────────────────────────────────────────────────┐
│                        Activity                                  │
├─────────────────────────────────────────────────────────────────┤
│  ● Send                                     -0.1 ETH            │
│    To: 0x8Ba1...                            Apr 15              │
│    Status: Confirmed ✓                                          │
├─────────────────────────────────────────────────────────────────┤
│  ● Receive                                  +0.5 ETH            │
│    From: 0x742d...                          Apr 14              │
│    Status: Confirmed ✓                                          │
├─────────────────────────────────────────────────────────────────┤
│  ● Contract Interaction                     -0.05 ETH           │
│    To: Uniswap                              Apr 13              │
│    Status: Confirmed ✓                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Integrasi dengan Remix IDE

### 8.1 Menghubungkan MetaMask ke Remix

**Step 1: Buka Remix IDE**

- Akses https://remix.ethereum.org

**Step 2: Pilih Environment**

1. Klik icon **Deploy & Run Transactions**
2. Di dropdown **Environment**, pilih **Injected Provider - MetaMask**

```
┌─────────────────────────────────────────────────────────────────┐
│  DEPLOY & RUN TRANSACTIONS                                       │
├─────────────────────────────────────────────────────────────────┤
│  Environment:                                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Injected Provider - MetaMask                              ▼ ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Account:                                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 0x742d...3Fe9 (0.5 ether)                                   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

**Step 3: Approve Connection**

- MetaMask popup akan muncul
- Pilih akun yang ingin dihubungkan
- Klik **Connect**

**Step 4: Verifikasi**

- Account di Remix akan menampilkan address MetaMask
- Balance akan sesuai dengan saldo di MetaMask

### 8.2 Deploy Contract ke Testnet

**Prasyarat:**

- MetaMask terhubung ke Sepolia
- Memiliki Sepolia ETH (dari faucet)

**Langkah Deploy:**

1. **Tulis/compile contract** (contoh dari Module 07)

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract HelloWorld {
    string public message;
    address public owner;

    constructor(string memory _message) {
        message = _message;
        owner = msg.sender;
    }

    function setMessage(string memory _newMessage) public {
        require(msg.sender == owner, "Only owner can change message");
        message = _newMessage;
    }
}
```

2. **Compile contract**

   - Klik Solidity Compiler
   - Klik Compile
3. **Deploy contract**

   - Klik Deploy & Run Transactions
   - Pastikan Environment: **Injected Provider - MetaMask**
   - Isi parameter constructor (contoh: "Hello Blockchain!")
   - Klik **Deploy**
4. **Approve di MetaMask**

   - MetaMask popup akan muncul
   - Review gas fee
   - Klik **Confirm**
5. **Tunggu konfirmasi**

   - Transaksi akan pending beberapa detik
   - Setelah confirmed, contract muncul di Deployed Contracts

### 8.3 Berinteraksi dengan Contract

Setelah deploy, contract address akan terlihat di Remix.

**Membaca Data (Read):**

- Klik function read-only (tombol biru)
- Hasil langsung muncul tanpa transaksi

**Menulis Data (Write):**

- Klik function yang mengubah state (tombol orange)
- MetaMask popup akan muncul untuk approval
- Konfirmasi dan tunggu transaksi

```
┌─────────────────────────────────────────────────────────────────┐
│  ▼ HELLOWORLD AT 0x1234...5678 (Sepolia)                        │
├─────────────────────────────────────────────────────────────────┤
│  message        [button - blue]   → "Hello Blockchain!"         │
│  owner          [button - blue]   → 0x742d...3Fe9               │
├─────────────────────────────────────────────────────────────────┤
│  setMessage  [input] [button - orange]                          │
│              └─────────────────────┘                            │
│              "New Message"                                       │
└─────────────────────────────────────────────────────────────────┘
```

**Verifikasi di Block Explorer:**

- Copy contract address
- Buka https://sepolia.etherscan.io
- Paste address di search
- Lihat semua transaksi dan contract details

---

## 9. Menghubungkan ke dApp

### 9.1 Cara Kerja dApp Connection

**dApp (Decentralized Application)** adalah aplikasi yang berinteraksi dengan blockchain.

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│    User     │◄───────►│  MetaMask   │◄───────►│    dApp     │
│  (Browser)  │         │  (Wallet)   │         │  (Website)  │
└─────────────┘         └──────┬──────┘         └─────────────┘
                               │
                               ▼
                        ┌─────────────┐
                        │  Blockchain │
                        │  (Ethereum) │
                        └─────────────┘
```

**Flow koneksi:**

1. User mengunjungi dApp
2. dApp request koneksi ke MetaMask
3. MetaMask popup minta approval
4. User approve → dApp bisa baca address
5. Saat transaksi, MetaMask minta approval lagi

### 9.2 Permission dan Security

**Ketika connect ke dApp, yang BISA dilakukan dApp:**

- Melihat address wallet
- Melihat balance
- Request approval untuk transaksi
- Request signature

**Yang TIDAK BISA dilakukan dApp tanpa approval:**

- Mengirim transaksi
- Mengakses private key
- Mengubah settings wallet

```
┌─────────────────────────────────────────────────────────────────┐
│               MetaMask Connection Request                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Uniswap wants to connect to your wallet                        │
│                                                                  │
│  This will allow the site to:                                   │
│  ✓ View your wallet address                                     │
│  ✓ View your account balance                                    │
│  ✓ Request approval for transactions                            │
│                                                                  │
│  This will NOT allow the site to:                               │
│  ✗ Access your private keys                                     │
│  ✗ Send transactions without your approval                      │
│                                                                  │
│           [Cancel]              [Connect]                        │
└─────────────────────────────────────────────────────────────────┘
```

### 9.3 Memutuskan Koneksi dApp

Untuk keamanan, disconnect dari dApp yang tidak digunakan:

1. Klik **3 titik (menu)** di MetaMask
2. Pilih **Connected sites**
3. Klik **Disconnect** pada dApp yang ingin diputus

```
┌─────────────────────────────────────────┐
│          Connected sites                 │
├─────────────────────────────────────────┤
│  uniswap.org              [Disconnect]  │
│  opensea.io               [Disconnect]  │
│  remix.ethereum.org       [Disconnect]  │
└─────────────────────────────────────────┘
```

---

## 10. Tips Keamanan MetaMask

**Checklist Keamanan:**

| No | Tips                                 | Penjelasan                                |
| -- | ------------------------------------ | ----------------------------------------- |
| 1  | **Backup seed phrase offline** | Tulis di kertas, simpan di tempat aman    |
| 2  | **Jangan share seed phrase**   | MetaMask tidak pernah meminta seed phrase |
| 3  | **Verifikasi URL**             | Pastikan URL benar sebelum connect        |
| 4  | **Revoke permissions**         | Disconnect dari dApp yang tidak digunakan |
| 5  | **Hardware wallet**            | Gunakan Ledger/Trezor untuk aset besar    |
| 6  | **Multiple accounts**          | Pisahkan akun untuk trading dan holding   |
| 7  | **Test transactions**          | Kirim jumlah kecil dulu untuk test        |
| 8  | **Review sebelum sign**        | Baca dengan teliti sebelum approve        |

**Red Flags (Tanda Bahaya):**

```
⚠️  WASPADA jika:
═══════════════════════════════════════════════════════════════
║  ❌ Diminta seed phrase via website/email/DM                 ║
║  ❌ "Free airdrop" yang meminta connect + sign               ║
║  ❌ URL yang mirip tapi tidak sama (metamask.io.fake.com)    ║
║  ❌ Diminta approve unlimited token spending                 ║
║  ❌ Pop-up tidak dari MetaMask extension                     ║
═══════════════════════════════════════════════════════════════
```

---

## Latihan

1. **Setup Wallet**

   - Install MetaMask di browser
   - Buat wallet baru
   - Backup seed phrase dengan aman
   - Tambahkan 2 akun baru
2. **Network & Faucet**

   - Tambahkan Sepolia testnet ke MetaMask
   - Dapatkan Sepolia ETH dari faucet
   - Kirim 0.01 ETH ke akun kedua Anda
3. **Deploy Smart Contract**

   - Connect MetaMask ke Remix IDE
   - Deploy contract HelloWorld ke Sepolia
   - Panggil function `setMessage` dan verifikasi perubahan
4. **Eksplorasi Transaksi**

   - Lihat transaksi di Etherscan Sepolia
   - Identifikasi: transaction hash, gas used, block number
   - Bandingkan gas fee antara Low, Market, dan Aggressive
5. **Keamanan**

   - List 3 dApp yang Anda connect
   - Disconnect semua dApp yang tidak digunakan
   - Export private key akun testing (dan pahami risikonya)
6. **Challenge: Multi-sig Simulation**

   - Buat 3 akun berbeda di MetaMask
   - Deploy contract voting dari Module 07
   - Lakukan voting dari 3 akun berbeda
   - Verifikasi hasil di Etherscan
