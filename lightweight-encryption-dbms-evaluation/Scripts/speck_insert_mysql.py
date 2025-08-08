# speck_insert_mysql.py

import mysql.connector
from faker import Faker
from datetime import datetime
from speck import SpeckCipher  # Make sure speck.py is in the same folder
import time

# ========== Database Connection ==========
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hotdog12",  # Change this
    database="encryption_test"    # Change this
)
cursor = conn.cursor()

# ========== SPECK Cipher Setup ==========
key_hex = "f6bc97ab7d325415184bd4c34244bfec"  # Your fixed key
key = int.from_bytes(bytes.fromhex(key_hex), byteorder='big')
cipher = SpeckCipher(key)

# ========== Faker Setup ==========
fake = Faker()

# ========== Insert Records ==========
start_time = time.time()

for _ in range(1000):
    username = fake.user_name()
    activity = fake.sentence()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = fake.ipv4()
    plaintext = fake.sentence().encode()

    # Encrypt
    plaintext = fake.sentence()
    plaintext_int = int.from_bytes(plaintext.encode(), byteorder='big')
    ciphertext = cipher.encrypt(plaintext_int)
    ciphertext_bytes = ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, byteorder='big')

    # Insert into users table
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
    user_id = cursor.lastrowid

    # Insert into user_logs table
    cursor.execute(
        "INSERT INTO user_logs (log_id, username, activity, timestamp, ip_address, sensitive_data) VALUES (%s, %s, %s, %s, %s, %s)",
        (user_id, username, activity, timestamp, ip_address, ciphertext_bytes)
    )

conn.commit()
end_time = time.time()

# ========== Done ==========
print("✅ Successfully inserted 1000 encrypted SPECK records.")
print(f"⏱️ Time taken: {round(end_time - start_time, 2)} seconds")

cursor.close()
conn.close()
