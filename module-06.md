# Module 06. Advanced Cryptocurrency

## Deskripsi

Modul ini merupakan kelanjutan dari [Module 05](module-05.md) yang membahas topik-topik cryptocurrency tingkat lanjut. Pada modul ini, kita akan memperdalam implementasi cryptocurrency dengan fitur-fitur yang digunakan pada blockchain nyata seperti Bitcoin dan Ethereum.

Topik yang dibahas pada modul ini:

1. **Double Spending Prevention** - Mencegah penggunaan coin yang sama dua kali
2. **Transaction Broadcasting** - Menyebarkan transaksi ke seluruh jaringan
3. **Block Confirmation** - Tingkat keamanan transaksi berdasarkan jumlah konfirmasi
4. **UTXO Model** - Model transaksi yang digunakan Bitcoin
5. **ECDSA** - Algoritma signature yang lebih efisien dari RSA
6. **Address Format** - Format alamat Base58Check seperti Bitcoin
7. **HD Wallet** - Hierarchical Deterministic Wallet
8. **Mnemonic Phrase** - Recovery phrase 12/24 kata (BIP39)
9. **SPV (Light Client)** - Verifikasi transaksi tanpa full node

Berikut adalah [full code](advanced-crypto/cryptocurrency.py) yang dibahas pada modul ini.

## Prasyarat

Sebelum mempelajari modul ini, pastikan telah:

1. Memahami [Module 05 - Cryptocurrency](module-05.md)
2. Menginstall library yang diperlukan:
   ```bash
   pip install ecdsa base58 mnemonic
   ```

## List of Contents

