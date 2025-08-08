from faker import Faker
import mysql.connector
import os
import time
from Crypto.Cipher import Salsa20

fake = Faker()
key = os.urandom(32)  # Salsa20 needs a 32-byte key
print("🔑 Save this key for decryption:", key.hex())

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hotdog12",
    database="encryption_test"
)
cursor = conn.cursor()

start_time = time.time()

for _ in range(1000):
    username = fake.user_name()
    activity = fake.sentence()
    timestamp = fake.date_time_this_year()
    ip_address = fake.ipv4()
    sensitive_data = fake.sentence()

    nonce = os.urandom(8)  # ✅ This is correct
    cipher = Salsa20.new(key=key, nonce=nonce)
    ciphertext = cipher.encrypt(sensitive_data.encode())

    # Insert into users table
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
    user_id = cursor.lastrowid

    # Insert into user_logs table
    cursor.execute("""
        INSERT INTO user_logs (log_id, username, activity, timestamp, ip_address, sensitive_data, nonce)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user_id, username, activity, timestamp, ip_address, ciphertext, nonce))

conn.commit()
cursor.close()
conn.close()

end_time = time.time()
print("✅ Successfully inserted 1000 encrypted Salsa20 records.")
print("⏱️ Time taken:", round(end_time - start_time, 2), "seconds")
