import os
import mysql.connector
from faker import Faker
from ascon import encrypt
import time

# ====== FIXED ASCON KEY ======
key = bytes.fromhex("08a083690d3ca432bc4776a22cf84df1")

# ====== CONNECT TO DATABASE ======
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hotdog12",
    database="encryption_test"
)
cursor = conn.cursor()

# ====== FAKE DATA GENERATOR ======
fake = Faker()

# ====== START TIMER ======
start_time = time.time()

# ====== INSERT 1000 ENCRYPTED RECORDS ======
for _ in range(1000):
    username = fake.user_name()
    message = fake.sentence()
    nonce = os.urandom(16)
    ciphertext = encrypt(
        key=key,
        nonce=nonce,
        associateddata=b"",
        plaintext=message.encode()
    )

    # Insert username into `users` table
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
    user_id = cursor.lastrowid

    # Insert encrypted data and nonce into `user_logs` table
    cursor.execute(
        "INSERT INTO user_logs (username, sensitive_data, nonce) VALUES (%s, %s, %s)",
        (username, ciphertext, nonce)
    )

conn.commit()

# ====== END TIMER ======
end_time = time.time()
elapsed_time = end_time - start_time

print("✅ Successfully inserted 1000 encrypted ASCON records.")
print(f"⏱️ Time taken: {elapsed_time:.2f} seconds")

# ====== CLOSE DB ======
conn.close()

