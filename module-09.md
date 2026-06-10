# Modul 9. Hardhat Project Setup & Compile

## Deskripsi

Modul ini membahas cara membuat project smart contract menggunakan **Hardhat**, framework development Ethereum yang paling populer. Mahasiswa akan belajar setup environment, memahami struktur project, menulis smart contract, dan melakukan compile.

## Tujuan Pembelajaran

Setelah menyelesaikan modul ini, mahasiswa mampu:

1. Membuat project Hardhat dari awal
2. Memahami struktur folder project smart contract
3. Mengkonfigurasi Hardhat untuk berbagai network
4. Memindahkan contract dari Remix ke project lokal
5. Menjalankan compile dan memahami output (ABI, bytecode, artifacts)

## Prasyarat

Sebelum memulai, pastikan sudah terinstall:

- **Node.js** v18+ ([Download](https://nodejs.org))
- **npm** (sudah termasuk dalam Node.js)
- **VS Code** dengan extension Solidity
- **Terminal** (Command Prompt, PowerShell, atau Terminal)

Cek instalasi:

```bash
node -v   # v18.x.x atau lebih baru
npm -v    # 9.x.x atau lebih baru
```

## List of Contents

- [Deskripsi](#deskripsi)
- [Tujuan Pembelajaran](#tujuan-pembelajaran)
- [Prasyarat](#prasyarat)
- [1. Pengenalan Node.js dan npm](#1-pengenalan-nodejs-dan-npm)
- [2. Pengantar Hardhat](#2-pengantar-hardhat)
- [3. Setup Project Hardhat](#3-setup-project-hardhat)
- [4. Struktur Project](#4-struktur-project)
  - [4.2 Contoh File Test (TypeScript + Mocha + Ethers.js)](#42-contoh-file-test-typescript--mocha--ethersjs)
- [5. Konfigurasi Hardhat](#5-konfigurasi-hardhat)
  - [5.3 Perbedaan JavaScript vs TypeScript Config](#53-perbedaan-javascript-vs-typescript-config)
- [6. Menulis Smart Contract](#6-menulis-smart-contract)
- [7. Compile Contract](#7-compile-contract)
- [8. Memahami Output Compile](#8-memahami-output-compile)
- [9. Troubleshooting](#9-troubleshooting)
- [Tugas](#tugas)
- [Referensi](#referensi)

## 1. Pengenalan Node.js dan npm

Sebelum memulai development dengan Hardhat, kita perlu memahami dan menginstall **Node.js** dan **npm** terlebih dahulu karena Hardhat berjalan di atas Node.js.

### 1.1 Apa itu Node.js?

**Node.js** adalah runtime environment yang memungkinkan JavaScript berjalan di luar browser (di sisi server/komputer). Dengan Node.js, developer dapat menjalankan kode JavaScript langsung di terminal/command line.

```
┌─────────────────────────────────────────────────────────────────┐
│                     NODE.JS OVERVIEW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Sebelum Node.js:                                              │
│   ┌──────────────┐                                              │
│   │   Browser    │  JavaScript hanya bisa jalan di browser      │
│   │  (Chrome,    │                                              │
│   │  Firefox)    │                                              │
│   └──────────────┘                                              │
│                                                                 │
│   Dengan Node.js:                                               │
│   ┌──────────────┐    ┌──────────────┐                          │
│   │   Browser    │    │   Server/    │  JavaScript bisa jalan   │
│   │              │    │   Terminal   │  di mana saja!           │
│   └──────────────┘    └──────────────┘                          │
│                                                                 │
│   Kegunaan Node.js:                                             │
│   - Menjalankan tools development (Hardhat, Webpack, dll)       │
│   - Membuat server backend                                      │
│   - Menjalankan script automation                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Apa itu npm?

**npm (Node Package Manager)** adalah package manager untuk JavaScript yang digunakan untuk:

- Menginstall library/package dari komunitas
- Mengelola dependencies project
- Menjalankan script project

```
┌─────────────────────────────────────────────────────────────────┐
│                       npm OVERVIEW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   npm Registry (npmjs.com)                                      │
│   ┌─────────────────────────────────────────────────────┐       │
│   │  hardhat  │  ethers  │  web3  │  react  │  ...      │       │
│   │  2M+ packages tersedia                              │       │
│   └─────────────────────────────────────────────────────┘       │
│                          ▲                                      │
│                          │ npm install                          │
│                          ▼                                      │
│   Project Lokal (node_modules/)                                 │
│   ┌─────────────────────────────────────────────────────┐       │
│   │  Semua package yang diinstall tersimpan di sini     │       │
│   └─────────────────────────────────────────────────────┘       │
│                                                                 │
│   Commands npm yang sering digunakan:                           │
│   - npm init          : Membuat project baru                    │
│   - npm install       : Install semua dependencies              │
│   - npm install <pkg> : Install package tertentu                │
│   - npm run <script>  : Menjalankan script                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Instalasi Node.js di Windows

#### Metode 1: Download Installer (Recommended untuk Pemula)

1. **Kunjungi website resmi Node.js**

   Buka browser dan akses: [https://nodejs.org/en/download](https://nodejs.org/en/download)
2. **Download installer**

   - Klik tombol download untuk Windows (file `.msi`)
3. **Jalankan installer**

   - Double-click file yang sudah didownload
   - Ikuti wizard instalasi:
     - Klik "Next"
     - Accept license agreement
     - Pilih lokasi instalasi (default saja)
     - **Pastikan** opsi "Add to PATH" tercentang
     - Klik "Install"
   - Tunggu proses instalasi selesai
   - Klik "Finish"
4. **Verifikasi instalasi**

   Buka **Command Prompt** atau **PowerShell** dan ketik:

   ```bash
   node -v
   npm -v
   ```

   Output yang diharapkan:

   ```text
   v24.16.0
   11.13.0
   ```

### 1.4 Instalasi Node.js di macOS

#### Metode 1: Download Installer

1. **Kunjungi website resmi Node.js**

   Buka browser dan akses: [https://nodejs.org/en/download](https://nodejs.org/en/download)
2. **Download installer**

   - Klik tombol download untuk macOS (file `.pkg`)
3. **Jalankan installer**

   - Double-click file `.pkg` yang sudah didownload
   - Ikuti wizard instalasi
   - Masukkan password administrator jika diminta
   - Tunggu proses instalasi selesai
4. **Verifikasi instalasi**

   Buka **Terminal** dan ketik:

   ```bash
   node -v
   npm -v
   ```

#### Metode 2: Menggunakan nvm (Node Version Manager)

nvm memungkinkan kita menginstall dan switch antara berbagai versi Node.js:

```bash
# Download and install nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.5/install.sh | bash

# in lieu of restarting the shell
\. "$HOME/.nvm/nvm.sh"

# Download and install Node.js:
nvm install 24

# Verify the Node.js version:
node -v # Should print "v24.16.0".

# Verify npm version:
npm -v # Should print "11.13.0".
```

#### Metode 3: Menggunakan Homebrew (Unofficial)

Homebrew adalah package manager populer untuk macOS.

```bash
# Download and install Homebrew
curl -o- https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash

# Download and install Node.js:
brew install node@24

# Verify the Node.js version:
node -v # Should print "v24.16.0".

# Verify npm version:
npm -v # Should print "11.13.0".
```

#### 1.5 Verifikasi Instalasi

Setelah instalasi selesai, pastikan Node.js dan npm terinstall dengan benar:

```bash
# Cek versi Node.js
node -v

# Cek versi npm
npm -v

# Test menjalankan JavaScript
node -e "console.log('Hello from Node.js!')"
```

**Output yang diharapkan:**

```text
v24.16.0
11.13.0
Hello from Node.js!
```

### 1.6 Troubleshooting Instalasi

| Masalah                         | Penyebab                  | Solusi                                                              |
| ------------------------------- | ------------------------- | ------------------------------------------------------------------- |
| `'node' is not recognized`    | Node.js tidak ada di PATH | Restart terminal/komputer, atau reinstall dengan opsi "Add to PATH" |
| Permission denied (macOS/Linux) | Tidak punya akses write   | Gunakan `sudo` atau install via nvm                               |
| Versi terlalu lama              | Instalasi lama            | Update Node.js ke versi terbaru                                     |
| npm error EACCES                | Permission issue          | Gunakan nvm atau fix npm permissions                                |

**Tips:**

- Selalu gunakan versi **LTS** untuk development karena lebih stabil
- Restart terminal setelah instalasi agar perubahan PATH ter-apply
- Jika sering berganti versi Node.js, pertimbangkan menggunakan **nvm**

## 2. Pengantar Hardhat

### 2.1 Apa itu Hardhat?

**Hardhat** adalah development environment untuk Ethereum yang memungkinkan developer untuk:

- Compile smart contract
- Deploy ke berbagai network
- Menulis dan menjalankan test
- Debug smart contract

```
┌─────────────────────────────────────────────────────────────────┐
│                    HARDHAT ECOSYSTEM                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│   │  Write   │──►│ Compile  │──►│   Test   │──►│  Deploy  │     │
│   │ Contract │   │          │   │          │   │          │     │
│   └──────────┘   └──────────┘   └──────────┘   └──────────┘     │
│                                                                 │
│   Tools:                                                        │
│   - Solidity Compiler                                           │
│   - Hardhat Network (local blockchain)                          │
│   - Ethers.js integration                                       │
│   - Testing framework (Mocha + Chai)                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Remix vs Hardhat

| Aspek                     | Remix IDE                  | Hardhat                         |
| ------------------------- | -------------------------- | ------------------------------- |
| **Tipe**            | Browser-based IDE          | Local development framework     |
| **Cocok untuk**     | Belajar cepat, prototyping | Project serius, tim development |
| **Testing**         | Manual (klik function)     | Automated unit testing          |
| **Version Control** | Sulit                      | Mudah (Git)                     |
| **CI/CD**           | Tidak mendukung            | Mendukung                       |
| **Extensibility**   | Terbatas                   | Plugin ecosystem                |

```
Remix: Cocok untuk belajar dan eksperimen cepat
       └─► Langsung di browser, tidak perlu setup

Hardhat: Cocok untuk project yang lebih rapi
         └─► Bisa ditest, dideploy, dan dikembangkan secara profesional
```

### 2.3 Mengapa Hardhat?

**Kelebihan Hardhat:**

| Fitur                        | Penjelasan                                    |
| ---------------------------- | --------------------------------------------- |
| **Hardhat Network**    | Built-in local Ethereum network untuk testing |
| **Solidity Debugging** | Stack traces dan console.log di Solidity      |
| **Flexible Testing**   | Integrasi dengan Mocha, Chai, Ethers.js       |
| **Plugin System**      | Ekstensif plugin untuk berbagai kebutuhan     |
| **TypeScript Support** | First-class TypeScript support                |

## 3. Setup Project Hardhat

#### Step 1: Buat Folder Project

```bash
mkdir project-smart-contract
cd project-smart-contract
```

#### Step 2: Inisialisasi npm

```bash
npm init -y
```

Perintah ini membuat file `package.json` dengan konfigurasi default.

#### Step 3: Install Hardhat

```bash
npm install --save-dev hardhat
```

#### Step 4: Inisialisasi Hardhat

```bash
npx hardhat init
```

Pilih opsi berikut saat muncul prompt:

```text
✔ What do you want to do? · Create a TypeScript project (with Mocha + Ethers.js)
✔ Hardhat project root: · /path/to/project-smart-contract
✔ Do you want to add a .gitignore? (Y/n) · y
```

> **Catatan**: Kita memilih **Mocha + Ethers.js** karena:
>
> - Dokumentasi dan tutorial lebih banyak tersedia
> - Lebih mudah untuk pemula
> - Sintaks Chai (`expect().to.equal()`) lebih readable
> - Komunitas besar, mudah mencari solusi jika ada masalah

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OPSI PROJECT HARDHAT                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Opsi 1: TypeScript + Mocha + Ethers.js  ← KITA PILIH INI                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Testing: Mocha + Chai                                              │   │
│  │  Blockchain: Ethers.js                                              │   │
│  │  Sintaks: expect(value).to.equal(100)                               │   │
│  │                                                                     │   │
│  │  + Dokumentasi sangat banyak                                        │   │
│  │  + Cocok untuk pemula                                               │   │
│  │  + Komunitas besar                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Opsi 2: TypeScript + Node Test Runner + Viem                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Testing: Node Test Runner (built-in Node.js)                       │   │
│  │  Blockchain: Viem                                                   │   │
│  │  Sintaks: assert.strictEqual(value, 100n)                           │   │
│  │                                                                     │   │
│  │  + Lebih modern & ringan                                            │   │
│  │  + Performa lebih baik                                              │   │
│  │  - Dokumentasi masih sedikit                                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

Hardhat 3 akan otomatis menginstall dependencies yang diperlukan:

```text
✔ Installing dependencies with npm...

  @nomicfoundation/hardhat-toolbox-mocha-ethers
  @nomicfoundation/hardhat-ignition
  ethers
  chai
  typescript
  ...
```

#### Step 5: Verifikasi Instalasi

```bash
npx hardhat compile
```

**Expected Output:**

```text
Compiled 1 Solidity file successfully (evm target: paris).
```

## 4. Struktur Project

Setelah inisialisasi, struktur folder project adalah:

```text
project-smart-contract/
├── contracts/              ← File smart contract Solidity
│   └── Lock.sol            ← Sample contract dari Hardhat
├── ignition/               ← Module deployment (Hardhat Ignition)
│   └── modules/
│       └── Lock.ts         ← TypeScript deployment module
├── test/                   ← File unit test
│   └── Lock.ts             ← TypeScript test file
├── hardhat.config.ts       ← Konfigurasi Hardhat (TypeScript)
├── tsconfig.json           ← Konfigurasi TypeScript
├── package.json            ← Dependencies dan scripts
├── package-lock.json
├── .gitignore
└── README.md
```

### 4.1 Penjelasan Folder

| Folder/File           | Fungsi                                         |
| --------------------- | ---------------------------------------------- |
| `contracts/`        | Tempat semua file smart contract (.sol)        |
| `ignition/`         | Script deployment menggunakan Hardhat Ignition |
| `test/`             | File unit test untuk smart contract (.ts)      |
| `hardhat.config.ts` | Konfigurasi compiler, network, plugins         |
| `tsconfig.json`     | Konfigurasi TypeScript compiler                |
| `artifacts/`        | Hasil compile (muncul setelah compile)         |
| `cache/`            | Cache untuk mempercepat compile                |

### 4.2 Contoh File Test (TypeScript + Mocha + Ethers.js)

File `test/Lock.ts` yang di-generate Hardhat 3:

> **Catatan Hardhat 3**: Menggunakan `network.create()` untuk mendapatkan `ethers` dan `networkHelpers`, serta menggunakan fixture pattern dengan `loadFixture()`.

```typescript
import { expect } from "chai";
import { network } from "hardhat";

// Buat network connection (top-level await di Hardhat 3)
const { ethers, networkHelpers } = await network.create();

describe("Lock", function () {
  // Fixture untuk deploy contract (di-cache oleh loadFixture)
  async function deployLockFixture() {
    const [owner] = await ethers.getSigners();
    const unlockTime = Math.floor(Date.now() / 1000) + 60;
    const lockedAmount = ethers.parseEther("1");
    const lock = await ethers.deployContract("Lock", [unlockTime], { value: lockedAmount });
    return { lock, owner, unlockTime, lockedAmount };
  }

  it("Should set the right owner", async function () {
    const { lock, owner } = await networkHelpers.loadFixture(deployLockFixture);
    expect(await lock.owner()).to.equal(owner.address);
  });
});
```

**Penjelasan sintaks Hardhat 3 (Mocha + Chai + Ethers.js):**

| Sintaks                             | Library        | Fungsi                                  |
| ----------------------------------- | -------------- | --------------------------------------- |
| `network.create()`                | Hardhat 3      | Membuat koneksi network                 |
| `networkHelpers.loadFixture()`    | Hardhat 3      | Menjalankan fixture dengan caching      |
| `describe()`, `it()`            | Mocha          | Struktur test (test suite & test case)  |
| `expect().to.equal()`             | Chai           | Assertion (pengecekan hasil)            |
| `ethers.getSigners()`             | Ethers.js      | Mendapatkan wallet accounts             |
| `ethers.deployContract()`         | Ethers.js      | Deploy contract langsung                |

### 4.3 Folder artifacts (setelah compile)

```text
artifacts/
├── contracts/
│   └── Lock.sol/
│       ├── Lock.json          ← ABI + Bytecode
│       └── Lock.dbg.json      ← Debug info
├── build-info/
│   └── xxx.json               ← Build metadata
└── ...
```

## 5. Konfigurasi Hardhat

### 5.1 File hardhat.config.ts

Buka file `hardhat.config.ts`:

> **Catatan Hardhat 3**: Menggunakan `defineConfig()` dan format plugin baru.

```typescript
import hardhatToolboxMochaEthersPlugin from "@nomicfoundation/hardhat-toolbox-mocha-ethers";
import { defineConfig } from "hardhat/config";

export default defineConfig({
  plugins: [hardhatToolboxMochaEthersPlugin],
  solidity: {
    profiles: {
      default: {
        version: "0.8.28",
      },
    },
  },
});
```

### 5.2 Konfigurasi Lengkap

Modifikasi menjadi konfigurasi yang lebih lengkap:

```typescript
import hardhatToolboxMochaEthersPlugin from "@nomicfoundation/hardhat-toolbox-mocha-ethers";
import { defineConfig } from "hardhat/config";

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
    // Hardhat Network (simulated, built-in)
    hardhatMainnet: {
      type: "edr-simulated",
      chainType: "l1",
    },
    // Localhost (untuk npx hardhat node)
    localhost: {
      type: "http",
      url: "http://127.0.0.1:8545",
    },
    // Ganache (opsional)
    ganache: {
      type: "http",
      url: "http://127.0.0.1:7545",
    },
  },
});
```

### 5.3 Perbedaan Hardhat 2 vs Hardhat 3

| Aspek                    | Hardhat 2                               | Hardhat 3                                      |
| ------------------------ | --------------------------------------- | ---------------------------------------------- |
| **Config**         | `HardhatUserConfig` object            | `defineConfig()` function                    |
| **Plugins**        | `import "@plugin"` (side effect)      | `plugins: [plugin]` array                    |
| **Solidity**       | `solidity: "0.8.28"`                  | `solidity: { profiles: { default: {...} } }` |
| **Networks**       | `networks: { hardhat: {} }`           | `networks: { name: { type: "..." } }`        |
| **Test**           | `import { ethers } from "hardhat"`    | `await network.create()`                     |
| **Fixture**        | `loadFixture()` dari `hardhat-network-helpers` | `networkHelpers.loadFixture()`               |
| **Deploy**         | `await Contract.deploy()`             | `await ethers.deployContract()`              |

### 5.4 Perbedaan JavaScript vs TypeScript Config

| JavaScript (`hardhat.config.js`) | TypeScript (`hardhat.config.ts`) |
| ---------------------------------- | ---------------------------------- |
| `require("...")`                 | `import ... from "..."`          |
| `module.exports = { }`           | `export default defineConfig({})` |
| Tidak ada type checking            | Type checking otomatis             |

### 5.5 Penjelasan Konfigurasi

| Bagian                          | Fungsi                                    |
| ------------------------------- | ----------------------------------------- |
| `defineConfig()`              | Fungsi konfigurasi Hardhat 3              |
| `plugins: []`                 | Array plugin yang digunakan               |
| `solidity.profiles`           | Profil compiler (default/production)      |
| `type: "edr-simulated"`       | Network simulator Hardhat 3               |
| `type: "http"`                | Network via HTTP RPC                      |
| `networks.localhost`          | Koneksi ke Hardhat node yang berjalan     |

### 5.6 Network Options

```
┌─────────────────────────────────────────────────────────────────┐
│                    NETWORK OPTIONS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Local Development:                                             │
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │  Hardhat Network │    │     Ganache      │                   │
│  │  Port: 8545      │    │  Port: 7545      │                   │
│  │  Chain ID: 31337 │    │  Chain ID: 1337  │                   │
│  │  Built-in        │    │  Separate app    │                   │
│  └──────────────────┘    └──────────────────┘                   │
│                                                                 │
│  Testnet (untuk nanti):                                         │
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │     Sepolia      │    │     Goerli       │                   │
│  │  Real testnet    │    │  (Deprecated)    │                   │
│  └──────────────────┘    └──────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 6. Menulis Smart Contract

### 6.1 Hapus Sample Contract

Hapus file sample dan buat contract baru:

```bash
rm contracts/Lock.sol
```

### 6.2 Buat Contract Baru

Buat file `contracts/CourseReward.sol`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title CourseReward
 * @dev Contract untuk memberikan reward kepada mahasiswa yang menyelesaikan kursus
 * @notice Contract ini digunakan sebagai contoh pembelajaran Hardhat
 */
contract CourseReward {
    // ============ State Variables ============

    /// @notice Address owner/dosen yang membuat contract
    address public owner;

    /// @notice Jumlah reward yang diberikan per mahasiswa
    uint256 public rewardAmount;

    /// @notice Mapping untuk menyimpan total reward per mahasiswa
    mapping(address => uint256) public rewards;

    /// @notice Mapping untuk tracking apakah mahasiswa sudah claim
    mapping(address => bool) public hasClaimed;

    // ============ Events ============

    /// @notice Event yang di-emit saat mahasiswa claim reward
    event RewardClaimed(address indexed student, uint256 amount);

    /// @notice Event yang di-emit saat owner mengubah reward amount
    event RewardAmountChanged(uint256 oldAmount, uint256 newAmount);

    // ============ Modifiers ============

    /// @notice Modifier untuk membatasi akses hanya untuk owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    // ============ Constructor ============

    /**
     * @notice Membuat contract baru dengan reward amount tertentu
     * @param _rewardAmount Jumlah reward per mahasiswa
     */
    constructor(uint256 _rewardAmount) {
        owner = msg.sender;
        rewardAmount = _rewardAmount;
    }

    // ============ External Functions ============

    /**
     * @notice Mahasiswa claim reward mereka
     * @dev Setiap mahasiswa hanya bisa claim sekali
     */
    function claimReward() external {
        require(!hasClaimed[msg.sender], "Reward already claimed");

        rewards[msg.sender] += rewardAmount;
        hasClaimed[msg.sender] = true;

        emit RewardClaimed(msg.sender, rewardAmount);
    }

    /**
     * @notice Owner mengubah jumlah reward
     * @param _newAmount Jumlah reward baru
     */
    function setRewardAmount(uint256 _newAmount) external onlyOwner {
        uint256 oldAmount = rewardAmount;
        rewardAmount = _newAmount;

        emit RewardAmountChanged(oldAmount, _newAmount);
    }

    // ============ View Functions ============

    /**
     * @notice Mendapatkan total reward yang dimiliki pemanggil
     * @return Total reward dalam wei
     */
    function getMyReward() external view returns (uint256) {
        return rewards[msg.sender];
    }

    /**
     * @notice Cek apakah address tertentu sudah claim
     * @param _student Address mahasiswa yang dicek
     * @return true jika sudah claim, false jika belum
     */
    function hasStudentClaimed(address _student) external view returns (bool) {
        return hasClaimed[_student];
    }
}
```

### 6.3 Anatomi Smart Contract

```
┌─────────────────────────────────────────────────────────────────┐
│                    STRUKTUR SMART CONTRACT                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. SPDX License Identifier                                     │
│     └─► Lisensi open source                                     │
│                                                                 │
│  2. Pragma                                                      │
│     └─► Versi compiler Solidity                                 │
│                                                                 │
│  3. Contract Declaration                                        │
│     └─► contract ContractName { ... }                           │
│                                                                 │
│  4. State Variables                                             │
│     └─► Data yang disimpan di blockchain                        │
│                                                                 │
│  5. Events                                                      │
│     └─► Log untuk tracking aktivitas                            │
│                                                                 │
│  6. Modifiers                                                   │
│     └─► Reusable access control                                 │
│                                                                 │
│  7. Constructor                                                 │
│     └─► Dijalankan sekali saat deploy                           │
│                                                                 │
│  8. Functions                                                   │
│     └─► Logic contract                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.4 Konsep Penting dalam Contract

| Konsep                   | Penjelasan                  | Contoh                                          |
| ------------------------ | --------------------------- | ----------------------------------------------- |
| **State Variable** | Data permanen di blockchain | `address public owner;`                       |
| **Mapping**        | Key-value storage           | `mapping(address => uint256) public rewards;` |
| **Event**          | Log untuk frontend/indexer  | `emit RewardClaimed(student, amount);`        |
| **Modifier**       | Reusable condition check    | `modifier onlyOwner()`                        |
| **require**        | Validasi kondisi            | `require(!hasClaimed[msg.sender], "...");`    |
| **msg.sender**     | Address pemanggil function  | `owner = msg.sender;`                         |

## 7. Compile Contract

### 7.1 Jalankan Compile

```bash
npx hardhat compile
```

**Expected Output:**

```text
Compiled 1 Solidity file successfully (evm target: paris).
```

### 7.2 Compile dengan Clean

Jika perlu compile ulang dari awal:

```bash
npx hardhat clean
npx hardhat compile
```

### 7.3 Compile Specific File

```bash
npx hardhat compile --force
```

### 7.4 Hasil Compile

Setelah compile, folder `artifacts` akan muncul:

```text
artifacts/
└── contracts/
    └── CourseReward.sol/
        ├── CourseReward.json      ← File utama (ABI + Bytecode)
        └── CourseReward.dbg.json  ← Debug information
```

## 8. Memahami Output Compile

### 8.1 File CourseReward.json

Buka file `artifacts/contracts/CourseReward.sol/CourseReward.json`:

```json
{
  "_format": "hh-sol-artifact-1",
  "contractName": "CourseReward",
  "sourceName": "contracts/CourseReward.sol",
  "abi": [...],
  "bytecode": "0x608060405234801561001057600080fd5b50...",
  "deployedBytecode": "0x608060405234801561001057600080fd5b50...",
  "linkReferences": {},
  "deployedLinkReferences": {}
}
```

### 8.2 Komponen Output

| Komponen                    | Penjelasan                                                 |
| --------------------------- | ---------------------------------------------------------- |
| **ABI**               | Application Binary Interface - definisi function dan event |
| **Bytecode**          | Kode yang akan dideploy ke blockchain                      |
| **Deployed Bytecode** | Kode yang tersimpan di blockchain setelah deploy           |

### 8.3 ABI (Application Binary Interface)

ABI adalah "kontrak" antara smart contract dan aplikasi yang ingin berinteraksi:

```json
{
  "abi": [
    {
      "inputs": [{"name": "_rewardAmount", "type": "uint256"}],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [],
      "name": "claimReward",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "rewardAmount",
      "outputs": [{"type": "uint256"}],
      "stateMutability": "view",
      "type": "function"
    }
  ]
}
```

```
┌─────────────────────────────────────────────────────────────────┐
│                         ABI USAGE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Frontend/Script                        Smart Contract         │
│   ┌─────────────┐                       ┌─────────────┐         │
│   │             │   ABI defines how     │             │         │
│   │  ethers.js  │◄─────────────────────►│ CourseReward│         │
│   │  web3.js    │   to call functions   │             │         │
│   │             │                       │             │         │
│   └─────────────┘                       └─────────────┘         │
│                                                                 │
│   ABI tells the frontend:                                       │
│   - What functions exist                                        │
│   - What parameters they need                                   │
│   - What they return                                            │
│   - What events can be emitted                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.4 Bytecode

Bytecode adalah representasi biner dari smart contract yang akan dieksekusi oleh EVM:

```
Source Code (Solidity)     Compile      Bytecode (Hex)
┌──────────────────────┐    ─────►    ┌─────────────────────┐
│ function claim() {   │              │ 0x608060405234801   │
│   rewards[msg.sender]│              │ 561001057600080fd   │
│   += rewardAmount;   │              │ 5b5060405161...     │
│ }                    │              │                     │
└──────────────────────┘              └─────────────────────┘
```

## 9. Troubleshooting

### 9.1 Error Compile Umum

| Error                                               | Penyebab                       | Solusi                               |
| --------------------------------------------------- | ------------------------------ | ------------------------------------ |
| `ParserError: Expected ';'`                       | Kurang titik koma              | Tambahkan `;` di akhir statement   |
| `DeclarationError: Identifier not found`          | Variable tidak dideklarasi     | Cek nama variable                    |
| `TypeError: ... is not implicitly convertible`    | Tipe data tidak cocok          | Cek tipe data                        |
| `CompilerError: Stack too deep`                   | Terlalu banyak local variables | Refactor code                        |
| `Source file requires different compiler version` | Versi pragma tidak cocok       | Sesuaikan versi di hardhat.config.ts |

### 9.2 Contoh Error dan Solusi

**Error: Kurang titik koma**

```solidity
// Error
uint256 public rewardAmount  // Kurang ;

// Fix
uint256 public rewardAmount;
```

**Error: Versi compiler tidak cocok**

```solidity
// Contract pakai ^0.8.20
pragma solidity ^0.8.20;
```

```typescript
// hardhat.config.ts pakai 0.8.17
export default defineConfig({
  solidity: {
    profiles: {
      default: {
        version: "0.8.17"  // Error! Tidak cocok dengan pragma
      }
    }
  }
});

// Fix: sesuaikan versi
export default defineConfig({
  solidity: {
    profiles: {
      default: {
        version: "0.8.20"  // Sesuai dengan pragma di contract
      }
    }
  }
});
```

**Error: Typo nama function**

```solidity
// Error
function claimReward() public {
    rewards[msg.sender] += rewardAmout;  // Typo: rewardAmout
}

// Fix
function claimReward() public {
    rewards[msg.sender] += rewardAmount;  // Correct
}
```

### 9.3 Tips Debugging

1. **Baca error message dengan teliti** - Solidity compiler memberikan informasi yang cukup detail
2. **Cek line number** - Error message biasanya mencantumkan baris yang bermasalah
3. **Compile sering** - Compile setiap selesai menulis satu function
4. **Gunakan VS Code extension** - Solidity extension memberikan real-time error highlighting

---

## Tugas

Sifat: Individu

- Setiap mahasiswa membuat Github repository untuk Tugas Blockchain.

### Tugas 1: Setup Project

1. Buat project Hardhat baru dengan nama `project2-smart-contract`
2. Pilih opsi **"Create a TypeScript project (with Mocha + Ethers.js)"**
3. Konfigurasi `hardhat.config.ts` dengan network localhost dan ganache

### Tugas 2: Buat Smart Contract

1. Buat smart contract sesuai tema project kalian
2. Contract minimal memiliki:
   - 2 state variables
   - 1 mapping
   - 1 event
   - 1 modifier
   - 3 functions
3. Compile dan pastikan tidak ada error

### Deliverable

Kumpulkan:

1. Screenshot hasil `npx hardhat compile`
2. Screenshot struktur folder project
3. Link repository GitHub (jika sudah di-commit)

## Referensi

- [Hardhat Documentation](https://hardhat.org/docs)
- [Hardhat Getting Started](https://hardhat.org/hardhat-runner/docs/getting-started)
- [Solidity Documentation](https://docs.soliditylang.org/)
