import mysql.connector
from faker import Faker
from cryptography.fernet import Fernet
import time

# --- Step 1: Generate or Load Your Key ---
# Generate a new key once, then reuse it
# key = Fernet.generate_key()
# print(f"Your encryption key: {key.decode()}")
# Save the key somewhere secure!

key = b'2Qn2CBrOU0FO-by145zwjtKWMJrBloN6kCa8A0pAUPU='  # Replace this with the generated key (bytes)
cipher = Fernet(key)

# --- Step 2: Connect to MySQL ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hotdog12",
    database="encryption_test"
)
cursor = conn.cursor()

fake = Faker()

# --- Step 3: Insert Encrypted Data ---
start_time = time.time()

for _ in range(1000):
    username = fake.user_name()
    activity = fake.random_element(["Login", "Logout", "Update Profile", "View Report", "Export Data"])
    timestamp = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = fake.ipv4()
    sensitive_data = fake.password(length=12)

    # Encrypt sensitive data
    encrypted_data = cipher.encrypt(sensitive_data.encode())

    cursor.execute("""
        INSERT INTO user_logs (username, activity, timestamp, ip_address, sensitive_data)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, activity, timestamp, ip_address, encrypted_data))

conn.commit()
cursor.close()
conn.close()

end_time = time.time()
elapsed = end_time - start_time

print(f"✅ Encrypted data inserted successfully!")
print(f"🕒 Time taken to insert 1000 encrypted records: {elapsed:.2f} seconds")
