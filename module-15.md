# Modul 15. dApp Advanced Features & Deployment

## Deskripsi

Modul ini membahas **fitur-fitur lanjutan** dalam pengembangan dApp, termasuk real-time event listening, optimasi UX, deployment ke testnet, dan best practices untuk production.

## Tujuan Pembelajaran

Setelah menyelesaikan modul ini, mahasiswa mampu:

1. Implementasi real-time event listening
2. Membuat notification system untuk events
3. Optimasi loading dan caching
4. Deploy smart contract ke testnet (Sepolia)
5. Deploy frontend ke hosting (Vercel/Netlify)
6. Menerapkan best practices untuk production dApp

## Prasyarat

- Sudah menyelesaikan Module 12-14
- dApp berfungsi penuh di local environment
- Memiliki akun GitHub untuk deployment

## List of Contents

- [Deskripsi](#deskripsi)
- [Tujuan Pembelajaran](#tujuan-pembelajaran)
- [Prasyarat](#prasyarat)
- [1. Real-time Event Listening](#1-real-time-event-listening)
- [2. Notification System](#2-notification-system)
- [3. Loading & Caching Optimization](#3-loading--caching-optimization)
- [4. Context API untuk Global State](#4-context-api-untuk-global-state)
- [5. Deploy ke Testnet (Sepolia)](#5-deploy-ke-testnet-sepolia)
- [6. Environment Variables](#6-environment-variables)
- [7. Deploy Frontend ke Vercel](#7-deploy-frontend-ke-vercel)
- [8. Production Best Practices](#8-production-best-practices)
- [9. Final Project: Complete dApp](#9-final-project-complete-dapp)
- [Ringkasan](#ringkasan)
- [Tugas](#tugas)

---

## 1. Real-time Event Listening

### 1.1 Event Listener Hook

> **Custom Hook untuk Event Listening:**
>
> Hook ini memudahkan kita mendengarkan event dari smart contract. Cukup berikan contract instance dan nama event, hook akan handle sisanya.
>
> **Fitur yang disediakan:**
> | Return Value | Fungsi |
> |--------------|--------|
> | `events` | Array event yang sudah diterima |
> | `isListening` | Boolean apakah sedang aktif listen |
> | `startListening()` | Mulai listen real-time |
> | `stopListening()` | Berhenti listen |
> | `fetchPastEvents()` | Ambil event yang sudah terjadi |
>
> **Cara pakai:**
> ```jsx
> const { events, startListening } = useContractEvents(
>   contract,
>   'RewardClaimed',
>   (data) => console.log('New claim!', data)
> )
> ```

**frontend/src/hooks/useContractEvents.js:**
```javascript
import { useState, useEffect, useCallback } from 'react'
import { ethers } from 'ethers'

/**
 * Custom hook for listening to contract events
 * @param {ethers.Contract} contract - Contract instance
 * @param {string} eventName - Name of the event to listen
 * @param {Function} callback - Callback when event received
 */
export function useContractEvents(contract, eventName, callback) {
  const [events, setEvents] = useState([])
  const [isListening, setIsListening] = useState(false)

  // Start listening
  const startListening = useCallback(() => {
    if (!contract || !eventName) return

    setIsListening(true)

    contract.on(eventName, (...args) => {
      // Last argument is event object
      const event = args[args.length - 1]
      const eventData = {
        args: args.slice(0, -1),
        event,
        timestamp: Date.now()
      }

      setEvents(prev => [eventData, ...prev].slice(0, 50)) // Keep last 50
      callback?.(eventData)
    })
  }, [contract, eventName, callback])

  // Stop listening
  const stopListening = useCallback(() => {
    if (!contract || !eventName) return

    contract.off(eventName)
    setIsListening(false)
  }, [contract, eventName])

  // Fetch past events
  const fetchPastEvents = useCallback(async (fromBlock = 0) => {
    if (!contract || !eventName) return []

    try {
      const filter = contract.filters[eventName]()
      const pastEvents = await contract.queryFilter(filter, fromBlock, 'latest')

      const formattedEvents = pastEvents.map(e => ({
        args: e.args,
        event: e,
        timestamp: null, // Would need block timestamp
        blockNumber: e.blockNumber
      }))

      setEvents(formattedEvents.reverse())
      return formattedEvents
    } catch (err) {
      console.error('Error fetching past events:', err)
      return []
    }
  }, [contract, eventName])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (contract && eventName) {
        contract.off(eventName)
      }
    }
  }, [contract, eventName])

  return {
    events,
    isListening,
    startListening,
    stopListening,
    fetchPastEvents,
    clearEvents: () => setEvents([])
  }
}
```

### 1.2 Event History Component

> **Komponen Live Feed:**
>
> Komponen ini menampilkan riwayat claim secara real-time. Saat ada user lain claim reward, list akan otomatis update!
>
> **Yang ditampilkan per event:**
> - Address yang claim (disingkat)
> - Jumlah poin yang didapat
> - Block number
>
> **Indikator status:**
> - 🟢 "Live" = sedang aktif mendengarkan event baru
> - ⚪ "Disconnected" = tidak aktif
>
> **Animasi UX:**
> - Event baru muncul dari kiri (slide-in animation)
> - Status dot berkedip saat Live (pulse animation)

**frontend/src/components/EventHistory.jsx:**
```jsx
import { useState, useEffect, useMemo } from 'react'
import { ethers } from 'ethers'
import { useWallet } from '../hooks/useWallet'
import { useContractEvents } from '../hooks/useContractEvents'
import CourseRewardABI from '../contracts/CourseReward.json'
import { getAddress } from '../contracts/addresses'
import './EventHistory.css'

function EventHistory() {
  const { chainId, isConnected } = useWallet()
  const contractAddress = getAddress('courseReward', chainId)

  const [contract, setContract] = useState(null)

  // Initialize contract
  useEffect(() => {
    if (!isConnected || !contractAddress) {
      setContract(null)
      return
    }

    const provider = new ethers.BrowserProvider(window.ethereum)
    const contractInstance = new ethers.Contract(
      contractAddress,
      CourseRewardABI.abi,
      provider
    )
    setContract(contractInstance)
  }, [isConnected, contractAddress])

  // Event listener
  const {
    events,
    isListening,
    startListening,
    stopListening,
    fetchPastEvents
  } = useContractEvents(contract, 'RewardClaimed', (eventData) => {
    console.log('New claim event:', eventData)
  })

  // Fetch past events on mount
  useEffect(() => {
    if (contract) {
      fetchPastEvents()
      startListening()
    }

    return () => {
      stopListening()
    }
  }, [contract])

  const formatAddress = (addr) => `${addr.slice(0, 6)}...${addr.slice(-4)}`

  if (!isConnected) {
    return (
      <div className="card event-history">
        <h2>Recent Claims</h2>
        <p className="muted">Connect wallet to view events</p>
      </div>
    )
  }

  return (
    <div className="card event-history">
      <div className="event-header">
        <h2>Recent Claims</h2>
        <div className="event-status">
          <span className={`status-dot ${isListening ? 'active' : ''}`}></span>
          {isListening ? 'Live' : 'Disconnected'}
        </div>
      </div>

      {events.length === 0 ? (
        <p className="no-events">No claims yet</p>
      ) : (
        <ul className="event-list">
          {events.map((e, index) => (
            <li key={index} className="event-item">
              <div className="event-icon">
                <span>R</span>
              </div>
              <div className="event-details">
                <span className="event-address">
                  {formatAddress(e.args[0] || e.args.student)}
                </span>
                <span className="event-amount">
                  +{(e.args[1] || e.args.amount).toString()} Points
                </span>
              </div>
              {e.blockNumber && (
                <span className="event-block">Block #{e.blockNumber}</span>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default EventHistory
```

**frontend/src/components/EventHistory.css:**
```css
.event-history {
  max-height: 400px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.event-header h2 {
  margin: 0;
}

.event-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: #666;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ccc;
}

.status-dot.active {
  background: #4CAF50;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.no-events {
  text-align: center;
  color: #999;
  padding: 30px 0;
}

.event-list {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
  flex: 1;
}

.event-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  background: #f9f9f9;
  margin-bottom: 8px;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.event-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4CAF50, #8BC34A);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 0.9rem;
}

.event-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.event-address {
  font-family: monospace;
  font-size: 0.9rem;
  color: #333;
}

.event-amount {
  font-size: 0.85rem;
  color: #4CAF50;
  font-weight: 600;
}

.event-block {
  font-size: 0.75rem;
  color: #999;
}
```

---

## 2. Notification System

### 2.1 Toast Notification Context

> **Sistem Notifikasi Pop-up:**
>
> Toast adalah notifikasi kecil yang muncul di pojok layar, kemudian hilang otomatis. Sangat berguna untuk feedback user.
>
> **Tipe toast yang tersedia:**
> | Tipe | Warna | Kegunaan |
> |------|-------|----------|
> | `success` | Hijau | Transaksi berhasil |
> | `error` | Merah | Ada error |
> | `warning` | Oranye | Perlu perhatian |
> | `info` | Biru | Informasi umum |
>
> **Cara pakai di komponen:**
> ```jsx
> const toast = useToast()
>
> // Panggil sesuai kebutuhan
> toast.success('Transaction successful!')
> toast.error('Something went wrong')
> toast.warning('Please check your network')
> toast.info('Processing your request...')
> ```
>
> **Kenapa pakai Context?**
> Agar toast bisa dipanggil dari komponen mana saja tanpa prop drilling.

**frontend/src/contexts/ToastContext.jsx:**
```jsx
import { createContext, useContext, useState, useCallback } from 'react'
import './Toast.css'

const ToastContext = createContext()

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const addToast = useCallback((message, type = 'info', duration = 5000) => {
    const id = Date.now()
    const toast = { id, message, type }

    setToasts(prev => [...prev, toast])

    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }

    return id
  }, [])

  const removeToast = useCallback((id) => {
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  // Convenience methods
  const success = useCallback((msg, duration) =>
    addToast(msg, 'success', duration), [addToast])

  const error = useCallback((msg, duration) =>
    addToast(msg, 'error', duration), [addToast])

  const warning = useCallback((msg, duration) =>
    addToast(msg, 'warning', duration), [addToast])

  const info = useCallback((msg, duration) =>
    addToast(msg, 'info', duration), [addToast])

  return (
    <ToastContext.Provider value={{ addToast, removeToast, success, error, warning, info }}>
      {children}

      {/* Toast Container */}
      <div className="toast-container">
        {toasts.map(toast => (
          <div key={toast.id} className={`toast toast-${toast.type}`}>
            <span className="toast-message">{toast.message}</span>
            <button
              className="toast-close"
              onClick={() => removeToast(toast.id)}
            >
              ×
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  const context = useContext(ToastContext)
  if (!context) {
    throw new Error('useToast must be used within ToastProvider')
  }
  return context
}
```

**frontend/src/contexts/Toast.css:**
```css
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 20px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease;
  min-width: 250px;
  max-width: 400px;
}

.toast-success {
  border-left: 4px solid #4CAF50;
}

.toast-error {
  border-left: 4px solid #f44336;
}

.toast-warning {
  border-left: 4px solid #ff9800;
}

.toast-info {
  border-left: 4px solid #2196F3;
}

.toast-message {
  flex: 1;
  font-size: 0.95rem;
  color: #333;
}

.toast-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #999;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.toast-close:hover {
  color: #333;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
```

### 2.2 Using Toast in Components

```jsx
import { useToast } from '../contexts/ToastContext'

function ClaimReward() {
  const toast = useToast()

  const handleClaim = async () => {
    try {
      const tx = await contract.claimReward()
      toast.info('Transaction submitted...')

      await tx.wait()
      toast.success('Reward claimed successfully!')

    } catch (err) {
      if (err.code === 4001) {
        toast.warning('Transaction cancelled')
      } else {
        toast.error('Failed to claim: ' + err.message)
      }
    }
  }
}
```

### 2.3 Update main.jsx

**frontend/src/main.jsx:**
```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import { ToastProvider } from './contexts/ToastContext.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ToastProvider>
      <App />
    </ToastProvider>
  </React.StrictMode>,
)
```

---

## 3. Loading & Caching Optimization

### 3.1 Data Caching Hook

> **Kenapa Perlu Caching?**
>
> Setiap kali memanggil function contract = request ke RPC node. Jika terlalu sering:
> - Lambat (network latency)
> - Bisa kena rate limit
> - User experience buruk
>
> **Solusi: Cache data di memory**
>
> | Tanpa Cache | Dengan Cache |
> |-------------|--------------|
> | Setiap render = fetch lagi | Fetch sekali, pakai cache |
> | Lambat | Cepat |
> | Boros request | Hemat request |
>
> **Hook ini menyediakan:**
> - `data` → hasil fetch (dari cache jika masih valid)
> - `loading` → status loading
> - `refetch()` → paksa fetch ulang
> - `cacheTime` → berapa lama cache valid (default 30 detik)

**frontend/src/hooks/useContractData.js:**
```javascript
import { useState, useEffect, useCallback, useRef } from 'react'

/**
 * Custom hook for fetching and caching contract data
 */
export function useContractData(fetchFn, dependencies = [], options = {}) {
  const {
    cacheTime = 30000, // 30 seconds default
    refetchOnWindowFocus = true,
    enabled = true
  } = options

  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const lastFetchTime = useRef(0)
  const cachedData = useRef(null)

  const fetch = useCallback(async (force = false) => {
    if (!enabled) return

    const now = Date.now()
    const timeSinceLastFetch = now - lastFetchTime.current

    // Return cached data if within cache time
    if (!force && cachedData.current && timeSinceLastFetch < cacheTime) {
      setData(cachedData.current)
      setLoading(false)
      return cachedData.current
    }

    try {
      setLoading(true)
      setError(null)

      const result = await fetchFn()

      cachedData.current = result
      lastFetchTime.current = now

      setData(result)
      return result
    } catch (err) {
      console.error('Error fetching data:', err)
      setError(err.message)
      return null
    } finally {
      setLoading(false)
    }
  }, [fetchFn, cacheTime, enabled])

  // Initial fetch
  useEffect(() => {
    fetch()
  }, [...dependencies, fetch])

  // Refetch on window focus
  useEffect(() => {
    if (!refetchOnWindowFocus) return

    const handleFocus = () => {
      fetch()
    }

    window.addEventListener('focus', handleFocus)
    return () => window.removeEventListener('focus', handleFocus)
  }, [fetch, refetchOnWindowFocus])

  return {
    data,
    loading,
    error,
    refetch: () => fetch(true),
    invalidateCache: () => {
      cachedData.current = null
      lastFetchTime.current = 0
    }
  }
}
```

### 3.2 Using Cached Data

```jsx
import { useContractData } from '../hooks/useContractData'

function ContractInfo({ contract }) {
  const { data, loading, error, refetch } = useContractData(
    async () => {
      const [rewardAmount, owner] = await Promise.all([
        contract.rewardAmount(),
        contract.owner()
      ])
      return {
        rewardAmount: rewardAmount.toString(),
        owner
      }
    },
    [contract], // dependencies
    {
      cacheTime: 60000, // 1 minute cache
      refetchOnWindowFocus: true
    }
  )

  if (loading && !data) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div>
      <p>Reward: {data.rewardAmount}</p>
      <p>Owner: {data.owner}</p>
      <button onClick={refetch}>Refresh</button>
    </div>
  )
}
```

### 3.3 Skeleton Loading

> **Skeleton = Placeholder Saat Loading**
>
> Daripada menampilkan "Loading..." yang membosankan, skeleton menampilkan bentuk konten yang akan muncul dengan animasi shimmer.
>
> **Keuntungan Skeleton:**
> - User tahu bentuk UI yang akan muncul
> - Terasa lebih cepat secara psikologis
> - UI tidak "loncat" saat data muncul
>
> **Cara pakai:**
> ```jsx
> {loading ? <CardSkeleton /> : <ActualCard data={data} />}
> ```

**frontend/src/components/Skeleton.jsx:**
```jsx
import './Skeleton.css'

export function Skeleton({ width, height, borderRadius = '4px' }) {
  return (
    <div
      className="skeleton"
      style={{ width, height, borderRadius }}
    />
  )
}

export function CardSkeleton() {
  return (
    <div className="card">
      <Skeleton width="40%" height="24px" />
      <div style={{ marginTop: '20px' }}>
        <Skeleton width="100%" height="16px" />
        <Skeleton width="80%" height="16px" />
        <Skeleton width="60%" height="16px" />
      </div>
    </div>
  )
}
```

**frontend/src/components/Skeleton.css:**
```css
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

## 4. Context API untuk Global State

### 4.1 Web3 Context

> **Global State untuk Web3:**
>
> Web3Context menggabungkan semua state Web3 (wallet + contract) ke satu tempat. Semua komponen bisa akses tanpa perlu prop drilling.
>
> **Data yang disimpan:**
>
> | Kategori | Data |
> |----------|------|
> | **Wallet** | account, chainId, balance, isConnected |
> | **Contract** | contract instance, contractWithSigner |
> | **Contract Data** | rewardAmount, owner |
> | **User Data** | hasClaimed, rewards |
>
> **Actions yang tersedia:**
> - `connect()` → connect MetaMask
> - `disconnect()` → reset semua state
> - `refreshData()` → refetch semua data
>
> **Keuntungan pakai Context:**
> ```jsx
> // TANPA Context - prop drilling 😫
> <App>
>   <Navbar account={account} />
>   <Main>
>     <Dashboard account={account} contract={contract} />
>   </Main>
> </App>
>
> // DENGAN Context - bersih! 😊
> <Web3Provider>
>   <App />  // Semua child bisa akses via useWeb3()
> </Web3Provider>
> ```

**frontend/src/contexts/Web3Context.jsx:**
```jsx
import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { ethers } from 'ethers'
import CourseRewardABI from '../contracts/CourseReward.json'
import { getAddress } from '../contracts/addresses'

const Web3Context = createContext()

export function Web3Provider({ children }) {
  // Wallet state
  const [account, setAccount] = useState(null)
  const [chainId, setChainId] = useState(null)
  const [balance, setBalance] = useState(null)
  const [isConnected, setIsConnected] = useState(false)
  const [isConnecting, setIsConnecting] = useState(false)

  // Contract state
  const [contract, setContract] = useState(null)
  const [contractWithSigner, setContractWithSigner] = useState(null)

  // Contract data
  const [contractData, setContractData] = useState({
    rewardAmount: null,
    owner: null
  })
  const [userData, setUserData] = useState({
    hasClaimed: false,
    rewards: '0'
  })

  const isMetaMaskInstalled = typeof window.ethereum !== 'undefined'

  // Connect wallet
  const connect = useCallback(async () => {
    if (!isMetaMaskInstalled) return false

    setIsConnecting(true)
    try {
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts'
      })

      if (accounts.length > 0) {
        setAccount(accounts[0])
        setIsConnected(true)

        const chainIdHex = await window.ethereum.request({
          method: 'eth_chainId'
        })
        setChainId(parseInt(chainIdHex, 16))

        return true
      }
      return false
    } catch (err) {
      console.error('Connect error:', err)
      return false
    } finally {
      setIsConnecting(false)
    }
  }, [isMetaMaskInstalled])

  // Disconnect
  const disconnect = useCallback(() => {
    setAccount(null)
    setChainId(null)
    setBalance(null)
    setIsConnected(false)
    setContract(null)
    setContractWithSigner(null)
    setContractData({ rewardAmount: null, owner: null })
    setUserData({ hasClaimed: false, rewards: '0' })
  }, [])

  // Initialize contract when connected
  useEffect(() => {
    if (!isConnected || !chainId) return

    const contractAddress = getAddress('courseReward', chainId)
    if (!contractAddress) {
      setContract(null)
      return
    }

    const provider = new ethers.BrowserProvider(window.ethereum)
    const contractInstance = new ethers.Contract(
      contractAddress,
      CourseRewardABI.abi,
      provider
    )
    setContract(contractInstance)

    // Get signer and contract with signer
    provider.getSigner().then(signer => {
      const contractWithSigner = new ethers.Contract(
        contractAddress,
        CourseRewardABI.abi,
        signer
      )
      setContractWithSigner(contractWithSigner)
    })

    // Get balance
    provider.getBalance(account).then(bal => {
      setBalance(ethers.formatEther(bal))
    })
  }, [isConnected, chainId, account])

  // Fetch contract data
  const fetchContractData = useCallback(async () => {
    if (!contract) return

    try {
      const [rewardAmount, owner] = await Promise.all([
        contract.rewardAmount(),
        contract.owner()
      ])
      setContractData({
        rewardAmount: rewardAmount.toString(),
        owner
      })
    } catch (err) {
      console.error('Error fetching contract data:', err)
    }
  }, [contract])

  // Fetch user data
  const fetchUserData = useCallback(async () => {
    if (!contract || !account) return

    try {
      const [hasClaimed, rewards] = await Promise.all([
        contract.hasClaimed(account),
        contract.rewards(account)
      ])
      setUserData({
        hasClaimed,
        rewards: rewards.toString()
      })
    } catch (err) {
      console.error('Error fetching user data:', err)
    }
  }, [contract, account])

  // Refresh all data
  const refreshData = useCallback(async () => {
    await Promise.all([fetchContractData(), fetchUserData()])
  }, [fetchContractData, fetchUserData])

  // Fetch data when contract/account changes
  useEffect(() => {
    if (contract) {
      fetchContractData()
    }
  }, [contract, fetchContractData])

  useEffect(() => {
    if (contract && account) {
      fetchUserData()
    }
  }, [contract, account, fetchUserData])

  // Listen for account/chain changes
  useEffect(() => {
    if (!isMetaMaskInstalled) return

    const handleAccountsChanged = (accounts) => {
      if (accounts.length > 0) {
        setAccount(accounts[0])
        setIsConnected(true)
      } else {
        disconnect()
      }
    }

    const handleChainChanged = (chainIdHex) => {
      setChainId(parseInt(chainIdHex, 16))
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
  }, [isMetaMaskInstalled, disconnect])

  const value = {
    // Wallet
    account,
    chainId,
    balance,
    isConnected,
    isConnecting,
    isMetaMaskInstalled,
    connect,
    disconnect,

    // Contract
    contract,
    contractWithSigner,
    contractData,
    userData,

    // Actions
    refreshData,
    fetchContractData,
    fetchUserData
  }

  return (
    <Web3Context.Provider value={value}>
      {children}
    </Web3Context.Provider>
  )
}

export function useWeb3() {
  const context = useContext(Web3Context)
  if (!context) {
    throw new Error('useWeb3 must be used within Web3Provider')
  }
  return context
}
```

### 4.2 Using Web3 Context

```jsx
// main.jsx
import { Web3Provider } from './contexts/Web3Context'
import { ToastProvider } from './contexts/ToastContext'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Web3Provider>
      <ToastProvider>
        <App />
      </ToastProvider>
    </Web3Provider>
  </React.StrictMode>,
)

// Any component
import { useWeb3 } from '../contexts/Web3Context'

function MyComponent() {
  const {
    account,
    isConnected,
    contract,
    contractData,
    userData,
    refreshData
  } = useWeb3()

  // Use the data...
}
```

---

## 5. Deploy ke Testnet (Sepolia)

### 5.1 Setup Alchemy/Infura

> **Kenapa Perlu Alchemy/Infura?**
>
> Untuk deploy ke testnet/mainnet, kita butuh "jalan masuk" ke network tersebut. Alchemy menyediakan layanan ini gratis untuk developer.
>
> **Analogi:** Alchemy = ISP (Internet Service Provider) untuk blockchain

**Langkah Detail:**

1. **Buat akun di Alchemy:** https://alchemy.com
   - Sign up dengan Google/GitHub
   - Verifikasi email

2. **Buat App baru:**
   - Klik "Create App"
   - Name: CourseReward
   - Chain: Ethereum
   - Network: Sepolia
   - Klik "Create"

3. **Copy API Key:**
   - Buka app yang baru dibuat
   - Klik "API Key"
   - Copy "HTTPS" URL (format: `https://eth-sepolia.g.alchemy.com/v2/xxx...`)

### 5.2 Update Hardhat Config

**contracts/hardhat.config.ts:**

> **Catatan Hardhat 3**: Menggunakan `defineConfig()` dan `configVariable()` untuk membaca environment variables.

```typescript
import hardhatToolboxMochaEthersPlugin from "@nomicfoundation/hardhat-toolbox-mocha-ethers";
import { configVariable, defineConfig } from "hardhat/config";

export default defineConfig({
  plugins: [hardhatToolboxMochaEthersPlugin],
  solidity: {
    profiles: {
      default: {
        version: "0.8.28",
      },
      production: {
        version: "0.8.28",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200,
          },
        },
      },
    },
  },
  networks: {
    hardhatMainnet: {
      type: "edr-simulated",
      chainType: "l1",
    },
    localhost: {
      type: "http",
      url: "http://127.0.0.1:8545",
    },
    sepolia: {
      type: "http",
      chainType: "l1",
      url: configVariable("SEPOLIA_RPC_URL"),
      accounts: [configVariable("SEPOLIA_PRIVATE_KEY")],
    },
  },
});
```

**Penjelasan konfigurasi Hardhat 3:**

| Komponen                  | Penjelasan                                |
| ------------------------- | ----------------------------------------- |
| `defineConfig()`        | Fungsi konfigurasi Hardhat 3              |
| `configVariable()`      | Membaca environment variable              |
| `type: "http"`          | Network via HTTP RPC                      |
| `type: "edr-simulated"` | Network simulator Hardhat 3               |
| `chainType: "l1"`       | Tipe chain (L1/L2)                        |

### 5.3 Environment Variables

> **PENTING: Keamanan Environment Variables**
>
> File `.env` berisi data sensitif yang **TIDAK BOLEH** di-commit ke GitHub!
>
> **Langkah keamanan:**
> 1. Pastikan `.env` ada di `.gitignore`
> 2. Jangan share private key ke siapapun
> 3. Gunakan wallet terpisah untuk development (jangan wallet utama!)
>
> **Cara membuat file .env:**
> ```bash
> cd contracts
> touch .env
> # Edit dengan text editor
> ```

**contracts/.env:**
```env
# RPC URLs
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR-API-KEY

# Private key (NEVER commit this!)
# Hardhat 3 menggunakan configVariable() - nama harus sesuai dengan config
SEPOLIA_PRIVATE_KEY=your-private-key-here

# Etherscan for verification (opsional)
ETHERSCAN_API_KEY=your-etherscan-api-key
```

**Penting:** Tambahkan `.env` ke `.gitignore`:
```
# .gitignore
.env
.env.local
```

### 5.4 Get Sepolia ETH

> **Apa itu Faucet?**
>
> Faucet adalah layanan yang memberikan ETH gratis untuk testnet. ETH ini tidak bernilai uang sungguhan, hanya untuk testing.
>
> **Langkah mendapatkan Sepolia ETH:**

1. **Buka salah satu faucet:**
   - https://sepoliafaucet.com (by Alchemy)
   - https://www.infura.io/faucet/sepolia
   - https://faucets.chain.link/sepolia

2. **Masukkan wallet address:**
   - Copy address dari MetaMask
   - Paste di form faucet

3. **Request test ETH:**
   - Klik tombol "Send me ETH" atau sejenisnya
   - Tunggu beberapa detik
   - Cek MetaMask (pastikan sudah switch ke Sepolia network)

> **Tips:** Jika satu faucet tidak berfungsi, coba faucet lainnya. Kadang faucet rate-limited atau maintenance.

### 5.5 Deploy Script untuk Testnet

> **Perbedaan Deploy ke Testnet vs Localhost:**
>
> | Aspek | Localhost | Testnet |
> |-------|-----------|---------|
> | Gas fee | Gratis | Bayar (ETH testnet) |
> | Kecepatan | Instant | ~15 detik per block |
> | Persistensi | Reset saat node restart | Permanen |
> | Verifikasi | Tidak perlu | Bisa verify di Etherscan |
>
> **Script ini melakukan:**
> 1. Deploy contract ke Sepolia
> 2. Tunggu 5 block confirmations (untuk keamanan)
> 3. Verifikasi contract di Etherscan (agar source code public)
>
> **Output yang penting disimpan:**
> - Contract Address → masukkan ke `addresses.js` di frontend
> - Etherscan link → untuk verifikasi dan share

**contracts/scripts/deploy-sepolia.ts:**

> **Catatan Hardhat 3**: Menggunakan `network.create()` untuk mendapatkan `ethers`.

```typescript
import { network } from "hardhat";

const { ethers } = await network.create();

console.log("Deploying to Sepolia...");

const [deployer] = await ethers.getSigners();
console.log("Deploying with account:", deployer.address);

const balance = await ethers.provider.getBalance(deployer.address);
console.log("Account balance:", ethers.formatEther(balance), "ETH");

// Deploy
const courseReward = await ethers.deployContract("CourseReward", [100]);

await courseReward.waitForDeployment();

const address = await courseReward.getAddress();
console.log("CourseReward deployed to:", address);

// Wait for block confirmations
console.log("Waiting for block confirmations...");
const deployTx = courseReward.deploymentTransaction();
if (deployTx) {
  await deployTx.wait(5);
}

console.log("\n=== DEPLOYMENT COMPLETE ===");
console.log("Network: Sepolia");
console.log("Contract Address:", address);
console.log("Etherscan:", `https://sepolia.etherscan.io/address/${address}`);
```

### 5.6 Hardhat Ignition untuk Sepolia (Recommended)

Hardhat 3 merekomendasikan penggunaan **Ignition** untuk deployment ke testnet/mainnet.

**contracts/ignition/modules/CourseReward.ts:**
```typescript
import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const CourseRewardModule = buildModule("CourseRewardModule", (m) => {
  // Parameter constructor
  const initialReward = m.getParameter("initialReward", 100);

  // Deploy contract
  const courseReward = m.contract("CourseReward", [initialReward]);

  return { courseReward };
});

export default CourseRewardModule;
```

**Deploy ke Sepolia dengan Ignition:**
```bash
npx hardhat ignition deploy ignition/modules/CourseReward.ts --network sepolia
```

**Keuntungan Ignition untuk Testnet:**

| Fitur                    | Penjelasan                                   |
| ------------------------ | -------------------------------------------- |
| **Resume**         | Melanjutkan jika deployment gagal di tengah  |
| **Verification**   | Otomatis verify di Etherscan                 |
| **Parameters**     | Mudah mengubah parameter untuk network berbeda |
| **Deployment ID**  | Tracking deployment yang sudah dilakukan     |

### 5.7 Deploy Command

> **Checklist Sebelum Deploy:**
> - [ ] File `.env` sudah terisi dengan benar
> - [ ] Wallet ada Sepolia ETH (minimal 0.01 ETH)
> - [ ] Alchemy API key sudah diset (`SEPOLIA_RPC_URL`)
> - [ ] Private key sudah diset (`SEPOLIA_PRIVATE_KEY`)

**Opsi 1: Menggunakan Script**
```bash
cd contracts
npx hardhat run scripts/deploy-sepolia.ts --network sepolia
```

**Opsi 2: Menggunakan Hardhat Ignition (Recommended)**
```bash
cd contracts
npx hardhat ignition deploy ignition/modules/CourseReward.ts --network sepolia
```

> **Output yang diharapkan:**
> ```
> Deploying to Sepolia...
> Deploying with account: 0x...
> Account balance: 0.5 ETH
> CourseReward deployed to: 0x1234...
> Waiting for block confirmations...
>
> === DEPLOYMENT COMPLETE ===
> Network: Sepolia
> Contract Address: 0x1234...
> Etherscan: https://sepolia.etherscan.io/address/0x1234...
> ```
>
> **Simpan Contract Address!** Akan digunakan di frontend.

### 5.8 Update Frontend Addresses

**frontend/src/contracts/addresses.js:**
```javascript
export const CONTRACT_ADDRESSES = {
  31337: { // Hardhat Local
    courseReward: '0x5FbDB2315678afecb367f032d93F642f64180aa3'
  },
  1337: { // Ganache
    courseReward: '0x5FbDB2315678afecb367f032d93F642f64180aa3'
  },
  11155111: { // Sepolia
    courseReward: '0xYOUR_SEPOLIA_CONTRACT_ADDRESS'
  }
}

export function getAddress(contractName, chainId) {
  return CONTRACT_ADDRESSES[chainId]?.[contractName] || null
}
```

---

## 6. Environment Variables

### 6.1 Frontend Environment Variables

**frontend/.env:**
```env
# Network Configuration
VITE_DEFAULT_CHAIN_ID=11155111
VITE_SUPPORTED_CHAINS=31337,1337,11155111

# RPC URLs (for fallback when MetaMask unavailable)
VITE_SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR-API-KEY

# Contract Addresses
VITE_CONTRACT_ADDRESS_31337=0x5FbDB2315678afecb367f032d93F642f64180aa3
VITE_CONTRACT_ADDRESS_11155111=0xYOUR_SEPOLIA_ADDRESS
```

### 6.2 Using Environment Variables

```javascript
// config.js
export const config = {
  defaultChainId: parseInt(import.meta.env.VITE_DEFAULT_CHAIN_ID || '31337'),
  supportedChains: (import.meta.env.VITE_SUPPORTED_CHAINS || '31337')
    .split(',')
    .map(Number),
  rpcUrls: {
    11155111: import.meta.env.VITE_SEPOLIA_RPC_URL
  }
}

export function getContractAddress(chainId) {
  return import.meta.env[`VITE_CONTRACT_ADDRESS_${chainId}`] || null
}
```

---

## 7. Deploy Frontend ke Vercel

### 7.1 Persiapan

1. Push code ke GitHub
2. Buat akun di https://vercel.com
3. Connect dengan GitHub

### 7.2 vercel.json

**frontend/vercel.json:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
}
```

### 7.3 Deploy Steps

> **Step-by-Step Deploy ke Vercel:**
>
> Vercel adalah platform hosting gratis yang sangat mudah digunakan. Cukup connect GitHub, dan setiap push akan otomatis deploy!

1. **Import Project:**
   - Login ke Vercel dengan GitHub
   - Click "New Project"
   - Pilih repository dApp kamu
   - Click "Import"

2. **Configure:**
   - Framework Preset: Vite
   - Root Directory: `frontend` (jika monorepo)
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Environment Variables:**
   - Add all `VITE_*` variables

4. **Deploy:**
   - Click "Deploy"
   - Wait for build

### 7.4 Custom Domain (Optional)

1. Go to Project Settings > Domains
2. Add your domain
3. Configure DNS records

---

## 8. Production Best Practices

### 8.1 Security Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY CHECKLIST                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Smart Contract:                                                │
│  ☐ Audited by professional auditor                              │
│  ☐ Use OpenZeppelin contracts where possible                    │
│  ☐ Reentrancy protection implemented                            │
│  ☐ Access control properly configured                           │
│  ☐ No private keys in code                                      │
│                                                                 │
│  Frontend:                                                      │
│  ☐ No sensitive data in frontend code                           │
│  ☐ Validate all user inputs                                     │
│  ☐ Use HTTPS only                                               │
│  ☐ Implement Content Security Policy                            │
│  ☐ Environment variables for configuration                      │
│                                                                 │
│  General:                                                       │
│  ☐ Test on testnet before mainnet                               │
│  ☐ Start with limited features/funds                            │
│  ☐ Have emergency pause mechanism                               │
│  ☐ Monitor contract events                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Performance Optimization

```javascript
// 1. Batch RPC calls
const [a, b, c] = await Promise.all([
  contract.funcA(),
  contract.funcB(),
  contract.funcC()
])

// 2. Use Multicall for many reads
import { Contract as MulticallContract, Provider } from 'ethers-multicall'

// 3. Implement caching
const cache = new Map()
async function cachedCall(key, fn, ttl = 30000) {
  if (cache.has(key)) {
    const { data, timestamp } = cache.get(key)
    if (Date.now() - timestamp < ttl) return data
  }
  const data = await fn()
  cache.set(key, { data, timestamp: Date.now() })
  return data
}

// 4. Lazy load components
const HeavyComponent = React.lazy(() => import('./HeavyComponent'))
```

### 8.3 Error Monitoring

```javascript
// Setup error boundary
class ErrorBoundary extends React.Component {
  state = { hasError: false }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    // Log to monitoring service
    console.error('Error:', error, errorInfo)
    // logErrorToService(error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong. Please refresh.</div>
    }
    return this.props.children
  }
}
```

---

## 9. Final Project: Complete dApp

### 9.1 Final Project Structure

```
dapp-project/
├── contracts/
│   ├── contracts/
│   │   └── CourseReward.sol
│   ├── scripts/
│   │   ├── deploy.js
│   │   └── deploy-sepolia.js
│   ├── test/
│   │   └── CourseReward.test.js
│   ├── hardhat.config.js
│   └── package.json
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── ContractInfo.jsx
│   │   │   ├── UserStatus.jsx
│   │   │   ├── ClaimReward.jsx
│   │   │   ├── AdminPanel.jsx
│   │   │   └── EventHistory.jsx
│   │   ├── contexts/
│   │   │   ├── Web3Context.jsx
│   │   │   └── ToastContext.jsx
│   │   ├── hooks/
│   │   │   ├── useWallet.js
│   │   │   ├── useContract.js
│   │   │   └── useContractEvents.js
│   │   ├── contracts/
│   │   │   ├── CourseReward.json
│   │   │   └── addresses.js
│   │   ├── utils/
│   │   │   └── errorHandler.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .env
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

### 9.2 Final App.jsx

```jsx
import Navbar from './components/Navbar'
import ContractInfo from './components/ContractInfo'
import UserStatus from './components/UserStatus'
import ClaimReward from './components/ClaimReward'
import AdminPanel from './components/AdminPanel'
import EventHistory from './components/EventHistory'
import { useWeb3 } from './contexts/Web3Context'
import { useToast } from './contexts/ToastContext'
import './App.css'

function App() {
  const { isMetaMaskInstalled, refreshData } = useWeb3()
  const toast = useToast()

  const handleClaimSuccess = () => {
    toast.success('Reward claimed successfully!')
    refreshData()
  }

  const handleAdminUpdate = () => {
    toast.success('Reward amount updated!')
    refreshData()
  }

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

      <main className="main-content">
        <AdminPanel onUpdate={handleAdminUpdate} />

        <div className="grid grid-2">
          <ContractInfo />
          <UserStatus />
        </div>

        <div className="grid grid-2">
          <ClaimReward onClaimSuccess={handleClaimSuccess} />
          <EventHistory />
        </div>
      </main>

      <footer className="footer">
        <p>Built with React + ethers.js + Hardhat</p>
      </footer>
    </div>
  )
}

export default App
```

---

## Ringkasan

| Topik                   | Poin Penting                                       |
| ----------------------- | -------------------------------------------------- |
| **Event Listening**   | Real-time updates dengan contract.on()             |
| **Notifications**     | Toast system untuk user feedback                   |
| **Caching**           | Reduce RPC calls, improve performance              |
| **Context API**       | Global state management untuk Web3                 |
| **Testnet Deploy**    | Sepolia untuk testing sebelum mainnet              |
| **Frontend Deploy**   | Vercel/Netlify untuk hosting                       |
| **Production**        | Security, monitoring, optimization                 |

---

## Tugas

### Tugas 1: Complete dApp

1. Implementasikan semua fitur yang dipelajari di Module 12-15
2. Deploy smart contract ke Sepolia testnet
3. Deploy frontend ke Vercel/Netlify
4. Dokumentasikan semua langkah

### Tugas 2: Event History dengan Pagination

Modifikasi EventHistory component:
1. Tampilkan 10 events per page
2. Tambah tombol "Load More"
3. Tampilkan total events count

### Tugas 3: Network Switcher

Buat fitur automatic network switch:
1. Detect jika user di wrong network
2. Tampilkan modal untuk switch
3. Auto switch ke network yang benar

### Tugas 4: Mobile Responsive

1. Pastikan dApp responsive di mobile
2. Test di berbagai screen sizes
3. Optimasi touch interactions

### Deliverable

Kumpulkan:
1. Link GitHub repository
2. Link deployed dApp (Vercel/Netlify)
3. Contract address di Sepolia
4. Screenshot dApp di desktop dan mobile
5. Video demo singkat (optional)
6. README.md dengan:
   - Project description
   - Features
   - Tech stack
   - Setup instructions
   - Deployment guide

---

## Referensi

- [Alchemy Documentation](https://docs.alchemy.com/)
- [Vercel Documentation](https://vercel.com/docs)
- [Etherscan API](https://docs.etherscan.io/)
- [React Context API](https://react.dev/reference/react/useContext)
- [ethers.js Events](https://docs.ethers.org/v6/getting-started/#starting-events)
- [Web3 Security Best Practices](https://ethereum.org/en/developers/docs/security/)
