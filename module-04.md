# Module 04. Blockchain Network dengan Flask API

## Deskripsi

Modul ini membahas bagaimana blockchain beroperasi dalam sebuah jaringan terdesentralisasi. Selain memahami konsep jaringan P2P (Peer-to-Peer), mahasiswa akan mengimplementasikan sebuah node blockchain yang dapat berkomunikasi dengan node lain melalui REST API menggunakan Flask.

Topik yang dibahas pada modul ini:

1. **Blockchain Network** – Konsep jaringan blockchain terdesentralisasi
2. **REST API Node** – Pembangunan API node blockchain menggunakan Flask
3. **Node Registration** – Registrasi dan penemuan node dalam jaringan
4. **Multi-Node Simulation** – Simulasi beberapa node pada satu mesin dengan port berbeda
5. **Consensus Algorithm** – Mekanisme sinkronisasi chain dengan memilih rantai valid terpanjang

## Prasyarat

Sebelum mempelajari modul ini, mahasiswa sebaiknya:

1. [Menginstall Python dan Visual Studio Code](module-01.md)
2. Memahami [konsep dasar blockchain](module-02.md)
3. Memahami dasar REST API dan HTTP method (GET, POST)

Install dependensi yang dibutuhkan:

```bash
pip install flask requests
```

## List of Contents

