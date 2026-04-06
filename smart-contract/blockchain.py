import hashlib
import datetime
import json
import time
import tracemalloc


class Transaction:
    def __init__(self, sender, receiver, amount,
                 tx_type='transfer', contract_id=None, action=None, params=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.tx_type = tx_type
        self.contract_id = contract_id
        self.action = action
        self.params = params or {}

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'tx_type': self.tx_type,
            'contract_id': self.contract_id,
            'action': self.action,
            'params': self.params
        }

    def print(self):
        print(self.to_dict())


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.timestamp = str(datetime.datetime.now())
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block = {
            'index': self.index,
            'transactions': [t.to_dict() for t in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
        }
        block_string = json.dumps(block, sort_keys=True)
        generated_hash = hashlib.sha256(block_string.encode()).hexdigest()
        return generated_hash

    def mine_block(self, difficulty):
        start = time.time()
        tracemalloc.start()

        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print('block mined:', self.hash)

        end = time.time()
        print('waktu eksekusi:', end - start, 'detik')

        current, peak = tracemalloc.get_traced_memory()
        print('memory sekarang:', current / 10**6, 'MB')
        print('memory maksimum:', peak / 10**6, 'MB')
        tracemalloc.stop()


class Blockchain:
    def __init__(self):
        self.chain = [self.init_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 3
        self.contracts = {}

    def init_genesis_block(self):
        return Block(0, [], '0')

    def get_latest_block(self):
        return self.chain[-1]

    def deploy_contract(self, contract):
        contract.deploy()
        self.contracts[contract.contract_id] = contract

    def execute_contract(self, contract_id, action, params):
        if contract_id not in self.contracts:
            print(f"contract '{contract_id}' tidak ditemukan")
            return None

        contract = self.contracts[contract_id]
        result = contract.execute(action, params)

        tx = Transaction(
            sender=params.get('caller', 'unknown'),
            receiver=contract_id,
            amount=0,
            tx_type='contract',
            contract_id=contract_id,
            action=action,
            params=params
        )
        self.pending_transactions.append(tx)
        return result

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        index = len(self.chain)
        previous_hash = self.get_latest_block().hash
        block = Block(index, self.pending_transactions, previous_hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
        return True
