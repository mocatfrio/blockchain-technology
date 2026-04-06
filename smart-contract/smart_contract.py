import json
from blockchain import Transaction, Blockchain


class SmartContract:
    def __init__(self, contract_id, owner, initial_state=None):
        self.contract_id = contract_id
        self.owner = owner
        self.state = initial_state if initial_state else {}
        self.is_deployed = False

    def deploy(self):
        self.is_deployed = True
        print(f"contract '{self.contract_id}' deployed oleh {self.owner}")

    def execute(self, action, params):
        raise NotImplementedError('subclass harus mengimplementasikan execute()')

    def to_dict(self):
        return {
            'contract_id': self.contract_id,
            'owner': self.owner,
            'state': self.state,
            'is_deployed': self.is_deployed
        }

    def print(self):
        print(json.dumps(self.to_dict(), indent=2))


class EscrowContract(SmartContract):
    def __init__(self, contract_id, owner, receiver, amount):
        self.contract_id = contract_id
        self.owner = owner
        self.state = {
            'receiver': receiver,
            'amount': amount,
            'released': False
        }
        self.is_deployed = False

    def execute(self, action, params):
        if not self.is_deployed:
            return {'status': 'failed', 'message': 'contract belum di-deploy'}

        if action == 'release':
            caller = params.get('caller')
            if caller != self.owner:
                return {'status': 'failed', 'message': 'hanya owner yang dapat melepas dana'}
            if self.state['released']:
                return {'status': 'failed', 'message': 'dana sudah pernah dilepas'}
            self.state['released'] = True
            return {
                'status': 'success',
                'message': f"dana sebesar {self.state['amount']} berhasil dikirim ke {self.state['receiver']}"
            }

        if action == 'check':
            return {'status': 'info', 'state': self.state}

        return {'status': 'failed', 'message': f"aksi '{action}' tidak dikenali"}


if __name__ == '__main__':
    my_blockchain = Blockchain()

    # deploy escrow contract
    print('deploy smart contract')
    escrow = EscrowContract('escrow-001', owner='Alice', receiver='Bob', amount=50)
    my_blockchain.deploy_contract(escrow)
    print()

    # cek state awal contract
    print('cek state awal contract')
    result = my_blockchain.execute_contract('escrow-001', 'check', {'caller': 'Alice'})
    print(result)
    print()

    # tambahkan transaksi biasa
    print('tambah transaksi biasa')
    tx1 = Transaction('Alice', 'Bob', 50)
    tx1.print()
    my_blockchain.add_transaction(tx1)
    print()

    # mining block 1
    print('mining block 1')
    my_blockchain.mine_pending_transactions()
    print()

    # eksekusi contract release dana
    print('eksekusi contract: release dana')
    result = my_blockchain.execute_contract('escrow-001', 'release', {'caller': 'Alice'})
    print(result)
    print()

    # coba release lagi (harus gagal)
    print('eksekusi contract: release dana (kedua kali)')
    result = my_blockchain.execute_contract('escrow-001', 'release', {'caller': 'Alice'})
    print(result)
    print()

    # mining block 2
    print('mining block 2')
    my_blockchain.mine_pending_transactions()
    print()

    # validasi blockchain
    print('blockchain valid?', my_blockchain.is_chain_valid())
