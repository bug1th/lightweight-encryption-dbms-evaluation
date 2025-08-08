CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

CREATE TABLE user_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    activity TEXT,
    timestamp DATETIME,
    ip_address VARCHAR(50),
    sensitive_data BLOB,
    nonce VARBINARY(255)
);
