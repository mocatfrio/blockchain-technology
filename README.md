# Blockchain Technology

Blockchain technology is a database mechanism that enables transparent information sharing within a business network by creating a decentralized, immutable system for recording transactions. This technology has been widely used across various sectors, including the creation of digital currencies such as Bitcoin and the Development of Smart Contracts. This course provides an understanding of the basic theories and concepts of Blockchain, Cryptocurrency, and Smart Contract technology. At the end of the lecture, students are expected to be able to implement Blockchain, Cryptocurrency, and Smart Contract technology.

## Course Learning Outcomes

1. Students are able to **design and implement the fundamental concepts of blockchain**, including distributed ledger architecture and cryptographic mechanisms that ensure data integrity
2. Students are able to **design and implement consensus mechanisms, cryptocurrency transaction structures, and network security mitigation strategies**
3. Students are able to **develop and deploy smart contracts on modern blockchain platforms** to automate business processes
4. Students are able to **integrate blockchain technology into real-world applications** (e.g., cybersecurity, supply chain, or finance) and develop a **prototype decentralized application (dApp)**

## Tools

- Python
- Solidity
- Remix IDE
- Foundry / Hardhat
- Ganache

## Topics

- Blockchain fundamentals
- Cryptocurrency
- Smart Contracts
- dApp

## Modules

| Module | Title                               | Link                      |
| ------ | ----------------------------------- | ------------------------- |
| 1      | Introduction to Python              | [Go to module](module-01.md) |
| 2      | Blockchain Fundamentals             | [Go to module](module-02.md) |
| 3      | Advanced Blockchain Concepts        | [Go to module](module-03.md) |
| 4      | Blockchain Network dengan Flask API | [Go to module](module-04.md) |
| 5      | Cryptocurrency                      | [Go to module](module-05.md) |
| 6      | Advanced Cryptocurrency             | [Go to module](module-06.md) |
| 7      | Smart Contract dengan Remix IDE     | [Go to module](module-07.md) |
| 8      | Smart Contracts (Python)            | [Go to module](module-08.md) |
| 9      | Smart Contract dengan Solidity      | [Go to module](module-09.md) |

## Concept Mapping

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           BLOCKCHAIN TECHNOLOGY                                  │
│                                                                                  │
│   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐           │
│   │   BLOCKCHAIN    │────►│ CRYPTOCURRENCY  │────►│ SMART CONTRACT  │           │
│   │   (Foundation)  │     │  (Application)  │     │   (Extension)   │           │
│   └────────┬────────┘     └────────┬────────┘     └────────┬────────┘           │
│            │                       │                       │                     │
│     Module 01-04             Module 05-06             Module 07-09               │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 1. Blockchain (Foundation)

| Topic                           | Sub-Topics                               | Module                 |
| ------------------------------- | ---------------------------------------- | ---------------------- |
| **Preparation**           | Python, VS Code Installation             | [Module 01](module-01.md) |
| **Data Structure**        | Block, Chain, Transaction                | [Module 02](module-02.md) |
| **Cryptography**          | Hash (SHA-256), Previous Hash            | [Module 02](module-02.md) |
| **Consensus**             | Proof of Work, Mining, Nonce, Difficulty | [Module 02](module-02.md) |
| **Validation**            | Chain Validation                         | [Module 02](module-02.md) |
| **Merkle Tree**           | Merkle Root, Merkle Proof                | [Module 03](module-03.md) |
| **Mining Reward**         | Coinbase Transaction, Halving            | [Module 03](module-03.md) |
| **Balance Tracking**      | UTXO vs Account Model                    | [Module 03](module-03.md) |
| **Mempool**               | Transaction Priority, Fee                | [Module 03](module-03.md) |
| **Difficulty Adjustment** | Target Block Time                        | [Module 03](module-03.md) |
| **P2P Network**           | Node, Decentralization                   | [Module 04](module-04.md) |
| **REST API**              | Flask, Endpoints                         | [Module 04](module-04.md) |
| **Consensus Algorithm**   | Longest Chain Rule                       | [Module 04](module-04.md) |

