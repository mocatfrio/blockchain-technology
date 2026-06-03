# Modul 13. Frontend Integration - Membaca Data dari Smart Contract

## Deskripsi

Modul ini membahas cara **mengintegrasikan frontend React dengan smart contract** untuk membaca data (read operations). Mahasiswa akan belajar menggunakan ethers.js untuk membuat provider, contract instance, dan memanggil view functions.

## Tujuan Pembelajaran

Setelah menyelesaikan modul ini, mahasiswa mampu:

1. Memahami konsep Provider dan Signer di ethers.js
2. Membuat contract instance dengan ABI dan address
3. Memanggil view functions (read-only)
4. Menangani loading state dan error
5. Menggunakan React hooks untuk state management
6. Membuat custom hooks untuk reusable logic

## Prasyarat

- Sudah menyelesaikan Module 12 (Setup dApp)
- Project frontend sudah running
- Hardhat node sudah berjalan dengan contract ter-deploy
- MetaMask sudah terhubung ke local network

## List of Contents

- [Deskripsi](#deskripsi)
- [Tujuan Pembelajaran](#tujuan-pembelajaran)
- [Prasyarat](#prasyarat)
- [1. Konsep Provider dan Signer](#1-konsep-provider-dan-signer)
- [2. Membuat Contract Instance](#2-membuat-contract-instance)
- [3. Memanggil View Functions](#3-memanggil-view-functions)
- [4. State Management dengan React](#4-state-management-dengan-react)
- [5. Custom Hook: useContract](#5-custom-hook-usecontract)
- [6. Custom Hook: useWallet](#6-custom-hook-usewallet)
- [7. Hands-on: Dashboard Contract](#7-hands-on-dashboard-contract)
- [8. Error Handling](#8-error-handling)
- [9. Best Practices](#9-best-practices)
- [Ringkasan](#ringkasan)
- [Tugas](#tugas)

---

## 1. Konsep Provider dan Signer

### 1.1 Apa itu Provider?

**Provider** adalah koneksi read-only ke blockchain. Provider digunakan untuk:
- Membaca data dari blockchain
- Memanggil view functions
- Mendapatkan informasi network
- Listen events

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROVIDER CONCEPT                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Provider = Read-Only Connection                                │
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐        │
│  │   Frontend  │────►│   Provider  │────►│  Blockchain │        │
│  │             │◄────│  (ethers)   │◄────│   (Read)    │        │
│  └─────────────┘     └─────────────┘     └─────────────┘        │
│                                                                 │
│  Bisa dilakukan dengan Provider:                                │
│  ✓ getBalance()                                                 │
│  ✓ getBlockNumber()                                             │
│  ✓ call view functions                                          │
│  ✓ getTransactionReceipt()                                      │
│                                                                 │
│  TIDAK bisa dilakukan:                                          │
│  ✗ sendTransaction()                                            │
│  ✗ sign message                                                 │
│  ✗ call state-changing functions                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Apa itu Signer?

**Signer** adalah entity yang bisa menandatangani transaksi. Signer memiliki akses ke private key dan bisa:
- Melakukan semua yang Provider bisa
- Mengirim transaksi
- Sign messages
- Memanggil state-changing functions

```
┌─────────────────────────────────────────────────────────────────┐
│                    SIGNER CONCEPT                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Signer = Provider + Private Key Access                         │
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐        │
│  │   Frontend  │────►│   Signer    │────►│  Blockchain │        │
│  │             │◄────│ (MetaMask)  │◄────│ (Read/Write)│        │
│  └─────────────┘     └─────────────┘     └─────────────┘        │
│                            │                                    │
│                            ▼                                    │
│                     ┌─────────────┐                             │
│                     │ Private Key │                             │
│                     │  (Secure)   │                             │
│                     └─────────────┘                             │
│                                                                 │
│  Bisa dilakukan dengan Signer:                                  │
│  ✓ Semua yang Provider bisa                                     │
│  ✓ sendTransaction()                                            │
│  ✓ signMessage()                                                │
│  ✓ call state-changing functions                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Provider Types di ethers.js v6

| Provider Type             | Penggunaan                 | Contoh                            |
| ------------------------- | -------------------------- | --------------------------------- |
| `BrowserProvider`       | Dari wallet (MetaMask)     | `new ethers.BrowserProvider(window.ethereum)` |
| `JsonRpcProvider`       | Langsung ke RPC URL        | `new ethers.JsonRpcProvider(url)` |
| `WebSocketProvider`     | Real-time dengan WebSocket | `new ethers.WebSocketProvider(wsUrl)` |
| `InfuraProvider`        | Via Infura service         | `new ethers.InfuraProvider(network, apiKey)` |
| `AlchemyProvider`       | Via Alchemy service        | `new ethers.AlchemyProvider(network, apiKey)` |

### 1.4 Membuat Provider

> **Langkah Praktis - Kapan pakai Provider mana?**
>
> | Situasi | Provider yang dipakai |
> |---------|----------------------|
> | User sudah connect MetaMask | `BrowserProvider` |
> | Hanya baca data tanpa wallet | `JsonRpcProvider` |
> | Butuh koneksi ke testnet/mainnet | `JsonRpcProvider` dengan URL Alchemy/Infura |
>
> **Analogi sederhana:**
> - `BrowserProvider` = masuk toko dengan kartu identitas (bisa beli barang)
> - `JsonRpcProvider` = lihat-lihat etalase toko (hanya bisa lihat, tidak bisa beli)

```javascript
import { ethers } from 'ethers'

// 1. Browser Provider (dari MetaMask)
// Gunakan ini saat user sudah connect wallet
const browserProvider = new ethers.BrowserProvider(window.ethereum)

// 2. JSON-RPC Provider (langsung ke node)
// Gunakan ini untuk read-only tanpa wallet
const jsonRpcProvider = new ethers.JsonRpcProvider('http://127.0.0.1:8545')

// 3. Untuk testnet/mainnet
const sepoliaProvider = new ethers.JsonRpcProvider(
  'https://eth-sepolia.g.alchemy.com/v2/YOUR-API-KEY'
)
```

### 1.5 Mendapatkan Signer

```javascript
import { ethers } from 'ethers'

// Dari BrowserProvider (MetaMask)
const provider = new ethers.BrowserProvider(window.ethereum)
const signer = await provider.getSigner()

// Signer memiliki address
console.log('Address:', await signer.getAddress())

// Signer bisa menandatangani
const signature = await signer.signMessage('Hello World')
```

---

## 2. Membuat Contract Instance

### 2.1 Komponen yang Dibutuhkan

Untuk berinteraksi dengan smart contract, kita butuh:

```
┌─────────────────────────────────────────────────────────────────┐
│                CONTRACT INSTANCE REQUIREMENTS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CONTRACT ADDRESS                                            │
│     └─► Dimana contract di-deploy                               │
│         "0x5FbDB2315678afecb367f032d93F642f64180aa3"            │
│                                                                 │
│  2. ABI (Application Binary Interface)                          │
│     └─► Deskripsi functions dan events                          │
│         [{ "name": "claimReward", "type": "function", ... }]   │
│                                                                 │
│  3. PROVIDER atau SIGNER                                        │
│     └─► Provider: untuk read-only                               │
│     └─► Signer: untuk read + write                              │
│                                                                 │
│  Contract Instance = Address + ABI + Provider/Signer            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Membuat Contract Instance

> **Step-by-Step untuk Pemula:**
>
> Untuk "berbicara" dengan smart contract dari frontend, kita butuh 3 hal:
>
> 1. **Contract Address** → "Alamat rumah" contract di blockchain
>    - Dapat dari hasil deploy (lihat terminal saat `npx hardhat run scripts/deploy.js`)
>    - Contoh: `0x5FbDB2315678afecb367f032d93F642f64180aa3`
>
> 2. **ABI (Application Binary Interface)** → "Buku petunjuk" function apa saja yang ada
>    - File JSON yang berisi daftar functions, events, dll
>    - Lokasi: `contracts/artifacts/contracts/NamaContract.sol/NamaContract.json`
>
> 3. **Provider/Signer** → "Koneksi" ke blockchain
>    - Provider untuk baca, Signer untuk baca+tulis
>
> **Cara copy ABI ke frontend:**
> ```bash
> # Dari folder project utama
> cp contracts/artifacts/contracts/CourseReward.sol/CourseReward.json frontend/src/contracts/
> ```

```javascript
import { ethers } from 'ethers'
import CourseRewardABI from './contracts/CourseReward.json'

// Contract address (dari hasil deploy)
const CONTRACT_ADDRESS = '0x5FbDB2315678afecb367f032d93F642f64180aa3'

// Membuat contract instance dengan Provider (read-only)
const provider = new ethers.BrowserProvider(window.ethereum)
const contractReadOnly = new ethers.Contract(
  CONTRACT_ADDRESS,
  CourseRewardABI.abi,
  provider
)

// Membuat contract instance dengan Signer (read + write)
const signer = await provider.getSigner()
const contractWithSigner = new ethers.Contract(
  CONTRACT_ADDRESS,
  CourseRewardABI.abi,
  signer
)
```

### 2.3 Perbedaan Contract dengan Provider vs Signer

```
┌─────────────────────────────────────────────────────────────────┐
│            CONTRACT WITH PROVIDER vs SIGNER                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Contract + Provider (Read Only)                                │
│  ════════════════════════════════════════════════════════════   │
│  const contract = new Contract(address, abi, provider)          │
│                                                                 │
│  ✓ contract.rewardAmount()     // view function                 │
│  ✓ contract.owner()            // view function                 │
│  ✓ contract.hasClaimed(addr)   // view function                 │
│  ✗ contract.claimReward()      // ERROR! butuh signer           │
│                                                                 │
│  Contract + Signer (Read + Write)                               │
│  ════════════════════════════════════════════════════════════   │
│  const contract = new Contract(address, abi, signer)            │
│                                                                 │
│  ✓ contract.rewardAmount()     // view function                 │
│  ✓ contract.claimReward()      // state-changing function       │
│  ✓ contract.setRewardAmount(n) // state-changing function       │
│                                                                 │
│  Best Practice:                                                 │
│  - Gunakan Provider untuk read operations                       │
│  - Gunakan Signer hanya saat akan write                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Memanggil View Functions

### 3.1 View Functions

View functions adalah functions yang tidak mengubah state blockchain. Karakteristik:
- Tidak membutuhkan gas fee
- Response instant
- Tidak perlu konfirmasi dari wallet

```javascript
// Contoh view functions di CourseReward.sol
// function rewardAmount() public view returns (uint256)
// function owner() public view returns (address)
// function hasClaimed(address) public view returns (bool)
// function rewards(address) public view returns (uint256)
// function getMyReward() external view returns (uint256)
```

### 3.2 Memanggil View Functions

> **Cara Membaca Data dari Smart Contract:**
>
> View functions adalah function yang hanya membaca data, tidak mengubah apapun di blockchain.
>
> **Langkah-langkahnya:**
> 1. Buat provider (koneksi ke blockchain)
> 2. Buat contract instance (gabungan address + ABI + provider)
> 3. Panggil function seperti memanggil method biasa
>
> **Contoh view functions di CourseReward:**
> - `rewardAmount()` → berapa poin reward
> - `owner()` → siapa pemilik contract
> - `hasClaimed(address)` → apakah address sudah claim
> - `rewards(address)` → berapa reward yang sudah dikumpulkan
>
> **Tips:** Semua view function gratis (tidak bayar gas) dan instant!

```javascript
import { ethers } from 'ethers'
import CourseRewardABI from './contracts/CourseReward.json'

const CONTRACT_ADDRESS = '0x5FbDB2315678afecb367f032d93F642f64180aa3'

async function readContractData() {
  // Setup provider dan contract
  const provider = new ethers.BrowserProvider(window.ethereum)
  const contract = new ethers.Contract(
    CONTRACT_ADDRESS,
    CourseRewardABI.abi,
    provider
  )

  // Memanggil view functions
  const rewardAmount = await contract.rewardAmount()
  console.log('Reward Amount:', rewardAmount.toString())

  const owner = await contract.owner()
  console.log('Owner:', owner)

  // Memanggil function dengan parameter
  const userAddress = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
  const hasClaimed = await contract.hasClaimed(userAddress)
  console.log('Has Claimed:', hasClaimed)

  const userReward = await contract.rewards(userAddress)
  console.log('User Reward:', userReward.toString())
}
```

### 3.3 Handling BigInt

Solidity `uint256` di-return sebagai JavaScript `BigInt`. Perlu di-convert untuk display:

```javascript
// ❌ Salah - BigInt tidak bisa langsung ditampilkan di beberapa kasus
const amount = await contract.rewardAmount()
console.log(amount) // 100n (BigInt)

// ✓ Benar - Convert ke string
console.log(amount.toString()) // "100"

// ✓ Untuk ETH dengan decimals
const balance = await provider.getBalance(address)
console.log(ethers.formatEther(balance)) // "10000.0"

// ✓ Untuk token dengan custom decimals
const tokenBalance = await tokenContract.balanceOf(address)
console.log(ethers.formatUnits(tokenBalance, 18)) // format dengan 18 decimals
```

### 3.4 Parallel Calls

Untuk efisiensi, panggil multiple view functions secara parallel:

```javascript
async function readAllData() {
  const provider = new ethers.BrowserProvider(window.ethereum)
  const contract = new ethers.Contract(CONTRACT_ADDRESS, ABI, provider)

  // ❌ Sequential - lambat
  const rewardAmount = await contract.rewardAmount()
  const owner = await contract.owner()
  const hasClaimed = await contract.hasClaimed(userAddress)

  // ✓ Parallel - lebih cepat
  const [rewardAmount, owner, hasClaimed] = await Promise.all([
    contract.rewardAmount(),
    contract.owner(),
    contract.hasClaimed(userAddress)
  ])

  return { rewardAmount, owner, hasClaimed }
}
```

---

## 4. State Management dengan React

### 4.1 Basic Pattern

> **Pola Dasar React + Blockchain:**
>
> Saat membuat komponen yang membaca data dari blockchain, kita selalu butuh 3 state:
>
> | State | Fungsi | Nilai Awal |
> |-------|--------|------------|
> | `data` | Menyimpan hasil dari blockchain | `null` |
> | `loading` | Menandakan sedang fetch data | `true` |
> | `error` | Menyimpan pesan error jika gagal | `null` |
>
> **Alur yang terjadi:**
> ```
> Komponen mount → loading=true → Fetch data →
>   ├─ Sukses: data=hasil, loading=false
>   └─ Gagal: error=pesan, loading=false
> ```
>
> **Kenapa pakai useEffect?**
> - Fetch data otomatis saat komponen pertama kali tampil
> - Bisa di-trigger ulang saat dependencies berubah

```jsx
import { useState, useEffect } from 'react'
import { ethers } from 'ethers'
import CourseRewardABI from './contracts/CourseReward.json'

const CONTRACT_ADDRESS = '0x5FbDB2315678afecb367f032d93F642f64180aa3'

function ContractInfo() {
  // States
  const [rewardAmount, setRewardAmount] = useState(null)
  const [owner, setOwner] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch data saat component mount
  useEffect(() => {
    fetchContractData()
  }, [])

  const fetchContractData = async () => {
    try {
      setLoading(true)
      setError(null)

      const provider = new ethers.BrowserProvider(window.ethereum)
      const contract = new ethers.Contract(
        CONTRACT_ADDRESS,
        CourseRewardABI.abi,
        provider
      )

      const [amount, ownerAddress] = await Promise.all([
        contract.rewardAmount(),
        contract.owner()
      ])

      setRewardAmount(amount.toString())
      setOwner(ownerAddress)
    } catch (err) {
      console.error('Error fetching data:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  // Render
  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div>
      <h2>Contract Info</h2>
      <p>Reward Amount: {rewardAmount}</p>
      <p>Owner: {owner}</p>
      <button onClick={fetchContractData}>Refresh</button>
    </div>
  )
}

export default ContractInfo
```

### 4.2 State Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    REACT STATE FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Initial Mount                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  loading: true                                          │    │
│  │  data: null                                             │    │
│  │  error: null                                            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                  │
│                    useEffect triggers                           │
│                    fetchContractData()                          │
│                              │                                  │
│              ┌───────────────┴───────────────┐                  │
│              │                               │                  │
│         Success                          Error                  │
│              │                               │                  │
│              ▼                               ▼                  │
│  ┌─────────────────────┐       ┌─────────────────────┐          │
│  │  loading: false     │       │  loading: false     │          │
│  │  data: {...}        │       │  data: null         │          │
│  │  error: null        │       │  error: "message"   │          │
│  └─────────────────────┘       └─────────────────────┘          │
│                                                                 │
│  User clicks Refresh → Re-run fetchContractData()               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Handling User-Specific Data

Ketika user connect, kita perlu fetch data yang spesifik untuk user tersebut:

```jsx
function UserContractInfo({ userAddress }) {
  const [userData, setUserData] = useState({
    hasClaimed: false,
    rewards: '0'
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (userAddress) {
      fetchUserData()
    }
  }, [userAddress]) // Re-fetch ketika address berubah

  const fetchUserData = async () => {
    try {
      setLoading(true)

      const provider = new ethers.BrowserProvider(window.ethereum)
      const contract = new ethers.Contract(
        CONTRACT_ADDRESS,
        CourseRewardABI.abi,
        provider
      )

      const [hasClaimed, rewards] = await Promise.all([
        contract.hasClaimed(userAddress),
        contract.rewards(userAddress)
      ])

      setUserData({
        hasClaimed,
        rewards: rewards.toString()
      })
    } catch (err) {
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div>Loading user data...</div>

  return (
    <div>
      <h3>Your Status</h3>
      <p>Has Claimed: {userData.hasClaimed ? 'Yes' : 'No'}</p>
      <p>Your Rewards: {userData.rewards}</p>
    </div>
  )
}
```

---

## 5. Custom Hook: useContract

### 5.1 Membuat useContract Hook

Custom hooks memungkinkan kita me-reuse logic di multiple components.

> **Apa itu Custom Hook?**
>
> Custom hook adalah function yang dimulai dengan `use` dan bisa menggunakan React hooks lainnya. Tujuannya untuk **mengumpulkan logic yang sering dipakai** agar tidak perlu ditulis ulang di setiap komponen.
>
> **Kenapa butuh useContract?**
>
> Tanpa custom hook, di setiap komponen kita harus:
> ```javascript
> // Kode ini harus ditulis di SETIAP komponen 😫
> const provider = new ethers.BrowserProvider(window.ethereum)
> const contract = new ethers.Contract(address, abi, provider)
> const result = await contract.someFunction()
> ```
>
> Dengan `useContract`, cukup:
> ```javascript
> // Sekali tulis, pakai di mana saja 😊
> const { contract, read } = useContract(address, abi)
> const result = await read('someFunction')
> ```
>
> **Langkah membuat custom hook:**
> 1. Buat file baru di `src/hooks/`
> 2. Export function yang dimulai dengan `use`
> 3. Gunakan React hooks di dalamnya (useState, useEffect, dll)

**frontend/src/hooks/useContract.js:**
```javascript
import { useState, useEffect, useCallback } from 'react'
import { ethers } from 'ethers'

/**
 * Custom hook untuk berinteraksi dengan smart contract
 * @param {string} contractAddress - Address contract
 * @param {Array} contractABI - ABI contract
 * @param {object} options - Options { providerType: 'browser' | 'jsonrpc' }
 */
export function useContract(contractAddress, contractABI, options = {}) {
  const [contract, setContract] = useState(null)
  const [provider, setProvider] = useState(null)
  const [signer, setSigner] = useState(null)
  const [isReady, setIsReady] = useState(false)
  const [error, setError] = useState(null)

  // Initialize contract
  useEffect(() => {
    const init = async () => {
      try {
        setError(null)

        // Check if MetaMask is available
        if (typeof window.ethereum === 'undefined') {
          throw new Error('MetaMask not installed')
        }

        // Create provider
        const browserProvider = new ethers.BrowserProvider(window.ethereum)
        setProvider(browserProvider)

        // Create read-only contract
        const contractInstance = new ethers.Contract(
          contractAddress,
          contractABI,
          browserProvider
        )
        setContract(contractInstance)

        setIsReady(true)
      } catch (err) {
        console.error('Error initializing contract:', err)
        setError(err.message)
      }
    }

    if (contractAddress && contractABI) {
      init()
    }
  }, [contractAddress, contractABI])

  // Get signer and contract with signer
  const connectSigner = useCallback(async () => {
    if (!provider) return null

    try {
      const signerInstance = await provider.getSigner()
      setSigner(signerInstance)

      // Return contract connected to signer
      const contractWithSigner = new ethers.Contract(
        contractAddress,
        contractABI,
        signerInstance
      )

      return contractWithSigner
    } catch (err) {
      console.error('Error connecting signer:', err)
      setError(err.message)
      return null
    }
  }, [provider, contractAddress, contractABI])

  // Helper: Call view function
  const read = useCallback(async (functionName, ...args) => {
    if (!contract) throw new Error('Contract not initialized')

    try {
      const result = await contract[functionName](...args)
      return result
    } catch (err) {
      console.error(`Error calling ${functionName}:`, err)
      throw err
    }
  }, [contract])

  return {
    contract,
    provider,
    signer,
    isReady,
    error,
    connectSigner,
    read
  }
}
```

### 5.2 Menggunakan useContract

```jsx
import { useContract } from './hooks/useContract'
import CourseRewardABI from './contracts/CourseReward.json'

const CONTRACT_ADDRESS = '0x5FbDB2315678afecb367f032d93F642f64180aa3'

function Dashboard() {
  const { contract, isReady, error, read } = useContract(
    CONTRACT_ADDRESS,
    CourseRewardABI.abi
  )

  const [data, setData] = useState({
    rewardAmount: null,
    owner: null
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (isReady) {
      loadData()
    }
  }, [isReady])

  const loadData = async () => {
    try {
      setLoading(true)

      const [rewardAmount, owner] = await Promise.all([
        read('rewardAmount'),
        read('owner')
      ])

      setData({
        rewardAmount: rewardAmount.toString(),
        owner
      })
    } catch (err) {
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (error) return <div>Error: {error}</div>
  if (!isReady || loading) return <div>Loading...</div>

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Reward Amount: {data.rewardAmount}</p>
      <p>Owner: {data.owner}</p>
    </div>
  )
}
```

---

## 6. Custom Hook: useWallet

### 6.1 Membuat useWallet Hook

> **Apa yang dilakukan useWallet?**
>
> Hook ini menangani semua hal yang berhubungan dengan wallet:
>
> | Fitur | Penjelasan |
> |-------|------------|
> | `connect()` | Memunculkan popup MetaMask |
> | `disconnect()` | Reset semua state |
> | `account` | Address wallet yang terhubung |
> | `balance` | Saldo ETH wallet |
> | `chainId` | Network mana yang aktif (Hardhat=31337, Sepolia=11155111) |
> | `isConnected` | Boolean apakah sudah connect |
>
> **Event listeners yang dihandle:**
> - `accountsChanged` → User ganti account di MetaMask
> - `chainChanged` → User ganti network
>
> **Cara pakai nanti:**
> ```jsx
> function MyComponent() {
>   const { account, balance, connect, isConnected } = useWallet()
>   // Langsung pakai!
> }
> ```

**frontend/src/hooks/useWallet.js:**
```javascript
import { useState, useEffect, useCallback } from 'react'
import { ethers } from 'ethers'

/**
 * Custom hook untuk manage wallet connection
 */
export function useWallet() {
  const [account, setAccount] = useState(null)
  const [chainId, setChainId] = useState(null)
  const [balance, setBalance] = useState(null)
  const [isConnecting, setIsConnecting] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState(null)

  // Check if MetaMask installed
  const isMetaMaskInstalled = useCallback(() => {
    return typeof window.ethereum !== 'undefined'
  }, [])

  // Get provider
  const getProvider = useCallback(() => {
    if (!isMetaMaskInstalled()) return null
    return new ethers.BrowserProvider(window.ethereum)
  }, [isMetaMaskInstalled])

  // Get signer
  const getSigner = useCallback(async () => {
    const provider = getProvider()
    if (!provider) return null
    return await provider.getSigner()
  }, [getProvider])

  // Connect wallet
  const connect = useCallback(async () => {
    if (!isMetaMaskInstalled()) {
      setError('MetaMask not installed')
      return false
    }

    setIsConnecting(true)
    setError(null)

    try {
      // Request accounts
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts'
      })

      if (accounts.length > 0) {
        setAccount(accounts[0])
        setIsConnected(true)

        // Get chain ID
        const chainIdHex = await window.ethereum.request({
          method: 'eth_chainId'
        })
        setChainId(parseInt(chainIdHex, 16))

        // Get balance
        const provider = getProvider()
        const balance = await provider.getBalance(accounts[0])
        setBalance(ethers.formatEther(balance))

        return true
      }

      return false
    } catch (err) {
      console.error('Error connecting:', err)
      if (err.code === 4001) {
        setError('Connection rejected by user')
      } else {
        setError(err.message)
      }
      return false
    } finally {
      setIsConnecting(false)
    }
  }, [isMetaMaskInstalled, getProvider])

  // Disconnect wallet
  const disconnect = useCallback(() => {
    setAccount(null)
    setChainId(null)
    setBalance(null)
    setIsConnected(false)
    setError(null)
  }, [])

  // Update balance
  const updateBalance = useCallback(async () => {
    if (!account) return

    try {
      const provider = getProvider()
      const balance = await provider.getBalance(account)
      setBalance(ethers.formatEther(balance))
    } catch (err) {
      console.error('Error updating balance:', err)
    }
  }, [account, getProvider])

  // Switch network
  const switchNetwork = useCallback(async (targetChainId) => {
    if (!isMetaMaskInstalled()) return false

    try {
      await window.ethereum.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: `0x${targetChainId.toString(16)}` }]
      })
      return true
    } catch (err) {
      console.error('Error switching network:', err)
      setError(err.message)
      return false
    }
  }, [isMetaMaskInstalled])

  // Listen for account changes
  useEffect(() => {
    if (!isMetaMaskInstalled()) return

    const handleAccountsChanged = (accounts) => {
      if (accounts.length > 0) {
        setAccount(accounts[0])
        setIsConnected(true)
        updateBalance()
      } else {
        disconnect()
      }
    }

    const handleChainChanged = (chainIdHex) => {
      setChainId(parseInt(chainIdHex, 16))
      updateBalance()
    }

    window.ethereum.on('accountsChanged', handleAccountsChanged)
    window.ethereum.on('chainChanged', handleChainChanged)

    // Check if already connected
    window.ethereum.request({ method: 'eth_accounts' })
      .then(accounts => {
        if (accounts.length > 0) {
          handleAccountsChanged(accounts)
          window.ethereum.request({ method: 'eth_chainId' })
            .then(chainIdHex => handleChainChanged(chainIdHex))
        }
      })

    return () => {
      window.ethereum.removeListener('accountsChanged', handleAccountsChanged)
      window.ethereum.removeListener('chainChanged', handleChainChanged)
    }
  }, [isMetaMaskInstalled, disconnect, updateBalance])

  // Format address for display
  const formatAddress = useCallback((address) => {
    if (!address) return ''
    return `${address.slice(0, 6)}...${address.slice(-4)}`
  }, [])

  return {
    account,
    chainId,
    balance,
    isConnecting,
    isConnected,
    error,
    connect,
    disconnect,
    updateBalance,
    switchNetwork,
    getProvider,
    getSigner,
    formatAddress,
    isMetaMaskInstalled: isMetaMaskInstalled()
  }
}
```

### 6.2 Menggunakan useWallet

```jsx
import { useWallet } from './hooks/useWallet'

function Navbar() {
  const {
    account,
    balance,
    isConnecting,
    isConnected,
    error,
    connect,
    disconnect,
    formatAddress
  } = useWallet()

  return (
    <nav className="navbar">
      <h1>My dApp</h1>

      {error && <span className="error">{error}</span>}

      {!isConnected ? (
        <button onClick={connect} disabled={isConnecting}>
          {isConnecting ? 'Connecting...' : 'Connect Wallet'}
        </button>
      ) : (
        <div className="wallet-info">
          <span>{formatAddress(account)}</span>
          <span>{parseFloat(balance).toFixed(4)} ETH</span>
          <button onClick={disconnect}>Disconnect</button>
        </div>
      )}
    </nav>
  )
}
```

---

## 7. Hands-on: Dashboard Contract

### 7.1 Struktur File

```
frontend/src/
├── hooks/
│   ├── useWallet.js
│   └── useContract.js
├── contracts/
│   ├── CourseReward.json
│   └── addresses.js
├── components/
│   ├── Navbar.jsx
│   ├── ContractInfo.jsx
│   └── UserStatus.jsx
├── App.jsx
├── App.css
└── main.jsx
```

### 7.2 Contract Addresses

**frontend/src/contracts/addresses.js:**
```javascript
export const CONTRACT_ADDRESSES = {
  31337: { // Hardhat
    courseReward: '0x5FbDB2315678afecb367f032d93F642f64180aa3'
  },
  1337: { // Ganache
    courseReward: '0x5FbDB2315678afecb367f032d93F642f64180aa3'
  }
}

export function getAddress(contractName, chainId) {
  return CONTRACT_ADDRESSES[chainId]?.[contractName] || null
}
```

### 7.3 Komponen Navbar

> **Komponen Navbar menampilkan:**
> - Nama dApp di kiri
> - Info network (Hardhat, Sepolia, dll)
> - Tombol Connect Wallet / Info wallet yang terhubung di kanan
>
> **Fitur penting:**
> - Saat belum connect → tampil tombol "Connect Wallet"
> - Saat sudah connect → tampil address (disingkat) + balance + tombol Disconnect
> - Menampilkan badge nama network agar user tahu di network mana
>
> **Cara menyingkat address:**
> ```
> 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
> ↓ formatAddress()
> 0xf39F...2266
> ```

**frontend/src/components/Navbar.jsx:**
```jsx
import { useWallet } from '../hooks/useWallet'
import './Navbar.css'

function Navbar() {
  const {
    account,
    chainId,
    balance,
    isConnecting,
    isConnected,
    connect,
    disconnect,
    formatAddress
  } = useWallet()

  const getNetworkName = (chainId) => {
    const networks = {
      1: 'Ethereum',
      5: 'Goerli',
      11155111: 'Sepolia',
      31337: 'Hardhat',
      1337: 'Ganache'
    }
    return networks[chainId] || `Chain ${chainId}`
  }

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>CourseReward dApp</h1>
      </div>

      <div className="navbar-wallet">
        {isConnected && chainId && (
          <span className="network-badge">
            {getNetworkName(chainId)}
          </span>
        )}

        {!isConnected ? (
          <button
            onClick={connect}
            disabled={isConnecting}
            className="btn btn-primary"
          >
            {isConnecting ? 'Connecting...' : 'Connect Wallet'}
          </button>
        ) : (
          <div className="wallet-connected">
            <span className="balance">
              {parseFloat(balance).toFixed(4)} ETH
            </span>
            <span className="address">
              {formatAddress(account)}
            </span>
            <button onClick={disconnect} className="btn btn-secondary">
              Disconnect
            </button>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
```

**frontend/src/components/Navbar.css:**
```css
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  margin-bottom: 30px;
}

.navbar-brand h1 {
  color: white;
  font-size: 1.5rem;
  margin: 0;
}

.navbar-wallet {
  display: flex;
  align-items: center;
  gap: 15px;
}

.network-badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 6px 12px;
  border-radius: 20px;
  color: white;
  font-size: 0.85rem;
}

.wallet-connected {
  display: flex;
  align-items: center;
  gap: 12px;
}

.balance {
  color: #4CAF50;
  font-weight: 600;
}

.address {
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 8px;
  color: white;
  font-family: monospace;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background: #45a049;
}

.btn-secondary {
  background: #ff5722;
  color: white;
}

.btn-secondary:hover {
  background: #f4511e;
}

.btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
```

### 7.4 Komponen ContractInfo

> **Komponen ini menampilkan info umum contract:**
> - Contract Address
> - Owner address
> - Reward Amount (berapa poin per claim)
>
> **Alur kerja komponen:**
> 1. Cek apakah wallet sudah connect
> 2. Ambil contract address berdasarkan chainId
> 3. Buat contract instance
> 4. Panggil `rewardAmount()` dan `owner()` secara paralel
> 5. Tampilkan hasilnya
>
> **Error handling yang perlu diperhatikan:**
> - Wallet belum connect → tampilkan pesan "Connect wallet to view"
> - Contract tidak ada di network ini → tampilkan pesan error
> - Gagal fetch data → tampilkan error + tombol Retry

**frontend/src/components/ContractInfo.jsx:**
```jsx
import { useState, useEffect } from 'react'
import { useContract } from '../hooks/useContract'
import { useWallet } from '../hooks/useWallet'
import CourseRewardABI from '../contracts/CourseReward.json'
import { getAddress } from '../contracts/addresses'
import './ContractInfo.css'

function ContractInfo() {
  const { chainId, isConnected } = useWallet()
  const contractAddress = getAddress('courseReward', chainId)

  const { contract, isReady, error: contractError } = useContract(
    contractAddress,
    CourseRewardABI.abi
  )

  const [data, setData] = useState({
    rewardAmount: null,
    owner: null
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (isReady && contract) {
      loadContractData()
    }
  }, [isReady, contract])

  const loadContractData = async () => {
    try {
      setLoading(true)
      setError(null)

      const [rewardAmount, owner] = await Promise.all([
        contract.rewardAmount(),
        contract.owner()
      ])

      setData({
        rewardAmount: rewardAmount.toString(),
        owner
      })
    } catch (err) {
      console.error('Error loading contract data:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const formatAddress = (address) => {
    if (!address) return ''
    return `${address.slice(0, 10)}...${address.slice(-8)}`
  }

  if (!isConnected) {
    return (
      <div className="card">
        <h2>Contract Information</h2>
        <p className="muted">Connect wallet to view contract info</p>
      </div>
    )
  }

  if (!contractAddress) {
    return (
      <div className="card">
        <h2>Contract Information</h2>
        <p className="error">Contract not deployed on this network</p>
      </div>
    )
  }

  if (contractError || error) {
    return (
      <div className="card">
        <h2>Contract Information</h2>
        <p className="error">Error: {contractError || error}</p>
        <button onClick={loadContractData} className="btn btn-primary">
          Retry
        </button>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="card">
        <h2>Contract Information</h2>
        <div className="loading">Loading contract data...</div>
      </div>
    )
  }

  return (
    <div className="card">
      <h2>Contract Information</h2>

      <div className="info-grid">
        <div className="info-item">
          <label>Contract Address</label>
          <span className="mono">{formatAddress(contractAddress)}</span>
        </div>

        <div className="info-item">
          <label>Owner</label>
          <span className="mono">{formatAddress(data.owner)}</span>
        </div>

        <div className="info-item">
          <label>Reward Amount</label>
          <span className="value">{data.rewardAmount} Points</span>
        </div>
      </div>

      <button onClick={loadContractData} className="btn btn-secondary refresh-btn">
        Refresh
      </button>
    </div>
  )
}

export default ContractInfo
```

**frontend/src/components/ContractInfo.css:**
```css
.card {
  background: white;
  border-radius: 16px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.card h2 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.25rem;
}

.info-grid {
  display: grid;
  gap: 15px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-item label {
  color: #666;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-item span {
  color: #333;
  font-size: 1rem;
}

.info-item .mono {
  font-family: monospace;
  background: #f5f5f5;
  padding: 8px 12px;
  border-radius: 6px;
  word-break: break-all;
}

.info-item .value {
  font-weight: 600;
  color: #4CAF50;
  font-size: 1.2rem;
}

.muted {
  color: #999;
  font-style: italic;
}

.error {
  color: #f44336;
}

.loading {
  color: #2196F3;
  font-style: italic;
}

.refresh-btn {
  width: 100%;
  margin-top: 10px;
}
```

### 7.5 Komponen UserStatus

> **Komponen ini menampilkan status user yang sedang login:**
> - Sudah claim atau belum (badge hijau/oranye)
> - Total reward yang sudah dikumpulkan
>
> **Perbedaan dengan ContractInfo:**
> - ContractInfo → data umum contract (sama untuk semua orang)
> - UserStatus → data spesifik per user (berbeda tiap address)
>
> **Re-fetch otomatis:**
> Komponen ini akan refetch data setiap kali `account` berubah (user ganti wallet di MetaMask).

**frontend/src/components/UserStatus.jsx:**
```jsx
import { useState, useEffect } from 'react'
import { useContract } from '../hooks/useContract'
import { useWallet } from '../hooks/useWallet'
import CourseRewardABI from '../contracts/CourseReward.json'
import { getAddress } from '../contracts/addresses'
import './UserStatus.css'

function UserStatus() {
  const { account, chainId, isConnected } = useWallet()
  const contractAddress = getAddress('courseReward', chainId)

  const { contract, isReady } = useContract(
    contractAddress,
    CourseRewardABI.abi
  )

  const [userData, setUserData] = useState({
    hasClaimed: false,
    rewards: '0'
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (isReady && contract && account) {
      loadUserData()
    }
  }, [isReady, contract, account])

  const loadUserData = async () => {
    try {
      setLoading(true)

      const [hasClaimed, rewards] = await Promise.all([
        contract.hasClaimed(account),
        contract.rewards(account)
      ])

      setUserData({
        hasClaimed,
        rewards: rewards.toString()
      })
    } catch (err) {
      console.error('Error loading user data:', err)
    } finally {
      setLoading(false)
    }
  }

  if (!isConnected) {
    return (
      <div className="card">
        <h2>Your Status</h2>
        <p className="muted">Connect wallet to view your status</p>
      </div>
    )
  }

  if (!contractAddress) {
    return null
  }

  if (loading) {
    return (
      <div className="card">
        <h2>Your Status</h2>
        <div className="loading">Loading...</div>
      </div>
    )
  }

  return (
    <div className="card">
      <h2>Your Status</h2>

      <div className="status-grid">
        <div className="status-item">
          <span className="status-label">Claim Status</span>
          <span className={`status-badge ${userData.hasClaimed ? 'claimed' : 'not-claimed'}`}>
            {userData.hasClaimed ? 'Claimed' : 'Not Claimed'}
          </span>
        </div>

        <div className="status-item">
          <span className="status-label">Your Rewards</span>
          <span className="rewards-value">{userData.rewards} Points</span>
        </div>
      </div>

      <button onClick={loadUserData} className="btn btn-secondary">
        Refresh Status
      </button>
    </div>
  )
}

export default UserStatus
```

**frontend/src/components/UserStatus.css:**
```css
.status-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.status-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-label {
  color: #666;
  font-size: 0.85rem;
  text-transform: uppercase;
}

.status-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  text-align: center;
}

.status-badge.claimed {
  background: #e8f5e9;
  color: #2e7d32;
}

.status-badge.not-claimed {
  background: #fff3e0;
  color: #ef6c00;
}

.rewards-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #4CAF50;
}
```

### 7.6 Main App Component

> **App.jsx adalah komponen utama yang menyatukan semuanya:**
>
> ```
> App
> ├── Navbar          → Header dengan tombol connect
> ├── Global Error    → Tampilkan error jika ada
> └── Main Content
>     ├── ContractInfo  → Info contract (reward amount, owner)
>     └── UserStatus    → Status user (sudah claim?, total rewards)
> ```
>
> **Flow data:**
> 1. User connect wallet di Navbar
> 2. ContractInfo dan UserStatus membaca chainId untuk mendapatkan contract address
> 3. Data di-fetch dari blockchain
> 4. UI di-render dengan data tersebut

**frontend/src/App.jsx:**
```jsx
import Navbar from './components/Navbar'
import ContractInfo from './components/ContractInfo'
import UserStatus from './components/UserStatus'
import { useWallet } from './hooks/useWallet'
import './App.css'

function App() {
  const { error, isMetaMaskInstalled } = useWallet()

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
        <div className="grid">
          <ContractInfo />
          <UserStatus />
        </div>
      </main>
    </div>
  )
}

export default App
```

**frontend/src/App.css:**
```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.app {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.main-content {
  padding: 20px 0;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.global-error {
  background: #ffebee;
  color: #c62828;
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #c62828;
}

.metamask-warning {
  background: white;
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  margin-top: 50px;
}

.metamask-warning h2 {
  color: #333;
  margin-bottom: 15px;
}

.metamask-warning p {
  color: #666;
  margin-bottom: 25px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background: #45a049;
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}
```

### 7.7 Menjalankan Aplikasi

1. **Terminal 1 - Hardhat Node & Deploy:**
```bash
cd contracts
npx hardhat node

# Terminal baru untuk deploy
npx hardhat run scripts/deploy.js --network localhost
```

2. **Catat contract address dari output deploy** dan update di `frontend/src/contracts/addresses.js`

3. **Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

4. **Browser:** Buka `http://localhost:5173`

---

## 8. Error Handling

### 8.1 Common Errors

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMMON ERRORS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. MetaMask Not Installed                                      │
│     Error: window.ethereum is undefined                         │
│     Solution: Check if MetaMask installed before accessing      │
│                                                                 │
│  2. User Rejected Request                                       │
│     Error code: 4001                                            │
│     Solution: Show user-friendly message, allow retry           │
│                                                                 │
│  3. Wrong Network                                               │
│     Error: Contract not found / call exception                  │
│     Solution: Check chainId, prompt network switch              │
│                                                                 │
│  4. Contract Not Deployed                                       │
│     Error: call revert exception                                │
│     Solution: Verify contract address is correct                │
│                                                                 │
│  5. Invalid Parameters                                          │
│     Error: missing argument / invalid value                     │
│     Solution: Validate inputs before calling                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Error Handling Pattern

```javascript
async function safeContractCall(contract, functionName, ...args) {
  try {
    const result = await contract[functionName](...args)
    return { success: true, data: result }
  } catch (err) {
    console.error(`Error calling ${functionName}:`, err)

    // Parse error
    let errorMessage = 'An error occurred'

    if (err.code === 'CALL_EXCEPTION') {
      errorMessage = 'Contract call failed. Check if contract is deployed.'
    } else if (err.code === 'NETWORK_ERROR') {
      errorMessage = 'Network error. Check your connection.'
    } else if (err.reason) {
      errorMessage = err.reason
    } else if (err.message) {
      errorMessage = err.message
    }

    return { success: false, error: errorMessage }
  }
}

// Usage
const result = await safeContractCall(contract, 'rewardAmount')
if (result.success) {
  console.log('Reward:', result.data.toString())
} else {
  console.error('Error:', result.error)
}
```

---

## 9. Best Practices

### 9.1 Performance Tips

```
┌─────────────────────────────────────────────────────────────────┐
│                    BEST PRACTICES                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Use Promise.all for parallel reads                          │
│     ────────────────────────────────────────────                │
│     // Bad: Sequential                                          │
│     const a = await contract.funcA()                            │
│     const b = await contract.funcB()                            │
│                                                                 │
│     // Good: Parallel                                           │
│     const [a, b] = await Promise.all([                          │
│       contract.funcA(),                                         │
│       contract.funcB()                                          │
│     ])                                                          │
│                                                                 │
│  2. Memoize contract instances                                  │
│     ────────────────────────────────────────────                │
│     // Create contract once, reuse everywhere                   │
│     const contract = useMemo(() =>                              │
│       new Contract(address, abi, provider),                     │
│       [address, provider]                                       │
│     )                                                           │
│                                                                 │
│  3. Handle loading states properly                              │
│     ────────────────────────────────────────────                │
│     Show loading indicator while fetching                       │
│     Disable buttons during transactions                         │
│                                                                 │
│  4. Cache data when appropriate                                 │
│     ────────────────────────────────────────────                │
│     Don't re-fetch data that rarely changes                     │
│     Use React state or context for caching                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Code Organization

```
src/
├── components/          # UI components
├── hooks/               # Custom hooks (useWallet, useContract)
├── contracts/           # ABI files and addresses
├── utils/               # Helper functions
│   ├── formatters.js    # Format address, numbers
│   └── errors.js        # Error handling utilities
├── constants/           # App constants
└── contexts/            # React contexts (if needed)
```

---

## Ringkasan

| Topik                | Poin Penting                                      |
| -------------------- | ------------------------------------------------- |
| **Provider**       | Read-only connection ke blockchain                |
| **Signer**         | Provider + ability to sign (dari wallet)          |
| **Contract**       | Instance untuk interact (address + ABI + provider)|
| **View Functions** | Read-only, no gas, instant                        |
| **Custom Hooks**   | Reusable logic (useWallet, useContract)           |
| **State Flow**     | loading -> success/error -> display               |

---

## Tugas

### Tugas 1: Implementasi Dashboard

1. Implementasikan semua komponen dari hands-on
2. Pastikan contract info dan user status tampil dengan benar
3. Screenshot tampilan dashboard

### Tugas 2: Tambah Komponen All Users

Buat komponen baru `AllUsers.jsx` yang menampilkan:
- Total users yang sudah claim (hint: perlu tracking di contract atau off-chain)
- List address yang sudah claim (jika ada event listener)

### Tugas 3: Network Switcher

1. Buat komponen yang mendeteksi jika user di wrong network
2. Tampilkan warning dan tombol "Switch Network"
3. Implementasi auto switch ke Hardhat network

### Deliverable

Kumpulkan:
1. Screenshot dashboard dengan semua komponen
2. File custom hooks (`useWallet.js`, `useContract.js`)
3. File komponen yang sudah dibuat
4. Screenshot network switcher (Tugas 3)

---

## Referensi

- [ethers.js v6 Documentation](https://docs.ethers.org/v6/)
- [React Hooks Documentation](https://react.dev/reference/react)
- [MetaMask JSON-RPC API](https://docs.metamask.io/wallet/reference/json-rpc-api/)
