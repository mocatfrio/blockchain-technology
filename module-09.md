# Modul Hands-on Smart Contract dengan Remix untuk Pemula

**Tools:** Browser, Remix Ethereum IDE
**Prasyarat:** Paham dasar blockchain, transaksi, wallet, dan konsep address secara umum

Setelah mengikuti modul ini, peserta diharapkan mampu:

* menjelaskan apa itu smart contract
* mengenali bagian dasar kode Solidity
* menjalankan smart contract sederhana di Remix
* membedakan function, state, dan constructor
* memahami `require`, `msg.sender`, dan owner-only access
* menguji skenario transaksi berhasil dan gagal

## 3. Gambaran Singkat

Dalam modul ini, peserta  **tidak menulis dari nol** .
Peserta akan:

* membuka kode yang sudah jadi
* membaca logika sederhana
* compile contract
* deploy contract
* menjalankan function
* mengamati perubahan state
* menganalisis kapan transaksi berhasil atau gagal

Fokusnya adalah  **memahami logika smart contract** , bukan syntax mendalam.

## 4. Konsep Dasar Sebelum Praktik

### Apa itu smart contract?

Smart contract adalah program yang berjalan di blockchain untuk menjalankan aturan secara otomatis.

### Bedanya dengan program biasa

Program biasa berjalan di komputer/server tertentu.
Smart contract berjalan di blockchain dan aturannya dijalankan secara konsisten oleh jaringan.

### Istilah penting

**State variable**
Data yang disimpan oleh contract.

**Function**
Aksi yang bisa dijalankan pada contract.

**Constructor**
Function khusus yang berjalan sekali saat contract dibuat.

**msg.sender**
Address yang sedang memanggil function.

**require**
Syarat yang harus dipenuhi. Kalau tidak terpenuhi, transaksi gagal.

**revert**
Keadaan saat transaksi dibatalkan karena syarat tidak terpenuhi.

**owner**
Address pemilik contract, biasanya pembuat contract.

---

## 5. Mengenal Remix

Remix adalah IDE berbasis web untuk menulis, compile, deploy, dan menguji smart contract.

Yang perlu diperhatikan:

* **File Explorer** : tempat file contract
* **Solidity Compiler** : compile kode
* **Deploy & Run Transactions** : deploy dan jalankan contract
* **Deployed Contracts** : tempat contract yang sudah aktif untuk diuji

---

## 6. Kontrak Contoh: Voting Contract Sederhana

Gunakan kode ini di Remix.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleVoting {
    address public owner;
    uint public yesCount;
    mapping(address => bool) public hasVoted;

    constructor() {
        owner = msg.sender;
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

---

## 7. Penjelasan Kode Secara Sederhana

### `address public owner;`

Menyimpan address pemilik contract.

### `uint public yesCount;`

Menyimpan jumlah vote “yes”.

### `mapping(address => bool) public hasVoted;`

Mencatat apakah suatu address sudah pernah vote.

### `constructor()`

Saat contract dibuat, address pembuat menjadi owner.

### `voteYes()`

Digunakan untuk memberikan suara.

* kalau address belum vote, vote diterima
* kalau sudah vote, transaksi gagal

### `resetVoting()`

Digunakan untuk mereset jumlah suara.

* hanya owner yang boleh menjalankan

---

## 8. Langkah Praktik di Remix

### Langkah 1: Buka Remix

Buka Remix di browser.

### Langkah 2: Buat file baru

Buat file bernama `SimpleVoting.sol`

### Langkah 3: Tempel kode

Salin kode contract ke file tersebut.

### Langkah 4: Compile

Buka menu **Solidity Compiler** lalu klik **Compile SimpleVoting.sol**

Kalau berhasil, tidak ada error merah.

### Langkah 5: Deploy

Buka menu **Deploy & Run Transactions**

* Environment: pilih **Remix VM**
* klik **Deploy**

### Langkah 6: Uji contract

Di bagian  **Deployed Contracts** , akan muncul contract `SimpleVoting`

## 14. Diskusi Konsep

Gunakan pertanyaan ini setelah praktik:

* Mengapa contract perlu menyimpan state?
* Mengapa satu account tidak boleh vote dua kali?
* Mengapa reset harus dibatasi ke owner?
* Apa peran `msg.sender`?
* Apa yang terjadi jika tidak ada `require`?
