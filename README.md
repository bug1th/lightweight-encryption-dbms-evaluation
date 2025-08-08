# lightweight-encryption-dbms-evaluation
Testing ASCON, SPECK, AES, and Salsa20 on a real-time database system using Python and MySQL

# Lightweight Encryption Performance Evaluation on MySQL

## Overview
This repository contains the methodology, performance metrics, and test outputs for evaluating the performance of four encryption algorithms when applied to an **OLTP-style MySQL database**:

- **AES-128 (Fernet)**
- **ASCON**
- **SPECK**
- **Salsa20**

Each algorithm was implemented in Python to encrypt the `sensitive_data` column of a synthetic `user_logs` dataset, stored in MySQL 8.0, and decrypted at the application layer.  
Testing was done using **1,000 records** per algorithm.

---

## Repository Contents
- **performance_summary.xlsx** → Performance table for all encryption algorithms.
- **screenshots/** → Screenshots showing successful decryption for each encryption method.
- **insertion_scripts/** → Python scripts for inserting encrypted data into MySQL.
- **decryption_scripts/** → Python scripts for decrypting data from MySQL.
- **requirements.txt** → Python dependencies.

---

## Performance Summary

| Algorithm       | Insert Time (1k records) | Decrypt Time (avg) | JOIN Compatibility | CPU & Memory |
|-----------------|--------------------------|--------------------|--------------------|--------------|
| AES-128 (Fernet) | 0.65 s                  | < 0.05 s           | ✅ Yes             | Not Measured |
| ASCON           | 1.03 s                  | < 0.05 s           | ✅ Yes             | Not Measured |
| SPECK           | 0.91 s                  | < 0.05 s           | ✅ Yes             | Not Measured |
| Salsa20         | 0.79 s                  | < 0.05 s           | ✅ Yes             | Not Measured |

---

## How to Reproduce
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/lightweight-encryption-db-tests.git
   cd lightweight-encryption-db-tests
