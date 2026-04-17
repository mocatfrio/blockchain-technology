from flask import Flask, jsonify, request
from blockchain import Blockchain, Transaction, Wallet
import requests

app = Flask(__name__)

# Inisialisasi blockchain dan wallet untuk node ini
blockchain = Blockchain(difficulty=3)
wallets = {}  # Menyimpan wallet yang dibuat di node ini
node_identifier = 'node-default'


# ============================================================
# WALLET ENDPOINTS
# ============================================================

@app.route('/wallet/new', methods=['GET'])
def create_wallet():
    """Membuat wallet baru"""
    wallet = Wallet()
    wallet_id = wallet.get_address()[:8]  # ID singkat untuk referensi
    wallets[wallet_id] = wallet

    return jsonify({
        'message': 'Wallet baru berhasil dibuat',
        'wallet_id': wallet_id,
        'address': wallet.get_address(),
        'public_key': wallet.get_public_key_string()
    }), 201


@app.route('/wallet/<wallet_id>', methods=['GET'])
def get_wallet(wallet_id):
    """Mendapatkan informasi wallet"""
    if wallet_id not in wallets:
        return jsonify({'message': 'Wallet tidak ditemukan'}), 404

    wallet = wallets[wallet_id]
    balance = blockchain.get_balance(wallet.get_address())

    return jsonify({
        'wallet_id': wallet_id,
        'address': wallet.get_address(),
        'balance': balance
    }), 200


@app.route('/wallets', methods=['GET'])
def list_wallets():
    """Daftar semua wallet di node ini"""
    wallet_list = []
    for wallet_id, wallet in wallets.items():
        wallet_list.append({
            'wallet_id': wallet_id,
            'address': wallet.get_address(),
            'balance': blockchain.get_balance(wallet.get_address())
        })
    return jsonify({'wallets': wallet_list}), 200


# ============================================================
# TRANSACTION ENDPOINTS
# ============================================================

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """Membuat transaksi baru dengan digital signature"""
    data = request.get_json()
    required = ['sender_wallet_id', 'receiver_address', 'amount']

    if not all(k in data for k in required):
        return jsonify({
            'message': 'Data tidak lengkap. Butuh: sender_wallet_id, receiver_address, amount'
        }), 400

    sender_wallet_id = data['sender_wallet_id']
    if sender_wallet_id not in wallets:
        return jsonify({'message': 'Wallet pengirim tidak ditemukan'}), 404

    sender_wallet = wallets[sender_wallet_id]

    # Cek saldo
    balance = blockchain.get_balance(sender_wallet.get_address())
    if balance < data['amount']:
        return jsonify({
            'message': 'Saldo tidak mencukupi',
            'balance': balance,
            'required': data['amount']
        }), 400

    # Buat transaksi
    tx = Transaction(
        sender_address=sender_wallet.get_address(),
        sender_public_key=sender_wallet.get_public_key_string(),
        receiver_address=data['receiver_address'],
        amount=data['amount']
    )

    # Sign transaksi dengan private key pengirim
    tx.sign_transaction(sender_wallet)

    # Tambahkan ke pending transactions
    try:
        block_index = blockchain.add_transaction(tx)
        return jsonify({
            'message': f'Transaksi akan ditambahkan ke block #{block_index}',
            'transaction': tx.to_dict(),
            'signature_valid': tx.is_valid()
        }), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.route('/transactions/pending', methods=['GET'])
def pending_transactions():
    """Melihat transaksi yang menunggu di-mining"""
    return jsonify({
        'pending': [tx.to_dict() for tx in blockchain.pending_transactions],
        'count': len(blockchain.pending_transactions)
    }), 200


# ============================================================
# MINING ENDPOINTS
# ============================================================

@app.route('/mine', methods=['POST'])
def mine():
    """Mining pending transactions dan memberikan reward ke miner"""
    data = request.get_json() or {}

    # Tentukan alamat miner
    if 'miner_wallet_id' in data:
        wallet_id = data['miner_wallet_id']
        if wallet_id not in wallets:
            return jsonify({'message': 'Wallet miner tidak ditemukan'}), 404
        miner_address = wallets[wallet_id].get_address()
    else:
        # Gunakan node identifier sebagai default
        miner_address = node_identifier

    # Minimal harus ada transaksi (atau buat dummy untuk demo)
    if not blockchain.pending_transactions:
        # Untuk demo, kita izinkan mining tanpa transaksi
        # Di produksi, sebaiknya ada minimal 1 transaksi
        pass

    block = blockchain.mine_pending_transactions(miner_address)

    return jsonify({
        'message': 'Block baru berhasil di-mining!',
        'block': block.to_dict(),
        'miner_address': miner_address,
        'miner_reward': blockchain.mining_reward
    }), 200


# ============================================================
# BLOCKCHAIN ENDPOINTS
# ============================================================

@app.route('/chain', methods=['GET'])
def get_chain():
    """Mendapatkan seluruh blockchain"""
    return jsonify({
        'chain': [block.to_dict() for block in blockchain.chain],
        'length': len(blockchain.chain)
    }), 200


