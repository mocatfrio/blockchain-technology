# Project 1: Blockchain & Cryptocurrency Simulation

## Informasi Umum

| Item | Detail |
|------|--------|
| **Nama Project** | Simulasi Blockchain & Cryptocurrency |
| **Modul Terkait** | Module 01-06 |
| **Minggu Demo** | Minggu 7 |
| **Bobot Nilai** | 40% |
| **Tipe** | Kelompok (2-3 orang) |

---

## Deskripsi

Pada project ini, mahasiswa akan mengembangkan **simulasi blockchain** lengkap dengan fitur **cryptocurrency** menggunakan **Python**. Project ini mengintegrasikan semua konsep dari Module 01-06:

- Struktur data blockchain (Module 02)
- Proof of Work & mining (Module 03)
- Network & API (Module 04)
- Digital signature & wallet (Module 05)
- Transaksi cryptocurrency (Module 06)

---

## Tujuan Pembelajaran

Setelah menyelesaikan project ini, mahasiswa mampu:

1. Mengimplementasikan struktur data blockchain (block, chain, hash)
2. Mengimplementasikan mekanisme konsensus Proof of Work
3. Membangun API untuk simulasi multi-node
4. Mengimplementasikan wallet dengan digital signature
5. Membangun sistem transaksi cryptocurrency yang aman

---

## Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BLOCKCHAIN & CRYPTOCURRENCY SYSTEM                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                         WALLET LAYER                             │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │    │
│  │  │   Wallet A  │    │   Wallet B  │    │   Wallet C  │          │    │
│  │  │ private_key │    │ private_key │    │ private_key │          │    │
│  │  │ public_key  │    │ public_key  │    │ public_key  │          │    │
│  │  │ address     │    │ address     │    │ address     │          │    │
│  │  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘          │    │
│  └─────────┼──────────────────┼──────────────────┼──────────────────┘    │
│            │                  │                  │                       │
│            ▼                  ▼                  ▼                       │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                      TRANSACTION LAYER                           │    │
│  │                                                                  │    │
│  │   Transaction {                                                  │    │
│  │     sender: public_key,                                          │    │
│  │     recipient: address,                                          │    │
│  │     amount: value,                                               │    │
│  │     signature: sign(private_key, data)                           │    │
│  │   }                                                              │    │
│  │                                                                  │    │
│  │   - Sign transaction dengan private key                         │    │
│  │   - Verify signature dengan public key                          │    │
│  │   - Check balance sebelum transfer                               │    │
│  │   - Prevent double-spending                                      │    │
│  │                                                                  │    │
│  └──────────────────────────────┬───────────────────────────────────┘    │
│                                 │                                        │
│                                 ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                       BLOCKCHAIN LAYER                           │    │
│  │                                                                  │    │
│  │   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │    │
│  │   │ Block 0 │───►│ Block 1 │───►│ Block 2 │───►│ Block 3 │      │    │
│  │   │ Genesis │    │         │    │         │    │         │      │    │
│  │   └─────────┘    └─────────┘    └─────────┘    └─────────┘      │    │
│  │                                                                  │    │
│  │   Block {                                                        │    │
│  │     index, timestamp, transactions[], proof, previous_hash      │    │
│  │   }                                                              │    │
│  │                                                                  │    │
│  │   - Proof of Work (mining)                                       │    │
│  │   - Chain validation                                             │    │
│  │   - Consensus (longest chain)                                    │    │
│  │                                                                  │    │
│  └──────────────────────────────┬───────────────────────────────────┘    │
│                                 │                                        │
│                                 ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                        NETWORK LAYER                             │    │
│  │                                                                  │    │
│  │   Node 1 (localhost:5000)  ◄────►  Node 2 (localhost:5001)      │    │
│  │              │                              │                    │    │
│  │              └──────────┬───────────────────┘                    │    │
│  │                         │                                        │    │
│  │                         ▼                                        │    │
│  │              Node 3 (localhost:5002)                             │    │
│  │                                                                  │    │
│  │   API Endpoints:                                                 │    │
│  │   - POST /transactions/new                                       │    │
│  │   - GET  /mine                                                   │    │
│  │   - GET  /chain                                                  │    │
│  │   - POST /nodes/register                                         │    │
│  │   - GET  /nodes/resolve                                          │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Fitur Wajib

