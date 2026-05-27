# Modul 14. Frontend Integration - Write Operations & Transactions

## Deskripsi

Modul ini membahas cara **mengirim transaksi** ke smart contract dari frontend, termasuk handling state-changing functions, konfirmasi wallet, menunggu transaction receipt, dan handling events.

## Tujuan Pembelajaran

Setelah menyelesaikan modul ini, mahasiswa mampu:

1. Memahami perbedaan read vs write operations
2. Mengirim transaksi ke smart contract
3. Handling wallet confirmation flow
4. Menunggu dan memproses transaction receipt
5. Menampilkan transaction status ke user
6. Listening dan handling smart contract events
7. Implementasi error handling untuk transactions

## Prasyarat

- Sudah menyelesaikan Module 13 (Read Operations)
- Dashboard dApp sudah bisa membaca data contract
- Memahami flow transaksi blockchain

## List of Contents

- [Deskripsi](#deskripsi)
- [Tujuan Pembelajaran](#tujuan-pembelajaran)
- [Prasyarat](#prasyarat)
- [1. Read vs Write Operations](#1-read-vs-write-operations)
- [2. Anatomy of a Transaction](#2-anatomy-of-a-transaction)
- [3. Sending Transactions](#3-sending-transactions)
- [4. Transaction States](#4-transaction-states)
- [5. Handling Transaction Receipt](#5-handling-transaction-receipt)
- [6. Listening to Events](#6-listening-to-events)
- [7. Hands-on: Claim Reward Feature](#7-hands-on-claim-reward-feature)
- [8. Hands-on: Admin Panel](#8-hands-on-admin-panel)
- [9. Transaction Error Handling](#9-transaction-error-handling)
- [10. Best Practices](#10-best-practices)
- [Ringkasan](#ringkasan)
- [Tugas](#tugas)

---

## 1. Read vs Write Operations

### 1.1 Perbandingan

```
┌─────────────────────────────────────────────────────────────────┐
│                READ vs WRITE OPERATIONS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  READ (View Functions)                                          │
│  ════════════════════════════════════════════════════════════   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  - Tidak mengubah state blockchain                      │    │
│  │  - Tidak memerlukan gas fee                             │    │
│  │  - Response instant                                     │    │
│  │  - Tidak perlu wallet signature                         │    │
│  │  - Bisa menggunakan Provider                            │    │
│  │                                                         │    │
│  │  Contoh: balanceOf(), totalSupply(), owner()           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  WRITE (State-Changing Functions)                               │
│  ════════════════════════════════════════════════════════════   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  - Mengubah state blockchain                            │    │
│  │  - Memerlukan gas fee                                   │    │
│  │  - Butuh waktu (menunggu block mining)                  │    │
│  │  - Perlu wallet signature                               │    │
│  │  - Harus menggunakan Signer                             │    │
│  │                                                         │    │
│  │  Contoh: transfer(), mint(), claimReward()             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Summary Table

| Aspek                    | Read (View)        | Write (State-Changing)    |
| ------------------------ | ------------------ | ------------------------- |
| **Gas Fee**        | Gratis             | Bayar gas                 |
| **Speed**          | Instant            | Menunggu block            |
| **Wallet**         | Tidak perlu        | Perlu signature           |
| **Provider/Signer**| Provider cukup     | Harus Signer              |
| **Reversible**     | N/A                | Tidak (immutable)         |
| **Events**         | Tidak emit         | Bisa emit events          |

---

## 2. Anatomy of a Transaction

### 2.1 Transaction Object

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRANSACTION OBJECT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  {                                                              │
│    // Who sends the transaction                                 │
│    from: "0xf39F...2266",                                       │
│                                                                 │
│    // Contract address                                          │
│    to: "0x5FbD...0aa3",                                         │
│                                                                 │
│    // ETH to send (optional, for payable functions)             │
│    value: "0",                                                  │
│                                                                 │
│    // Encoded function call                                     │
│    data: "0x4e71d92d", // claimReward() selector                │
│                                                                 │
│    // Gas settings                                              │
│    gasLimit: 100000,                                            │
│    maxFeePerGas: "20000000000",                                 │
│    maxPriorityFeePerGas: "1000000000",                          │
│                                                                 │
│    // Network                                                   │
│    chainId: 31337,                                              │
│                                                                 │
│    // Unique identifier per account                             │
│    nonce: 5                                                     │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Transaction Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRANSACTION LIFECYCLE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CREATE                                                      │
│     └─► Frontend creates transaction object                     │
│                                                                 │
│  2. SIGN                                                        │
│     └─► User signs with wallet (MetaMask popup)                 │
│                                                                 │
│  3. BROADCAST                                                   │
│     └─► Signed transaction sent to network                      │
│     └─► Returns transaction hash immediately                    │
│                                                                 │
│  4. PENDING                                                     │
│     └─► Transaction in mempool, waiting to be mined             │
│                                                                 │
│  5. MINED                                                       │
│     └─► Included in a block                                     │
│     └─► Returns transaction receipt                             │
│                                                                 │
│  6. CONFIRMED                                                   │
│     └─► Multiple blocks mined after                             │
│     └─► Transaction is "final"                                  │
│                                                                 │
│  Timeline:                                                      │
│  ┌────────┬────────┬────────┬────────┬────────┬────────┐        │
│  │ Create │  Sign  │Broadcast│ Pending│  Mined │Confirmed│       │
│  │  (ms)  │ (user) │  (ms)  │(seconds)│(seconds)│(minutes)│       │
│  └────────┴────────┴────────┴────────┴────────┴────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Sending Transactions

### 3.1 Basic Transaction

```javascript
import { ethers } from 'ethers'
import CourseRewardABI from './contracts/CourseReward.json'

const CONTRACT_ADDRESS = '0x5FbDB2315678afecb367f032d93F642f64180aa3'

async function claimReward() {
  // 1. Get provider and signer
  const provider = new ethers.BrowserProvider(window.ethereum)
  const signer = await provider.getSigner()

  // 2. Create contract instance with signer
  const contract = new ethers.Contract(
    CONTRACT_ADDRESS,
    CourseRewardABI.abi,
    signer
  )

  // 3. Call state-changing function
  // This triggers MetaMask popup
  const tx = await contract.claimReward()

  console.log('Transaction hash:', tx.hash)

  // 4. Wait for transaction to be mined
  const receipt = await tx.wait()

  console.log('Transaction confirmed!')
  console.log('Block number:', receipt.blockNumber)
  console.log('Gas used:', receipt.gasUsed.toString())

  return receipt
}
```

### 3.2 Transaction with Parameters

```javascript
async function setRewardAmount(newAmount) {
  const provider = new ethers.BrowserProvider(window.ethereum)
  const signer = await provider.getSigner()

  const contract = new ethers.Contract(
    CONTRACT_ADDRESS,
    CourseRewardABI.abi,
    signer
  )

  // Pass parameters to function
  const tx = await contract.setRewardAmount(newAmount)

  console.log('Transaction sent:', tx.hash)

  const receipt = await tx.wait()

  console.log('New reward amount set!')
  return receipt
}
```

### 3.3 Transaction with ETH Value (Payable Functions)

```javascript
async function depositEther(amountInEth) {
  const provider = new ethers.BrowserProvider(window.ethereum)
  const signer = await provider.getSigner()

  const contract = new ethers.Contract(
    CONTRACT_ADDRESS,
    CourseRewardABI.abi,
    signer
  )

  // Convert ETH to Wei and pass as value
  const tx = await contract.deposit({
    value: ethers.parseEther(amountInEth.toString())
  })

  const receipt = await tx.wait()
  return receipt
}
```

### 3.4 Custom Gas Settings

```javascript
async function claimRewardWithCustomGas() {
  const provider = new ethers.BrowserProvider(window.ethereum)
  const signer = await provider.getSigner()

  const contract = new ethers.Contract(
    CONTRACT_ADDRESS,
    CourseRewardABI.abi,
    signer
  )

  // Estimate gas first
  const estimatedGas = await contract.claimReward.estimateGas()

  // Add buffer (e.g., 20%)
  const gasLimit = estimatedGas * 120n / 100n

  // Send with custom gas
  const tx = await contract.claimReward({
    gasLimit: gasLimit
  })

  return await tx.wait()
}
```

---

## 4. Transaction States

### 4.1 State Machine

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRANSACTION STATE MACHINE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                     ┌─────────────┐                             │
│                     │    IDLE     │                             │
│                     └──────┬──────┘                             │
│                            │ User clicks button                 │
│                            ▼                                    │
│                     ┌─────────────┐                             │
│                     │  AWAITING   │                             │
│                     │  SIGNATURE  │◄─────────────┐              │
│                     └──────┬──────┘              │              │
│                            │                     │              │
│              ┌─────────────┼─────────────┐       │              │
│              │             │             │       │              │
│         User rejects  User signs    Timeout      │              │
│              │             │             │       │              │
│              ▼             ▼             ▼       │              │
│       ┌───────────┐ ┌───────────┐ ┌───────────┐  │              │
│       │ REJECTED  │ │  PENDING  │ │   ERROR   │──┘              │
│       └───────────┘ └─────┬─────┘ └───────────┘                 │
│                           │                                     │
│              ┌────────────┼────────────┐                        │
│              │            │            │                        │
│          Success       Failed      Dropped                      │
│              │            │            │                        │
│              ▼            ▼            ▼                        │
│       ┌───────────┐ ┌───────────┐ ┌───────────┐                 │
│       │  SUCCESS  │ │  FAILED   │ │  DROPPED  │                 │
│       └───────────┘ └───────────┘ └───────────┘                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Handling States in React

```jsx
import { useState } from 'react'

// Transaction status enum
const TX_STATUS = {
  IDLE: 'idle',
  AWAITING_SIGNATURE: 'awaiting_signature',
  PENDING: 'pending',
  SUCCESS: 'success',
  FAILED: 'failed',
  REJECTED: 'rejected'
}

function ClaimButton({ contract, onSuccess }) {
  const [txStatus, setTxStatus] = useState(TX_STATUS.IDLE)
  const [txHash, setTxHash] = useState(null)
  const [error, setError] = useState(null)

  const handleClaim = async () => {
    try {
      setError(null)
      setTxStatus(TX_STATUS.AWAITING_SIGNATURE)

      // This triggers MetaMask popup
      const tx = await contract.claimReward()

      setTxHash(tx.hash)
      setTxStatus(TX_STATUS.PENDING)

      // Wait for confirmation
      const receipt = await tx.wait()

      setTxStatus(TX_STATUS.SUCCESS)
      onSuccess?.(receipt)

    } catch (err) {
      console.error('Transaction error:', err)

      if (err.code === 4001 || err.code === 'ACTION_REJECTED') {
        setTxStatus(TX_STATUS.REJECTED)
        setError('Transaction rejected by user')
      } else {
        setTxStatus(TX_STATUS.FAILED)
        setError(err.reason || err.message)
      }
    }
  }

  const getButtonText = () => {
    switch (txStatus) {
      case TX_STATUS.AWAITING_SIGNATURE:
        return 'Confirm in Wallet...'
      case TX_STATUS.PENDING:
        return 'Processing...'
      case TX_STATUS.SUCCESS:
        return 'Claimed!'
      default:
        return 'Claim Reward'
    }
  }

  const isDisabled = [
    TX_STATUS.AWAITING_SIGNATURE,
    TX_STATUS.PENDING,
    TX_STATUS.SUCCESS
  ].includes(txStatus)

  return (
    <div className="claim-section">
      <button
        onClick={handleClaim}
        disabled={isDisabled}
        className={`btn btn-primary ${txStatus}`}
      >
        {getButtonText()}
      </button>

      {txHash && (
        <p className="tx-hash">
          TX: {txHash.slice(0, 10)}...{txHash.slice(-8)}
        </p>
      )}

      {error && (
        <p className="error">{error}</p>
      )}
    </div>
  )
}
```

---

## 5. Handling Transaction Receipt

### 5.1 Transaction Receipt Structure

```javascript
// Transaction Receipt object
{
  // Transaction identification
  hash: "0x1234...",
  blockNumber: 12345,
  blockHash: "0xabcd...",
  transactionIndex: 0,

  // Addresses
  from: "0xf39F...",
  to: "0x5FbD...", // Contract address

  // Gas info
  gasUsed: 50000n,
  gasPrice: 20000000000n,

  // Status
  status: 1, // 1 = success, 0 = failed

  // Events/Logs
  logs: [
    {
      address: "0x5FbD...",
      topics: [...],
      data: "0x..."
    }
  ]
}
```

### 5.2 Processing Receipt

```javascript
async function claimAndProcessReceipt(contract) {
  const tx = await contract.claimReward()
  const receipt = await tx.wait()

  // Check if transaction was successful
  if (receipt.status === 1) {
    console.log('Transaction successful!')

    // Calculate gas cost
    const gasCost = receipt.gasUsed * receipt.gasPrice
    console.log('Gas cost:', ethers.formatEther(gasCost), 'ETH')

    // Process events
    for (const log of receipt.logs) {
      // Parse event if it's from our contract
      try {
        const event = contract.interface.parseLog(log)
        console.log('Event:', event.name, event.args)
      } catch (e) {
        // Log from different contract, ignore
      }
    }
  } else {
    console.log('Transaction failed!')
  }

  return receipt
}
```

### 5.3 Waiting for Confirmations

```javascript
async function waitForConfirmations(tx, confirmations = 1) {
  console.log('Waiting for', confirmations, 'confirmations...')

  // wait() accepts number of confirmations
  const receipt = await tx.wait(confirmations)

  console.log('Transaction confirmed with', confirmations, 'blocks')
  return receipt
}

// Usage
const tx = await contract.claimReward()
await waitForConfirmations(tx, 2) // Wait for 2 confirmations
```

---

## 6. Listening to Events

### 6.1 Event Basics

Events di Solidity:
```solidity
event RewardClaimed(address indexed student, uint256 amount);
event RewardAmountChanged(uint256 oldAmount, uint256 newAmount);
```

### 6.2 Listening to Past Events

```javascript
async function getPastClaimEvents(contract, fromBlock = 0) {
  // Query past events
  const filter = contract.filters.RewardClaimed()
  const events = await contract.queryFilter(filter, fromBlock, 'latest')

  console.log('Total claims:', events.length)

  events.forEach(event => {
    console.log('Student:', event.args.student)
    console.log('Amount:', event.args.amount.toString())
    console.log('Block:', event.blockNumber)
    console.log('---')
  })

  return events
}
```

### 6.3 Real-time Event Listening

```javascript
function listenToClaimEvents(contract, callback) {
  // Subscribe to RewardClaimed events
  contract.on('RewardClaimed', (student, amount, event) => {
    console.log('New claim detected!')
    console.log('Student:', student)
    console.log('Amount:', amount.toString())
    console.log('Transaction:', event.log.transactionHash)

    callback?.({ student, amount, event })
  })

  // Return cleanup function
  return () => {
    contract.off('RewardClaimed')
  }
}

// Usage in React
useEffect(() => {
  if (!contract) return

  const cleanup = listenToClaimEvents(contract, (data) => {
    console.log('Claim event received:', data)
    // Refresh UI
    refreshData()
  })

  // Cleanup on unmount
  return cleanup
}, [contract])
```

### 6.4 Filtering Events

```javascript
// Get events for specific student
async function getClaimsForStudent(contract, studentAddress) {
  // Filter by indexed parameter
  const filter = contract.filters.RewardClaimed(studentAddress)
  const events = await contract.queryFilter(filter)

  return events
}

// Get events in specific block range
async function getRecentClaims(contract, blocksBack = 1000) {
  const provider = contract.runner.provider
  const currentBlock = await provider.getBlockNumber()
  const fromBlock = currentBlock - blocksBack

  const filter = contract.filters.RewardClaimed()
  const events = await contract.queryFilter(filter, fromBlock, 'latest')

  return events
}
```

---

## 7. Hands-on: Claim Reward Feature

### 7.1 ClaimReward Component

**frontend/src/components/ClaimReward.jsx:**
```jsx
import { useState, useEffect } from 'react'
import { ethers } from 'ethers'
import { useWallet } from '../hooks/useWallet'
import CourseRewardABI from '../contracts/CourseReward.json'
import { getAddress } from '../contracts/addresses'
import './ClaimReward.css'

const TX_STATUS = {
  IDLE: 'idle',
  CHECKING: 'checking',
  AWAITING_SIGNATURE: 'awaiting_signature',
  PENDING: 'pending',
  SUCCESS: 'success',
  FAILED: 'failed',
  REJECTED: 'rejected',
  ALREADY_CLAIMED: 'already_claimed'
}

function ClaimReward({ onClaimSuccess }) {
  const { account, chainId, isConnected, getSigner } = useWallet()
  const contractAddress = getAddress('courseReward', chainId)

  const [txStatus, setTxStatus] = useState(TX_STATUS.IDLE)
  const [txHash, setTxHash] = useState(null)
  const [error, setError] = useState(null)
  const [hasClaimed, setHasClaimed] = useState(false)
  const [rewardAmount, setRewardAmount] = useState('0')

  // Check if user has already claimed
  useEffect(() => {
    if (isConnected && contractAddress && account) {
      checkClaimStatus()
    }
  }, [isConnected, contractAddress, account])

  const checkClaimStatus = async () => {
    try {
      setTxStatus(TX_STATUS.CHECKING)

      const provider = new ethers.BrowserProvider(window.ethereum)
      const contract = new ethers.Contract(
        contractAddress,
        CourseRewardABI.abi,
        provider
      )

      const [claimed, amount] = await Promise.all([
        contract.hasClaimed(account),
        contract.rewardAmount()
      ])

      setHasClaimed(claimed)
      setRewardAmount(amount.toString())

      if (claimed) {
        setTxStatus(TX_STATUS.ALREADY_CLAIMED)
      } else {
        setTxStatus(TX_STATUS.IDLE)
      }
    } catch (err) {
      console.error('Error checking claim status:', err)
      setTxStatus(TX_STATUS.IDLE)
    }
  }

  const handleClaim = async () => {
    if (!isConnected || !contractAddress) return

    try {
      setError(null)
      setTxHash(null)
      setTxStatus(TX_STATUS.AWAITING_SIGNATURE)

      // Get signer
      const signer = await getSigner()
      if (!signer) {
        throw new Error('Could not get signer')
      }

      // Create contract with signer
      const contract = new ethers.Contract(
        contractAddress,
        CourseRewardABI.abi,
        signer
      )

      // Send transaction
      const tx = await contract.claimReward()

      setTxHash(tx.hash)
      setTxStatus(TX_STATUS.PENDING)

      // Wait for confirmation
      const receipt = await tx.wait()

      if (receipt.status === 1) {
        setTxStatus(TX_STATUS.SUCCESS)
        setHasClaimed(true)
        onClaimSuccess?.(receipt)
      } else {
        setTxStatus(TX_STATUS.FAILED)
        setError('Transaction failed')
      }

    } catch (err) {
      console.error('Claim error:', err)

      if (err.code === 4001 || err.code === 'ACTION_REJECTED') {
        setTxStatus(TX_STATUS.REJECTED)
        setError('Transaction was rejected')
      } else if (err.reason) {
        setTxStatus(TX_STATUS.FAILED)
        setError(err.reason)
      } else {
        setTxStatus(TX_STATUS.FAILED)
        setError(err.message || 'Transaction failed')
      }
    }
  }

  const resetState = () => {
    setTxStatus(TX_STATUS.IDLE)
    setTxHash(null)
    setError(null)
    checkClaimStatus()
  }

  // Render helpers
  const getButtonText = () => {
    switch (txStatus) {
      case TX_STATUS.CHECKING:
        return 'Checking...'
      case TX_STATUS.AWAITING_SIGNATURE:
        return 'Confirm in Wallet...'
      case TX_STATUS.PENDING:
        return 'Processing...'
      case TX_STATUS.SUCCESS:
        return 'Claimed Successfully!'
      case TX_STATUS.ALREADY_CLAIMED:
        return 'Already Claimed'
      default:
        return `Claim ${rewardAmount} Points`
    }
  }

  const isButtonDisabled = () => {
    return [
      TX_STATUS.CHECKING,
      TX_STATUS.AWAITING_SIGNATURE,
      TX_STATUS.PENDING,
      TX_STATUS.SUCCESS,
      TX_STATUS.ALREADY_CLAIMED
    ].includes(txStatus)
  }

  if (!isConnected) {
    return (
      <div className="card claim-card">
        <h2>Claim Reward</h2>
        <p className="muted">Connect wallet to claim your reward</p>
      </div>
    )
  }

  if (!contractAddress) {
    return (
      <div className="card claim-card">
        <h2>Claim Reward</h2>
        <p className="error">Contract not available on this network</p>
      </div>
    )
  }

  return (
    <div className="card claim-card">
      <h2>Claim Reward</h2>

      <div className="claim-info">
        <p>
          Reward Amount: <strong>{rewardAmount} Points</strong>
        </p>
      </div>

      <button
        onClick={handleClaim}
        disabled={isButtonDisabled()}
        className={`btn btn-claim ${txStatus}`}
      >
        {txStatus === TX_STATUS.PENDING && (
          <span className="spinner"></span>
        )}
        {getButtonText()}
      </button>

      {/* Transaction Hash */}
      {txHash && (
        <div className="tx-info">
          <label>Transaction Hash:</label>
          <code>{txHash}</code>
        </div>
      )}

      {/* Success Message */}
      {txStatus === TX_STATUS.SUCCESS && (
        <div className="success-message">
          <p>Your reward has been claimed successfully!</p>
          <button onClick={resetState} className="btn btn-secondary">
            Done
          </button>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={resetState} className="btn btn-secondary">
            Try Again
          </button>
        </div>
      )}
    </div>
  )
}

export default ClaimReward
```

### 7.2 ClaimReward Styles

**frontend/src/components/ClaimReward.css:**
```css
.claim-card {
  text-align: center;
}

.claim-info {
  margin-bottom: 20px;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 8px;
}

.claim-info p {
  margin: 0;
  color: #333;
}

.claim-info strong {
  color: #4CAF50;
  font-size: 1.25rem;
}

.btn-claim {
  width: 100%;
  padding: 15px 30px;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-claim.idle {
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
}

.btn-claim.idle:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
}

.btn-claim.awaiting_signature {
  background: #ff9800;
  color: white;
}

.btn-claim.pending {
  background: #2196F3;
  color: white;
}

.btn-claim.success {
  background: #4CAF50;
  color: white;
}

.btn-claim.already_claimed {
  background: #9e9e9e;
  color: white;
}

.btn-claim:disabled {
  cursor: not-allowed;
  transform: none;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.tx-info {
  margin-top: 20px;
  padding: 15px;
  background: #e3f2fd;
  border-radius: 8px;
  text-align: left;
}

.tx-info label {
  display: block;
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 5px;
}

.tx-info code {
  display: block;
  font-size: 0.75rem;
  color: #1976D2;
  word-break: break-all;
}

.success-message {
  margin-top: 20px;
  padding: 20px;
  background: #e8f5e9;
  border-radius: 8px;
  color: #2e7d32;
}

.success-message p {
  margin-bottom: 15px;
}

.error-message {
  margin-top: 20px;
  padding: 20px;
  background: #ffebee;
  border-radius: 8px;
  color: #c62828;
}

.error-message p {
  margin-bottom: 15px;
}
```

---

## 8. Hands-on: Admin Panel

### 8.1 AdminPanel Component

**frontend/src/components/AdminPanel.jsx:**
```jsx
import { useState, useEffect } from 'react'
import { ethers } from 'ethers'
import { useWallet } from '../hooks/useWallet'
import CourseRewardABI from '../contracts/CourseReward.json'
import { getAddress } from '../contracts/addresses'
import './AdminPanel.css'

function AdminPanel({ onUpdate }) {
  const { account, chainId, isConnected, getSigner } = useWallet()
  const contractAddress = getAddress('courseReward', chainId)

  const [isOwner, setIsOwner] = useState(false)
  const [currentAmount, setCurrentAmount] = useState('0')
  const [newAmount, setNewAmount] = useState('')
  const [loading, setLoading] = useState(true)
  const [txStatus, setTxStatus] = useState('idle')
  const [error, setError] = useState(null)

  // Check if connected account is owner
  useEffect(() => {
    if (isConnected && contractAddress && account) {
      checkOwnership()
    }
  }, [isConnected, contractAddress, account])

  const checkOwnership = async () => {
    try {
      setLoading(true)
      const provider = new ethers.BrowserProvider(window.ethereum)
      const contract = new ethers.Contract(
        contractAddress,
        CourseRewardABI.abi,
        provider
      )

      const [owner, amount] = await Promise.all([
        contract.owner(),
        contract.rewardAmount()
      ])

      setIsOwner(owner.toLowerCase() === account.toLowerCase())
      setCurrentAmount(amount.toString())
    } catch (err) {
      console.error('Error checking ownership:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSetReward = async (e) => {
    e.preventDefault()

    if (!newAmount || isNaN(newAmount) || Number(newAmount) < 0) {
      setError('Please enter a valid amount')
      return
    }

    try {
      setError(null)
      setTxStatus('awaiting')

      const signer = await getSigner()
      const contract = new ethers.Contract(
        contractAddress,
        CourseRewardABI.abi,
        signer
      )

      const tx = await contract.setRewardAmount(newAmount)

      setTxStatus('pending')

      await tx.wait()

      setTxStatus('success')
      setCurrentAmount(newAmount)
      setNewAmount('')
      onUpdate?.()

      // Reset status after delay
      setTimeout(() => setTxStatus('idle'), 3000)

    } catch (err) {
      console.error('Error setting reward:', err)
      setTxStatus('error')

      if (err.code === 4001 || err.code === 'ACTION_REJECTED') {
        setError('Transaction rejected')
      } else {
        setError(err.reason || err.message)
      }
    }
  }

  // Don't render if not owner
  if (!isConnected || loading) {
    return null
  }

  if (!isOwner) {
    return null
  }

  return (
    <div className="card admin-panel">
      <div className="admin-header">
        <h2>Admin Panel</h2>
        <span className="owner-badge">Owner</span>
      </div>

      <div className="current-value">
        <label>Current Reward Amount</label>
        <span>{currentAmount} Points</span>
      </div>

      <form onSubmit={handleSetReward} className="admin-form">
        <div className="form-group">
          <label htmlFor="newAmount">New Reward Amount</label>
          <input
            type="number"
            id="newAmount"
            value={newAmount}
            onChange={(e) => setNewAmount(e.target.value)}
            placeholder="Enter new amount"
            min="0"
            disabled={txStatus === 'awaiting' || txStatus === 'pending'}
          />
        </div>

        <button
          type="submit"
          className={`btn btn-admin ${txStatus}`}
          disabled={txStatus === 'awaiting' || txStatus === 'pending'}
        >
          {txStatus === 'awaiting' && 'Confirm in Wallet...'}
          {txStatus === 'pending' && 'Updating...'}
          {txStatus === 'success' && 'Updated!'}
          {txStatus === 'idle' && 'Update Reward'}
          {txStatus === 'error' && 'Try Again'}
        </button>
      </form>

      {error && (
        <div className="admin-error">
          {error}
        </div>
      )}
    </div>
  )
}

export default AdminPanel
```

### 8.2 AdminPanel Styles

**frontend/src/components/AdminPanel.css:**
```css
.admin-panel {
  border: 2px solid #ff9800;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.admin-header h2 {
  margin: 0;
}

.owner-badge {
  background: #ff9800;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.current-value {
  background: #fff3e0;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.current-value label {
  display: block;
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 5px;
}

.current-value span {
  font-size: 1.25rem;
  font-weight: 600;
  color: #e65100;
}

.admin-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 0.9rem;
  color: #333;
}

.form-group input {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #ff9800;
}

.form-group input:disabled {
  background: #f5f5f5;
}

.btn-admin {
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-admin.idle {
  background: #ff9800;
  color: white;
}

.btn-admin.idle:hover {
  background: #f57c00;
}

.btn-admin.awaiting,
.btn-admin.pending {
  background: #2196F3;
  color: white;
}

.btn-admin.success {
  background: #4CAF50;
  color: white;
}

.btn-admin.error {
  background: #f44336;
  color: white;
}

.btn-admin:disabled {
  cursor: not-allowed;
}

.admin-error {
  margin-top: 15px;
  padding: 10px 15px;
  background: #ffebee;
  color: #c62828;
  border-radius: 8px;
  font-size: 0.9rem;
}
```

### 8.3 Updated App Component

**frontend/src/App.jsx:**
```jsx
import { useState, useCallback } from 'react'
import Navbar from './components/Navbar'
import ContractInfo from './components/ContractInfo'
import UserStatus from './components/UserStatus'
import ClaimReward from './components/ClaimReward'
import AdminPanel from './components/AdminPanel'
import { useWallet } from './hooks/useWallet'
import './App.css'

function App() {
  const { error, isMetaMaskInstalled } = useWallet()
  const [refreshKey, setRefreshKey] = useState(0)

  // Force refresh all components
  const handleRefresh = useCallback(() => {
    setRefreshKey(prev => prev + 1)
  }, [])

  if (!isMetaMaskInstalled) {
    return (
      <div className="app">
        <div className="metamask-warning">
          <h2>MetaMask Required</h2>
          <p>Please install MetaMask to use this dApp</p>
          <a
            href="https://metamask.io/download/"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-primary"
          >
            Install MetaMask
          </a>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <Navbar />

      {error && (
        <div className="global-error">
          {error}
        </div>
      )}

      <main className="main-content">
        {/* Admin Panel - Only visible to owner */}
        <AdminPanel key={`admin-${refreshKey}`} onUpdate={handleRefresh} />

        {/* Main Grid */}
        <div className="grid">
          <ContractInfo key={`info-${refreshKey}`} />
          <UserStatus key={`status-${refreshKey}`} />
        </div>

        {/* Claim Section */}
        <ClaimReward
          key={`claim-${refreshKey}`}
          onClaimSuccess={handleRefresh}
        />
      </main>
    </div>
  )
}

export default App
```

---

## 9. Transaction Error Handling

### 9.1 Common Transaction Errors

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMMON TX ERRORS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Error Code: 4001 / ACTION_REJECTED                             │
│  ──────────────────────────────────────────────────────────     │
│  Cause: User rejected the transaction in wallet                 │
│  Handle: Show friendly message, allow retry                     │
│                                                                 │
│  Error: INSUFFICIENT_FUNDS                                      │
│  ──────────────────────────────────────────────────────────     │
│  Cause: Not enough ETH for gas                                  │
│  Handle: Show balance warning, suggest getting more ETH         │
│                                                                 │
│  Error: CALL_EXCEPTION                                          │
│  ──────────────────────────────────────────────────────────     │
│  Cause: Contract function reverted                              │
│  Handle: Parse reason, show to user                             │
│                                                                 │
│  Error: UNPREDICTABLE_GAS_LIMIT                                 │
│  ──────────────────────────────────────────────────────────     │
│  Cause: Transaction will fail (simulate failed)                 │
│  Handle: Check inputs, show reason                              │
│                                                                 │
│  Error: NONCE_EXPIRED                                           │
│  ──────────────────────────────────────────────────────────     │
│  Cause: Transaction replaced or nonce reused                    │
│  Handle: Refresh and retry                                      │
│                                                                 │
│  Error: REPLACEMENT_UNDERPRICED                                 │
│  ──────────────────────────────────────────────────────────     │
│  Cause: Replacement tx has lower gas price                      │
│  Handle: Increase gas price or wait                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Error Handler Utility

**frontend/src/utils/errorHandler.js:**
```javascript
export function parseTransactionError(error) {
  // User rejected
  if (error.code === 4001 || error.code === 'ACTION_REJECTED') {
    return {
      type: 'USER_REJECTED',
      message: 'Transaction was rejected',
      retry: true
    }
  }

  // Insufficient funds
  if (error.code === 'INSUFFICIENT_FUNDS') {
    return {
      type: 'INSUFFICIENT_FUNDS',
      message: 'Insufficient ETH for gas fee',
      retry: false
    }
  }

  // Contract revert
  if (error.code === 'CALL_EXCEPTION') {
    return {
      type: 'CONTRACT_ERROR',
      message: error.reason || 'Contract execution failed',
      retry: true
    }
  }

  // Simulation failed
  if (error.code === 'UNPREDICTABLE_GAS_LIMIT') {
    let reason = 'Transaction will fail'
    if (error.reason) {
      reason = error.reason
    }
    return {
      type: 'SIMULATION_FAILED',
      message: reason,
      retry: true
    }
  }

  // Network error
  if (error.code === 'NETWORK_ERROR') {
    return {
      type: 'NETWORK_ERROR',
      message: 'Network connection error',
      retry: true
    }
  }

  // Default
  return {
    type: 'UNKNOWN',
    message: error.message || 'An error occurred',
    retry: true
  }
}

export function getErrorMessage(error) {
  const parsed = parseTransactionError(error)
  return parsed.message
}
```

### 9.3 Using Error Handler

```jsx
import { parseTransactionError } from '../utils/errorHandler'

async function handleTransaction() {
  try {
    const tx = await contract.someFunction()
    await tx.wait()
  } catch (err) {
    const { type, message, retry } = parseTransactionError(err)

    if (type === 'USER_REJECTED') {
      // User cancelled, just reset state
      setStatus('idle')
    } else if (type === 'INSUFFICIENT_FUNDS') {
      // Show get ETH message
      setError('Please get more ETH to pay for gas')
    } else {
      // Show error with retry option
      setError(message)
      if (retry) {
        setShowRetry(true)
      }
    }
  }
}
```

---

## 10. Best Practices

### 10.1 Transaction UX Guidelines

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRANSACTION UX BEST PRACTICES                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CLEAR FEEDBACK                                              │
│     ────────────────────────────────────────────                │
│     - Show distinct states: Awaiting, Pending, Success, Error   │
│     - Display transaction hash for verification                 │
│     - Provide link to block explorer                            │
│                                                                 │
│  2. DISABLE ACTIONS DURING TX                                   │
│     ────────────────────────────────────────────                │
│     - Disable button while awaiting signature                   │
│     - Prevent double-submit                                     │
│     - Show loading indicator                                    │
│                                                                 │
│  3. ESTIMATE BEFORE SUBMIT                                      │
│     ────────────────────────────────────────────                │
│     - Use estimateGas() to check if tx will succeed             │
│     - Show estimated gas cost before confirming                 │
│                                                                 │
│  4. HANDLE ALL ERROR CASES                                      │
│     ────────────────────────────────────────────                │
│     - User rejection (code 4001)                                │
│     - Contract revert (show reason)                             │
│     - Network errors                                            │
│     - Timeout handling                                          │
│                                                                 │
│  5. REFRESH DATA AFTER SUCCESS                                  │
│     ────────────────────────────────────────────                │
│     - Update UI to reflect new state                            │
│     - Re-fetch relevant data                                    │
│     - Clear form inputs                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 10.2 Code Patterns

```javascript
// Pattern 1: Optimistic Updates with Rollback
async function optimisticClaim() {
  const previousState = { ...userData }

  // Optimistically update UI
  setUserData({ ...userData, hasClaimed: true })

  try {
    const tx = await contract.claimReward()
    await tx.wait()
    // Refresh actual data
    await refreshData()
  } catch (err) {
    // Rollback on error
    setUserData(previousState)
    throw err
  }
}

// Pattern 2: Confirmation with Retry
async function sendWithRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (err) {
      if (i === maxRetries - 1) throw err
      if (err.code === 4001) throw err // Don't retry user rejection
      await new Promise(r => setTimeout(r, 1000 * (i + 1)))
    }
  }
}

// Pattern 3: Gas Estimation Check
async function safeTransaction(contract, method, args) {
  try {
    // Check if tx will succeed
    await contract[method].estimateGas(...args)

    // If estimate succeeds, send tx
    const tx = await contract[method](...args)
    return await tx.wait()
  } catch (err) {
    // Parse and throw meaningful error
    throw new Error(getErrorMessage(err))
  }
}
```

---

## Ringkasan

| Topik               | Poin Penting                                          |
| ------------------- | ----------------------------------------------------- |
| **Write vs Read** | Write butuh gas & signature, read instant & gratis    |
| **Tx Lifecycle**  | Create -> Sign -> Broadcast -> Pending -> Mined       |
| **Signer**        | Diperlukan untuk write operations                     |
| **tx.wait()**     | Menunggu transaksi dikonfirmasi                       |
| **Events**        | Listen realtime atau query past events                |
| **Error Handling**| Parse error codes, show user-friendly messages        |
| **UX**            | Clear states, disable during tx, refresh after success|

---

## Tugas

### Tugas 1: Implementasi Full dApp

1. Implementasikan semua komponen dari hands-on
2. Pastikan claim reward berfungsi end-to-end
3. Test dengan multiple accounts

### Tugas 2: Add Transaction History

Buat komponen `TransactionHistory.jsx` yang:
1. Listen ke events RewardClaimed
2. Tampilkan list transaksi terbaru
3. Tampilkan: address, amount, tx hash, timestamp

### Tugas 3: Add Block Explorer Link

1. Untuk setiap transaction hash, tambahkan link ke block explorer
2. Gunakan Etherscan untuk mainnet/testnet
3. Untuk localhost, tampilkan hash saja

**Hint:**
```javascript
const getExplorerUrl = (txHash, chainId) => {
  if (chainId === 1) return `https://etherscan.io/tx/${txHash}`
  if (chainId === 11155111) return `https://sepolia.etherscan.io/tx/${txHash}`
  return null // localhost
}
```

### Deliverable

Kumpulkan:
1. Screenshot dApp dengan semua fitur berfungsi
2. Screenshot MetaMask confirmation popup
3. Screenshot transaction success state
4. Screenshot transaction history (Tugas 2)
5. Source code komponen yang sudah dibuat

---

## Referensi

- [ethers.js Transactions](https://docs.ethers.org/v6/getting-started/#starting-transactions)
- [ethers.js Events](https://docs.ethers.org/v6/getting-started/#starting-events)
- [MetaMask Error Codes](https://docs.metamask.io/wallet/reference/json-rpc-api/)
- [EIP-1193 Provider Errors](https://eips.ethereum.org/EIPS/eip-1193)
