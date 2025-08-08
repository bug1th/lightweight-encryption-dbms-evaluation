import mysql.connector
from cryptography.fernet import Fernet

# Use the same key you used for encryption
key = b'2Qn2CBrOU0FO-by145zwjtKWMJrBloN6kCa8A0pAUPU='
cipher = Fernet(key)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hotdog12",  # 👈 replace with your password
    database="encryption_test"
)
cursor = conn.cursor()

# Fetch encrypted data
cursor.execute("SELECT log_id, username, sensitive_data FROM user_logs LIMIT 5;")
rows = cursor.fetchall()

print("🔓 Decrypted Records:\n")
for row in rows:
    log_id, username, encrypted_data = row
    decrypted = cipher.decrypt(encrypted_data).decode()
    print(f"ID: {log_id} | User: {username} | Sensitive Data: {decrypted}")

cursor.close()
conn.close()