### Bagian A: Blockchain Foundation (Module 01-04)

| No | Fitur | Deskripsi | Modul |
|----|-------|-----------|-------|
| 1 | **Block Structure** | index, timestamp, transactions, proof, previous_hash | 02 |
| 2 | **Hashing** | SHA-256 untuk block hash | 02 |
| 3 | **Chain Validation** | Validasi integritas seluruh chain | 02 |
| 4 | **Proof of Work** | Mining dengan difficulty (leading zeros) | 03 |
| 5 | **Genesis Block** | Block pertama dengan previous_hash = "0" | 02 |
| 6 | **Flask API** | REST API untuk interaksi | 04 |
| 7 | **Multi-Node** | Register dan sync antar node | 04 |
| 8 | **Consensus** | Longest chain rule | 04 |

### Bagian B: Cryptocurrency (Module 05-06)

| No | Fitur | Deskripsi | Modul |
|----|-------|-----------|-------|
| 9 | **Wallet** | Generate private/public key pair | 05 |
| 10 | **Digital Signature** | Sign transaksi dengan private key | 05 |
| 11 | **Verification** | Verify signature dengan public key | 05 |
| 12 | **Balance Tracking** | Hitung saldo berdasarkan transaksi | 06 |
| 13 | **Transfer** | Kirim "coin" antar wallet | 06 |
| 14 | **Double-Spending Prevention** | Cegah penggunaan coin ganda | 06 |
| 15 | **Mining Reward** | Reward untuk miner | 03, 06 |

---

## Fitur Bonus (Opsional)

| No | Fitur | Deskripsi | Poin |
|----|-------|-----------|------|
| 1 | **Merkle Tree** | Merkle root untuk transaksi dalam block | +5 |
| 2 | **Difficulty Adjustment** | Adjust difficulty berdasarkan waktu mining | +5 |
| 3 | **Transaction Fee** | Fee untuk setiap transaksi | +3 |
| 4 | **UTXO Model** | Unspent Transaction Output tracking | +5 |
| 5 | **Address Format** | Format address seperti Bitcoin (Base58) | +3 |
| 6 | **Mempool** | Pending transactions pool | +3 |
| 7 | **Block Explorer** | Simple web UI untuk view chain | +5 |

---

## Struktur Project

```
project-blockchain-crypto/
├── blockchain/
│   ├── __init__.py
│   ├── blockchain.py       # Class Blockchain
│   ├── block.py            # Class Block
│   └── proof_of_work.py    # Mining logic
├── wallet/
│   ├── __init__.py
│   ├── wallet.py           # Class Wallet (keypair)
│   └── transaction.py      # Class Transaction (sign/verify)
├── network/
│   ├── __init__.py
│   └── node.py             # Flask API
├── tests/
│   ├── test_blockchain.py
│   ├── test_wallet.py
│   └── test_transaction.py
├── app.py                  # Main entry point
├── requirements.txt
└── README.md
```

---

## Spesifikasi Teknis

### Class Blockchain

```python
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.nodes = set()
        self.create_genesis_block()

    def create_genesis_block(self) -> Block
    def add_block(self, proof: int, previous_hash: str) -> Block
    def add_transaction(self, transaction: Transaction) -> int
    def proof_of_work(self, previous_proof: int) -> int
    def hash(self, block: Block) -> str
    def is_chain_valid(self, chain: list) -> bool
    def register_node(self, address: str) -> None
    def resolve_conflicts(self) -> bool
    def get_balance(self, address: str) -> float
```

### Class Wallet

```python
class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.address = None
        self.generate_keys()

    def generate_keys(self) -> None
    def sign(self, data: str) -> str
    def get_address(self) -> str
```

