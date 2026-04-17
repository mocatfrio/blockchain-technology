# Module 01. Installation Guide: Python dan Visual Studio Code

## Deskripsi

Panduan ini membantu peserta menyiapkan lingkungan belajar dengan menginstal **Python** dan **Visual Studio Code (VS Code)**. Setelah mengikuti langkah-langkah ini, peserta akan siap menjalankan program Python untuk praktikum Blockchain Technology.

## List of Contents

- [Deskripsi](#deskripsi)
- [List of Contents](#list-of-contents)
- [1. Instalasi Python](#1-instalasi-python)
  - [1.1 Unduh Python](#11-unduh-python)
  - [1.2 Instal Python di Windows](#12-instal-python-di-windows)
  - [1.3 Instal Python di macOS](#13-instal-python-di-macos)
  - [1.4 Instal Python di Linux](#14-instal-python-di-linux)
- [2. Verifikasi Instalasi Python](#2-verifikasi-instalasi-python)
- [3. Instalasi Visual Studio Code](#3-instalasi-visual-studio-code)
  - [3.1 Unduh VS Code](#31-unduh-vs-code)
  - [3.2 Instal VS Code di Windows](#32-instal-vs-code-di-windows)
  - [3.3 Instal VS Code di macOS](#33-instal-vs-code-di-macos)
  - [3.4 Instal VS Code di Linux](#34-instal-vs-code-di-linux)
- [4. Membuat dan Menjalankan Program Python Pertama](#4-membuat-dan-menjalankan-program-python-pertama)
  - [4.1 Buat Folder Project](#41-buat-folder-project)
  - [4.2 Buat File Python](#42-buat-file-python)
  - [4.3 Jalankan Program](#43-jalankan-program)

## 1. Instalasi Python

### 1.1 Unduh Python

Buka situs resmi Python:

```text
https://www.python.org/downloads/
```

Unduh versi Python terbaru yang direkomendasikan untuk sistem operasi Anda:

* Windows
* macOS
* Linux

### 1.2 Instal Python di Windows

1. Jalankan file installer Python yang sudah diunduh
2. Centang opsi:

```text
Add Python to PATH
```

3. Klik **Install Now**
4. Tunggu hingga proses instalasi selesai
5. Klik **Close**

> Penting: Jangan lupa mencentang **Add Python to PATH** agar Python dapat dijalankan dari terminal.

### 1.3 Instal Python di macOS

1. Buka file installer Python `.pkg`
2. Ikuti langkah instalasi sampai selesai
3. Setelah selesai, buka Terminal untuk memeriksa instalasi

### 1.4 Instal Python di Linux

Pada beberapa distribusi Linux, Python sudah terpasang secara default. Untuk memastikan atau menginstalnya, jalankan:

```bash
sudo apt update
sudo apt install python3
```

Untuk distribusi lain, gunakan package manager yang sesuai.

## 2. Verifikasi Instalasi Python

Buka terminal atau command prompt, lalu jalankan:

```bash
python --version
```

atau jika sistem menggunakan `python3`:

```bash
python3 --version
```

Contoh output:

```text
Python 3.12.0
```

Jika versi Python muncul, berarti instalasi berhasil.

## 3. Instalasi Visual Studio Code

### 3.1 Unduh VS Code

Buka situs resmi Visual Studio Code:

```text
https://code.visualstudio.com/
```

Unduh installer sesuai sistem operasi Anda.

### 3.2 Instal VS Code di Windows

1. Jalankan file installer VS Code
2. Klik **Next**
3. Setujui license agreement
4. Pilih lokasi instalasi
5. Pada bagian opsi tambahan, disarankan mencentang:

   * Add to PATH
   * Add "Open with Code" action
6. Klik **Install**
7. Setelah selesai, klik **Finish**

### 3.3 Instal VS Code di macOS

1. Unduh file VS Code
2. Ekstrak file jika diperlukan
3. Pindahkan aplikasi **Visual Studio Code** ke folder **Applications**
4. Buka VS Code

### 3.4 Instal VS Code di Linux

Untuk Ubuntu atau Debian:

```bash
sudo snap install --classic code
```

Atau gunakan package installer dari situs resmi VS Code.

## 4. Membuat dan Menjalankan Program Python Pertama

### 4.1 Buat Folder Project

Buat folder baru, misalnya:

```text
blockchain-python
```

Lalu buka folder tersebut di VS Code.

### 4.2 Buat File Python

Buat file baru bernama:

```text
hello.py
```

Isi file dengan kode berikut:

```python
print("Hello, Blockchain World!")
```

### 4.3 Jalankan Program

Buka terminal di VS Code, lalu jalankan:

```bash
python hello.py
```

atau:

```bash
python3 hello.py
```

Contoh output:

```text
Hello, Blockchain World!
```
