-- script that creates a table users
-- addin
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    country ENUM ('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