@app.route('/chain/valid', methods=['GET'])
def validate_chain():
    """Memvalidasi blockchain"""
    is_valid = blockchain.is_chain_valid()
    return jsonify({
        'valid': is_valid,
        'length': len(blockchain.chain),
        'message': 'Blockchain valid' if is_valid else 'Blockchain tidak valid!'
    }), 200


@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    """Mendapatkan saldo dari alamat tertentu"""
    balance = blockchain.get_balance(address)
    return jsonify({
        'address': address,
        'balance': balance
    }), 200


# ============================================================
# NODE ENDPOINTS (Multi-Node Network)
# ============================================================

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """Mendaftarkan node baru ke jaringan"""
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


@app.route('/nodes', methods=['GET'])
def get_nodes():
    """Melihat daftar node yang terdaftar"""
    return jsonify({
        'nodes': list(blockchain.nodes),
        'count': len(blockchain.nodes)
    }), 200


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    """
    Sinkronisasi dengan node lain (consensus).
    Menggunakan Longest Chain Rule.
    """
    replaced = False
    longest_chain = None
    max_length = len(blockchain.chain)

    for node in blockchain.nodes:
        try:
            response = requests.get(f'{node}/chain', timeout=5)
            if response.status_code == 200:
                data = response.json()
                length = data['length']
                chain = data['chain']

                if length > max_length:
                    max_length = length
                    longest_chain = chain
        except requests.exceptions.RequestException as e:
            print(f"Gagal menghubungi node {node}: {e}")
            continue

    if longest_chain:
        replaced = blockchain.replace_chain(longest_chain)

    if replaced:
        return jsonify({
            'message': 'Chain lokal diganti dengan chain baru dari jaringan',
            'new_length': len(blockchain.chain),
            'chain': [block.to_dict() for block in blockchain.chain]
        }), 200
    else:
        return jsonify({
            'message': 'Chain lokal sudah yang terpanjang, tidak ada perubahan',
            'length': len(blockchain.chain)
        }), 200


# ============================================================
# SIGNATURE VERIFICATION ENDPOINT
# ============================================================

@app.route('/verify/transaction', methods=['POST'])
def verify_transaction():
    """Memverifikasi digital signature dari transaksi"""
    data = request.get_json()
    required = ['sender_address', 'sender_public_key', 'receiver_address',
                'amount', 'timestamp', 'signature']

    if not all(k in data for k in required):
        return jsonify({
            'message': 'Data transaksi tidak lengkap',
            'required_fields': required
        }), 400

    # Reconstruct transaksi
    tx = Transaction(
        sender_address=data['sender_address'],
        sender_public_key=data['sender_public_key'],
        receiver_address=data['receiver_address'],
        amount=data['amount']
    )
    tx.timestamp = data['timestamp']
    tx.signature = data['signature']

    is_valid = tx.is_valid()

    return jsonify({
        'valid': is_valid,
        'message': 'Digital signature VALID - transaksi asli' if is_valid
                   else 'Digital signature INVALID - transaksi mungkin dipalsukan!'
    }), 200


# ============================================================
# INFO ENDPOINT
# ============================================================

@app.route('/', methods=['GET'])
def info():
    """Informasi tentang node"""
    return jsonify({
        'node_id': node_identifier,
        'blockchain_length': len(blockchain.chain),
        'difficulty': blockchain.difficulty,
        'mining_reward': blockchain.mining_reward,
        'pending_transactions': len(blockchain.pending_transactions),
        'registered_nodes': len(blockchain.nodes),
        'wallets_count': len(wallets),
        'endpoints': {
            'wallet': [
                'GET /wallet/new - Buat wallet baru',
                'GET /wallet/<id> - Info wallet',
                'GET /wallets - Daftar semua wallet'
            ],
            'transactions': [
                'POST /transactions/new - Buat transaksi',
                'GET /transactions/pending - Lihat pending transactions'
            ],
            'mining': [
                'POST /mine - Mining block'
            ],
            'blockchain': [
                'GET /chain - Lihat seluruh blockchain',
                'GET /chain/valid - Validasi blockchain',
                'GET /balance/<address> - Cek saldo'
            ],
            'nodes': [
                'POST /nodes/register - Daftarkan node',
                'GET /nodes - Lihat node terdaftar',
                'GET /nodes/resolve - Sinkronisasi (consensus)'
            ],
            'verification': [
                'POST /verify/transaction - Verifikasi signature'
            ]
        }
    }), 200


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    import sys

    # Default port 5000, bisa diubah via argument
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    node_identifier = f'node-{port}'

    print("=" * 60)
    print(f"  BLOCKCHAIN NODE: {node_identifier}")
    print(f"  Port: {port}")
    print(f"  Difficulty: {blockchain.difficulty}")
    print(f"  Mining Reward: {blockchain.mining_reward} coins")
    print("=" * 60)
    print("\nEndpoints tersedia di http://localhost:{}/".format(port))
    print("\nTekan Ctrl+C untuk menghentikan server\n")

    app.run(host='0.0.0.0', port=port, debug=True)
