# Modul 10. Smart Contract Testing

## Deskripsi

Modul ini membahas cara menulis **unit test** untuk smart contract menggunakan Hardhat. Testing adalah komponen krusial dalam development smart contract karena bug yang sudah dideploy ke blockchain sulit untuk diperbaiki.

## Tujuan Pembelajaran

Setelah menyelesaikan modul ini, mahasiswa mampu:

1. Memahami pentingnya testing dalam smart contract development
2. Menulis test menggunakan Mocha dan Chai
3. Menguji skenario berhasil (positive test)
4. Menguji skenario gagal (negative test)
5. Menguji access control
6. Menguji event emission
7. Menggunakan test coverage untuk mengukur kualitas test

## Prasyarat

- Sudah menyelesaikan Module 09 (Hardhat Setup & Compile)
- Project Hardhat sudah ter-setup dengan contract `CourseReward.sol`
- Memahami dasar JavaScript (function, async/await)

## List of Contents

- [Deskripsi](#deskripsi)
- [Tujuan Pembelajaran](#tujuan-pembelajaran)
- [Prasyarat](#prasyarat)
- [1. Pentingnya Testing](#1-pentingnya-testing)
- [2. Testing Framework di Hardhat](#2-testing-framework-di-hardhat)
- [3. Struktur Test File](#3-struktur-test-file)
- [4. Setup Test Environment](#4-setup-test-environment)
- [5. Menulis Test Cases](#5-menulis-test-cases)
- [6. Test Skenario Gagal](#6-test-skenario-gagal)
- [7. Test Access Control](#7-test-access-control)
- [8. Test Event](#8-test-event)
- [9. Menjalankan Test](#9-menjalankan-test)
- [10. Test Coverage](#10-test-coverage)
- [Ringkasan](#ringkasan)
- [Tugas](#tugas)

---

## 1. Pentingnya Testing

### 1.1 Mengapa Smart Contract Harus Ditest?

```
┌─────────────────────────────────────────────────────────────────┐
│               MENGAPA TESTING PENTING?                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ❌ Tanpa Testing:                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │   Write     │───►│   Deploy    │───►│    BUG!     │          │
│  │   Code      │    │  to Chain   │    │  Sulit Fix  │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│                                                                 │
│  ✅ Dengan Testing:                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │   Write     │───►│    Test     │───►│   Deploy    │          │
│  │   Code      │    │  Locally    │    │  Confident  │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│                            │                                    │
│                            ▼                                    │
│                     ┌─────────────┐                             │
│                     │  Find Bug   │                             │
│                     │  Fix Early  │                             │
│                     └─────────────┘                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Karakteristik Smart Contract

| Karakteristik       | Implikasi                            |
| ------------------- | ------------------------------------ |
| **Immutable** | Tidak bisa diubah setelah deploy     |
| **Public**    | Semua orang bisa lihat dan panggil   |
| **Financial** | Sering mengelola aset bernilai       |
| **Permanent** | Bug tercatat selamanya di blockchain |

### 1.3 Manual Testing vs Automated Testing

| Aspek                   | Manual (Remix)              | Automated (Hardhat)      |
| ----------------------- | --------------------------- | ------------------------ |
| **Proses**        | Klik function satu per satu | Jalankan script          |
| **Repeatability** | Sulit diulang persis sama   | Selalu konsisten         |
| **Coverage**      | Mudah lupa skenario         | Semua skenario tercatat  |
| **Documentation** | Tidak ada                   | Test sebagai dokumentasi |
| **CI/CD**         | Tidak bisa                  | Bisa otomatis            |

## 2. Testing Framework di Hardhat

### 2.1 Komponen Testing

Hardhat menggunakan kombinasi tools untuk testing:

| Tool                            | Fungsi                                     |
| ------------------------------- | ------------------------------------------ |
| **Mocha**                 | Test framework (describe, it, beforeEach)  |
| **Chai**                  | Assertion library (expect, to.equal)       |
| **Hardhat Chai Matchers** | Assertion khusus untuk smart contract      |
| **Ethers.js**             | Library untuk berinteraksi dengan contract |

### 2.2 Instalasi

Jika menggunakan Hardhat Toolbox, semua sudah terinstall:

```bash
npm install --save-dev @nomicfoundation/hardhat-toolbox
```

### 2.3 Konsep Dasar (Hardhat 3)

> **Catatan Hardhat 3**: Menggunakan `network.create()` untuk mendapatkan `ethers` dan `networkHelpers`, serta menggunakan fixture pattern dengan `loadFixture()`.

```typescript
import { expect } from "chai";
import { network } from "hardhat";

// Buat network connection (top-level await di Hardhat 3)
const { ethers, networkHelpers } = await network.create();

// Mocha: describe dan it
describe("Nama Test Suite", function () {
  // Fixture pattern: deploy contract sekali, di-cache untuk setiap test
  async function deployFixture() {
    const [owner] = await ethers.getSigners();
    const contract = await ethers.deployContract("ContractName", [args]);
    return { contract, owner };
  }

  it("Nama test case", async function () {
    const { contract, owner } = await networkHelpers.loadFixture(deployFixture);
    // Test code menggunakan contract dan owner
  });
});

// Chai: expect assertions
expect(value).to.equal(expectedValue);
expect(promise).to.be.revertedWith("Error message");
```

---

## 3. Struktur Test File

### 3.1 Buat File Test

Hapus test sample dan buat file baru:

```bash
rm test/Lock.js
```

Buat file `test/CourseReward.test.ts`:

> **Catatan Hardhat 3**: Menggunakan TypeScript dan fixture pattern.

```typescript
import { expect } from "chai";
import { network } from "hardhat";

// Buat network connection (top-level await di Hardhat 3)
const { ethers, networkHelpers } = await network.create();

describe("CourseReward", function () {
  const INITIAL_REWARD = 100;

  // Fixture untuk deploy contract (di-cache oleh loadFixture)
  async function deployFixture() {
    const [owner, student1, student2] = await ethers.getSigners();
    const courseReward = await ethers.deployContract("CourseReward", [INITIAL_REWARD]);
    return { courseReward, owner, student1, student2 };
  }

  // Test cases menggunakan fixture
  it("should do something", async function () {
    const { courseReward, owner } = await networkHelpers.loadFixture(deployFixture);
    // Test code
  });
});
```

### 3.2 Anatomi Test File (Hardhat 3 dengan Fixture Pattern)

```
┌─────────────────────────────────────────────────────────────────┐
│                STRUKTUR TEST FILE (HARDHAT 3)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Import dependencies                                         │
│     ├── chai (expect)                                           │
│     └── network (dari hardhat)                                  │
│                                                                 │
│  2. await network.create()                                      │
│     └── Mendapatkan ethers & networkHelpers                     │
│                                                                 │
│  3. describe("Contract Name", function () {                     │
│     │                                                           │
│     ├── 4. async function deployFixture() {                     │
│     │      // Deploy contract dan return semua yang dibutuhkan  │
│     │      return { contract, owner, user };                    │
│     │   }                                                       │
│     │                                                           │
│     ├── 5. describe("Feature Group", function () {              │
│     │      │                                                    │
│     │      ├── it("should do X", async function () {            │
│     │      │      const { contract } = await                    │
│     │      │        networkHelpers.loadFixture(deployFixture);  │
│     │      │   });                                              │
│     │      │                                                    │
│     │      └── it("should do Y", async function () { ... });    │
│     │   });                                                     │
│     │                                                           │
│     └── describe("Another Feature", function () { ... });       │
│  });                                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Keuntungan Fixture Pattern vs beforeEach

| Aspek                | beforeEach (Hardhat 2)       | Fixture Pattern (Hardhat 3)           |
| -------------------- | ---------------------------- | ------------------------------------- |
| **Caching**    | Deploy ulang setiap test     | Di-cache, snapshot blockchain state   |
| **Performa**   | Lambat untuk banyak test     | Cepat karena state di-reset via snapshot |
| **Isolation**  | Setiap test independen       | Setiap test independen                |
| **State**      | Harus reset manual           | Otomatis reset ke snapshot awal       |

## 4. Setup Test Environment

### 4.1 Fixture Pattern: Deploy dengan Caching (Hardhat 3)

> **Catatan Hardhat 3**: Fixture pattern menggantikan `beforeEach`. Fixture di-cache sehingga tidak perlu deploy ulang setiap test - state di-reset via blockchain snapshot.

```typescript
import { expect } from "chai";
import { network } from "hardhat";

// Buat network connection (top-level await di Hardhat 3)
const { ethers, networkHelpers } = await network.create();

describe("CourseReward", function () {
  const INITIAL_REWARD = 100;

  // Fixture untuk deploy contract (di-cache oleh loadFixture)
  async function deployFixture() {
    // Ambil signers (akun testing)
    const [owner, student1, student2] = await ethers.getSigners();

    // Deploy contract baru
    const courseReward = await ethers.deployContract("CourseReward", [INITIAL_REWARD]);

    return { courseReward, owner, student1, student2 };
  }

  it("should deploy successfully", async function () {
    const { courseReward } = await networkHelpers.loadFixture(deployFixture);
    expect(await courseReward.rewardAmount()).to.equal(INITIAL_REWARD);
  });
});
```

### 4.2 Penjelasan Kode

| Kode                                        | Penjelasan                                |
| ------------------------------------------- | ----------------------------------------- |
| `network.create()`                        | Membuat koneksi network Hardhat 3         |
| `ethers.getSigners()`                     | Mendapatkan array akun testing            |
| `ethers.deployContract()`                 | Deploy contract langsung                  |
| `networkHelpers.loadFixture()`            | Menjalankan fixture dengan caching        |
| `return { ... }`                          | Mengembalikan semua yang dibutuhkan test  |

### 4.3 Mengapa Fixture Pattern?

```
┌─────────────────────────────────────────────────────────────────┐
│                    FIXTURE PATTERN FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Pertama kali:                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ deployFixture() dijalankan → State disimpan sebagai snapshot││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  Test 1              Test 2              Test 3                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │ loadFixture │    │ loadFixture │    │ loadFixture │          │
│  │ → Reset ke  │    │ → Reset ke  │    │ → Reset ke  │          │
│  │   snapshot  │    │   snapshot  │    │   snapshot  │          │
│  │             │    │             │    │             │          │
│  │ it("test1") │    │ it("test2") │    │ it("test3") │          │
│  │ // fresh    │    │ // fresh    │    │ // fresh    │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│                                                                 │
│  ✅ Deploy hanya SEKALI, state di-reset via snapshot!           │
│  ✅ Lebih cepat daripada beforeEach yang deploy ulang           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 5. Menulis Test Cases

### 5.1 Test Deployment

```typescript
describe("Deployment", function () {
  it("should set the correct owner", async function () {
    const { courseReward, owner } = await networkHelpers.loadFixture(deployFixture);
    expect(await courseReward.owner()).to.equal(owner.address);
  });

  it("should set the correct initial reward amount", async function () {
    const { courseReward } = await networkHelpers.loadFixture(deployFixture);
    expect(await courseReward.rewardAmount()).to.equal(INITIAL_REWARD);
  });

  it("should have zero rewards for new addresses", async function () {
    const { courseReward, student1 } = await networkHelpers.loadFixture(deployFixture);
    expect(await courseReward.rewards(student1.address)).to.equal(0n);
  });
});
```

### 5.2 Test Fungsi Utama: claimReward

```typescript
describe("Claim Reward", function () {
  it("should allow student to claim reward", async function () {
    const { courseReward, student1 } = await networkHelpers.loadFixture(deployFixture);

    // Student1 claim reward
    await courseReward.connect(student1).claimReward();

    // Cek reward bertambah
    expect(await courseReward.rewards(student1.address)).to.equal(INITIAL_REWARD);

    // Cek status hasClaimed
    expect(await courseReward.hasClaimed(student1.address)).to.equal(true);
  });

  it("should update rewards mapping correctly", async function () {
    const { courseReward, student1 } = await networkHelpers.loadFixture(deployFixture);

    // Sebelum claim
    expect(await courseReward.connect(student1).getMyReward()).to.equal(0n);

    // Claim
    await courseReward.connect(student1).claimReward();

    // Setelah claim - pakai connect untuk "impersonate"
    expect(await courseReward.connect(student1).getMyReward()).to.equal(INITIAL_REWARD);
  });
});
```

### 5.3 Penjelasan `connect()`

```javascript
// Default: transaksi dari owner (akun pertama)
await courseReward.claimReward();  // msg.sender = owner

// Dengan connect: transaksi dari akun lain
await courseReward.connect(student1).claimReward();  // msg.sender = student1
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONNECT EXPLANATION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Tanpa connect:                                                 │
│  courseReward.claimReward()                                     │
│       │                                                         │
│       └──► msg.sender = owner (default signer)                  │
│                                                                 │
│  Dengan connect:                                                │
│  courseReward.connect(student1).claimReward()                   │
│       │                                                         │
│       └──► msg.sender = student1                                │
│                                                                 │
│  Ini penting untuk test multi-user scenarios!                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 6. Test Skenario Gagal

### 6.1 Mengapa Test Skenario Gagal?

Test yang baik tidak hanya mengecek "happy path", tapi juga memastikan error handling bekerja dengan benar.

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEST COVERAGE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ Positive Tests (Happy Path):                                │
│     - Student bisa claim reward                                 │
│     - Owner bisa ubah reward                                    │
│                                                                 │
│  ✅ Negative Tests (Error Cases):                               │
│     - Student tidak bisa claim dua kali                         │
│     - Non-owner tidak bisa ubah reward                          │
│     - Invalid input handling                                    │
│                                                                 │
│  Test yang baik = Positive + Negative tests                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Test: Tidak Boleh Claim Dua Kali

```typescript
describe("Claim Restrictions", function () {
  it("should not allow student to claim twice", async function () {
    const { courseReward, student1 } = await networkHelpers.loadFixture(deployFixture);

    // Claim pertama - berhasil
    await courseReward.connect(student1).claimReward();

    // Claim kedua - harus gagal
    await expect(
      courseReward.connect(student1).claimReward()
    ).to.be.revertedWith("Reward already claimed");
  });

  it("should allow different students to claim", async function () {
    const { courseReward, student1, student2 } = await networkHelpers.loadFixture(deployFixture);

    // Student1 claim
    await courseReward.connect(student1).claimReward();

    // Student2 juga bisa claim (berbeda orang)
    await courseReward.connect(student2).claimReward();

    expect(await courseReward.rewards(student1.address)).to.equal(INITIAL_REWARD);
    expect(await courseReward.rewards(student2.address)).to.equal(INITIAL_REWARD);
  });
});
```

### 6.3 Pattern: revertedWith

```javascript
// Memastikan transaksi gagal dengan error message tertentu
await expect(
  contract.functionThatShouldFail()
).to.be.revertedWith("Expected error message");

// Atau untuk custom error (Solidity 0.8.4+)
await expect(
  contract.functionThatShouldFail()
).to.be.revertedWithCustomError(contract, "CustomErrorName");
```

## 7. Test Access Control

### 7.1 Test Owner Functions

```typescript
describe("Access Control", function () {
  describe("setRewardAmount", function () {
    it("should allow owner to change reward amount", async function () {
      const { courseReward } = await networkHelpers.loadFixture(deployFixture);
      const newAmount = 200;

      await courseReward.setRewardAmount(newAmount);

      expect(await courseReward.rewardAmount()).to.equal(newAmount);
    });

    it("should reject non-owner changing reward amount", async function () {
      const { courseReward, student1 } = await networkHelpers.loadFixture(deployFixture);

      await expect(
        courseReward.connect(student1).setRewardAmount(200)
      ).to.be.revertedWith("Only owner can call this function");
    });
  });
});
```

### 7.2 Pattern Test Access Control

```
┌─────────────────────────────────────────────────────────────────┐
│                ACCESS CONTROL TEST PATTERN                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Untuk setiap function dengan modifier (onlyOwner, dll):        │
│                                                                 │
│  1. Test authorized user BISA memanggil                         │
│     it("owner should be able to...", async function () {        │
│       await contract.restrictedFunction();  // ✅ Success       │
│     });                                                         │
│                                                                 │
│  2. Test unauthorized user TIDAK BISA memanggil                 │
│     it("non-owner should not be able to...", async function () {│
│       await expect(                                             │
│         contract.connect(nonOwner).restrictedFunction()         │
│       ).to.be.revertedWith("...");  // ✅ Reverted              │
│     });                                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 8. Test Event

### 8.1 Mengapa Test Event?

Event penting untuk:

- Frontend listening (realtime updates)
- Indexing (The Graph, dll)
- Audit trail

### 8.2 Test Event Emission

```typescript
describe("Events", function () {
  it("should emit RewardClaimed event when student claims", async function () {
    const { courseReward, student1 } = await networkHelpers.loadFixture(deployFixture);

    await expect(courseReward.connect(student1).claimReward())
      .to.emit(courseReward, "RewardClaimed")
      .withArgs(student1.address, INITIAL_REWARD);
  });

  it("should emit RewardAmountChanged when owner changes amount", async function () {
    const { courseReward } = await networkHelpers.loadFixture(deployFixture);
    const oldAmount = INITIAL_REWARD;
    const newAmount = 200;

    await expect(courseReward.setRewardAmount(newAmount))
      .to.emit(courseReward, "RewardAmountChanged")
      .withArgs(oldAmount, newAmount);
  });
});
```

### 8.3 Pattern Test Event

```javascript
// Test bahwa event di-emit
await expect(transaction)
  .to.emit(contract, "EventName");

// Test event dengan arguments
await expect(transaction)
  .to.emit(contract, "EventName")
  .withArgs(arg1, arg2, arg3);

// Test multiple events
await expect(transaction)
  .to.emit(contract, "Event1")
  .to.emit(contract, "Event2");
```

## 9. Menjalankan Test

### 9.1 File Test Lengkap

Berikut file test lengkap `test/CourseReward.test.ts` (Hardhat 3):

```typescript
import { expect } from "chai";
import { network } from "hardhat";

// Buat network connection (top-level await di Hardhat 3)
const { ethers, networkHelpers } = await network.create();

describe("CourseReward", function () {
  const INITIAL_REWARD = 100;

  // Fixture untuk deploy contract (di-cache oleh loadFixture)
  async function deployFixture() {
    const [owner, student1, student2] = await ethers.getSigners();
    const courseReward = await ethers.deployContract("CourseReward", [INITIAL_REWARD]);
    return { courseReward, owner, student1, student2 };
  }

  describe("Deployment", function () {
    it("should set the correct owner", async function () {
      const { courseReward, owner } = await networkHelpers.loadFixture(deployFixture);
      expect(await courseReward.owner()).to.equal(owner.address);
    });

    it("should set the correct initial reward amount", async function () {
      const { courseReward } = await networkHelpers.loadFixture(deployFixture);
      expect(await courseReward.rewardAmount()).to.equal(INITIAL_REWARD);
    });
  });

  describe("Claim Reward", function () {
    it("should allow student to claim reward", async function () {
      const { courseReward, student1 } = await networkHelpers.loadFixture(deployFixture);
      await courseReward.connect(student1).claimReward();

      expect(await courseReward.rewards(student1.address)).to.equal(INITIAL_REWARD);
      expect(await courseReward.hasClaimed(student1.address)).to.equal(true);
    });

    it("should not allow student to claim twice", async function () {
      const { courseReward, student1 } = await networkHelpers.loadFixture(deployFixture);
      await courseReward.connect(student1).claimReward();

      await expect(
        courseReward.connect(student1).claimReward()
      ).to.be.revertedWith("Reward already claimed");
    });

    it("should allow different students to claim", async function () {
      const { courseReward, student1, student2 } = await networkHelpers.loadFixture(deployFixture);
      await courseReward.connect(student1).claimReward();
      await courseReward.connect(student2).claimReward();

      expect(await courseReward.rewards(student1.address)).to.equal(INITIAL_REWARD);
      expect(await courseReward.rewards(student2.address)).to.equal(INITIAL_REWARD);
    });
  });

  describe("Access Control", function () {
    it("should allow owner to change reward amount", async function () {
      const { courseReward } = await networkHelpers.loadFixture(deployFixture);
      await courseReward.setRewardAmount(200);
      expect(await courseReward.rewardAmount()).to.equal(200);
    });

    it("should reject non-owner changing reward amount", async function () {
      const { courseReward, student1 } = await networkHelpers.loadFixture(deployFixture);
      await expect(
        courseReward.connect(student1).setRewardAmount(200)
      ).to.be.revertedWith("Only owner can call this function");
    });
  });

  describe("Events", function () {
    it("should emit RewardClaimed event", async function () {
      const { courseReward, student1 } = await networkHelpers.loadFixture(deployFixture);
      await expect(courseReward.connect(student1).claimReward())
        .to.emit(courseReward, "RewardClaimed")
        .withArgs(student1.address, INITIAL_REWARD);
    });

    it("should emit RewardAmountChanged event", async function () {
      const { courseReward } = await networkHelpers.loadFixture(deployFixture);
      await expect(courseReward.setRewardAmount(200))
        .to.emit(courseReward, "RewardAmountChanged")
        .withArgs(INITIAL_REWARD, 200);
    });
  });
});
```

### 9.2 Jalankan Test

```bash
npx hardhat test
```

**Expected Output:**

```text
  CourseReward
    Deployment
      ✔ should set the correct owner
      ✔ should set the correct initial reward amount
    Claim Reward
      ✔ should allow student to claim reward
      ✔ should not allow student to claim twice
      ✔ should allow different students to claim
    Access Control
      ✔ should allow owner to change reward amount
      ✔ should reject non-owner changing reward amount
    Events
      ✔ should emit RewardClaimed event
      ✔ should emit RewardAmountChanged event

  9 passing (1s)
```

### 9.3 Opsi Test Command

| Command                                        | Fungsi                                |
| ---------------------------------------------- | ------------------------------------- |
| `npx hardhat test`                           | Jalankan semua test                   |
| `npx hardhat test test/CourseReward.test.js` | Jalankan test spesifik                |
| `npx hardhat test --grep "claim"`            | Jalankan test yang mengandung "claim" |
| `npx hardhat test --parallel`                | Jalankan test secara parallel         |

## 10. Test Coverage

### 10.1 Apa itu Test Coverage?

Test coverage mengukur berapa persen kode yang diuji oleh test.

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEST COVERAGE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Coverage mengukur:                                             │
│                                                                 │
│  ┌────────────────┐                                             │
│  │ Statements     │  Berapa % statement yang dieksekusi         │
│  ├────────────────┤                                             │
│  │ Branches       │  Berapa % if/else yang ditest               │
│  ├────────────────┤                                             │
│  │ Functions      │  Berapa % function yang dipanggil           │
│  ├────────────────┤                                             │
│  │ Lines          │  Berapa % baris yang dieksekusi             │
│  └────────────────┘                                             │
│                                                                 │
│  Target ideal: 80-100% coverage                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 10.2 Jalankan Coverage

```bash
npx hardhat coverage
```

**Expected Output:**

```text
------------------|----------|----------|----------|----------|
File              |  % Stmts | % Branch |  % Funcs |  % Lines |
------------------|----------|----------|----------|----------|
 contracts/       |      100 |       75 |      100 |      100 |
  CourseReward.sol|      100 |       75 |      100 |      100 |
------------------|----------|----------|----------|----------|
All files         |      100 |       75 |      100 |      100 |
------------------|----------|----------|----------|----------|
```

### 10.3 Membaca Coverage Report

| Metric     | Nilai | Interpretasi                                |
| ---------- | ----- | ------------------------------------------- |
| Statements | 100%  | Semua statement dieksekusi ✅               |
| Branch     | 75%   | Ada branch (if/else) yang belum ditest ⚠️ |
| Functions  | 100%  | Semua function dipanggil ✅                 |
| Lines      | 100%  | Semua baris dieksekusi ✅                   |

### 10.4 HTML Coverage Report

Coverage juga generate HTML report di folder `coverage/`:

```bash
open coverage/index.html  # Mac
start coverage/index.html  # Windows
```

---

## Tugas

### Tugas 1: Tulis Test untuk Contract Anda

1. Buat file test untuk smart contract project Anda
2. Minimal 5 test case:
   - Test deployment
   - Test fungsi utama (positive)
   - Test skenario gagal (negative)
   - Test access control
   - Test event

### Tugas 2: Achieve 80% Coverage

1. Jalankan `npx hardhat coverage`
2. Pastikan coverage minimal 80% untuk semua metrics
3. Screenshot hasil coverage

### Tugas 3: Tambah Test Case Kreatif

1. Tambahkan minimal 1 test case yang tidak ada di modul
2. Jelaskan mengapa test tersebut penting

### Deliverable

Kumpulkan:

1. File test (`test/NamaContract.test.js`)
2. Screenshot hasil `npx hardhat test` (semua passing)
3. Screenshot hasil `npx hardhat coverage`

## Referensi

- [Hardhat Testing Documentation](https://hardhat.org/tutorial/testing-contracts)
- [Chai Assertion Library](https://www.chaijs.com/)
- [Hardhat Chai Matchers](https://hardhat.org/hardhat-chai-matchers/docs/overview)
- [Mocha Test Framework](https://mochajs.org/)
