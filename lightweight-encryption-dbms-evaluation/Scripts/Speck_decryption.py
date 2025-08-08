# speck_decrypt_mysql.py

import mysql.connector
from speck import SpeckCipher  # Make sure speck.py is in your project
import binascii
import time

# ========== CONFIG ==========
key_hex = "f6bc97ab7d325415184bd4c34244bfec"  # Replace with your actual key
key = int(key_hex, 16)

# ========== SETUP ==========
cipher = SpeckCipher(key)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hotdog12",  # Replace with your MySQL password
    database="encryption_test"  # Replace with your database name
)
cursor = db.cursor()

# ========== FETCH ENCRYPTED RECORDS ==========
cursor.execute("SELECT u.username, l.sensitive_data FROM users u JOIN user_logs l ON u.id = l.log_id LIMIT 5")
rows = cursor.fetchall()

print("🔓 Decrypted Records:\n")

for username, encrypted_blob in rows:
    try:
        ciphertext = int(binascii.hexlify(encrypted_blob), 16)
        decrypted_text = cipher.decrypt(ciphertext)
        decrypted_bytes = decrypted_text.to_bytes((decrypted_text.bit_length() + 7) // 8, 'big')
        decrypted_str = decrypted_bytes.decode(errors='ignore')

        print(f"🧍 {username}: {decrypted_str}")

    except Exception as e:
        print(f"❌ {username}: Decryption failed → {e}")
