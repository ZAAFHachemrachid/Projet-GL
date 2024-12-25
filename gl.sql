  -- Create the database
CREATE DATABASE IF NOT EXISTS StockManagement;
USE StockManagement;

-- Create the Product table
CREATE TABLE Product (
    reference VARCHAR(50) PRIMARY KEY,
    designation VARCHAR(100) NOT NULL,
    prixAchat DOUBLE NOT NULL,
    dateAchat DATE NOT NULL,
    quantite INT NOT NULL
);

-- Create the Admins table
CREATE TABLE Admins (
    identifier INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create the Stock table
CREATE TABLE Stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_reference VARCHAR(50),
    FOREIGN KEY (product_reference) REFERENCES Product(reference)
);

-- Create the GestionStock table
CREATE TABLE GestionStock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT,
    stock_id INT,
    FOREIGN KEY (admin_id) REFERENCES Admins(identifier),
    FOREIGN KEY (stock_id) REFERENCES Stock(id)
);