import mysql.connector
from ascon import decrypt
import binascii

# Convert your saved hex key back into bytes
key = bytes.fromhex("08a083690d3ca432bc4776a22cf84df1")

# Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",       # <- replace with your MySQL username
    password="hotdog12",   # <- replace with your MySQL password
    database="encryption_test"    # <- replace with your database name
)
cursor = conn.cursor()

# Execute the JOIN query
cursor.execute("""
    SELECT u.username, l.sensitive_data, l.nonce
    FROM users u
    JOIN user_logs l ON u.username = l.username
    LIMIT 10
""")

results = cursor.fetchall()

print("\n🔓 Decrypted Join Results:\n")
for username, encrypted_data, nonce in results:
    try:
        if encrypted_data and nonce:
            plaintext = decrypt(
                key=key,
                nonce=nonce,
                associateddata=b"",  # Empty AD
                ciphertext=encrypted_data
            )
            print(f"🧍 {username}: {plaintext.decode()}")
        else:
            print(f"🧍 {username}: ❌ Missing data (nonce or ciphertext)")
    except Exception as e:
        print(f"🧍 {username}: ❌ Decryption failed → {e}")

cursor.close()
conn.close()
