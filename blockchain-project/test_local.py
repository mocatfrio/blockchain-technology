"""
Test script untuk menguji blockchain secara lokal tanpa Flask API.
Jalankan dengan: python test_local.py
"""

from blockchain import Blockchain, Transaction, Wallet


def print_separator(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    print_separator("BLOCKCHAIN TEST - Local Mode")

    # 1. Inisialisasi Blockchain
    print("\n[1] Membuat Blockchain...")
    blockchain = Blockchain(difficulty=3)
    print(f"    - Difficulty: {blockchain.difficulty}")
    print(f"    - Mining Reward: {blockchain.mining_reward} coins")
    print(f"    - Genesis Block Hash: {blockchain.chain[0].hash[:32]}...")

    # 2. Membuat Wallet
    print_separator("MEMBUAT WALLET")

    alice = Wallet()
    bob = Wallet()
    charlie = Wallet()
    miner = Wallet()

    print(f"Alice   : {alice.get_address()[:24]}...")
    print(f"Bob     : {bob.get_address()[:24]}...")
    print(f"Charlie : {charlie.get_address()[:24]}...")
    print(f"Miner   : {miner.get_address()[:24]}...")

    # 3. Mining Block 1 - Alice mendapat reward
    print_separator("MINING BLOCK #1 (Alice sebagai miner)")

    # Tambahkan dummy transaction agar bisa mining
    blockchain.pending_transactions.append(
        Transaction("SYSTEM", "", alice.get_address(), 0)
    )
    blockchain.mine_pending_transactions(alice.get_address())
    print(f"Alice balance setelah mining: {blockchain.get_balance(alice.get_address())} coins")

    # 4. Membuat Transaksi dengan Digital Signature
    print_separator("TRANSAKSI 1: Alice -> Bob (3 coins)")

    tx1 = Transaction(
        sender_address=alice.get_address(),
        sender_public_key=alice.get_public_key_string(),
        receiver_address=bob.get_address(),
        amount=3
    )

    # Sign transaksi
    tx1.sign_transaction(alice)
    print(f"Signature: {tx1.signature[:40]}...")
    print(f"Signature Valid: {tx1.is_valid()}")

    # Tambahkan ke pending
    blockchain.add_transaction(tx1)
    print("Transaksi ditambahkan ke pending transactions")

    # 5. Transaksi kedua
    print_separator("TRANSAKSI 2: Alice -> Charlie (2 coins)")

    tx2 = Transaction(
        sender_address=alice.get_address(),
        sender_public_key=alice.get_public_key_string(),
        receiver_address=charlie.get_address(),
        amount=2
    )
    tx2.sign_transaction(alice)
    print(f"Signature Valid: {tx2.is_valid()}")

    blockchain.add_transaction(tx2)

    # 6. Mining Block 2 - Miner mendapat reward
    print_separator("MINING BLOCK #2 (Miner sebagai miner)")

    blockchain.mine_pending_transactions(miner.get_address())

    # 7. Cek Saldo
    print_separator("SALDO AKHIR")

    print(f"Alice   : {blockchain.get_balance(alice.get_address())} coins")
    print(f"Bob     : {blockchain.get_balance(bob.get_address())} coins")
    print(f"Charlie : {blockchain.get_balance(charlie.get_address())} coins")
    print(f"Miner   : {blockchain.get_balance(miner.get_address())} coins")

    # 8. Validasi Blockchain
    print_separator("VALIDASI BLOCKCHAIN")

    print(f"Blockchain Valid: {blockchain.is_chain_valid()}")
    print(f"Total Blocks: {len(blockchain.chain)}")

    # 9. Tampilkan isi blockchain
    print_separator("ISI BLOCKCHAIN")

    for block in blockchain.chain:
        print(f"\nBlock #{block.index}")
        print(f"  Hash: {block.hash[:32]}...")
        print(f"  Previous Hash: {block.previous_hash[:32]}...")
        print(f"  Nonce: {block.nonce}")
        print(f"  Transactions: {len(block.transactions)}")
        for i, tx in enumerate(block.transactions):
            print(f"    [{i+1}] {tx.sender_address[:12]}... -> {tx.receiver_address[:12]}... : {tx.amount} coins")

    # 10. Test Invalid Signature
    print_separator("TEST INVALID SIGNATURE")

    print("Mencoba membuat transaksi dengan signature palsu...")
    fake_tx = Transaction(
        sender_address=bob.get_address(),
        sender_public_key=bob.get_public_key_string(),
        receiver_address=charlie.get_address(),
        amount=100
    )
    fake_tx.signature = "FAKE_SIGNATURE_12345"
    print(f"Fake transaction valid: {fake_tx.is_valid()}")

    # 11. Test Sign dengan Wallet yang Salah
    print_separator("TEST SIGN DENGAN WALLET LAIN")

    wrong_tx = Transaction(
        sender_address=bob.get_address(),
        sender_public_key=bob.get_public_key_string(),
        receiver_address=charlie.get_address(),
        amount=1
    )
    try:
        # Mencoba sign dengan wallet Alice (bukan Bob)
        wrong_tx.sign_transaction(alice)
        print("ERROR: Seharusnya tidak bisa sign!")
    except Exception as e:
        print(f"Exception (expected): {e}")

    print_separator("TEST SELESAI")
    print("\nSemua fitur berjalan dengan baik!")


if __name__ == "__main__":
    main()
