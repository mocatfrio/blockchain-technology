from flask import Flask, jsonify, request
from blockchain import Blockchain, Transaction
import requests

app = Flask(__name__)

blockchain = Blockchain(difficulty=2)

node_identifier = 'node-default'

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({
        'chain': [block.to_dict() for block in blockchain.chain],
        'length': len(blockchain.chain)
    }), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    data = request.get_json()
    required = ['sender', 'receiver', 'amount']

    if not all(k in data for k in required):
        return jsonify({'message': 'data tidak lengkap'}), 400

    tx = Transaction(data['sender'], data['receiver'], data['amount'])
    blockchain.add_transaction(tx)

    return jsonify({
        'message': f"transaksi akan ditambahkan ke block #{len(blockchain.chain)}"
    }), 201


@app.route('/transactions/pending', methods=['GET'])
def pending_transactions():
    return jsonify({
        'pending': [tx.to_dict() for tx in blockchain.pending_transactions],
        'count': len(blockchain.pending_transactions)
    }), 200

@app.route('/mine', methods=['GET'])
def mine():
    if not blockchain.pending_transactions:
        return jsonify({'message': 'tidak ada transaksi untuk di-mining'}), 400

    block = blockchain.mine_pending_transactions(miner_address=node_identifier)

    return jsonify({
        'message': 'block baru berhasil di-mining!',
        'block': block.to_dict()
    }), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    data = request.get_json()
    nodes = data.get('nodes')

    if not nodes:
        return jsonify({'message': 'daftar node tidak boleh kosong'}), 400

    for node in nodes:
        blockchain.register_node(node)

    return jsonify({
        'message': f'{len(nodes)} node berhasil didaftarkan',
        'total_nodes': list(blockchain.nodes)
    }), 201


@app.route('/nodes', methods=['GET'])
def get_nodes():
    return jsonify({
        'nodes': list(blockchain.nodes),
        'count': len(blockchain.nodes)
    }), 200


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
            'message': 'chain lokal diganti dengan chain baru dari jaringan',
            'chain': [block.to_dict() for block in blockchain.chain]
        }), 200
    else:
        return jsonify({
            'message': 'chain lokal sudah oke, tidak ada perubahan',
            'chain': [block.to_dict() for block in blockchain.chain]
        }), 200

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    node_identifier = f'node-{port}'
    print(f'node {node_identifier} berjalan di port {port}')
    app.run(host='0.0.0.0', port=port, debug=True)