### Class Transaction

```python
class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.signature = None

    def sign(self, private_key) -> None
    def verify(self) -> bool
    def to_dict(self) -> dict
```

### API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/chain` | Mendapatkan seluruh blockchain |
| GET | `/mine` | Mining block baru |
| POST | `/transactions/new` | Membuat transaksi baru |
| GET | `/balance/<address>` | Mendapatkan saldo address |
| POST | `/wallet/new` | Membuat wallet baru |
| POST | `/nodes/register` | Register node baru |
| GET | `/nodes/resolve` | Consensus - resolve conflicts |

### Contoh Request/Response

**POST /transactions/new**

Request:
```json
{
  "sender": "04a1b2c3...",
  "recipient": "04d4e5f6...",
  "amount": 10,
  "signature": "3045022100..."
}
```

Response:
```json
{
  "message": "Transaction akan ditambahkan ke Block 5"
}
```

**GET /balance/04a1b2c3...**

Response:
```json
{
  "address": "04a1b2c3...",
  "balance": 50.0
}
```

---

## Skenario Testing

### Test Blockchain

| No | Test Case | Expected Result |
|----|-----------|-----------------|
| 1 | Create genesis block | Block dengan index=0, previous_hash="0" |
| 2 | Add new block | Chain length bertambah |
| 3 | Validate chain | Return True untuk chain valid |
| 4 | Tamper block | Validation return False |
| 5 | Proof of Work | Hash memenuhi difficulty |

### Test Wallet & Transaction

| No | Test Case | Expected Result |
|----|-----------|-----------------|
| 6 | Generate wallet | Private/public key generated |
| 7 | Sign transaction | Signature tidak kosong |
| 8 | Verify valid signature | Return True |
| 9 | Verify invalid signature | Return False |
| 10 | Transfer with sufficient balance | Transaction accepted |
| 11 | Transfer with insufficient balance | Transaction rejected |
| 12 | Double-spending attempt | Second transaction rejected |

### Test Network

| No | Test Case | Expected Result |
|----|-----------|-----------------|
| 13 | Register node | Node ditambahkan ke set |
| 14 | Sync chain (shorter) | Chain tidak berubah |
| 15 | Sync chain (longer valid) | Chain di-replace |

---

## Deliverables

### 1. Source Code (GitHub Repository)

- [ ] Folder `blockchain/` - Core blockchain logic
- [ ] Folder `wallet/` - Wallet dan transaction
- [ ] Folder `network/` - Flask API
- [ ] Folder `tests/` - Unit tests
- [ ] `app.py` - Main application
- [ ] `requirements.txt` - Dependencies
- [ ] `README.md` - Dokumentasi

### 2. README.md

```markdown
# Nama Project - Blockchain & Cryptocurrency

## Anggota Kelompok
- Nama 1 (NRP)
- Nama 2 (NRP)

## Deskripsi
[Penjelasan singkat project]

## Fitur
- [x] Block structure dengan SHA-256 hashing
- [x] Proof of Work mining
- [x] Chain validation
- [x] Multi-node network
- [x] Wallet dengan digital signature
- [x] Cryptocurrency transfer
- [x] Balance tracking
- [x] Double-spending prevention

## Cara Menjalankan

### Prerequisites
- Python 3.8+
- pip

### Installation
pip install -r requirements.txt

### Run Single Node
python app.py --port 5000

### Run Multiple Nodes
python app.py --port 5000
python app.py --port 5001
python app.py --port 5002

## API Documentation
[Dokumentasi endpoint]

## Screenshot Demo
[Screenshot bukti demo]
```

### 3. Demo Skenario

Saat presentasi, demonstrasikan:

| No | Skenario | Langkah |
|----|----------|---------|
| 1 | **Setup** | Jalankan 2-3 node |
| 2 | **Create Wallets** | Buat 2 wallet (Alice, Bob) |
| 3 | **Mining** | Mine beberapa block untuk dapat reward |
| 4 | **Transfer** | Alice transfer ke Bob |
| 5 | **Verify** | Cek balance Alice & Bob |
| 6 | **Invalid Transfer** | Coba transfer melebihi balance |
| 7 | **Sync** | Tunjukkan consensus antar node |
| 8 | **Tampering** | Coba ubah data, tunjukkan validation gagal |

