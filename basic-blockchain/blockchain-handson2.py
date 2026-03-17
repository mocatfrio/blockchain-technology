import datetime
import json
import hashlib

# Simulasi secret key user
USER_KEYS = {
    "Alice": "alice_private_key_123",
    "Bob": "bob_private_key_456",
    "Charlie": "charlie_private_key_789",
}

class Transaction:
  def __init__(self, sender, receiver, amount, signature=None):
    # atribut 
    self.sender = sender
    self.receiver = receiver
    self.amount = amount
    
  def to_dict(self):
    return {
      "sender": self.sender,
      "receiver": self.receiver,
      "amount": self.amount,
      "signature": self.signature
    }
    
  def get_message(self):
      return f"{self.sender}->{self.receiver}:{self.amount}"

  def sign_transaction(self, private_key):
      message = self.get_message() + private_key
      self.signature = hashlib.sha256(message.encode()).hexdigest()

  def is_valid(self):
      if self.sender == "SYSTEM":
          return True

      if self.sender not in USER_KEYS:
          return False

      expected_signature = hashlib.sha256(
          (self.get_message() + USER_KEYS[self.sender]).encode()
      ).hexdigest()

      return self.signature == expected_signature

  def print(self):
      print(self.to_dict())


class Block:

    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.transactions = transactions
        self.nonce = 0
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [t.to_dict() for t in self.transactions],
            "nonce": self.nonce,
            "previous_hash": self.previous_hash,
        }
        block_string = json.dumps(block)
        generated_hash = hashlib.sha256(block_string.encode()).hexdigest()
        return generated_hash

    def print_hash(self):
        print(self.calculate_hash())
        
    def mine_block(self, difficulty):
      while self.hash[:difficulty] != "0" * difficulty:
        self.nonce += 1
        self.hash = self.calculate_hash()
      print("Block mined: ", self.hash, "| nonce: ", self.nonce)


class Blockchain:
    def __init__(self):
        self.chain = [self.init_genesis_block()]
        self.difficulty = 3
        self.pending_transactions = []

    def init_genesis_block(self):
        return Block(0, [], "0")

    def add_transactions(self, transaction):
        self.pending_transactions.append(transaction)

    def get_latest_chain(self):
        return self.chain[-1]

    def mine_pending_transactions(self, miner_address="Miner"):
        if len(self.pending_transactions) == 0:
            print("Tidak ada transaksi untuk di-mine")
            return

        reward_tx = Transaction("SYSTEM", miner_address, 1)
        self.pending_transactions.append(reward_tx)
        
        print("Mining reward ditambahkan:")
        reward_tx.print()

        index = len(self.chain)
        previous_hash = self.get_latest_chain().hash
        block_new = Block(index, self.pending_transactions, previous_hash)
        block_new.mine_block(self.difficulty)

        self.chain.append(block_new)
        self.pending_transactions = []

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i] 
            prev = self.chain[i-1]

            if current.previous_hash != prev.hash:
                return False

            if current.hash != current.calculate_hash():
                return False

            if current.hash[:self.difficulty] != "0" * self.difficulty:
                return False

            for tx in current.transactions:
                if not tx.is_valid():
                    return False

        return True


if __name__ == "__main__":
    trans = Transaction("Alice", "Bob", 10)
    trans.sign_transaction(USER_KEYS["Alice"])
    trans.print()

    block = Block(1, [trans], 0)
    block.print_hash()

    myBlockchain = Blockchain()
    success = myBlockchain.add_transactions(trans)

    if success:
      myBlockchain.mine_pending_transactions("Miner1")

    print("Apakah Blockchain valid?")
    print(myBlockchain.is_valid())
