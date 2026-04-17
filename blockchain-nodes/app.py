import json
import hashlib
import requests
import datetime

from flask import Flask, request, jsonify


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_dict(self):
        return {"sender": self.sender, "receiver": self.receiver, "amount": self.amount}


class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=str(datetime.datetime.now()), nonce=0, block_hash=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.previous_hash = previous_hash
        if block_hash:
            self.hash = block_hash
        else:
            self.calculate_hash()

    def calculate_hash(self):
        block = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [
                trans.to_dict() if isinstance(trans, Transaction) else trans
                for trans in self.transactions
            ],
            "nonce": self.nonce,
            "previous_hash": self.previous_hash,
        }
        block_string = json.dumps(block, sort_keys=True)
        generated_hash = hashlib.sha256(block_string.encode()).hexdigest()
        return generated_hash

    def mine_block(self, difficulty):
        target = "0" * difficulty #000
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [
                t.to_dict() if isinstance(t, Transaction) else t
                for t in self.transactions
            ],
            "nonce": self.nonce,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
        }


class Blockchain:
    def __init__(self):
        self.difficulty = 3
        self.chain = [self.init_genesis_block()]
        self.pending_transactions = []
        self.nodes = set()

    def init_genesis_block(self):
        genesis_transactions = []
        genesis_timestamp = str(datetime.datetime.now())
        genesis_block = Block(
            0, genesis_transactions, "0", timestamp=genesis_timestamp, nonce=0
        )
        genesis_block.hash = genesis_block.calculate_hash()
        return genesis_block

    def reset(self):
        self.chain = [self.init_genesis_block()]
        self.pending_transactions = []
        self.nodes = set()

    def get_latest_chain(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address="Miner"):
        if len(self.pending_transactions) == 0:
            return None

        reward_tx = Transaction("SYSTEM", miner_address, 1)
        transactions = self.pending_transactions + [reward_tx]

        index = len(self.chain)
        previous_hash = self.get_latest_chain().hash
        timestamp = datetime.datetime.now().isoformat()

        block_new = Block(index, transactions, previous_hash, timestamp=timestamp)
        block_new.mine_block(self.difficulty)

        self.chain.append(block_new)
        self.pending_transactions = []
        return block_new

    def is_valid(self):
        target = "0" * self.difficulty

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]

            if current.previous_hash != prev.hash:
                return False

            if current.hash != current.calculate_hash():
                return False

            if current.hash[: self.difficulty] != target:
                return False

        return True

    def register_node(self, node_address):
        clean_node = node_address.replace("http://", "").replace("https://", "").strip()
        if clean_node:
            self.nodes.add(clean_node)

    def to_list(self):
        return [block.to_dict() for block in self.chain]

    def pending_to_list(self):
        return [
            tx.to_dict() if isinstance(tx, Transaction) else tx
            for tx in self.pending_transactions
        ]

    def load_chain(self, chain_data):
        new_chain = []
        for block_data in chain_data:
            block = Block(
                index=block_data["index"],
                transactions=block_data["transactions"],
                previous_hash=block_data["previous_hash"],
                timestamp=block_data["timestamp"],
                nonce=block_data["nonce"],
                block_hash=block_data["hash"],
            )
            new_chain.append(block)
        self.chain = new_chain

    def is_chain_data_valid(self, chain_data):
        if len(chain_data) == 0:
            return False

        target = "0" * self.difficulty

        for i in range(1, len(chain_data)):
            current = chain_data[i]
            prev = chain_data[i - 1]

            block_content = {
                "index": current["index"],
                "timestamp": current["timestamp"],
                "transactions": current["transactions"],
                "nonce": current["nonce"],
                "previous_hash": current["previous_hash"],
            }

            recalculated_hash = hashlib.sha256(
                json.dumps(block_content, sort_keys=True).encode()
            ).hexdigest()

            if current["previous_hash"] != prev["hash"]:
                return False

            if current["hash"] != recalculated_hash:
                return False

            if current["hash"][: self.difficulty] != target:
                return False

        return True

    def resolve_conflicts(self):
        longest_chain = None
        max_length = len(self.chain)

        for node in self.nodes:
            try:
                response = requests.get(f"http://{node}/chain", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    length = data["data"]["length"]
                    chain = data["data"]["chain"]

                    if length > max_length and self.is_chain_data_valid(chain):
                        max_length = length
                        longest_chain = chain
            except requests.RequestException:
                pass

        if longest_chain:
            self.load_chain(longest_chain)
            return True

        return False


app = Flask(__name__)
blockchain = Blockchain()
NODE_NAME = "Node"

def success_response(message, data=None, status_code=200):
    return (
        jsonify(
            {
                "success": True,
                "node_name": NODE_NAME,
                "message": message,
                "data": data or {},
            }
        ),
        status_code,
    )


def error_response(message, status_code=400):
    return (
        jsonify(
            {"success": False, "node_name": NODE_NAME, "message": message, "data": {}}
        ),
        status_code,
    )


@app.route("/", methods=["GET"])
def home():
    return success_response(
        "Blockchain node is running",
        {
            "chain_length": len(blockchain.chain),
            "pending_count": len(blockchain.pending_transactions),
            "connected_nodes": list(blockchain.nodes),
            "valid": blockchain.is_valid(),
            "difficulty": blockchain.difficulty,
        },
    )


@app.route("/status", methods=["GET"])
def status():
    return success_response(
        "Node status",
        {
            "chain_length": len(blockchain.chain),
            "pending_count": len(blockchain.pending_transactions),
            "connected_nodes": list(blockchain.nodes),
            "valid": blockchain.is_valid(),
            "difficulty": blockchain.difficulty,
        },
    )


@app.route("/pending", methods=["GET"])
def pending():
    return success_response(
        "Pending transactions",
        {
            "pending_count": len(blockchain.pending_transactions),
            "pending_transactions": blockchain.pending_to_list(),
        },
    )


@app.route("/nodes", methods=["GET"])
def get_nodes():
    return success_response(
        "Connected nodes",
        {"total_nodes": len(blockchain.nodes), "nodes": list(blockchain.nodes)},
    )


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    data = request.get_json(silent=True)

    required = ["sender", "receiver", "amount"]
    if not data or not all(k in data for k in required):
        return error_response("sender, receiver, amount wajib diisi", 400)

    try:
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return error_response("amount harus berupa angka", 400)

    tx = Transaction(data["sender"], data["receiver"], amount)
    blockchain.add_transaction(tx)

    return success_response(
        "Transaksi berhasil ditambahkan ke pending transactions",
        {
            "transaction": tx.to_dict(),
            "pending_count": len(blockchain.pending_transactions),
        },
        201,
    )


@app.route("/transactions/broadcast", methods=["POST"])
def broadcast_transaction():
    data = request.get_json(silent=True)

    required = ["sender", "receiver", "amount"]
    if not data or not all(k in data for k in required):
        return error_response("sender, receiver, amount wajib diisi", 400)

    try:
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return error_response("amount harus berupa angka", 400)

    tx = Transaction(data["sender"], data["receiver"], amount)
    blockchain.add_transaction(tx)

    results = []
    for node in blockchain.nodes:
        try:
            response = requests.post(
                f"http://{node}/transactions/new", json=tx.to_dict(), timeout=3
            )
            results.append({"node": node, "status_code": response.status_code})
        except requests.RequestException:
            results.append({"node": node, "status_code": "unreachable"})

    return success_response(
        "Transaksi ditambahkan dan dibroadcast",
        {
            "transaction": tx.to_dict(),
            "broadcast_results": results,
            "pending_count": len(blockchain.pending_transactions),
        },
        201,
    )


@app.route("/mine", methods=["POST"])
def mine():
    data = request.get_json(silent=True) or {}
    miner = data.get("miner", "Miner")

    new_block = blockchain.mine_pending_transactions(miner)

    if not new_block:
        return error_response("Tidak ada pending transaction untuk di-mine", 400)

    return success_response(
        "Block berhasil di-mine",
        {"block": new_block.to_dict(), "chain_length": len(blockchain.chain)},
        200,
    )


@app.route("/chain", methods=["GET"])
def get_chain():
    return success_response(
        "Blockchain data",
        {"chain": blockchain.to_list(), "length": len(blockchain.chain)},
    )


@app.route("/nodes/register", methods=["POST"])
def register_nodes():
    data = request.get_json(silent=True)
    nodes = data.get("nodes") if data else None

    if not nodes or not isinstance(nodes, list):
        return error_response("nodes harus berupa list", 400)

    for node in nodes:
        blockchain.register_node(node)

    return success_response(
        "Node berhasil diregister", {"total_nodes": list(blockchain.nodes)}, 201
    )


@app.route("/nodes/resolve", methods=["GET"])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        return success_response(
            "Chain diganti dengan chain terpanjang yang valid",
            {"chain": blockchain.to_list(), "length": len(blockchain.chain)},
        )
    return success_response(
        "Chain node ini sudah paling panjang / konsisten",
        {"chain": blockchain.to_list(), "length": len(blockchain.chain)},
    )


@app.route("/validate", methods=["GET"])
def validate():
    return success_response("Validation result", {"valid": blockchain.is_valid()})


@app.route("/tamper", methods=["POST"])
def tamper():
    data = request.get_json(silent=True)

    if not data:
        return error_response("Body JSON diperlukan", 400)

    index = data.get("index")
    new_amount = data.get("new_amount")

    if index is None or new_amount is None:
        return error_response("index dan new_amount wajib diisi", 400)

    try:
        index = int(index)
        new_amount = float(new_amount)
    except (ValueError, TypeError):
        return error_response("index harus integer dan new_amount harus angka", 400)

    if index <= 0 or index >= len(blockchain.chain):
        return error_response("index block tidak valid", 400)

    block = blockchain.chain[index]

    if len(block.transactions) == 0:
        return error_response("block tidak punya transaksi", 400)

    first_tx = block.transactions[0]
    if isinstance(first_tx, Transaction):
        first_tx.amount = new_amount
    else:
        first_tx["amount"] = new_amount

    return success_response(
        f"Block {index} berhasil di-tamper",
        {"block": block.to_dict(), "valid_after_tamper": blockchain.is_valid()},
    )


@app.route("/reset", methods=["POST"])
def reset():
    blockchain.reset()
    return success_response(
        "Node berhasil di-reset",
        {
            "chain_length": len(blockchain.chain),
            "pending_count": len(blockchain.pending_transactions),
            "connected_nodes": list(blockchain.nodes),
        },
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5001)
    parser.add_argument("--name", type=str, default="Node")
    args = parser.parse_args()

    NODE_NAME = args.name
    app.run(host="0.0.0.0", port=args.port, debug=True)