---

## Rubrik Penilaian

| Komponen | Bobot | Kriteria |
|----------|-------|----------|
| **Blockchain Core** | 25% | Block, chain, hash, PoW, validation |
| **Cryptocurrency** | 25% | Wallet, signature, transfer, balance |
| **Network** | 15% | API, multi-node, consensus |
| **Testing** | 15% | Unit test, minimal 10 test cases |
| **Dokumentasi** | 10% | README lengkap, kode terdokumentasi |
| **Demo** | 10% | Presentasi jelas, demo lancar |

### Detail Penilaian

| Nilai | Kriteria |
|-------|----------|
| A (90-100) | Semua fitur wajib + 3 bonus, demo lancar |
| B (80-89) | Semua fitur wajib, demo lancar |
| C (70-79) | 80% fitur wajib, minor bugs |
| D (60-69) | 60% fitur wajib, beberapa bugs |
| E (<60) | Kurang dari 60% fitur |

---

## Timeline

| Minggu | Aktivitas | Fokus |
|--------|-----------|-------|
| 1 | Setup environment | Python, VS Code |
| 2 | Blockchain structure | Block, chain, hash |
| 3 | Mining & PoW | Proof of Work, difficulty |
| 4 | Network | Flask API, multi-node |
| 5 | Wallet | Private/public key, signature |
| 6 | Cryptocurrency | Transaction, balance, security |
| **7** | **DEMO** | Presentasi project |

---

## Tips Pengerjaan

### Do's ✅

1. **Mulai dari modul** - Ikuti step-by-step di Module 02-06
2. **Test setiap komponen** - Jangan tunggu selesai semua baru test
3. **Commit sering** - Backup progress ke Git
4. **Gunakan Postman** - Untuk test API endpoints
5. **Print debug** - Tambahkan print untuk tracing

### Don'ts ❌

1. **Jangan skip validation** - Chain validation penting
2. **Jangan hardcode** - Gunakan parameter/config
3. **Jangan abaikan edge cases** - Balance negatif, invalid signature
4. **Jangan copy tanpa paham** - Pahami setiap fungsi
5. **Jangan tunggu deadline** - Mulai dari minggu 2

---

## FAQ

### Q: Harus pakai library crypto tertentu?
**A:** Bebas, bisa pakai `cryptography`, `pycryptodome`, atau `ecdsa`. Yang penting fungsi sign/verify bekerja.

### Q: Boleh pakai database?
**A:** Boleh untuk bonus (persistence), tapi tidak wajib. In-memory sudah cukup.

### Q: Berapa node minimum untuk demo?
**A:** Minimal 2 node untuk menunjukkan consensus.

### Q: Harus pakai RSA atau ECDSA?
**A:** Bebas. RSA lebih mudah dipahami, ECDSA lebih mirip Bitcoin.

### Q: Apakah perlu frontend?
**A:** Tidak wajib. Bisa demo via Postman atau curl.

---

## Referensi

- [Module 02 - Blockchain Fundamentals](../module-02.md)
- [Module 03 - Advanced Blockchain Concepts](../module-03.md)
- [Module 04 - Blockchain Network](../module-04.md)
- [Module 05 - Cryptocurrency](../module-05.md)
- [Module 06 - Advanced Cryptocurrency](../module-06.md)
- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## Submission

### Deadline
**Minggu 7** (sesuai jadwal demo)

### Cara Submit
1. Push semua kode ke GitHub repository
2. Pastikan repository **public** atau invite dosen
3. Siapkan demo untuk presentasi
4. Kumpulkan link repository

### Format Nama Repository
```
blockchain-project1-[nama-kelompok]
```

Contoh: `blockchain-project1-team-alpha`
