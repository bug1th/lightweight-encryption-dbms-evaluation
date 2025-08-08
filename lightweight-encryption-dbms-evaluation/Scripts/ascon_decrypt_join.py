import mysql.connector
import ascon
import binascii

# ========== SET YOUR SECRET KEY ==========
key = bytes.fromhex("08a083690d3ca432bc4776a22cf84df1")  # Replace with your saved key
print(f"🔑 Using key: {key.hex()}")

# ========== MYSQL CONNECTION ==========
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hotdog12",  # Replace with your actual MySQL password
    database="encryption_test"   # Replace with your actual database name
)

cursor = db.cursor()

# ========== FETCH ENCRYPTED DATA ==========
cursor.execute("SELECT username, sensitive_data, nonce FROM user_logs LIMIT 5")
records = cursor.fetchall()

print("\n🔓 Decrypted Records:\n")
for row in records:
    username, encrypted_data, nonce = row

    try:
        if encrypted_data is None or nonce is None:
            raise ValueError("Encrypted data or nonce is NULL.")

        plaintext = ascon.decrypt(
            key=key,
            nonce=nonce,
            associateddata=b"",  # Assuming you didn’t use AAD
            ciphertext=encrypted_data
        )

        print(f"🧍 {username}: {plaintext.decode()}")
    except Exception as e:
        print(f"❌ {username}: Decryption failed → {e}")

cursor.close()
db.close()