### 2. Cryptocurrency (Application)

| Topic                              | Sub-Topics                            | Module                 |
| ---------------------------------- | ------------------------------------- | ---------------------- |
| **Digital Signature**        | Asymmetric Cryptography, RSA          | [Module 05](module-05.md) |
| **Wallet**                   | Private Key, Public Key, Keypair      | [Module 05](module-05.md) |
| **Transaction Verification** | Sign, Verify                          | [Module 05](module-05.md) |
| **Multi-Node Network**       | Network Simulation                    | [Module 05](module-05.md) |
| **Double Spending**          | Prevention Mechanism                  | [Module 06](module-06.md) |
| **Transaction Broadcasting** | Propagation                           | [Module 06](module-06.md) |
| **Block Confirmation**       | Confirmation Count, Security Level    | [Module 06](module-06.md) |
| **UTXO Model**               | Input, Output, Change                 | [Module 06](module-06.md) |
| **ECDSA**                    | Elliptic Curve Digital Signature      | [Module 06](module-06.md) |
| **Address Format**           | Base58Check, Version Byte             | [Module 06](module-06.md) |
| **HD Wallet**                | BIP32, Derivation Path                | [Module 06](module-06.md) |
| **Mnemonic Phrase**          | BIP39, Seed Recovery                  | [Module 06](module-06.md) |
| **SPV**                      | Light Client, Simplified Verification | [Module 06](module-06.md) |

### 3. Smart Contract (Extension)

| Topic                         | Sub-Topics                            | Module                                         |
| ----------------------------- | ------------------------------------- | ---------------------------------------------- |
| **Basic Concepts**      | Definition, Vending Machine Analogy   | [Module 07](module-07.md), [Module 08](module-08.md) |
| **Remix IDE**           | File Explorer, Compiler, Deploy       | [Module 07](module-07.md)                         |
| **Solidity Basics**     | State Variable, Function, Constructor | [Module 07](module-07.md)                         |
| **Access Control**      | msg.sender, require, Owner            | [Module 07](module-07.md)                         |
| **Python Simulation**   | SmartContract Class, State            | [Module 08](module-08.md)                         |
| **Contract Deployment** | Deploy to Blockchain                  | [Module 08](module-08.md)                         |
| **Contract Execution**  | Execute via Transaction               | [Module 08](module-08.md)                         |
| **Use Case: Escrow**    | Fund Custody                          | [Module 08](module-08.md)                         |
| **EVM**                 | Ethereum Virtual Machine              | [Module 09](module-09.md)                         |
| **Solidity**            | Smart Contract Language               | [Module 09](module-09.md)                         |
| **Hardhat**             | Development Framework                 | [Module 09](module-09.md)                         |
| **Contract Testing**    | Automated Test                        | [Module 09](module-09.md)                         |

### Learning Path

```
                              ┌─────────────┐
                              │  Module 01  │
                              │ Preparation │
                              └──────┬──────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                    BLOCKCHAIN                       │
          │                                                     │
          │   Module 02 ───────► Module 03 ───────► Module 04   │
          │  Fundamentals        Advanced          Network      │
          │                                                     │
          └──────────────────────────┬──────────────────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                  CRYPTOCURRENCY                     │
          │                                                     │
          │          Module 05 ─────────────► Module 06         │
          │        Cryptocurrency          Advanced Crypto      │
          │                                                     │
          └──────────────────────────┬──────────────────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                  SMART CONTRACT                     │
          │                                                     │
          │   Module 07 ───────► Module 08 ───────► Module 09   │
          │   Remix IDE       Python Simulation    Solidity     │
          │                                                     │
          └─────────────────────────────────────────────────────┘
```

### Tools by Category

| Category                 | Tools                                         | Module       |
| ------------------------ | --------------------------------------------- | ------------ |
| **Blockchain**     | Python, Flask                                 | Module 01-04 |
| **Cryptocurrency** | Python, Flask, RSA/ECDSA                      | Module 05-06 |
| **Smart Contract** | Remix IDE, Python, Solidity, Hardhat, Ganache | Module 07-09 |