- [Deskripsi](#deskripsi)
- [Prasyarat](#prasyarat)
- [List of Contents](#list-of-contents)
- [1. Double Spending Prevention](#1-double-spending-prevention)
  - [1.1 Apa itu Double Spending?](#11-apa-itu-double-spending)
  - [1.2 Cara Mencegah Double Spending](#12-cara-mencegah-double-spending)
  - [1.3 Implementasi](#13-implementasi)
- [2. Transaction Broadcasting](#2-transaction-broadcasting)
  - [2.1 Konsep Broadcasting](#21-konsep-broadcasting)
  - [2.2 Implementasi](#22-implementasi)
- [3. Block Confirmation](#3-block-confirmation)
  - [3.1 Apa itu Konfirmasi?](#31-apa-itu-konfirmasi)
  - [3.2 Berapa Konfirmasi yang Aman?](#32-berapa-konfirmasi-yang-aman)
  - [3.3 Implementasi](#33-implementasi)
- [4. UTXO Model](#4-utxo-model)
  - [4.1 UTXO vs Account Model](#41-utxo-vs-account-model)
  - [4.2 Cara Kerja UTXO](#42-cara-kerja-utxo)
  - [4.3 Implementasi](#43-implementasi)
- [5. ECDSA (Elliptic Curve Digital Signature)](#5-ecdsa-elliptic-curve-digital-signature)
  - [5.1 Mengapa ECDSA?](#51-mengapa-ecdsa)
  - [5.2 Cara Kerja ECDSA](#52-cara-kerja-ecdsa)
  - [5.3 Implementasi](#53-implementasi)
- [6. Address Format (Base58Check)](#6-address-format-base58check)
  - [6.1 Mengapa Base58?](#61-mengapa-base58)
  - [6.2 Struktur Address Bitcoin](#62-struktur-address-bitcoin)
  - [6.3 Implementasi](#63-implementasi)
- [7. HD Wallet (Hierarchical Deterministic)](#7-hd-wallet-hierarchical-deterministic)
  - [7.1 Apa itu HD Wallet?](#71-apa-itu-hd-wallet)
  - [7.2 Keuntungan HD Wallet](#72-keuntungan-hd-wallet)
  - [7.3 Derivation Path](#73-derivation-path)
  - [7.4 Implementasi](#74-implementasi)
- [8. Mnemonic Phrase (BIP39)](#8-mnemonic-phrase-bip39)
  - [8.1 Apa itu Mnemonic?](#81-apa-itu-mnemonic)
  - [8.2 Cara Kerja BIP39](#82-cara-kerja-bip39)
  - [8.3 Implementasi](#83-implementasi)
- [9. SPV (Simplified Payment Verification)](#9-spv-simplified-payment-verification)
  - [9.1 Apa itu SPV?](#91-apa-itu-spv)
  - [9.2 Cara Kerja SPV](#92-cara-kerja-spv)
  - [9.3 Implementasi](#93-implementasi)
- [10. Program Lengkap](#10-program-lengkap)
- [Latihan](#latihan)

## 1. Double Spending Prevention

### 1.1 Apa itu Double Spending?

**Double Spending** adalah upaya untuk menggunakan coin yang sama lebih dari satu kali. Ini adalah masalah fundamental dalam sistem uang digital.

```
Contoh Double Spending:

Alice memiliki 10 coin

Transaksi 1: Alice → Bob (10 coin)     ← valid
Transaksi 2: Alice → Charlie (10 coin) ← INVALID! coin sudah dipakai

Tanpa pencegahan, Alice bisa "mencetak uang" dengan mengirim
coin yang sama ke banyak orang.
```

### 1.2 Cara Mencegah Double Spending

Ada beberapa mekanisme pencegahan:

| Mekanisme | Penjelasan |
|-----------|------------|
| **UTXO Tracking** | Setiap coin dilacak sebagai output yang belum digunakan |
| **Mempool Validation** | Cek apakah input sudah digunakan di transaksi lain |
| **Blockchain Validation** | Cek apakah input sudah digunakan di block sebelumnya |
| **Confirmation** | Tunggu beberapa block untuk memastikan transaksi final |

### 1.3 Implementasi

```python
class DoubleSpendingPrevention:
    """
    Mencegah double spending dengan melacak UTXO yang sudah digunakan.
    """

    def __init__(self):
        self.spent_outputs = set()  # Set of (tx_hash, output_index)
        self.mempool_spent = set()  # Outputs yang dipakai di mempool

    def is_output_spent(self, tx_hash, output_index):
        """Cek apakah output sudah digunakan."""
        output_ref = (tx_hash, output_index)
        return output_ref in self.spent_outputs

    def is_output_in_mempool(self, tx_hash, output_index):
        """Cek apakah output sudah digunakan di mempool."""
        output_ref = (tx_hash, output_index)
        return output_ref in self.mempool_spent

    def validate_transaction(self, transaction, blockchain, mempool):
        """
        Validasi transaksi untuk mencegah double spending.
        Returns: (is_valid, error_message)
        """
        for inp in transaction.inputs:
            output_ref = (inp.tx_hash, inp.output_index)

            # Cek 1: Sudah spent di blockchain?
            if output_ref in self.spent_outputs:
                return False, f"Output {output_ref} sudah digunakan di blockchain"

            # Cek 2: Sudah dipakai di transaksi lain di mempool?
            if output_ref in self.mempool_spent:
                return False, f"Output {output_ref} sudah digunakan di mempool"

            # Cek 3: Apakah output benar-benar ada?
            if not self._output_exists(inp.tx_hash, inp.output_index, blockchain):
                return False, f"Output {output_ref} tidak ditemukan"

        return True, "Valid"

    def mark_as_spent(self, tx_hash, output_index):
        """Tandai output sebagai sudah digunakan (setelah block dikonfirmasi)."""
        self.spent_outputs.add((tx_hash, output_index))
        # Hapus dari mempool_spent jika ada
        self.mempool_spent.discard((tx_hash, output_index))

    def add_to_mempool(self, tx_hash, output_index):
        """Tandai output sebagai digunakan di mempool."""
        self.mempool_spent.add((tx_hash, output_index))

    def remove_from_mempool(self, tx_hash, output_index):
        """Hapus dari mempool (jika transaksi dibatalkan)."""
        self.mempool_spent.discard((tx_hash, output_index))

    def _output_exists(self, tx_hash, output_index, blockchain):
        """Cek apakah output ada di blockchain."""
        for block in blockchain.chain:
            for tx in block.transactions:
                if tx.hash == tx_hash:
                    if output_index < len(tx.outputs):
                        return True
        return False
```

## 2. Transaction Broadcasting

### 2.1 Konsep Broadcasting

Ketika user membuat transaksi, transaksi tersebut harus disebarkan ke seluruh node di jaringan agar bisa di-mining.

```
┌──────────┐     broadcast      ┌──────────┐
│  Node A  │ ─────────────────► │  Node B  │
│ (sender) │                    └────┬─────┘
└──────────┘                         │ broadcast
                                     ▼
┌──────────┐     broadcast      ┌──────────┐
│  Node D  │ ◄───────────────── │  Node C  │
└──────────┘                    └──────────┘

Transaksi menyebar ke seluruh jaringan dalam hitungan detik.
```

### 2.2 Implementasi

```python
import requests
from threading import Thread

class TransactionBroadcaster:
    """
    Menyebarkan transaksi ke seluruh node di jaringan.
    """

    def __init__(self, known_nodes):
        self.known_nodes = set(known_nodes)
        self.broadcast_timeout = 5  # seconds

    def broadcast_transaction(self, transaction):
        """
        Broadcast transaksi ke semua node yang dikenal.
        Menggunakan threading untuk broadcast paralel.
        """
        threads = []
        results = {}

        for node in self.known_nodes:
            thread = Thread(
                target=self._send_to_node,
                args=(node, transaction, results)
            )
            threads.append(thread)
            thread.start()

        # Tunggu semua thread selesai
        for thread in threads:
            thread.join(timeout=self.broadcast_timeout)

        # Hitung berapa node yang berhasil menerima
        success_count = sum(1 for v in results.values() if v)
        print(f"Broadcast ke {success_count}/{len(self.known_nodes)} node")

        return results

    def _send_to_node(self, node_url, transaction, results):
        """Kirim transaksi ke satu node."""
        try:
            response = requests.post(
                f"{node_url}/transactions/receive",
                json=transaction.to_dict(),
                timeout=self.broadcast_timeout
            )
            results[node_url] = response.status_code == 201
        except requests.exceptions.RequestException:
            results[node_url] = False

    def broadcast_block(self, block):
        """
        Broadcast block baru ke semua node.
        Dipanggil setelah miner berhasil mining.
        """
        threads = []
        results = {}

        for node in self.known_nodes:
            thread = Thread(
                target=self._send_block_to_node,
                args=(node, block, results)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join(timeout=self.broadcast_timeout)

        success_count = sum(1 for v in results.values() if v)
        print(f"Block broadcast ke {success_count}/{len(self.known_nodes)} node")

        return results

    def _send_block_to_node(self, node_url, block, results):
        """Kirim block ke satu node."""
        try:
            response = requests.post(
                f"{node_url}/blocks/receive",
                json=block.to_dict(),
                timeout=self.broadcast_timeout
            )
            results[node_url] = response.status_code == 201
        except requests.exceptions.RequestException:
            results[node_url] = False
```

## 3. Block Confirmation

### 3.1 Apa itu Konfirmasi?

**Konfirmasi** adalah jumlah block yang sudah ditambahkan setelah block yang berisi transaksi kita.

```
Block 100: [Tx A, Tx B, Tx C]  ← Transaksi kita di sini
Block 101: [...]               ← 1 konfirmasi
Block 102: [...]               ← 2 konfirmasi
Block 103: [...]               ← 3 konfirmasi
Block 104: [...]               ← 4 konfirmasi (current block)

Transaksi kita memiliki 4 konfirmasi.
```

### 3.2 Berapa Konfirmasi yang Aman?

| Konfirmasi | Keamanan | Use Case |
|------------|----------|----------|
| 0 (unconfirmed) | Sangat rendah | Tidak disarankan |
| 1 | Rendah | Transaksi kecil, instant |
| 3 | Sedang | Transaksi normal |
| 6 | Tinggi | Standar Bitcoin |
| 12+ | Sangat tinggi | Transaksi besar |

Semakin banyak konfirmasi, semakin sulit bagi attacker untuk melakukan **reorganisasi** (mengganti block dengan versi alternatif).

### 3.3 Implementasi

```python
class ConfirmationTracker:
    """
    Melacak jumlah konfirmasi untuk setiap transaksi.
    """

    def __init__(self, blockchain):
        self.blockchain = blockchain

    def get_confirmations(self, tx_hash):
        """
        Mendapatkan jumlah konfirmasi untuk transaksi.
        Returns: (confirmations, block_index) atau (0, None) jika tidak ditemukan
        """
        current_height = len(self.blockchain.chain) - 1

        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.hash == tx_hash:
                    confirmations = current_height - block.index + 1
                    return confirmations, block.index

        # Cek di mempool
        for tx in self.blockchain.mempool:
            if tx.hash == tx_hash:
                return 0, None  # Belum dikonfirmasi

        return -1, None  # Tidak ditemukan

    def is_confirmed(self, tx_hash, required_confirmations=6):
        """
        Cek apakah transaksi sudah memiliki cukup konfirmasi.
        """
        confirmations, _ = self.get_confirmations(tx_hash)
        return confirmations >= required_confirmations

    def get_confirmation_status(self, tx_hash):
        """
        Mendapatkan status konfirmasi yang human-readable.
        """
        confirmations, block_index = self.get_confirmations(tx_hash)

        if confirmations == -1:
            return "NOT_FOUND", "Transaksi tidak ditemukan"
        elif confirmations == 0:
            return "PENDING", "Menunggu di mempool"
        elif confirmations < 3:
            return "LOW", f"{confirmations} konfirmasi (risiko tinggi)"
        elif confirmations < 6:
            return "MEDIUM", f"{confirmations} konfirmasi (risiko sedang)"
        else:
            return "HIGH", f"{confirmations} konfirmasi (aman)"

    def wait_for_confirmation(self, tx_hash, required=6, timeout=600, check_interval=10):
        """
        Menunggu sampai transaksi mendapat konfirmasi yang cukup.
        """
        import time
        start_time = time.time()

        while time.time() - start_time < timeout:
            confirmations, _ = self.get_confirmations(tx_hash)

            if confirmations >= required:
                return True, confirmations

            print(f"Konfirmasi: {confirmations}/{required}, menunggu...")
            time.sleep(check_interval)

        return False, self.get_confirmations(tx_hash)[0]
```

## 4. UTXO Model

### 4.1 UTXO vs Account Model

| Aspek | UTXO (Bitcoin) | Account (Ethereum) |
|-------|----------------|-------------------|
| Konsep | Seperti uang kertas | Seperti rekening bank |
| Balance | Jumlah semua UTXO | Satu nilai saldo |
| Transaksi | Consume UTXO lama, create baru | Update saldo |
| Privacy | Lebih baik | Kurang |
| Parallelization | Lebih mudah | Lebih sulit |

### 4.2 Cara Kerja UTXO

```
=== Awal ===
Alice memiliki UTXO:
- UTXO #1: 30 coin (dari mining)
- UTXO #2: 20 coin (dari Bob)

=== Transaksi: Alice kirim 45 coin ke Charlie ===

Input:
- UTXO #1 (30 coin) ← akan di-consume
- UTXO #2 (20 coin) ← akan di-consume
Total: 50 coin

Output:
- 45 coin → Charlie (UTXO baru #3)
- 4 coin  → Alice   (UTXO baru #4, kembalian)
- 1 coin  → Fee     (untuk miner)
Total: 50 coin

=== Setelah Transaksi ===
Alice memiliki UTXO:
- UTXO #4: 4 coin (kembalian)

Charlie memiliki UTXO:
- UTXO #3: 45 coin
```

### 4.3 Implementasi

```python
import hashlib
import json
import time

class TransactionOutput:
    """Output dari transaksi (UTXO potensial)."""

    def __init__(self, recipient, amount):
        self.recipient = recipient
        self.amount = amount

    def to_dict(self):
        return {
            'recipient': self.recipient,
            'amount': self.amount
        }


class TransactionInput:
    """Input transaksi yang mereferensikan UTXO."""

    def __init__(self, tx_hash, output_index, signature=None):
        self.tx_hash = tx_hash          # Hash transaksi sumber
        self.output_index = output_index # Index output di transaksi sumber
        self.signature = signature       # Signature untuk membuktikan kepemilikan

    def to_dict(self):
        return {
            'tx_hash': self.tx_hash,
            'output_index': self.output_index,
            'signature': self.signature
        }


class UTXOTransaction:
    """Transaksi dengan model UTXO."""

    def __init__(self, inputs, outputs):
        self.inputs = inputs    # List of TransactionInput
        self.outputs = outputs  # List of TransactionOutput
        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        tx_data = {
            'inputs': [inp.to_dict() for inp in self.inputs],
            'outputs': [out.to_dict() for out in self.outputs],
            'timestamp': self.timestamp
        }
        tx_string = json.dumps(tx_data, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def to_dict(self):
        return {
            'hash': self.hash,
            'inputs': [inp.to_dict() for inp in self.inputs],
            'outputs': [out.to_dict() for out in self.outputs],
            'timestamp': self.timestamp
        }


class UTXOSet:
    """
    Mengelola set UTXO (Unspent Transaction Outputs).
    """

    def __init__(self):
        # Key: (tx_hash, output_index), Value: TransactionOutput
        self.utxos = {}

    def add_utxo(self, tx_hash, output_index, output):
        """Tambahkan UTXO baru."""
        key = (tx_hash, output_index)
        self.utxos[key] = output

    def remove_utxo(self, tx_hash, output_index):
        """Hapus UTXO (ketika di-spend)."""
        key = (tx_hash, output_index)
        if key in self.utxos:
            del self.utxos[key]
            return True
        return False

    def get_utxo(self, tx_hash, output_index):
        """Ambil UTXO tertentu."""
        key = (tx_hash, output_index)
        return self.utxos.get(key)

    def get_utxos_for_address(self, address):
        """Ambil semua UTXO milik address tertentu."""
        result = []
        for (tx_hash, output_index), output in self.utxos.items():
            if output.recipient == address:
                result.append({
                    'tx_hash': tx_hash,
                    'output_index': output_index,
                    'amount': output.amount
                })
        return result

    def get_balance(self, address):
        """Hitung total balance dari semua UTXO."""
        utxos = self.get_utxos_for_address(address)
        return sum(utxo['amount'] for utxo in utxos)

    def select_utxos_for_amount(self, address, amount):
        """
        Pilih UTXO untuk memenuhi jumlah tertentu.
        Returns: (selected_utxos, total_amount)
        """
        utxos = self.get_utxos_for_address(address)
        # Urutkan dari terkecil (untuk meminimalkan jumlah input)
        utxos.sort(key=lambda x: x['amount'])

        selected = []
        total = 0

        for utxo in utxos:
            selected.append(utxo)
            total += utxo['amount']
            if total >= amount:
                break

        if total < amount:
            return None, 0  # Saldo tidak cukup

        return selected, total

    def process_transaction(self, transaction):
        """
        Proses transaksi: hapus input UTXO, tambah output UTXO.
        """
        # Hapus UTXO yang digunakan sebagai input
        for inp in transaction.inputs:
            self.remove_utxo(inp.tx_hash, inp.output_index)

        # Tambah UTXO baru dari output
        for idx, out in enumerate(transaction.outputs):
            self.add_utxo(transaction.hash, idx, out)

    def create_transaction(self, sender, recipient, amount, fee=0):
        """
        Buat transaksi UTXO.
        """
        total_needed = amount + fee

        # Pilih UTXO
        selected_utxos, total_input = self.select_utxos_for_amount(sender, total_needed)

        if selected_utxos is None:
            raise ValueError(f"Saldo tidak cukup. Dibutuhkan: {total_needed}")

        # Buat inputs
        inputs = [
            TransactionInput(utxo['tx_hash'], utxo['output_index'])
            for utxo in selected_utxos
        ]

        # Buat outputs
        outputs = [TransactionOutput(recipient, amount)]

        # Kembalian (jika ada)
        change = total_input - total_needed
        if change > 0:
            outputs.append(TransactionOutput(sender, change))

        return UTXOTransaction(inputs, outputs)
```

## 5. ECDSA (Elliptic Curve Digital Signature)

### 5.1 Mengapa ECDSA?

| Aspek | RSA | ECDSA |
|-------|-----|-------|
| Key Size | 2048-4096 bit | 256 bit |
| Signature Size | ~256 bytes | ~64 bytes |
| Speed | Lebih lambat | Lebih cepat |
| Security | Sama untuk key yang setara | Sama |
| Digunakan oleh | TLS, Email | Bitcoin, Ethereum |

ECDSA memberikan keamanan yang sama dengan key yang jauh lebih kecil.

### 5.2 Cara Kerja ECDSA

```
1. Generate Key Pair
   - Private Key: angka random 256-bit
   - Public Key: titik pada kurva elliptic (private_key × G)

2. Signing
   - Hash message
   - Generate random k
   - Hitung r = (k × G).x mod n
   - Hitung s = k⁻¹(hash + r × private_key) mod n
   - Signature = (r, s)

3. Verification
   - Hitung w = s⁻¹ mod n
   - Hitung u1 = hash × w mod n
   - Hitung u2 = r × w mod n
   - Hitung point = u1×G + u2×PublicKey
   - Valid jika point.x == r
```

### 5.3 Implementasi

```python
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError
import hashlib

class ECDSAWallet:
    """
    Wallet menggunakan ECDSA (seperti Bitcoin/Ethereum).
    """

    def __init__(self, private_key=None):
        if private_key:
            self.private_key = SigningKey.from_string(
                bytes.fromhex(private_key),
                curve=SECP256k1
            )
        else:
            self.private_key = SigningKey.generate(curve=SECP256k1)

        self.public_key = self.private_key.get_verifying_key()

    def get_private_key_hex(self):
        """Mendapatkan private key dalam format hex."""
        return self.private_key.to_string().hex()

    def get_public_key_hex(self):
        """Mendapatkan public key dalam format hex."""
        return self.public_key.to_string().hex()

    def get_public_key_compressed(self):
        """
        Mendapatkan compressed public key (33 bytes).
        Format: prefix (02/03) + x coordinate
        """
        point = self.public_key.pubkey.point
        x = point.x()
        y = point.y()

        # Prefix: 02 jika y genap, 03 jika y ganjil
        prefix = '02' if y % 2 == 0 else '03'

        # X coordinate dalam 32 bytes
        x_hex = format(x, '064x')

        return prefix + x_hex

    def sign(self, message):
        """
        Menandatangani message.
        Returns: signature dalam format hex
        """
        if isinstance(message, str):
            message = message.encode()

        # Hash message terlebih dahulu
        message_hash = hashlib.sha256(message).digest()

        # Sign
        signature = self.private_key.sign(message_hash)

        return signature.hex()

    @staticmethod
    def verify(public_key_hex, message, signature_hex):
        """
        Memverifikasi signature.
        Returns: True jika valid
        """
        try:
            public_key = VerifyingKey.from_string(
                bytes.fromhex(public_key_hex),
                curve=SECP256k1
            )

            if isinstance(message, str):
                message = message.encode()

            message_hash = hashlib.sha256(message).digest()
            signature = bytes.fromhex(signature_hex)

            return public_key.verify(signature, message_hash)

        except BadSignatureError:
            return False
        except Exception as e:
            print(f"Verification error: {e}")
            return False

    def get_address(self):
        """
        Generate address dari public key.
        Simplified version (real Bitcoin uses more steps).
        """
        pubkey_bytes = self.public_key.to_string()
        sha256_hash = hashlib.sha256(pubkey_bytes).digest()
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        return ripemd160_hash.hex()
```

## 6. Address Format (Base58Check)

### 6.1 Mengapa Base58?

Base58 menghilangkan karakter yang membingungkan:
- `0` (nol) dan `O` (huruf O)
- `I` (huruf I) dan `l` (huruf L)
- `+` dan `/` (tidak URL-safe)

```
Base64: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
Base58: 123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz
```

### 6.2 Struktur Address Bitcoin

```
┌─────────┬────────────────────────────────────┬──────────┐
│ Version │           Public Key Hash          │ Checksum │
│ 1 byte  │              20 bytes              │ 4 bytes  │
└─────────┴────────────────────────────────────┴──────────┘

Version bytes:
- 0x00: Bitcoin Mainnet (address dimulai dengan '1')
- 0x05: Bitcoin P2SH (address dimulai dengan '3')
- 0x6f: Bitcoin Testnet (address dimulai dengan 'm' atau 'n')
```

### 6.3 Implementasi

```python
import base58
import hashlib

class AddressGenerator:
    """
    Generate dan validasi address format Base58Check.
    """

    # Version bytes
    MAINNET_PUBKEY = b'\x00'    # '1...'
    MAINNET_SCRIPT = b'\x05'   # '3...'
    TESTNET_PUBKEY = b'\x6f'   # 'm...' atau 'n...'

    @staticmethod
    def hash160(data):
        """SHA256 followed by RIPEMD160."""
        sha256_hash = hashlib.sha256(data).digest()
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        return ripemd160_hash

    @staticmethod
    def checksum(data):
        """Double SHA256, ambil 4 byte pertama."""
        first_hash = hashlib.sha256(data).digest()
        second_hash = hashlib.sha256(first_hash).digest()
        return second_hash[:4]

    @classmethod
    def public_key_to_address(cls, public_key_hex, version=None):
        """
        Convert public key ke address Base58Check.
        """
        if version is None:
            version = cls.MAINNET_PUBKEY

        # 1. Hash public key (Hash160)
        public_key_bytes = bytes.fromhex(public_key_hex)
        pubkey_hash = cls.hash160(public_key_bytes)

        # 2. Tambah version byte di depan
        versioned = version + pubkey_hash

        # 3. Hitung checksum
        check = cls.checksum(versioned)

        # 4. Gabungkan dan encode Base58
        address_bytes = versioned + check
        address = base58.b58encode(address_bytes).decode()

        return address

    @classmethod
    def validate_address(cls, address):
        """
        Validasi address Base58Check.
        Returns: (is_valid, version, pubkey_hash)
        """
        try:
            # Decode Base58
            decoded = base58.b58decode(address)

            # Minimal 25 bytes (1 version + 20 hash + 4 checksum)
            if len(decoded) != 25:
                return False, None, None

            # Pisahkan komponen
            version = decoded[0:1]
            pubkey_hash = decoded[1:21]
            checksum = decoded[21:25]

            # Verifikasi checksum
            expected_checksum = cls.checksum(decoded[:21])
            if checksum != expected_checksum:
                return False, None, None

            return True, version.hex(), pubkey_hash.hex()

        except Exception:
            return False, None, None

    @classmethod
    def get_address_type(cls, address):
        """Mendapatkan tipe address."""
        is_valid, version, _ = cls.validate_address(address)

        if not is_valid:
            return "INVALID"

        version_byte = bytes.fromhex(version)

        if version_byte == cls.MAINNET_PUBKEY:
            return "MAINNET_P2PKH"
        elif version_byte == cls.MAINNET_SCRIPT:
            return "MAINNET_P2SH"
        elif version_byte == cls.TESTNET_PUBKEY:
            return "TESTNET_P2PKH"
        else:
            return "UNKNOWN"
```

## 7. HD Wallet (Hierarchical Deterministic)

### 7.1 Apa itu HD Wallet?

**HD Wallet** adalah wallet yang dapat generate banyak keypair dari satu **seed**. Semua address bisa di-recover hanya dengan satu master seed.

```
                    Master Seed
                        │
                  Master Key (m)
                 /      │      \
               m/0     m/1     m/2      ← Account level
              / │ \
         m/0/0 m/0/1 m/0/2              ← Address level

Setiap cabang adalah keypair yang valid!
```

### 7.2 Keuntungan HD Wallet

| Keuntungan | Penjelasan |
|------------|------------|
| **Single Backup** | Hanya perlu backup seed sekali |
| **Privacy** | Bisa generate address baru untuk setiap transaksi |
| **Organization** | Bisa pisahkan akun (personal, bisnis, dll) |
| **Security** | Bisa share public key tanpa expose private key |

### 7.3 Derivation Path

Format standar (BIP44): `m / purpose' / coin_type' / account' / change / address_index`

```
m/44'/0'/0'/0/0  ← Bitcoin, Account 0, External, Address 0
m/44'/0'/0'/0/1  ← Bitcoin, Account 0, External, Address 1
m/44'/0'/0'/1/0  ← Bitcoin, Account 0, Internal (change), Address 0
m/44'/60'/0'/0/0 ← Ethereum, Account 0, Address 0
```

### 7.4 Implementasi

```python
import hashlib
import hmac
from ecdsa import SigningKey, SECP256k1

class HDWallet:
    """
    Simplified HD Wallet implementation.
    """

    def __init__(self, seed):
        """
        Initialize HD Wallet dari seed bytes.
        """
        self.seed = seed

        # Generate master key menggunakan HMAC-SHA512
        I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()

        # 32 bytes pertama = master private key
        # 32 bytes terakhir = master chain code
        self.master_private_key = I[:32]
        self.master_chain_code = I[32:]

        # Generate master public key
        self.master_public_key = self._private_to_public(self.master_private_key)

    def _private_to_public(self, private_key_bytes):
        """Convert private key ke public key."""
        sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
        vk = sk.get_verifying_key()
        return vk.to_string()

    def derive_child(self, index, hardened=False):
        """
        Derive child key pada index tertentu.
        Hardened derivation menggunakan index >= 0x80000000
        """
        if hardened:
            index += 0x80000000

        if index >= 0x80000000:
            # Hardened: gunakan private key
            data = b'\x00' + self.master_private_key + index.to_bytes(4, 'big')
        else:
            # Normal: gunakan public key
            data = self.master_public_key + index.to_bytes(4, 'big')

        I = hmac.new(self.master_chain_code, data, hashlib.sha512).digest()

        # Child private key = (IL + parent_private_key) mod n
        IL = int.from_bytes(I[:32], 'big')
        parent_key = int.from_bytes(self.master_private_key, 'big')

        # Order of the curve
        n = SECP256k1.order

        child_key_int = (IL + parent_key) % n
        child_private_key = child_key_int.to_bytes(32, 'big')
        child_chain_code = I[32:]

        return child_private_key, child_chain_code

    def derive_path(self, path):
        """
        Derive key dari path string (e.g., "m/44'/0'/0'/0/0").
        """
        if not path.startswith('m'):
            raise ValueError("Path harus dimulai dengan 'm'")

        current_private = self.master_private_key
        current_chain = self.master_chain_code

        # Parse path
        parts = path.split('/')[1:]  # Skip 'm'

        for part in parts:
            hardened = part.endswith("'")
            index = int(part.rstrip("'"))

            if hardened:
                index += 0x80000000

            # Derive
            if index >= 0x80000000:
                data = b'\x00' + current_private + index.to_bytes(4, 'big')
            else:
                current_public = self._private_to_public(current_private)
                data = current_public + index.to_bytes(4, 'big')

            I = hmac.new(current_chain, data, hashlib.sha512).digest()

            IL = int.from_bytes(I[:32], 'big')
            parent_key = int.from_bytes(current_private, 'big')
            n = SECP256k1.order

            child_key_int = (IL + parent_key) % n
            current_private = child_key_int.to_bytes(32, 'big')
            current_chain = I[32:]

        return current_private, self._private_to_public(current_private)

    def get_address_at_path(self, path):
        """
        Generate address pada path tertentu.
        """
        private_key, public_key = self.derive_path(path)

        # Generate address
        pubkey_hash = AddressGenerator.hash160(public_key)
        versioned = b'\x00' + pubkey_hash
        checksum = AddressGenerator.checksum(versioned)
        address = base58.b58encode(versioned + checksum).decode()

        return {
            'path': path,
            'private_key': private_key.hex(),
            'public_key': public_key.hex(),
            'address': address
        }

    def generate_addresses(self, count=5, account=0):
        """
        Generate beberapa address untuk account tertentu.
        """
        addresses = []
        for i in range(count):
            path = f"m/44'/0'/{account}'/0/{i}"
            addr_info = self.get_address_at_path(path)
            addresses.append(addr_info)
        return addresses
```

## 8. Mnemonic Phrase (BIP39)

### 8.1 Apa itu Mnemonic?

**Mnemonic phrase** adalah 12-24 kata yang merepresentasikan seed wallet. Lebih mudah diingat dan ditulis daripada hex string.

```
Contoh 12-word mnemonic:
"abandon ability able about above absent absorb abstract absurd abuse access accident"

Merepresentasikan seed 128-bit yang bisa generate unlimited addresses.
```

### 8.2 Cara Kerja BIP39

```
1. Generate Entropy (128-256 bit random)
         │
         ▼
2. Add Checksum (4-8 bit dari SHA256)
         │
         ▼
3. Split menjadi 11-bit segments
         │
         ▼
4. Map setiap segment ke word (dari wordlist 2048 kata)
         │
         ▼
5. Mnemonic → Seed (menggunakan PBKDF2)
         │
         ▼
6. Seed → Master Key (BIP32)
```

### 8.3 Implementasi

```python
from mnemonic import Mnemonic
import hashlib

class MnemonicWallet:
    """
    Wallet dengan BIP39 mnemonic phrase.
    """

    def __init__(self, language='english'):
        self.mnemo = Mnemonic(language)

    def generate_mnemonic(self, strength=128):
        """
        Generate mnemonic baru.
        strength: 128 (12 words), 160 (15), 192 (18), 224 (21), 256 (24)
        """
        return self.mnemo.generate(strength)

    def validate_mnemonic(self, mnemonic):
        """Validasi mnemonic phrase."""
        return self.mnemo.check(mnemonic)

    def mnemonic_to_seed(self, mnemonic, passphrase=""):
        """
        Convert mnemonic ke seed (64 bytes).
        Passphrase opsional untuk keamanan tambahan.
        """
        return self.mnemo.to_seed(mnemonic, passphrase)

    def create_wallet(self, mnemonic=None, passphrase=""):
        """
        Buat wallet lengkap dari mnemonic.
        """
        if mnemonic is None:
            mnemonic = self.generate_mnemonic()

        if not self.validate_mnemonic(mnemonic):
            raise ValueError("Mnemonic tidak valid")

        seed = self.mnemonic_to_seed(mnemonic, passphrase)
        hd_wallet = HDWallet(seed)

        return {
            'mnemonic': mnemonic,
            'seed': seed.hex(),
            'master_private_key': hd_wallet.master_private_key.hex(),
            'addresses': hd_wallet.generate_addresses(5)
        }

    def recover_wallet(self, mnemonic, passphrase=""):
        """
        Recover wallet dari mnemonic phrase.
        """
        return self.create_wallet(mnemonic, passphrase)


# Contoh penggunaan
def demo_mnemonic():
    wallet = MnemonicWallet()

    # Generate wallet baru
    print("=== Generate Wallet Baru ===")
    new_wallet = wallet.create_wallet()
    print(f"Mnemonic: {new_wallet['mnemonic']}")
    print(f"Seed: {new_wallet['seed'][:32]}...")
    print(f"\nAddresses:")
    for addr in new_wallet['addresses']:
        print(f"  {addr['path']}: {addr['address']}")

    # Recovery test
    print("\n=== Recovery Wallet ===")
    recovered = wallet.recover_wallet(new_wallet['mnemonic'])
    print(f"Recovered addresses match: {recovered['addresses'] == new_wallet['addresses']}")
```

---

## 9. SPV (Simplified Payment Verification)

### 9.1 Apa itu SPV?

**SPV** memungkinkan verifikasi transaksi tanpa mengunduh seluruh blockchain. SPV client hanya menyimpan **block headers** (~80 bytes per block vs MB per block).

```
Full Node:                    SPV Client:
┌─────────────────────┐      ┌─────────────────────┐
│ Block Header        │      │ Block Header        │
│ - Previous Hash     │      │ - Previous Hash     │
│ - Merkle Root       │      │ - Merkle Root       │
│ - Timestamp         │      │ - Timestamp         │
│ - Nonce             │      │ - Nonce             │
├─────────────────────┤      └─────────────────────┘
│ Transaction 1       │
│ Transaction 2       │      Hanya simpan headers!
│ Transaction 3       │      (80 bytes vs megabytes)
│ ...                 │
│ Transaction N       │
└─────────────────────┘
```

### 9.2 Cara Kerja SPV

```
1. SPV client minta block headers dari full node
2. Client minta Merkle proof untuk transaksi tertentu
3. Client verifikasi:
   - Merkle proof valid (transaksi ada di block)
   - Block header valid (hash correct, difficulty met)
   - Block ada di longest chain

Tidak perlu download seluruh transaksi!
```

### 9.3 Implementasi

```python
class BlockHeader:
    """Block header untuk SPV."""

    def __init__(self, index, previous_hash, merkle_root, timestamp, nonce, difficulty):
        self.index = index
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.nonce = nonce
        self.difficulty = difficulty
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        header_data = f"{self.index}{self.previous_hash}{self.merkle_root}{self.timestamp}{self.nonce}"
        return hashlib.sha256(header_data.encode()).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_root,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'difficulty': self.difficulty,
            'hash': self.hash
        }


class SPVClient:
    """
    Simplified Payment Verification client.
    Hanya menyimpan block headers, tidak full blocks.
    """

    def __init__(self):
        self.headers = []  # List of BlockHeader
        self.known_transactions = {}  # tx_hash -> confirmation info

    def sync_headers(self, full_node_url):
        """
        Sinkronisasi headers dari full node.
        """
        try:
            response = requests.get(f"{full_node_url}/headers")
            if response.status_code == 200:
                headers_data = response.json()['headers']
                self.headers = [
                    BlockHeader(
                        h['index'], h['previous_hash'], h['merkle_root'],
                        h['timestamp'], h['nonce'], h['difficulty']
                    )
                    for h in headers_data
                ]
                print(f"Synced {len(self.headers)} headers")
                return True
        except Exception as e:
            print(f"Sync error: {e}")
        return False

    def verify_transaction(self, tx_hash, full_node_url):
        """
        Verifikasi transaksi menggunakan Merkle proof.
        """
        # Minta Merkle proof dari full node
        try:
            response = requests.get(
                f"{full_node_url}/merkle-proof/{tx_hash}"
            )
            if response.status_code != 200:
                return False, "Transaksi tidak ditemukan"

            data = response.json()
            block_index = data['block_index']
            merkle_proof = data['proof']
            tx_data = data['transaction']

        except Exception as e:
            return False, f"Error: {e}"

        # Verifikasi 1: Block ada di chain kita
        if block_index >= len(self.headers):
            return False, "Block belum di-sync"

        header = self.headers[block_index]

        # Verifikasi 2: Merkle proof valid
        tx_hash_bytes = hashlib.sha256(
            json.dumps(tx_data, sort_keys=True).encode()
        ).hexdigest()

        if not self._verify_merkle_proof(tx_hash_bytes, merkle_proof, header.merkle_root):
            return False, "Merkle proof tidak valid"

        # Verifikasi 3: Hitung konfirmasi
        confirmations = len(self.headers) - block_index

        return True, f"Valid dengan {confirmations} konfirmasi"

    def _verify_merkle_proof(self, tx_hash, proof, merkle_root):
        """
        Verifikasi Merkle proof.
        """
        current_hash = tx_hash

        for sibling_hash, position in proof:
            if position == 'left':
                combined = sibling_hash + current_hash
            else:
                combined = current_hash + sibling_hash
            current_hash = hashlib.sha256(combined.encode()).hexdigest()

        return current_hash == merkle_root

    def get_balance(self, address, full_node_url):
        """
        Dapatkan balance address (memerlukan bantuan full node).
        SPV tidak bisa hitung sendiri karena tidak punya semua transaksi.
        """
        try:
            response = requests.get(f"{full_node_url}/balance/{address}")
            if response.status_code == 200:
                return response.json()['balance']
        except Exception:
            pass
        return None

    def watch_transaction(self, tx_hash, required_confirmations=6):
        """
        Watch transaksi sampai mendapat konfirmasi yang cukup.
        """
        self.known_transactions[tx_hash] = {
            'required': required_confirmations,
            'confirmed': False
        }

    def check_watched_transactions(self, full_node_url):
        """
        Cek status transaksi yang di-watch.
        """
        results = {}

        for tx_hash, info in self.known_transactions.items():
            if info['confirmed']:
                results[tx_hash] = "Already confirmed"
                continue

            is_valid, message = self.verify_transaction(tx_hash, full_node_url)

            if is_valid:
                # Parse konfirmasi dari message
                confirmations = int(message.split()[2])
                if confirmations >= info['required']:
                    info['confirmed'] = True
                    results[tx_hash] = f"Confirmed! ({confirmations} confirmations)"
                else:
                    results[tx_hash] = f"Pending ({confirmations}/{info['required']})"
            else:
                results[tx_hash] = f"Invalid: {message}"

        return results
```


## 10. Program Lengkap

```python
# cryptocurrency.py - Program lengkap menggabungkan semua konsep

if __name__ == "__main__":
    print("=" * 60)
    print("ADVANCED CRYPTOCURRENCY DEMO")
    print("=" * 60)

    # 1. Mnemonic Wallet
    print("\n--- 1. Generate Mnemonic Wallet ---")
    mnemonic_wallet = MnemonicWallet()
    wallet_data = mnemonic_wallet.create_wallet()
    print(f"Mnemonic: {wallet_data['mnemonic']}")
    print(f"First address: {wallet_data['addresses'][0]['address']}")

    # 2. ECDSA Signing
    print("\n--- 2. ECDSA Signing ---")
    ecdsa_wallet = ECDSAWallet()
    message = "Transfer 10 BTC to Alice"
    signature = ecdsa_wallet.sign(message)
    print(f"Message: {message}")
    print(f"Signature: {signature[:32]}...")

    is_valid = ECDSAWallet.verify(
        ecdsa_wallet.get_public_key_hex(),
        message,
        signature
    )
    print(f"Signature valid: {is_valid}")

    # 3. Address Generation
    print("\n--- 3. Address Format ---")
    address = AddressGenerator.public_key_to_address(
        ecdsa_wallet.get_public_key_hex()
    )
    print(f"Address: {address}")
    is_valid, version, _ = AddressGenerator.validate_address(address)
    print(f"Valid: {is_valid}, Type: {AddressGenerator.get_address_type(address)}")

    # 4. UTXO Demo
    print("\n--- 4. UTXO Model ---")
    utxo_set = UTXOSet()

    # Simulasi coinbase (mining reward)
    coinbase_output = TransactionOutput("Alice", 50)
    utxo_set.add_utxo("genesis", 0, coinbase_output)
    print(f"Alice balance: {utxo_set.get_balance('Alice')}")

    # Buat transaksi
    try:
        tx = utxo_set.create_transaction("Alice", "Bob", 30, fee=1)
        utxo_set.process_transaction(tx)
        print(f"\nSetelah transfer 30 ke Bob:")
        print(f"Alice balance: {utxo_set.get_balance('Alice')}")
        print(f"Bob balance: {utxo_set.get_balance('Bob')}")
    except ValueError as e:
        print(f"Error: {e}")

    # 5. Double Spending Check
    print("\n--- 5. Double Spending Prevention ---")
    ds_prevention = DoubleSpendingPrevention()
    ds_prevention.mark_as_spent("genesis", 0)
    print(f"Output (genesis, 0) spent: {ds_prevention.is_output_spent('genesis', 0)}")

    print("\n" + "=" * 60)
    print("Demo selesai!")
    print("=" * 60)
```

## Latihan

1. **Multi-signature Wallet**: Implementasikan wallet yang membutuhkan 2-of-3 signature untuk mengirim transaksi.

2. **Transaction Fee Estimation**: Buat fungsi yang mengestimasi fee berdasarkan ukuran transaksi dan kondisi mempool.

3. **Address Watch**: Implementasikan fitur untuk memantau address tertentu dan mendapat notifikasi ketika ada transaksi masuk.

4. **Wallet Encryption**: Tambahkan fitur enkripsi untuk menyimpan private key dengan password.

5. **Transaction History**: Buat fungsi untuk menampilkan riwayat transaksi lengkap dari sebuah address.

6. **HD Wallet dengan Multiple Accounts**: Extend HD Wallet untuk mendukung beberapa account dengan label (personal, business, savings).
