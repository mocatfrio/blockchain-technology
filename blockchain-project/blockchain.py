import hashlib
import json
import time
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import base64


class Wallet:
    """
    Wallet menyimpan keypair (private key dan public key) untuk user.
    - Private key digunakan untuk menandatangani transaksi
    - Public key digunakan untuk memverifikasi signature dan sebagai identitas
    """

    def __init__(self):
        # Generate RSA key pair dengan ukuran 2048 bit
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def get_public_key_string(self):
        """Mengubah public key menjadi string format PEM untuk identifikasi"""
        public_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return public_bytes.decode('utf-8')

    def get_address(self):
        """Membuat address dari hash public key (40 karakter hex)"""
        public_key_string = self.get_public_key_string()
        return hashlib.sha256(public_key_string.encode()).hexdigest()[:40]

    def sign(self, message):
        """Menandatangani pesan dengan private key menggunakan RSA + SHA256"""
        message_bytes = message.encode('utf-8')
        signature = self.private_key.sign(
            message_bytes,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        # Encode ke base64 agar bisa disimpan sebagai string
        return base64.b64encode(signature).decode('utf-8')

    def to_dict(self):
        return {
            'address': self.get_address(),
            'public_key': self.get_public_key_string()
        }


class Transaction:
    """
    Transaction merepresentasikan transfer coin antar wallet.
    Setiap transaksi harus ditandatangani oleh pengirim.
    """

    def __init__(self, sender_address, sender_public_key, receiver_address, amount):
        self.sender_address = sender_address
        self.sender_public_key = sender_public_key
        self.receiver_address = receiver_address
        self.amount = amount
        self.timestamp = time.time()
        self.signature = None

    def to_dict(self, include_signature=True):
        """Mengubah transaksi ke dictionary"""
        data = {
            'sender_address': self.sender_address,
            'sender_public_key': self.sender_public_key,
            'receiver_address': self.receiver_address,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
        if include_signature and self.signature:
            data['signature'] = self.signature
        return data

    def calculate_hash(self):
        """Hash dari data transaksi (tanpa signature)"""
        tx_string = json.dumps(self.to_dict(include_signature=False), sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def sign_transaction(self, wallet):
        """Menandatangani transaksi dengan wallet pengirim"""
        if wallet.get_address() != self.sender_address:
            raise Exception("Anda tidak bisa menandatangani transaksi untuk wallet lain!")

        tx_hash = self.calculate_hash()
        self.signature = wallet.sign(tx_hash)

    def is_valid(self):
        """Memverifikasi signature transaksi"""
        # Transaksi dari SYSTEM (mining reward) tidak perlu signature
        if self.sender_address == "SYSTEM":
            return True

        if not self.signature:
            print("Transaksi tidak memiliki signature!")
            return False

        try:
            # Reconstruct public key dari string PEM
            public_key = serialization.load_pem_public_key(
                self.sender_public_key.encode('utf-8'),
                backend=default_backend()
            )

            # Decode signature dari base64
            signature_bytes = base64.b64decode(self.signature)

            # Verify signature
            tx_hash = self.calculate_hash()
            public_key.verify(
                signature_bytes,
                tx_hash.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            print("Signature tidak valid!")
            return False
        except Exception as e:
            print(f"Error verifikasi: {e}")
            return False


class Block:
    """
    Block menyimpan sekumpulan transaksi dan metadata.
    Setiap block terhubung ke block sebelumnya melalui previous_hash.
    """

    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Menghitung hash block menggunakan SHA-256"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty):
        """Mining block dengan Proof of Work"""
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash

    def has_valid_transactions(self):
        """Memverifikasi semua transaksi dalam block"""
        for tx in self.transactions:
            if not tx.is_valid():
                return False
        return True

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }


class Blockchain:
    """
    Blockchain adalah rangkaian block yang terhubung.
    Menyediakan fungsi untuk menambah transaksi, mining, validasi, dan consensus.
    """

    def __init__(self, difficulty=3):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = difficulty
        self.mining_reward = 10  # Reward untuk miner
        self.nodes = set()  # Daftar node dalam jaringan
        self._create_genesis_block()

    def _create_genesis_block(self):
        """Membuat block pertama (genesis block)"""
        genesis = Block(0, [], '0')
        genesis.mine(self.difficulty)
        self.chain.append(genesis)

    def get_last_block(self):
        """Mengambil block terakhir dalam chain"""
        return self.chain[-1]

    def add_transaction(self, transaction):
        """Menambahkan transaksi ke pending transactions"""
        # Validasi transaksi (kecuali dari SYSTEM)
        if transaction.sender_address != "SYSTEM":
            if not transaction.is_valid():
                raise Exception("Transaksi tidak valid! Signature tidak cocok.")

        self.pending_transactions.append(transaction)
        return len(self.chain)

    def mine_pending_transactions(self, miner_address):
        """Mining semua pending transactions dan memberikan reward ke miner"""
        # Buat transaksi reward untuk miner (Coinbase Transaction)
        reward_tx = Transaction(
            sender_address="SYSTEM",
            sender_public_key="",
            receiver_address=miner_address,
            amount=self.mining_reward
        )
        self.pending_transactions.insert(0, reward_tx)  # Coinbase tx di awal

        # Buat block baru
        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_last_block().hash
        )

        # Mining
        print(f"Mining block #{block.index}...")
        block.mine(self.difficulty)
        print(f"Block #{block.index} berhasil di-mining: {block.hash[:16]}...")

        # Tambahkan ke chain
        self.chain.append(block)

        # Reset pending transactions
        self.pending_transactions = []

        return block

    def get_balance(self, address):
        """Menghitung saldo dari sebuah address"""
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender_address == address:
                    balance -= tx.amount
                if tx.receiver_address == address:
                    balance += tx.amount
        return balance

    def is_chain_valid(self):
        """Memvalidasi keseluruhan blockchain"""
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

            # Cek semua transaksi dalam block
            if not current.has_valid_transactions():
                print(f"Transaksi dalam block #{current.index} tidak valid!")
                return False

        return True

    # === Multi-Node Functions ===

    def register_node(self, address):
        """Mendaftarkan node baru ke jaringan"""
        self.nodes.add(address)

    def replace_chain(self, new_chain_data):
        """Mengganti chain lokal dengan chain baru yang lebih panjang"""
        if len(new_chain_data) <= len(self.chain):
            return False

        # Reconstruct chain dari data
        new_chain = []
        for block_data in new_chain_data:
            transactions = []
            for tx_data in block_data['transactions']:
                tx = Transaction(
                    sender_address=tx_data['sender_address'],
                    sender_public_key=tx_data.get('sender_public_key', ''),
                    receiver_address=tx_data['receiver_address'],
                    amount=tx_data['amount']
                )
                tx.timestamp = tx_data['timestamp']
                tx.signature = tx_data.get('signature')
                transactions.append(tx)

            block = Block(
                index=block_data['index'],
                transactions=transactions,
                previous_hash=block_data['previous_hash'],
                nonce=block_data['nonce']
            )
            block.timestamp = block_data['timestamp']
            block.hash = block_data['hash']
            new_chain.append(block)

        # Validasi chain baru
        for i in range(1, len(new_chain)):
            current = new_chain[i]
            previous = new_chain[i - 1]
            if current.previous_hash != previous.hash:
                return False

        self.chain = new_chain
        return True


# === Test Program (tanpa Flask) ===
if __name__ == "__main__":
    print("=" * 60)
    print("BLOCKCHAIN TEST - Digital Signature & Mining Reward")
    print("=" * 60)

    # Inisialisasi blockchain
    blockchain = Blockchain(difficulty=3)
    print(f"\nBlockchain dibuat dengan difficulty {blockchain.difficulty}")
    print(f"Mining reward: {blockchain.mining_reward} coins")

    # Buat wallet
    print("\n--- Membuat Wallet ---")
    alice_wallet = Wallet()
    bob_wallet = Wallet()
    miner_wallet = Wallet()

    print(f"Alice address: {alice_wallet.get_address()[:20]}...")
    print(f"Bob address: {bob_wallet.get_address()[:20]}...")
    print(f"Miner address: {miner_wallet.get_address()[:20]}...")

    # Mining pertama untuk mendapatkan coin
    print("\n--- Mining Block 1 (untuk mendapatkan reward) ---")
    blockchain.pending_transactions.append(
        Transaction("SYSTEM", "", alice_wallet.get_address(), 0)  # Dummy tx
    )
    blockchain.mine_pending_transactions(alice_wallet.get_address())
    print(f"Alice balance: {blockchain.get_balance(alice_wallet.get_address())} coins")

    # Buat transaksi dari Alice ke Bob
    print("\n--- Membuat Transaksi Alice -> Bob ---")
    tx1 = Transaction(
        sender_address=alice_wallet.get_address(),
        sender_public_key=alice_wallet.get_public_key_string(),
        receiver_address=bob_wallet.get_address(),
        amount=3
    )
    tx1.sign_transaction(alice_wallet)
    print(f"Transaksi signed: {tx1.signature[:30]}...")
    print(f"Signature valid: {tx1.is_valid()}")

    # Tambahkan transaksi
    blockchain.add_transaction(tx1)

    # Mining block 2
    print("\n--- Mining Block 2 ---")
    blockchain.mine_pending_transactions(miner_wallet.get_address())

    # Cek saldo
    print("\n--- Saldo Akhir ---")
    print(f"Alice: {blockchain.get_balance(alice_wallet.get_address())} coins")
    print(f"Bob: {blockchain.get_balance(bob_wallet.get_address())} coins")
    print(f"Miner: {blockchain.get_balance(miner_wallet.get_address())} coins")

    # Validasi blockchain
    print("\n--- Validasi Blockchain ---")
    print(f"Blockchain valid: {blockchain.is_chain_valid()}")
    print(f"Total blocks: {len(blockchain.chain)}")

    # Test invalid signature
    print("\n--- Test Invalid Signature ---")
    fake_tx = Transaction(
        sender_address=alice_wallet.get_address(),
        sender_public_key=alice_wallet.get_public_key_string(),
        receiver_address=bob_wallet.get_address(),
        amount=100
    )
    fake_tx.signature = "fake_signature_here"
    print(f"Fake transaction valid: {fake_tx.is_valid()}")
