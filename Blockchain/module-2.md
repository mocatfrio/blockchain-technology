# Module 2: Implementasi Blockchain dengan Mining Sederhana

## Tujuan Pembelajaran

Setelah praktikum ini, mahasiswa mampu:

* Memahami **struktur block dan transaction**
* Mengimplementasikan **hashing**
* Mengimplementasikan **Proof of Work (mining)**
* Mengelola **transaction pool**
* Memverifikasi **validitas blockchain**

# Bagian 1 — Setup Environment

Install:

* Visual Studio Code
* Python

Buat folder project:

```
blockchain-simulation

```

File utama:

```
blockchain.py
```

# Bagian 2 — Import Library

```python
import hashlib
import datetime
import json
```

# Bagian 3 — Struktur Transaction

Tambahkan class  **Transaction** .

```python
class Transaction:

    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount
        }
```

Contoh transaksi:

```
Alice → Bob : 10
Bob → Charlie : 5
```

# Bagian 4 — Struktur Block

Block sekarang berisi:

* index
* timestamp
* transactions
* nonce
* previous hash
* hash

```python
class Block:

    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [t.to_dict() for t in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)

        return hashlib.sha256(block_string.encode()).hexdigest()
```

---

# Bagian 5 — Proof of Work (Mining)

Tambahkan fungsi mining.

Difficulty = jumlah  **leading zero pada hash** .

```python
def mine_block(self, difficulty):
    while self.hash[:difficulty] != "0" * difficulty:
        self.nonce += 1
        self.hash = self.calculate_hash()
    print("Block mined:", self.hash)
```

Tambahkan fungsi ini di dalam class  **Block** .

# Bagian 6 — Struktur Blockchain

```python
class Blockchain:

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 3
```

Genesis block:

```python
def create_genesis_block(self):
    return Block(0, [], "0")
```

Ambil block terakhir:

```python
def get_latest_block(self):
    return self.chain[-1]
```

# Bagian 7 — Menambahkan Transaction

```python
def add_transaction(self, transaction):
    self.pending_transactions.append(transaction)
```

---

# Bagian 8 — Mining Block

```python
def mine_pending_transactions(self):
    block = Block(
        len(self.chain),
        self.pending_transactions,
        self.get_latest_block().hash
    )
    block.mine_block(self.difficulty)
    self.chain.append(block)
    self.pending_transactions = []
```

---

# Bagian 9 — Validasi Blockchain

```python
def is_chain_valid(self):

    for i in range(1, len(self.chain)):
        current = self.chain[i]
        previous = self.chain[i - 1]

        if current.hash != current.calculate_hash():
            return False

        if current.previous_hash != previous.hash:
            return False

    return True
```

---

# Bagian 10 — Simulasi Blockchain

Tambahkan kode utama.

```python
my_blockchain = Blockchain()

my_blockchain.add_transaction(Transaction("Alice", "Bob", 10))
my_blockchain.add_transaction(Transaction("Bob", "Charlie", 5))

print("Mining block...")
my_blockchain.mine_pending_transactions()

my_blockchain.add_transaction(Transaction("Charlie", "Alice", 3))

print("Mining block...")
my_blockchain.mine_pending_transactions()

print("Blockchain valid?", my_blockchain.is_chain_valid())
```

---

# Output yang Diharapkan

```
Mining block...
Block mined: 000a8f13e...

Mining block...
Block mined: 000d23a4b...

Blockchain valid? True
```

Mahasiswa akan melihat:

* **mining process**
* **nonce berubah**
* **hash memenuhi difficulty**

# Eksperimen (Untuk Diskusi)

Minta mahasiswa mencoba:

### 1️⃣ Mengubah transaksi

```
my_blockchain.chain[1].transactions[0].amount = 1000
```

Cek kembali validitas chain.

### 2️⃣ Mengubah difficulty

```
difficulty = 4
```

Bandingkan waktu mining.

### 3️⃣ Menambah mining reward

Tambahkan transaksi:

```
MINER → reward
```

# Class Participation Questions

1. Mengapa mining membutuhkan  **nonce** ?
2. Mengapa difficulty mempengaruhi waktu mining?
3. Mengapa perubahan satu transaksi merusak blockchain?

# Skill yang Dipelajari Mahasiswa

Mahasiswa akan memahami secara praktis:

* Block structure
* Transaction structure
* Hashing
* Proof of Work
* Mining
* Blockchain validation