- [Deskripsi](#deskripsi)
- [Prasyarat](#prasyarat)
- [List of Contents](#list-of-contents)
- [1. Teori Dasar Blockchain Network](#1-teori-dasar-blockchain-network)
  - [1.1 Apa itu Jaringan Blockchain?](#11-apa-itu-jaringan-blockchain)
  - [1.2 Peer-to-Peer (P2P) Network](#12-peer-to-peer-p2p-network)
  - [1.3 Apa itu Node?](#13-apa-itu-node)
  - [1.4 REST API sebagai Antarmuka Node](#14-rest-api-sebagai-antarmuka-node)
  - [1.5 Algoritma Consensus](#15-algoritma-consensus)
  - [1.6 Longest Chain Rule](#16-longest-chain-rule)
- [2. Implementasi Program](#2-implementasi-program)
  - [2.1 Struktur Proyek](#21-struktur-proyek)
  - [2.2 Class Transaction dan Block](#22-class-transaction-dan-block)
  - [2.3 Class Blockchain dengan Node Registry](#23-class-blockchain-dengan-node-registry)
  - [2.4 Mengganti Chain (replace_chain)](#24-mengganti-chain-replace_chain)
  - [2.5 Inisialisasi Flask App](#25-inisialisasi-flask-app)
  - [2.6 Endpoint GET /chain](#26-endpoint-get-chain)
  - [2.7 Endpoint POST /transactions/new](#27-endpoint-post-transactionsnew)
  - [2.8 Endpoint GET /mine](#28-endpoint-get-mine)
  - [2.9 Endpoint POST /nodes/register](#29-endpoint-post-nodesregister)
  - [2.10 Endpoint GET /nodes/resolve](#210-endpoint-get-nodesresolve)
  - [2.11 Menjalankan Multi-Node](#211-menjalankan-multi-node)
- [3. Pengujian dengan Postman](#3-pengujian-dengan-postman)
  - [3.1 Tambah Transaksi](#31-tambah-transaksi)
  - [3.2 Mining Block](#32-mining-block)
  - [3.3 Registrasi Node](#33-registrasi-node)
  - [3.4 Resolve Consensus](#34-resolve-consensus)
- [Latihan](#latihan)

## 1. Teori Dasar Blockchain Network

### 1.1 Apa itu Jaringan Blockchain?

Blockchain tidak berjalan pada satu komputer tunggal. Ia beroperasi pada sebuah **jaringan terdesentralisasi** yang terdiri dari banyak komputer (node) yang masing-masing menyimpan salinan penuh dari blockchain.

Tidak ada server pusat. Setiap node setara dan dapat bergabung atau meninggalkan jaringan kapan saja. Inilah yang membuat blockchain bersifat **desentralisasi** dan tahan terhadap kegagalan tunggal (_single point of failure_).

```
Node A ──── Node B
  │    ╲  ╱    │
  │     ╲╱     │
  │     ╱╲     │
  │   ╱    ╲   │
Node D ──── Node C
```

### 1.2 Peer-to-Peer (P2P) Network

Dalam jaringan P2P, setiap node:

- Menyimpan salinan blockchain secara lokal
- Dapat menerima dan menyebarkan transaksi baru
- Dapat melakukan mining
- Berkomunikasi langsung dengan node lain tanpa perantara

Berbeda dengan arsitektur client-server tradisional di mana ada satu server yang melayani banyak client, dalam P2P setiap mahasiswa adalah sekaligus client dan server.

| Arsitektur      | Client-Server           | P2P (Blockchain)     |
| --------------- | ----------------------- | -------------------- |
| Kendali         | Terpusat                | Terdesentralisasi    |
| Titik kegagalan | Single point of failure | Tidak ada            |
| Kepercayaan     | Percaya pada server     | Verifikasi matematis |
| Skalabilitas    | Terbatas                | Horizontal           |

### 1.3 Apa itu Node?

**Node** adalah setiap komputer yang berpartisipasi dalam jaringan blockchain. Dalam implementasi modul ini, setiap node adalah sebuah aplikasi Flask yang berjalan pada port tertentu.

Jenis-jenis node dalam blockchain nyata:

- **Full Node**: menyimpan seluruh salinan blockchain, memvalidasi semua transaksi
- **Mining Node**: full node yang juga melakukan proses mining
- **Light Node**: hanya menyimpan header block, bergantung pada full node untuk data lengkap

Dalam modul ini kita mengimplementasikan **mining node** — setiap node dapat menambahkan transaksi, mining, dan memvalidasi chain.

### 1.4 REST API sebagai Antarmuka Node

Untuk mensimulasikan komunikasi antar-node, kita menggunakan **REST API** dengan Flask. Setiap node membuka beberapa endpoint HTTP yang dapat diakses oleh node lain maupun pengguna (melalui Postman atau browser).

| Method | Endpoint                  | Fungsi                                 |
| ------ | ------------------------- | -------------------------------------- |
| GET    | `/chain`                | Mengambil seluruh blockchain           |
| POST   | `/transactions/new`     | Menambahkan transaksi baru             |
| GET    | `/transactions/pending` | Melihat transaksi yang belum di-mining |
| GET    | `/mine`                 | Mining block baru                      |
| POST   | `/nodes/register`       | Mendaftarkan node lain                 |
| GET    | `/nodes`                | Melihat daftar node yang terdaftar     |
| GET    | `/nodes/resolve`        | Menjalankan algoritma consensus        |

### 1.5 Algoritma Consensus

**Consensus** adalah kesepakatan seluruh node dalam jaringan tentang keadaan blockchain yang sah. Tanpa consensus, setiap node bisa memiliki versi blockchain yang berbeda-beda, dan tidak ada yang tahu mana yang benar.

Masalah yang dipecahkan consensus:

- node A dan node B melakukan mining hampir bersamaan, menghasilkan block berbeda
- node mana yang harus diikuti?

### 1.6 Longest Chain Rule

Aturan yang paling sederhana dan umum digunakan adalah **Longest Chain Rule** (digunakan juga oleh Bitcoin):

> **Chain yang paling panjang dianggap sebagai chain yang sah.**

Alasannya: chain yang lebih panjang merepresentasikan lebih banyak pekerjaan komputasi (Proof of Work) yang telah dilakukan, sehingga lebih sulit untuk dimanipulasi.

```
node A: [Genesis] → [Block 1] → [Block 2] → [Block 3]  ← PEMENANG (4 block)
node B: [Genesis] → [Block 1] → [Block 2]               (3 block)
node C: [Genesis] → [Block 1] → [Block 2] → [Block 3]  ← PEMENANG (4 block)
```

Jika node B menerima chain dari node A atau C, node B akan mengganti chain lokalnya.

## 2. Implementasi Program

### 2.1 Struktur Proyek

```
blockchain-network/
├── blockchain.py   # Class Transaction, Block, Blockchain
└── app.py          # Flask REST API (node)
```

Setiap node menjalankan `app.py` pada port yang berbeda:

```bash
python app.py 5000   # node 1
python app.py 5001   # node 2
python app.py 5002   # node 3
```

### 2.2 Class Transaction dan Block

Class `Transaction` dan `Block` serupa dengan modul sebelumnya, dengan tambahan metode `to_dict()` yang penting untuk serialisasi data ke format JSON saat berkomunikasi antar-node melalui HTTP.

```python
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
```

```python
class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty):
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }
```

### 2.3 Class Blockchain dengan Node Registry

Blockchain kini memiliki atribut `nodes` — sebuah `set` yang menyimpan alamat node-node yang dikenal dalam jaringan.

```python
class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = difficulty
        self.mining_reward = 10
        self.nodes = set()
        self._create_genesis_block()

    def register_node(self, address):
        self.nodes.add(address)
```

Menggunakan `set` (bukan `list`) memastikan tidak ada duplikat node yang terdaftar.

### 2.4 Mengganti Chain (replace_chain)

Metode `replace_chain` adalah inti dari algoritma consensus. Node akan mengganti chain lokalnya jika chain dari jaringan lebih panjang dan valid.

```python
def replace_chain(self, new_chain_data):
    if len(new_chain_data) <= len(self.chain):
        return False

    new_chain = []
    for block_data in new_chain_data:
        txs = [
            Transaction(tx['sender'], tx['receiver'], tx['amount'])
            for tx in block_data['transactions']
        ]
        block = Block(
            index=block_data['index'],
            transactions=txs,
            previous_hash=block_data['previous_hash'],
            nonce=block_data['nonce']
        )
        block.timestamp = block_data['timestamp']
        block.hash = block_data['hash']
        new_chain.append(block)

    for i in range(1, len(new_chain)):
        current = new_chain[i]
        previous = new_chain[i - 1]
        if current.previous_hash != previous.hash:
            return False

    self.chain = new_chain
    return True
```

Langkah-langkah:

1. Jika chain baru tidak lebih panjang → tolak
2. Rekonstruksi objek `Block` dari data JSON yang diterima
3. Validasi keterkaitan setiap block (previous_hash)
4. Jika valid → ganti chain lokal

### 2.5 Inisialisasi Flask App

```python
from flask import Flask, jsonify, request
from blockchain import Blockchain, Transaction
import requests

app = Flask(__name__)
blockchain = Blockchain(difficulty=2)
node_identifier = 'node-default'
```

`node_identifier` digunakan sebagai alamat penerima _mining reward_ — setiap node mendapatkan reward ketika berhasil mining block.

### 2.6 Endpoint GET /chain

```python
@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({
        'chain': [block.to_dict() for block in blockchain.chain],
        'length': len(blockchain.chain)
    }), 200
```

Mengembalikan seluruh isi blockchain dalam format JSON. Endpoint ini digunakan oleh node lain saat menjalankan algoritma consensus untuk membandingkan panjang chain.

### 2.7 Endpoint POST /transactions/new

```python
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    data = request.get_json()
    required = ['sender', 'receiver', 'amount']

    if not all(k in data for k in required):
        return jsonify({'message': 'Data tidak lengkap'}), 400

    tx = Transaction(data['sender'], data['receiver'], data['amount'])
    blockchain.add_transaction(tx)

    return jsonify({
        'message': f"Transaksi akan ditambahkan ke block #{len(blockchain.chain)}"
    }), 201
```

Menerima data transaksi dalam format JSON via body request. Validasi memastikan ketiga field (`sender`, `receiver`, `amount`) tersedia.

### 2.8 Endpoint GET /mine

```python
@app.route('/mine', methods=['GET'])
def mine():
    if not blockchain.pending_transactions:
        return jsonify({'message': 'Tidak ada transaksi untuk di-mining'}), 400

    block = blockchain.mine_pending_transactions(miner_address=node_identifier)

    return jsonify({
        'message': 'Block baru berhasil di-mining!',
        'block': block.to_dict()
    }), 200
```

Memicu proses mining. Node yang mining mendapatkan _mining reward_ secara otomatis (ditambahkan sebagai transaksi `SYSTEM → node_identifier`).

### 2.9 Endpoint POST /nodes/register

```python
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    data = request.get_json()
    nodes = data.get('nodes')

    if not nodes:
        return jsonify({'message': 'Daftar node tidak boleh kosong'}), 400

    for node in nodes:
        blockchain.register_node(node)

    return jsonify({
        'message': f'{len(nodes)} node berhasil didaftarkan',
        'total_nodes': list(blockchain.nodes)
    }), 201
```

Mendaftarkan satu atau beberapa node ke dalam registry. Contoh body request:

```json
{
  "nodes": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]
}
```

### 2.10 Endpoint GET /nodes/resolve

```python
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = False
    longest_chain = None
    max_length = len(blockchain.chain)

    for node in blockchain.nodes:
        try:
            response = requests.get(f'{node}/chain', timeout=3)
            if response.status_code == 200:
                data = response.json()
                length = data['length']
                chain = data['chain']

                if length > max_length:
                    max_length = length
                    longest_chain = chain
        except requests.exceptions.RequestException:
            continue

    if longest_chain:
        replaced = blockchain.replace_chain(longest_chain)

    if replaced:
        return jsonify({
            'message': 'Chain lokal diganti dengan chain terpanjang dari jaringan',
            'chain': [block.to_dict() for block in blockchain.chain]
        }), 200
    else:
        return jsonify({
            'message': 'Chain lokal sudah yang terpanjang, tidak ada perubahan',
            'chain': [block.to_dict() for block in blockchain.chain]
        }), 200
```

Alur kerja consensus:

1. Iterasi setiap node yang terdaftar
2. Ambil chain dari masing-masing node via `GET /chain`
3. Jika ada chain yang lebih panjang, catat sebagai kandidat
4. Setelah semua node diperiksa, ganti chain lokal jika ada kandidat yang lebih panjang

### 2.11 Menjalankan Multi-Node

Buka **3 terminal terpisah** dan jalankan masing-masing:

```bash
# terminal 1 - node 1 (port 5000)
python app.py 5000

# terminal 2 - node 2 (port 5001)
python app.py 5001

# terminal 3 - node 3 (port 5002)
python app.py 5002
```

Setiap terminal merepresentasikan satu node dalam jaringan.

---

## 3. Pengujian dengan Postman

### 3.1 Tambah Transaksi

Kirim transaksi ke node 1 (port 5000):

**Request:**

```
POST http://127.0.0.1:5000/transactions/new
Content-Type: application/json

{
    "sender": "Alice",
    "receiver": "Bob",
    "amount": 50
}
```

**Response:**

```json
{
  "message": "Transaksi akan ditambahkan ke block #1"
}
```

### 3.2 Mining Block

Mining di node 1 setelah menambahkan transaksi:

**Request:**

```
GET http://127.0.0.1:5000/mine
```

**Response:**

```json
{
  "message": "Block baru berhasil di-mining!",
  "block": {
    "index": 1,
    "hash": "00a3f...",
    "previous_hash": "00b1c...",
    "transactions": [
      { "sender": "Alice", "receiver": "Bob", "amount": 50 },
      { "sender": "SYSTEM", "receiver": "node-5000", "amount": 10 }
    ],
    "nonce": 142
  }
}
```

> Node 1 mendapatkan mining reward sebesar 10 dari `SYSTEM`.

### 3.3 Registrasi Node

Daftarkan node 2 dan node 3 ke dalam registry node 1:

**Request:**

```
POST http://127.0.0.1:5000/nodes/register
Content-Type: application/json

{
    "nodes": [
        "http://127.0.0.1:5001",
        "http://127.0.0.1:5002"
    ]
}
```

**Response:**

```json
{
  "message": "2 node berhasil didaftarkan",
  "total_nodes": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]
}
```

### 3.4 Resolve Consensus

node 2 (yang belum memiliki block hasil mining) meminta consensus:

**Request:**

```
GET http://127.0.0.1:5001/nodes/resolve
```

Jika node 2 belum mendaftarkan node 1, daftarkan dulu:

```
POST http://127.0.0.1:5001/nodes/register
Content-Type: application/json

{
    "nodes": ["http://127.0.0.1:5000"]
}
```

Kemudian resolve:

```
GET http://127.0.0.1:5001/nodes/resolve
```

**Response (chain diganti):**

```json
{
    "message": "Chain lokal diganti dengan chain terpanjang dari jaringan",
    "chain": [
        { "index": 0, "hash": "00b1c...", ... },
        { "index": 1, "hash": "00a3f...", ... }
    ]
}
```

node 2 kini memiliki chain yang sama dengan node 1.

## Latihan

1. **Simulasi**: Jalankan 2 node, tambahkan transaksi berbeda di masing-masing node, lalu mining di keduanya secara bersamaan. Amati apa yang terjadi saat resolve consensus dijalankan.
2. **Broadcast Transaksi**: Modifikasi endpoint `POST /transactions/new` agar secara otomatis menyebarkan (broadcast) transaksi baru ke semua node yang terdaftar.
3. **Sinkronisasi Otomatis**: Modifikasi endpoint `GET /mine` agar setelah mining berhasil, node secara otomatis mengirimkan block baru ke semua node yang terdaftar (tanpa menunggu `resolve`).
4. **Node Discovery**: Implementasikan mekanisme agar ketika node A mendaftarkan node B, node B juga otomatis mengetahui keberadaan node A (two-way registration).
