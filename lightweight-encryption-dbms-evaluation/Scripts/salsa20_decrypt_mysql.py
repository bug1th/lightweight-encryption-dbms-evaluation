import mysql.connector
from Crypto.Cipher import Salsa20
import binascii

# Use your saved Salsa20 key
key = bytes.fromhex("72e5c380368d44c6bf68dcf6f974a330a471f6822acfe9131a525fe583ad0d06")

# Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hotdog12",
    database="encryption_test"
)
cursor = conn.cursor()

# Fetch encrypted data and nonce
cursor.execute("""
    SELECT u.username, l.sensitive_data, l.nonce
    FROM users u
    JOIN user_logs l ON u.id = l.log_id
    LIMIT 5;
""")
records = cursor.fetchall()

print("\n🔓 Decrypted Records:\n")
for username, ciphertext, nonce in records:
    try:
        cipher = Salsa20.new(key=key, nonce=nonce)
        decrypted = cipher.decrypt(ciphertext).decode()
        print(f"🧍 {username}: {decrypted}")
    except Exception as e:
        print(f"❌ {username}: Decryption failed → {e}")

cursor.close()
conn.close()
