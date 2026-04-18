# Module 09. Persiapan Environment untuk Smart Contract Development

## Deskripsi

Modul ini adalah **persiapan teknis** sebelum masuk ke Module 10 (Smart Contract dengan Hardhat). Di sini kamu akan menginstall semua tools yang dibutuhkan untuk development Smart Contract secara lokal.

> **Penting**: Selesaikan modul ini terlebih dahulu sebelum melanjutkan ke Module 10. Pastikan semua tools terinstall dengan benar.

**Estimasi waktu**: 30-60 menit (tergantung kecepatan internet)

## Tujuan Pembelajaran

Setelah mengikuti modul ini, kamu akan:

1. Memahami mengapa perlu development environment lokal
2. Berhasil menginstall Node.js
3. Berhasil menginstall pnpm (package manager)
4. Berhasil menginstall dan menjalankan Ganache (local blockchain)
5. Menginstall extension Solidity di VS Code
6. Memverifikasi semua instalasi berfungsi dengan benar

## List of Contents

- [Deskripsi](#deskripsi)
- [Tujuan Pembelajaran](#tujuan-pembelajaran)
- [1. Mengapa Perlu Development Environment Lokal?](#1-mengapa-perlu-development-environment-lokal)
- [2. Instalasi Node.js](#2-instalasi-nodejs)
  - [2.1 Windows](#21-windows)
  - [2.2 macOS](#22-macos)
  - [2.3 Linux (Ubuntu/Debian)](#23-linux-ubuntudebian)
  - [2.4 Verifikasi Instalasi Node.js](#24-verifikasi-instalasi-nodejs)
- [3. Instalasi pnpm (Package Manager)](#3-instalasi-pnpm-package-manager)
- [4. Instalasi Ganache (Local Blockchain)](#4-instalasi-ganache-local-blockchain)
  - [4.1 Download dan Install](#41-download-dan-install)
  - [4.2 Mengenal Tampilan Ganache](#42-mengenal-tampilan-ganache)
  - [4.3 Informasi Penting di Ganache](#43-informasi-penting-di-ganache)
- [5. Setup VS Code untuk Solidity](#5-setup-vs-code-untuk-solidity)
- [6. Clone dan Setup Project](#6-clone-dan-setup-project)
- [7. Verifikasi Akhir](#7-verifikasi-akhir)
- [Troubleshooting](#troubleshooting)

---

## 1. Mengapa Perlu Development Environment Lokal?

Pada Module 08, kita menggunakan **Remix IDE** yang berjalan di browser. Ini bagus untuk belajar, tapi memiliki keterbatasan:

| Aspek | Remix IDE (Browser) | Development Lokal (Hardhat) |
|-------|---------------------|----------------------------|
| Setup | Tidak perlu install | Perlu install tools |
| Proyek besar | Sulit dikelola | Mudah diorganisir |
| Version control | Tidak ada | Bisa pakai Git |
| Testing | Manual | Otomatis dengan script |
| Deployment | Satu-satu | Bisa diotomasi |
| Kolaborasi | Sulit | Mudah dengan Git |

**Kesimpulan**: Untuk proyek Smart Contract yang serius, kita butuh development environment lokal.

**Tools yang akan kita install:**

```
┌─────────────────────────────────────────────────────────────┐
│  NODE.JS                                                    │
│  Platform untuk menjalankan JavaScript di luar browser      │
│  └── pnpm (package manager untuk install library)           │
│      └── Hardhat (framework Smart Contract)                 │
│          └── ethers.js (library untuk interact blockchain)  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  GANACHE                                                    │
│  Blockchain lokal (tiruan) untuk testing                    │
│  - Gratis, tidak pakai ETH sungguhan                        │
│  - 10 akun dengan saldo 100 ETH masing-masing               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  VS CODE + Extension Solidity                               │
│  Editor kode dengan fitur syntax highlighting               │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Instalasi Node.js

**Apa itu Node.js?**

Node.js adalah platform yang memungkinkan kita menjalankan JavaScript di luar browser. Hardhat dan tools blockchain lainnya dibangun di atas Node.js.

### 2.1 Windows

**Langkah-langkah:**

1. **Buka website Node.js**
   - Buka browser dan kunjungi: https://nodejs.org

2. **Download installer**
   - Klik tombol **LTS** (Long Term Support) - yang berwarna hijau
   - File akan terdownload (contoh: `node-v20.11.0-x64.msi`)

   ![Download Node.js](image/module-08b/nodejs-download.png)

3. **Jalankan installer**
   - Double-click file yang sudah didownload
   - Klik **Next** di setiap langkah
   - Biarkan semua pengaturan default
   - Klik **Install**
   - Tunggu proses instalasi selesai
   - Klik **Finish**

4. **Buka Command Prompt**
   - Tekan `Windows + R` di keyboard
   - Ketik `cmd`
   - Tekan Enter

5. **Cek instalasi**
   - Di Command Prompt, ketik:
   ```bash
   node --version
   ```
   - Tekan Enter

**Hasil yang diharapkan:**
```
v20.11.0
```
(Angka versi mungkin berbeda, yang penting muncul angka versi)

### 2.2 macOS

**Langkah-langkah:**

1. **Buka website Node.js**
   - Buka browser dan kunjungi: https://nodejs.org

2. **Download installer**
   - Klik tombol **LTS** (warna hijau)
   - File `.pkg` akan terdownload

3. **Jalankan installer**
   - Buka file `.pkg` yang sudah didownload
   - Ikuti petunjuk instalasi (klik Continue/Next)
   - Masukkan password Mac jika diminta
   - Klik Install
   - Tunggu sampai selesai

4. **Buka Terminal**
   - Tekan `Cmd + Space`
   - Ketik `Terminal`
   - Tekan Enter

5. **Cek instalasi**
   ```bash
   node --version
   ```

**Hasil yang diharapkan:**
```
v20.11.0
```

### 2.3 Linux (Ubuntu/Debian)

**Langkah-langkah:**

1. **Buka Terminal**
   - Tekan `Ctrl + Alt + T`

2. **Tambahkan repository NodeSource**
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   ```
   - Masukkan password jika diminta
   - Tunggu proses selesai

3. **Install Node.js**
   ```bash
   sudo apt-get install -y nodejs
   ```

4. **Cek instalasi**
   ```bash
   node --version
   ```

**Hasil yang diharapkan:**
```
v20.11.0
```

### 2.4 Verifikasi Instalasi Node.js

Setelah instalasi, pastikan juga **npm** (Node Package Manager) terinstall:

```bash
npm --version
```

**Hasil yang diharapkan:**
```
10.2.3
```
(Angka versi mungkin berbeda)

> **Checkpoint 1**: Jika `node --version` dan `npm --version` keduanya menampilkan angka versi, lanjut ke langkah berikutnya!

---

## 3. Instalasi pnpm (Package Manager)

**Apa itu pnpm?**

pnpm adalah package manager alternatif yang lebih cepat dan hemat ruang disk dibanding npm. Kita akan menggunakan pnpm untuk menginstall library-library yang dibutuhkan project.

**Langkah-langkah (semua OS sama):**

1. **Buka Terminal/Command Prompt**

2. **Jalankan perintah instalasi**
   ```bash
   npm install -g pnpm
   ```

   **Penjelasan:**
   - `npm` = package manager bawaan Node.js
   - `install` = perintah untuk menginstall
   - `-g` = global (bisa dipakai di mana saja)
   - `pnpm` = nama package yang diinstall

3. **Tunggu proses instalasi**
   - Akan muncul progress bar
   - Tunggu sampai selesai

4. **Verifikasi instalasi**
   ```bash
   pnpm --version
   ```

**Hasil yang diharapkan:**
```
8.15.4
```

**Troubleshooting:**

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `EACCES permission denied` | Tidak punya akses | **macOS/Linux**: tambahkan `sudo` di depan: `sudo npm install -g pnpm` |
| `npm is not recognized` | Node.js belum terinstall | Kembali ke langkah 2 (Install Node.js) |
| `command not found: pnpm` | PATH belum terupdate | Tutup dan buka ulang Terminal/Command Prompt |

> **Checkpoint 2**: Jika `pnpm --version` menampilkan angka versi, lanjut ke langkah berikutnya!

---

## 4. Instalasi Ganache (Local Blockchain)

**Apa itu Ganache?**

Ganache adalah blockchain tiruan yang berjalan di komputer kita. Ini memungkinkan kita untuk:
- Testing Smart Contract tanpa biaya
- Mendapatkan ETH gratis (uang tiruan)
- Melihat transaksi secara visual
- Debug dengan mudah

**Analogi**: Ganache seperti "simulator" pesawat untuk pilot. Kita bisa belajar dan bereksperimen tanpa risiko.

### 4.1 Download dan Install

1. **Buka website Ganache**
   - Kunjungi: https://trufflesuite.com/ganache

2. **Download sesuai OS**
   - Klik tombol download untuk OS kamu:
     - Windows: `.exe` atau `.appx`
     - macOS: `.dmg`
     - Linux: `.AppImage`

3. **Install aplikasi**

   **Windows:**
   - Double-click file installer
   - Ikuti petunjuk instalasi
   - Selesai

   **macOS:**
   - Buka file `.dmg`
   - Drag Ganache ke folder Applications
   - Buka dari Launchpad atau Applications

   **Linux:**
   - Buat file executable: `chmod +x Ganache-*.AppImage`
   - Jalankan: `./Ganache-*.AppImage`

4. **Jalankan Ganache**
   - Buka aplikasi Ganache
   - Klik **Quickstart** untuk memulai blockchain lokal

### 4.2 Mengenal Tampilan Ganache

Setelah Ganache berjalan, kamu akan melihat tampilan seperti ini:

```
┌─────────────────────────────────────────────────────────────────────┐
│  GANACHE                                                    [─][□][×]│
├─────────────────────────────────────────────────────────────────────┤
│  ACCOUNTS  BLOCKS  TRANSACTIONS  CONTRACTS  EVENTS  LOGS           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  RPC SERVER: HTTP://127.0.0.1:7545    NETWORK ID: 5777              │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  ACCOUNT                                          BALANCE           │
│  ────────────────────────────────────────────────────────────────   │
│  0x1234...5678  [🔑]                              100.00 ETH        │
│  0xAbCd...9012  [🔑]                              100.00 ETH        │
│  0x3456...7890  [🔑]                              100.00 ETH        │
│  ... (total 10 akun)                                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.3 Informasi Penting di Ganache

**1. RPC Server URL**
```
HTTP://127.0.0.1:7545
```
Ini adalah "alamat" blockchain lokal kita. Nanti kita akan menggunakan URL ini untuk koneksi dari script.

**2. Daftar Akun**
- Ada 10 akun yang sudah dibuat otomatis
- Setiap akun punya saldo 100 ETH (uang tiruan)
- Setiap akun punya alamat unik (contoh: `0x1234...5678`)

**3. Private Key** (sangat penting!)
- Klik ikon kunci (🔑) di samping akun untuk melihat private key
- **JANGAN PERNAH** share private key ke siapapun!
- Kita akan membutuhkan private key ini di Module 10

**Cara mendapatkan Private Key:**
1. Klik ikon kunci (🔑) di samping salah satu akun
2. Akan muncul popup dengan private key
3. Copy private key tersebut (akan dipakai di Module 10)

```
┌────────────────────────────────────────────────┐
│  ACCOUNT KEYS                                  │
│                                                │
│  Address:                                      │
│  0x1234567890abcdef1234567890abcdef12345678    │
│                                                │
│  Private Key:                                  │
│  0xabcdef1234567890abcdef1234567890abcdef...   │
│                                        [COPY]  │
└────────────────────────────────────────────────┘
```

> **Checkpoint 3**: Jika Ganache berjalan dan menampilkan daftar akun, lanjut ke langkah berikutnya!

---

## 5. Setup VS Code untuk Solidity

**Apa itu extension Solidity?**

Extension ini menambahkan fitur-fitur yang memudahkan menulis kode Solidity:
- Syntax highlighting (kode berwarna)
- Auto-completion (saran kode otomatis)
- Error detection (mendeteksi kesalahan)

**Langkah-langkah:**

1. **Buka VS Code**

2. **Buka panel Extensions**
   - Tekan `Ctrl + Shift + X` (Windows/Linux)
   - Atau `Cmd + Shift + X` (macOS)
   - Atau klik ikon kotak-kotak di sidebar kiri

3. **Cari extension Solidity**
   - Ketik `solidity` di kotak pencarian
   - Cari extension **"Solidity"** oleh **Juan Blanco**
   - Ini adalah extension Solidity paling populer

4. **Install extension**
   - Klik tombol **Install** berwarna biru
   - Tunggu sampai selesai

5. **Verifikasi**
   - Buat file baru dengan ekstensi `.sol`
   - Ketik beberapa kode Solidity
   - Jika kode berwarna-warni, extension sudah aktif!

**Test extension:**

Buat file `test.sol` dan ketik:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Test {
    uint public angka = 42;
}
```

Jika kode terlihat berwarna-warni (bukan hitam putih semua), extension sudah bekerja!

> **Checkpoint 4**: Extension Solidity terinstall dan aktif.

---

## 6. Clone dan Setup Project

**Langkah-langkah:**

1. **Buka Terminal/Command Prompt**

2. **Pindah ke folder project**
   ```bash
   cd smart-contract/contracts
   ```

   > Jika folder belum ada, tanyakan ke dosen/asisten untuk mendapatkan project files.

3. **Install dependensi**
   ```bash
   pnpm install
   ```

   **Apa yang terjadi:**
   - pnpm membaca file `package.json`
   - Menginstall semua library yang tercantum
   - Membuat folder `node_modules`

4. **Tunggu proses instalasi**
   - Ini mungkin memakan waktu 1-5 menit
   - Tergantung kecepatan internet

**Output yang diharapkan:**
```
Packages: +245
++++++++++++++++++++++++++++++++++++++++++++++++++
Progress: resolved 245, reused 0, downloaded 245, added 245, done
```

> **Checkpoint 5**: `pnpm install` berhasil tanpa error.

---

## 7. Verifikasi Akhir

Sebelum melanjutkan ke Module 10, pastikan semua tools berfungsi dengan menjalankan checklist ini:

### Checklist Instalasi

Buka Terminal/Command Prompt dan jalankan perintah-perintah berikut:

**1. Node.js**
```bash
node --version
```
Expected: `v20.x.x` atau lebih baru

**2. npm**
```bash
npm --version
```
Expected: `10.x.x` atau lebih baru

**3. pnpm**
```bash
pnpm --version
```
Expected: `8.x.x` atau lebih baru

**4. Ganache**
- Buka aplikasi Ganache
- Klik Quickstart
- Pastikan muncul daftar 10 akun

**5. VS Code Extension**
- Buat file `.sol`
- Pastikan syntax highlighting aktif (kode berwarna)

### Ringkasan Informasi Penting

Catat informasi berikut untuk dipakai di Module 10:

| Item | Nilai | Contoh |
|------|-------|--------|
| Node.js version | ... | v20.11.0 |
| pnpm version | ... | 8.15.4 |
| Ganache RPC URL | ... | HTTP://127.0.0.1:7545 |
| Private Key (akun 1) | ... | 0xabcd... |

---

## Troubleshooting

### Error Umum dan Solusinya

**1. `node is not recognized` / `command not found: node`**

| Penyebab | Solusi |
|----------|--------|
| Node.js belum terinstall | Install Node.js dari awal |
| PATH belum terupdate | Restart Terminal/Command Prompt |
| Instalasi gagal | Uninstall dan install ulang Node.js |

**2. `EACCES permission denied`**

| OS | Solusi |
|-----|--------|
| macOS/Linux | Tambahkan `sudo` di depan perintah |
| Windows | Jalankan Command Prompt sebagai Administrator |

**3. `npm ERR! network`**

| Penyebab | Solusi |
|----------|--------|
| Tidak ada internet | Cek koneksi internet |
| Firewall/proxy | Minta bantuan IT untuk konfigurasi |

**4. Ganache tidak bisa dibuka**

| Penyebab | Solusi |
|----------|--------|
| Port 7545 sudah dipakai | Tutup aplikasi lain yang mungkin pakai port tersebut |
| File corrupt | Download ulang dan install ulang |

**5. Extension Solidity tidak aktif**

| Penyebab | Solusi |
|----------|--------|
| File bukan `.sol` | Pastikan nama file diakhiri `.sol` |
| Extension belum direload | Restart VS Code |
| Konflik dengan extension lain | Disable extension Solidity lain |

---

## Selesai!

Jika semua checkpoint sudah selesai:

- [x] Node.js terinstall
- [x] pnpm terinstall
- [x] Ganache terinstall dan berjalan
- [x] VS Code extension Solidity aktif
- [x] Project dependencies terinstall

**Kamu siap melanjutkan ke [Module 10: Smart Contract dengan Solidity dan Hardhat](module-10.md)!**

> **Tips**: Biarkan Ganache tetap berjalan di background saat mengerjakan Module 10.
