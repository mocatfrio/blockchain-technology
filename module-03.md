# Module 03. Advanced Blockchain Concepts

## Deskripsi

Modul ini merupakan kelanjutan dari [Module 02](module-02.md) yang membahas konsep-konsep blockchain tingkat lanjut. Pada modul ini, kita akan memperdalam pemahaman tentang struktur data dan mekanisme yang membuat blockchain lebih efisien dan aman.

Topik yang dibahas pada modul ini:

1. **Merkle Tree** - Struktur data untuk verifikasi transaksi secara efisien
2. **Mining Reward** - Mekanisme insentif untuk miner
3. **Balance Tracking** - Pelacakan saldo menggunakan model berbasis akun
4. **Mempool** - Manajemen transaksi yang menunggu konfirmasi
5. **Difficulty Adjustment** - Penyesuaian tingkat kesulitan mining

Berikut adalah [full code](advanced-blockchain/blockchain.py) yang dibahas pada modul ini.

## Prasyarat

Sebelum mempelajari modul ini, pastikan telah:

1. Memahami [Module 02 - Blockchain Fundamentals](module-02.md)
2. Menginstall library yang diperlukan:
   ```bash
   pip install datetime
   ```

## List of Contents

- [Deskripsi](#deskripsi)
- [Prasyarat](#prasyarat)
- [List of Contents](#list-of-contents)
- [1. Teori Merkle Tree](#1-teori-merkle-tree)
  - [1.1 Apa itu Merkle Tree?](#11-apa-itu-merkle-tree)
  - [1.2 Mengapa Merkle Tree Penting?](#12-mengapa-merkle-tree-penting)
  - [1.3 Cara Kerja Merkle Tree](#13-cara-kerja-merkle-tree)
  - [1.4 Merkle Proof](#14-merkle-proof)
- [2. Teori Mining Reward](#2-teori-mining-reward)
  - [2.1 Mengapa Mining Reward Diperlukan?](#21-mengapa-mining-reward-diperlukan)
  - [2.2 Coinbase Transaction](#22-coinbase-transaction)
  - [2.3 Block Subsidy dan Halving](#23-block-subsidy-dan-halving)
- [3. Teori Balance Tracking](#3-teori-balance-tracking)
  - [3.1 UTXO vs Account Model](#31-utxo-vs-account-model)
  - [3.2 Account-Based Model](#32-account-based-model)
- [4. Teori Mempool](#4-teori-mempool)
  - [4.1 Apa itu Mempool?](#41-apa-itu-mempool)
  - [4.2 Transaction Priority](#42-transaction-priority)
- [5. Teori Difficulty Adjustment](#5-teori-difficulty-adjustment)
  - [5.1 Mengapa Perlu Adjustment?](#51-mengapa-perlu-adjustment)
  - [5.2 Target Block Time](#52-target-block-time)
- [6. Implementasi Program](#6-implementasi-program)
  - [6.1 Struktur Project](#61-struktur-project)
  - [6.2 Import Library](#62-import-library)
  - [6.3 Class MerkleTree](#63-class-merkletree)
  - [6.4 Class Transaction dengan Fee](#64-class-transaction-dengan-fee)
  - [6.5 Class Block dengan Merkle Root](#65-class-block-dengan-merkle-root)
  - [6.6 Class Blockchain dengan Mining Reward](#66-class-blockchain-dengan-mining-reward)
  - [6.7 Program Utama](#67-program-utama)
- [7. Pengujian](#7-pengujian)
  - [7.1 Menguji Merkle Tree](#71-menguji-merkle-tree)
  - [7.2 Menguji Mining Reward](#72-menguji-mining-reward)
  - [7.3 Menguji Balance Tracking](#73-menguji-balance-tracking)
- [Latihan](#latihan)

---

## 1. Teori Merkle Tree

### 1.1 Apa itu Merkle Tree?

**Merkle Tree** (atau Hash Tree) adalah struktur data berbentuk pohon biner di mana:

- Setiap **leaf node** berisi hash dari data (dalam konteks blockchain: hash transaksi)
- Setiap **non-leaf node** berisi hash gabungan dari dua child node-nya
- **Root node** (Merkle Root) merepresentasikan seluruh data dalam satu hash

```
                    Merkle Root
                   /            \
                 H(AB)          H(CD)
                /    \          /    \
             H(A)   H(B)     H(C)   H(D)
              |      |        |      |
            Tx A   Tx B     Tx C   Tx D
```

Merkle Tree pertama kali dipatenkan oleh Ralph Merkle pada tahun 1979 dan menjadi komponen fundamental dalam Bitcoin dan blockchain lainnya.

### 1.2 Mengapa Merkle Tree Penting?

Merkle Tree memberikan beberapa keuntungan penting:

| Keuntungan | Penjelasan |
|------------|------------|
| **Verifikasi Efisien** | Tidak perlu mengunduh seluruh block untuk memverifikasi satu transaksi |
| **Integritas Data** | Perubahan satu transaksi akan mengubah Merkle Root |
| **Light Client Support** | Memungkinkan SPV (Simplified Payment Verification) |
| **Bandwidth Efficient** | Hanya perlu log₂(n) hash untuk membuktikan satu transaksi |

Contoh efisiensi:
- Block dengan 1000 transaksi
- Tanpa Merkle Tree: perlu 1000 hash untuk verifikasi
- Dengan Merkle Tree: hanya perlu ~10 hash (log₂(1000) ≈ 10)

### 1.3 Cara Kerja Merkle Tree

**Langkah pembentukan Merkle Tree:**

1. Hash setiap transaksi untuk mendapatkan leaf nodes
2. Pasangkan leaf nodes dan hash gabungannya
3. Ulangi langkah 2 sampai tersisa satu node (root)

**Contoh dengan 4 transaksi:**

```
Transaksi:
- Tx A: "Alice kirim 10 ke Bob"
- Tx B: "Bob kirim 5 ke Charlie"
- Tx C: "Charlie kirim 3 ke Diana"
- Tx D: "Diana kirim 2 ke Eve"

Langkah 1: Hash setiap transaksi
- H(A) = sha256("Alice kirim 10 ke Bob") = "a1b2..."
- H(B) = sha256("Bob kirim 5 ke Charlie") = "c3d4..."
- H(C) = sha256("Charlie kirim 3 ke Diana") = "e5f6..."
- H(D) = sha256("Diana kirim 2 ke Eve") = "g7h8..."

Langkah 2: Hash pasangan
- H(AB) = sha256(H(A) + H(B)) = "i9j0..."
- H(CD) = sha256(H(C) + H(D)) = "k1l2..."

Langkah 3: Hash root
- Merkle Root = sha256(H(AB) + H(CD)) = "m3n4..."
```

**Jika jumlah transaksi ganjil:**

Jika ada jumlah ganjil pada suatu level, transaksi terakhir diduplikasi:

```
        Merkle Root
       /           \
    H(AB)         H(CC)    ← C diduplikasi
   /    \         /    \
 H(A)  H(B)    H(C)  H(C)
```

### 1.4 Merkle Proof

**Merkle Proof** adalah bukti bahwa suatu transaksi termasuk dalam block tanpa perlu mengunduh seluruh transaksi.

Untuk membuktikan Tx B ada dalam block:

```
                    Merkle Root ✓
                   /            \
                H(AB) ✓        H(CD) ← diberikan
                /    \
            H(A) ←   H(B) ✓
          diberikan    |
                     Tx B ← yang ingin dibuktikan
```

**Data yang diperlukan untuk proof:**
1. Hash transaksi target: H(B)
2. Sibling hash: H(A)
3. Uncle hash: H(CD)
4. Merkle Root untuk verifikasi

Dengan 3 hash saja, kita bisa membuktikan Tx B ada dalam block yang berisi 4 transaksi.

---

## 2. Teori Mining Reward

### 2.1 Mengapa Mining Reward Diperlukan?

Mining adalah proses yang membutuhkan sumber daya komputasi. Tanpa insentif, tidak ada motivasi bagi node untuk melakukan mining. **Mining Reward** memberikan:

| Aspek | Penjelasan |
|-------|------------|
| **Insentif Ekonomi** | Miner mendapat imbalan atas kerja komputasinya |
| **Distribusi Coin** | Cara untuk menerbitkan coin baru ke dalam sistem |
| **Keamanan Jaringan** | Semakin banyak miner, semakin aman jaringan |

Mining reward terdiri dari dua komponen:
1. **Block Subsidy** - Coin baru yang diciptakan
2. **Transaction Fees** - Biaya dari pengirim transaksi

```
Total Reward = Block Subsidy + Transaction Fees
```

### 2.2 Coinbase Transaction

**Coinbase Transaction** adalah transaksi khusus yang:

- Tidak memiliki pengirim (sender = "COINBASE" atau "SYSTEM")
- Dibuat otomatis saat mining berhasil
- Mengirimkan reward ke alamat miner
- Selalu menjadi transaksi **pertama** dalam block

```
┌─────────────────────────────────────────┐
│              BLOCK #5                   │
├─────────────────────────────────────────┤
│  Transaction 0: (Coinbase)              │
│    From: COINBASE                       │
│    To: Miner_Address                    │
│    Amount: 50 coins (subsidy)           │
│    + 0.5 coins (fees)                   │
├─────────────────────────────────────────┤
│  Transaction 1:                         │
│    From: Alice                          │
│    To: Bob                              │
│    Amount: 10 coins                     │
│    Fee: 0.3 coins                       │
├─────────────────────────────────────────┤
│  Transaction 2:                         │
│    From: Bob                            │
│    To: Charlie                          │
│    Amount: 5 coins                      │
│    Fee: 0.2 coins                       │
└─────────────────────────────────────────┘
```

### 2.3 Block Subsidy dan Halving

Pada Bitcoin, block subsidy mengalami **halving** (pengurangan setengah) setiap 210.000 block (~4 tahun):

| Era | Block Range | Subsidy | Tahun |
|-----|------------|---------|-------|
| 1 | 0 - 209,999 | 50 BTC | 2009-2012 |
| 2 | 210,000 - 419,999 | 25 BTC | 2012-2016 |
| 3 | 420,000 - 629,999 | 12.5 BTC | 2016-2020 |
| 4 | 630,000 - 839,999 | 6.25 BTC | 2020-2024 |
| 5 | 840,000 - ... | 3.125 BTC | 2024-... |

Halving memastikan total supply Bitcoin terbatas (21 juta BTC).

---

## 3. Teori Balance Tracking

### 3.1 UTXO vs Account Model

Ada dua model utama untuk melacak kepemilikan dalam blockchain:

| Aspek | UTXO Model (Bitcoin) | Account Model (Ethereum) |
|-------|---------------------|-------------------------|
| **Konsep** | Seperti uang kertas - setiap "koin" adalah output yang belum digunakan | Seperti rekening bank - setiap alamat punya saldo |
| **Transaksi** | Menghabiskan UTXO lama, membuat UTXO baru | Mengurangi saldo pengirim, menambah saldo penerima |
| **Privacy** | Lebih baik (alamat bisa berubah) | Kurang (alamat tetap) |
| **Smart Contract** | Sulit | Mudah |
| **Kompleksitas** | Lebih kompleks | Lebih sederhana |

**Contoh UTXO:**
```
Alice memiliki:
- UTXO #1: 30 coins
- UTXO #2: 20 coins

Alice kirim 45 coins ke Bob:
- Input: UTXO #1 (30) + UTXO #2 (20) = 50 coins
- Output 1: 45 coins ke Bob (UTXO baru)
- Output 2: 5 coins ke Alice (kembalian, UTXO baru)
```

**Contoh Account Model:**
```
State awal:
- Alice: 50 coins
- Bob: 10 coins

Alice kirim 45 coins ke Bob:
- Alice: 50 - 45 = 5 coins
- Bob: 10 + 45 = 55 coins
```

### 3.2 Account-Based Model

Pada modul ini, kita menggunakan **Account-Based Model** karena lebih sederhana untuk dipelajari. Implementasinya:

```python
# Menghitung saldo dengan iterasi semua transaksi
def get_balance(address):
    balance = 0
    for block in blockchain:
        for tx in block.transactions:
            if tx.sender == address:
                balance -= tx.amount
            if tx.receiver == address:
                balance += tx.amount
    return balance
```

---

## 4. Teori Mempool

### 4.1 Apa itu Mempool?

**Mempool** (Memory Pool) adalah tempat penyimpanan sementara untuk transaksi yang:
- Sudah divalidasi
- Belum dimasukkan ke dalam block
- Menunggu untuk di-mining

```
┌─────────────────────────────────────────────────────┐
│                     MEMPOOL                         │
├─────────────────────────────────────────────────────┤
│  Tx #1: Alice → Bob (10 coins)     Fee: 0.5        │
│  Tx #2: Charlie → Diana (5 coins)  Fee: 0.3        │
│  Tx #3: Eve → Frank (20 coins)     Fee: 0.8  ← prioritas tinggi
│  Tx #4: Grace → Henry (2 coins)    Fee: 0.1        │
└─────────────────────────────────────────────────────┘
                         │
                         ▼ Mining
┌─────────────────────────────────────────────────────┐
│                    NEW BLOCK                        │
│  Coinbase: SYSTEM → Miner (50 + 1.7 coins)         │
│  Tx #3: Eve → Frank (20 coins)     ← fee tertinggi │
│  Tx #1: Alice → Bob (10 coins)                     │
│  Tx #2: Charlie → Diana (5 coins)                  │
│  Tx #4: Grace → Henry (2 coins)                    │
└─────────────────────────────────────────────────────┘
```

### 4.2 Transaction Priority

Miner biasanya memprioritaskan transaksi berdasarkan:

1. **Fee per byte** - Transaksi dengan fee lebih tinggi diprioritaskan
2. **Age** - Transaksi yang sudah lama menunggu
3. **Size** - Transaksi yang lebih kecil lebih mudah dimasukkan

Dalam implementasi sederhana, kita bisa menggunakan fee sebagai prioritas:

```python
# Urutkan transaksi berdasarkan fee (tertinggi dulu)
sorted_transactions = sorted(mempool, key=lambda tx: tx.fee, reverse=True)
```

---

## 5. Teori Difficulty Adjustment

### 5.1 Mengapa Perlu Adjustment?

Seiring waktu, faktor-faktor berikut berubah:
- Jumlah miner bertambah/berkurang
- Hardware mining semakin canggih
- Total hash power jaringan berfluktuasi

Tanpa adjustment, block time bisa menjadi:
- Terlalu cepat → keamanan berkurang
- Terlalu lambat → transaksi menumpuk

### 5.2 Target Block Time

Setiap blockchain memiliki target block time:

| Blockchain | Target Block Time |
|------------|-------------------|
| Bitcoin | ~10 menit |
| Ethereum | ~12 detik |
| Litecoin | ~2.5 menit |

**Algoritma Adjustment Sederhana:**

```python
# Setiap N block, hitung rata-rata waktu
actual_time = waktu_N_block_terakhir
expected_time = N * target_block_time

if actual_time < expected_time:
    # Mining terlalu cepat, naikkan difficulty
    difficulty += 1
elif actual_time > expected_time * 2:
    # Mining terlalu lambat, turunkan difficulty
    difficulty -= 1
```

---

## 6. Implementasi Program

### 6.1 Struktur Project

Buat folder baru `advanced-blockchain` dengan struktur:

```
advanced-blockchain/
├── blockchain.py    # Core blockchain dengan fitur baru
└── test.py          # Testing (opsional)
```

### 6.2 Import Library

```python
# blockchain.py
import hashlib
import json
import time
from datetime import datetime
```

### 6.3 Class MerkleTree

```python
class MerkleTree:
    """
    Implementasi Merkle Tree untuk verifikasi transaksi.
    """

    @staticmethod
    def hash(data):
        """Membuat hash SHA-256 dari data."""
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def build_tree(transactions):
        """
        Membangun Merkle Tree dari list transaksi.
        Mengembalikan Merkle Root.
        """
        if not transactions:
            return MerkleTree.hash("")

        # Hash setiap transaksi (leaf nodes)
        leaves = [MerkleTree.hash(json.dumps(tx.to_dict(), sort_keys=True))
                  for tx in transactions]

        # Bangun tree dari bawah ke atas
        while len(leaves) > 1:
            # Jika ganjil, duplikasi node terakhir
            if len(leaves) % 2 == 1:
                leaves.append(leaves[-1])

            # Gabungkan pasangan dan hash
            next_level = []
            for i in range(0, len(leaves), 2):
                combined = leaves[i] + leaves[i + 1]
                next_level.append(MerkleTree.hash(combined))

            leaves = next_level

        return leaves[0]  # Merkle Root

    @staticmethod
    def get_proof(transactions, target_index):
        """
        Mendapatkan Merkle Proof untuk transaksi pada index tertentu.
        Mengembalikan list of (hash, position) tuples.
        """
        if not transactions or target_index >= len(transactions):
            return []

        # Hash semua transaksi
        current_level = [MerkleTree.hash(json.dumps(tx.to_dict(), sort_keys=True))
                        for tx in transactions]

        proof = []
        index = target_index

        while len(current_level) > 1:
            # Duplikasi jika ganjil
            if len(current_level) % 2 == 1:
                current_level.append(current_level[-1])

            # Tentukan sibling
            if index % 2 == 0:
                sibling_index = index + 1
                position = 'right'
            else:
                sibling_index = index - 1
                position = 'left'

            proof.append((current_level[sibling_index], position))

            # Bangun level berikutnya
            next_level = []
            for i in range(0, len(current_level), 2):
                combined = current_level[i] + current_level[i + 1]
                next_level.append(MerkleTree.hash(combined))

            current_level = next_level
            index = index // 2

        return proof

    @staticmethod
    def verify_proof(tx_hash, proof, merkle_root):
        """
        Memverifikasi Merkle Proof.
        """
        current_hash = tx_hash

        for sibling_hash, position in proof:
            if position == 'left':
                combined = sibling_hash + current_hash
            else:
                combined = current_hash + sibling_hash
            current_hash = MerkleTree.hash(combined)

        return current_hash == merkle_root
```

### 6.4 Class Transaction dengan Fee

```python
class Transaction:
    """
    Transaksi dengan tambahan fee untuk prioritas.
    """

    def __init__(self, sender, receiver, amount, fee=0):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee
        self.timestamp = time.time()

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'fee': self.fee,
            'timestamp': self.timestamp
        }

    def __repr__(self):
        return f"Tx({self.sender} → {self.receiver}: {self.amount}, fee={self.fee})"
```

### 6.5 Class Block dengan Merkle Root

```python
class Block:
    """
    Block dengan Merkle Root untuk verifikasi transaksi efisien.
    """

    def __init__(self, index, transactions, previous_hash, miner=None):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.miner = miner
        self.nonce = 0

        # Hitung Merkle Root dari transaksi
        self.merkle_root = MerkleTree.build_tree(transactions)

        # Hash block
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Menghitung hash block menggunakan Merkle Root."""
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'merkle_root': self.merkle_root,  # Gunakan Merkle Root, bukan seluruh transaksi
            'previous_hash': self.previous_hash,
            'miner': self.miner,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty):
        """Mining block dengan Proof of Work."""
        target = '0' * difficulty
        start_time = time.time()

        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

        mining_time = time.time() - start_time
        return mining_time

    def verify_transaction(self, tx_index):
        """
        Memverifikasi transaksi dalam block menggunakan Merkle Proof.
        """
        if tx_index >= len(self.transactions):
            return False

        tx = self.transactions[tx_index]
        tx_hash = MerkleTree.hash(json.dumps(tx.to_dict(), sort_keys=True))
        proof = MerkleTree.get_proof(self.transactions, tx_index)

        return MerkleTree.verify_proof(tx_hash, proof, self.merkle_root)

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'merkle_root': self.merkle_root,
            'previous_hash': self.previous_hash,
            'miner': self.miner,
            'nonce': self.nonce,
            'hash': self.hash
        }
```

### 6.6 Class Blockchain dengan Mining Reward

```python
class Blockchain:
    """
    Blockchain dengan fitur:
    - Mining reward
    - Balance tracking
    - Mempool dengan prioritas
    - Difficulty adjustment
    """

    # Konstanta
    INITIAL_DIFFICULTY = 4
    BLOCK_REWARD = 50
    HALVING_INTERVAL = 10  # Untuk simulasi, halving setiap 10 block
    ADJUSTMENT_INTERVAL = 5  # Adjust difficulty setiap 5 block
    TARGET_BLOCK_TIME = 2  # Target 2 detik per block (untuk simulasi)

    def __init__(self):
        self.chain = []
        self.mempool = []  # Pending transactions
        self.difficulty = self.INITIAL_DIFFICULTY
        self.block_times = []  # Untuk tracking waktu mining

        # Buat genesis block
        self._create_genesis_block()

    def _create_genesis_block(self):
        """Membuat block pertama (genesis block)."""
        genesis = Block(0, [], "0", miner="GENESIS")
        genesis.mine(self.difficulty)
        self.chain.append(genesis)
        print(f"Genesis block created: {genesis.hash[:16]}...")

    def get_latest_block(self):
        """Mengambil block terakhir."""
        return self.chain[-1]

    def get_block_reward(self):
        """
        Menghitung block reward dengan halving.
        """
        halvings = len(self.chain) // self.HALVING_INTERVAL
        reward = self.BLOCK_REWARD / (2 ** halvings)
        return reward

    def add_transaction(self, transaction):
        """
        Menambahkan transaksi ke mempool setelah validasi.
        """
        # Validasi: sender harus punya cukup saldo
        if transaction.sender != "COINBASE":
            sender_balance = self.get_balance(transaction.sender)
            total_needed = transaction.amount + transaction.fee

            if sender_balance < total_needed:
                raise ValueError(
                    f"Saldo tidak cukup. Balance: {sender_balance}, "
                    f"Dibutuhkan: {total_needed}"
                )

        self.mempool.append(transaction)
        print(f"Transaksi ditambahkan ke mempool: {transaction}")
        return True

    def get_mempool_sorted(self):
        """
        Mengurutkan mempool berdasarkan fee (prioritas tertinggi dulu).
        """
        return sorted(self.mempool, key=lambda tx: tx.fee, reverse=True)

    def mine_block(self, miner_address):
        """
        Mining block baru dengan transaksi dari mempool.
        """
        if not self.mempool:
            print("Mempool kosong, tidak ada transaksi untuk di-mining.")
            return None

        # Ambil transaksi dari mempool (sudah diurutkan berdasarkan fee)
        transactions_to_mine = self.get_mempool_sorted()

        # Hitung total fee
        total_fees = sum(tx.fee for tx in transactions_to_mine)

        # Buat coinbase transaction (reward + fees)
        block_reward = self.get_block_reward()
        total_reward = block_reward + total_fees

        coinbase_tx = Transaction(
            sender="COINBASE",
            receiver=miner_address,
            amount=total_reward,
            fee=0
        )

        # Coinbase transaction selalu di posisi pertama
        all_transactions = [coinbase_tx] + transactions_to_mine

        # Buat block baru
        new_block = Block(
            index=len(self.chain),
            transactions=all_transactions,
            previous_hash=self.get_latest_block().hash,
            miner=miner_address
        )

        # Mining
        print(f"\nMining block #{new_block.index}...")
        print(f"Difficulty: {self.difficulty}")
        print(f"Transaksi: {len(transactions_to_mine)} + 1 coinbase")
        print(f"Block reward: {block_reward} + {total_fees} fees = {total_reward}")

        mining_time = new_block.mine(self.difficulty)
        self.block_times.append(mining_time)

        # Tambahkan ke chain
        self.chain.append(new_block)

        # Kosongkan mempool
        self.mempool = []

        print(f"Block #{new_block.index} berhasil di-mining!")
        print(f"Hash: {new_block.hash[:16]}...")
        print(f"Merkle Root: {new_block.merkle_root[:16]}...")
        print(f"Waktu mining: {mining_time:.2f} detik")

        # Cek apakah perlu adjustment
        self._adjust_difficulty()

        return new_block

    def _adjust_difficulty(self):
        """
        Menyesuaikan difficulty berdasarkan waktu mining.
        """
        if len(self.chain) % self.ADJUSTMENT_INTERVAL != 0:
            return

        if len(self.block_times) < self.ADJUSTMENT_INTERVAL:
            return

        # Hitung rata-rata waktu mining
        recent_times = self.block_times[-self.ADJUSTMENT_INTERVAL:]
        avg_time = sum(recent_times) / len(recent_times)

        print(f"\n=== Difficulty Adjustment ===")
        print(f"Rata-rata waktu mining: {avg_time:.2f} detik")
        print(f"Target: {self.TARGET_BLOCK_TIME} detik")

        old_difficulty = self.difficulty

        if avg_time < self.TARGET_BLOCK_TIME * 0.5:
            # Terlalu cepat, naikkan difficulty
            self.difficulty += 1
            print(f"Mining terlalu cepat! Difficulty: {old_difficulty} → {self.difficulty}")
        elif avg_time > self.TARGET_BLOCK_TIME * 2:
            # Terlalu lambat, turunkan difficulty
            if self.difficulty > 1:
                self.difficulty -= 1
                print(f"Mining terlalu lambat! Difficulty: {old_difficulty} → {self.difficulty}")
        else:
            print(f"Difficulty tetap: {self.difficulty}")

    def get_balance(self, address):
        """
        Menghitung saldo address berdasarkan semua transaksi.
        (Account-based model)
        """
        balance = 0

        for block in self.chain:
            for tx in block.transactions:
                if tx.receiver == address:
                    balance += tx.amount
                if tx.sender == address:
                    balance -= (tx.amount + tx.fee)

        # Juga hitung transaksi di mempool
        for tx in self.mempool:
            if tx.sender == address:
                balance -= (tx.amount + tx.fee)

        return balance

    def get_all_balances(self):
        """
        Mendapatkan saldo semua address yang pernah bertransaksi.
        """
        addresses = set()

        for block in self.chain:
            for tx in block.transactions:
                if tx.sender != "COINBASE":
                    addresses.add(tx.sender)
                addresses.add(tx.receiver)

        return {addr: self.get_balance(addr) for addr in addresses}

    def is_chain_valid(self):
        """
        Memvalidasi keseluruhan blockchain.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Cek hash block
            if current.hash != current.calculate_hash():
                print(f"Hash block #{current.index} tidak valid!")
                return False

            # Cek previous hash
            if current.previous_hash != previous.hash:
                print(f"Previous hash block #{current.index} tidak valid!")
                return False

            # Cek Merkle Root
            expected_merkle = MerkleTree.build_tree(current.transactions)
            if current.merkle_root != expected_merkle:
                print(f"Merkle root block #{current.index} tidak valid!")
                return False

        return True

    def print_chain(self):
        """
        Menampilkan seluruh blockchain.
        """
        print("\n" + "=" * 60)
        print("BLOCKCHAIN")
        print("=" * 60)

        for block in self.chain:
            print(f"\nBlock #{block.index}")
            print(f"  Timestamp: {datetime.fromtimestamp(block.timestamp)}")
            print(f"  Miner: {block.miner}")
            print(f"  Transactions: {len(block.transactions)}")
            print(f"  Merkle Root: {block.merkle_root[:32]}...")
            print(f"  Previous Hash: {block.previous_hash[:32]}...")
            print(f"  Hash: {block.hash[:32]}...")
            print(f"  Nonce: {block.nonce}")

            if block.transactions:
                print("  Transaksi:")
                for tx in block.transactions:
                    print(f"    - {tx}")

        print("\n" + "=" * 60)
```

### 6.7 Program Utama

```python
if __name__ == "__main__":
    # Inisialisasi blockchain
    print("=" * 60)
    print("ADVANCED BLOCKCHAIN DEMO")
    print("=" * 60)

    blockchain = Blockchain()

    # Simulasi transaksi dan mining
    print("\n--- Skenario 1: Mining pertama untuk mendapatkan reward ---")

    # Miner pertama (Alice) mining untuk mendapatkan coin awal
    tx1 = Transaction("Alice", "Alice", 0, fee=0)  # Dummy tx
    blockchain.add_transaction(tx1)
    blockchain.mine_block("Alice")

    print(f"\nBalance Alice: {blockchain.get_balance('Alice')}")

    # Transaksi dengan fee
    print("\n--- Skenario 2: Transfer dengan fee ---")

    tx2 = Transaction("Alice", "Bob", 10, fee=0.5)
    tx3 = Transaction("Alice", "Charlie", 15, fee=0.3)

    blockchain.add_transaction(tx2)
    blockchain.add_transaction(tx3)

    # Bob mining block ini
    blockchain.mine_block("Bob")

    print("\n--- Balance setelah mining ---")
    for addr, balance in blockchain.get_all_balances().items():
        print(f"  {addr}: {balance}")

    # Lebih banyak transaksi
    print("\n--- Skenario 3: Multiple blocks ---")

    for i in range(3):
        tx = Transaction("Bob", "Diana", 2, fee=0.1)
        try:
            blockchain.add_transaction(tx)
        except ValueError as e:
            print(f"Error: {e}")
            break
        blockchain.mine_block("Charlie")

    # Validasi chain
    print("\n--- Validasi Blockchain ---")
    print(f"Blockchain valid: {blockchain.is_chain_valid()}")

    # Tampilkan merkle proof
    print("\n--- Merkle Proof Demo ---")
    last_block = blockchain.get_latest_block()
    if last_block.transactions:
        print(f"Verifikasi transaksi index 0: {last_block.verify_transaction(0)}")

    # Tampilkan seluruh chain
    blockchain.print_chain()

    # Final balances
    print("\n--- Final Balances ---")
    for addr, balance in blockchain.get_all_balances().items():
        print(f"  {addr}: {balance:.2f}")
```

---

## 7. Pengujian

### 7.1 Menguji Merkle Tree

```python
# test_merkle.py
from blockchain import MerkleTree, Transaction

# Buat beberapa transaksi
transactions = [
    Transaction("Alice", "Bob", 10),
    Transaction("Bob", "Charlie", 5),
    Transaction("Charlie", "Diana", 3),
    Transaction("Diana", "Eve", 2),
]

# Build Merkle Tree
merkle_root = MerkleTree.build_tree(transactions)
print(f"Merkle Root: {merkle_root}")

# Test Merkle Proof untuk transaksi ke-1 (Bob → Charlie)
tx_index = 1
tx = transactions[tx_index]
tx_hash = MerkleTree.hash(json.dumps(tx.to_dict(), sort_keys=True))
proof = MerkleTree.get_proof(transactions, tx_index)

print(f"\nMerkle Proof untuk transaksi #{tx_index}:")
for i, (hash_val, pos) in enumerate(proof):
    print(f"  Level {i}: {hash_val[:16]}... ({pos})")

# Verifikasi
is_valid = MerkleTree.verify_proof(tx_hash, proof, merkle_root)
print(f"\nProof valid: {is_valid}")
```

### 7.2 Menguji Mining Reward

```python
# test_reward.py
from blockchain import Blockchain, Transaction

bc = Blockchain()
bc.HALVING_INTERVAL = 3  # Halving setiap 3 block untuk testing

print("Block Rewards dengan Halving:")
for i in range(10):
    tx = Transaction("Test", "Test", 0)
    bc.add_transaction(tx)
    bc.mine_block("Miner")
    print(f"  Block #{len(bc.chain)-1}: Reward = {bc.get_block_reward()}")
```

### 7.3 Menguji Balance Tracking

```python
# test_balance.py
from blockchain import Blockchain, Transaction

bc = Blockchain()

# Mining awal untuk Alice
bc.add_transaction(Transaction("Alice", "Alice", 0))
bc.mine_block("Alice")

print(f"Alice awal: {bc.get_balance('Alice')}")

# Transfer
bc.add_transaction(Transaction("Alice", "Bob", 20, fee=1))
bc.mine_block("Charlie")

print(f"\nSetelah transfer:")
print(f"  Alice: {bc.get_balance('Alice')}")
print(f"  Bob: {bc.get_balance('Bob')}")
print(f"  Charlie: {bc.get_balance('Charlie')}")

# Coba transfer lebih dari saldo
try:
    bc.add_transaction(Transaction("Bob", "Diana", 100))
except ValueError as e:
    print(f"\nError (expected): {e}")
```

---

## Latihan

1. **Merkle Tree dengan transaksi ganjil**: Tambahkan 5 atau 7 transaksi dan verifikasi bahwa Merkle Tree tetap bekerja dengan benar.

2. **Implementasi Transaction Pool Limit**: Modifikasi mempool agar hanya menerima maksimal N transaksi. Transaksi dengan fee terendah akan dibuang jika mempool penuh.

3. **Visualisasi Merkle Tree**: Buat fungsi untuk menampilkan struktur Merkle Tree secara visual (ASCII art).

4. **Double Spending Prevention**: Tambahkan validasi untuk mencegah double spending - transaksi yang menggunakan saldo yang sudah dipakai di transaksi lain dalam mempool.

5. **Block Size Limit**: Implementasikan batasan ukuran block (maksimal N transaksi per block). Transaksi yang tidak muat akan tetap di mempool.

6. **Statistik Mining**: Buat fungsi untuk menampilkan statistik mining (total hash rate, rata-rata waktu per block, total coin yang sudah di-mining).
