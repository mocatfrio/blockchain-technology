import hashlib
import json
import time


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


class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = difficulty
        self.mining_reward = 10
        self.nodes = set()
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis = Block(0, [], '0')
        genesis.mine(self.difficulty)
        self.chain.append(genesis)

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        reward_tx = Transaction('SYSTEM', miner_address, self.mining_reward)
        self.pending_transactions.append(reward_tx)

        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_last_block().hash
        )
        block.mine(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
        print(f'block #{block.index} berhasil di-mining: {block.hash[:16]}...')
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def register_node(self, address):
        self.nodes.add(address)

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
