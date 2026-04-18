USE your_database_name;

SET SQL_SAFE_UPDATES = 0;

-- Add clean date column (safe)
ALTER TABLE combined_compressed
ADD COLUMN IF NOT EXISTS InvoiceDate_clean DATETIME;

UPDATE combined_compressed
SET InvoiceDate_clean = STR_TO_DATE(InvoiceDate, '%d-%m-%Y %H:%i')
WHERE InvoiceDate_clean IS NULL;

-- Add total amount column (safe)
ALTER TABLE combined_compressed
ADD COLUMN IF NOT EXISTS TotalAmount DECIMAL(12,2);

UPDATE combined_compressed
SET TotalAmount = Quantity * Price
WHERE TotalAmount IS NULL;

-- Create transformed table
DROP TABLE IF EXISTS transformed_sales;

CREATE TABLE transformed_sales AS
SELECT 
    InvoiceNo,
    StockCode,
    Description,
    Quantity,
    Price,
    CustomerID,
    Country,
    InvoiceDate_clean AS order_date,
    TotalAmount AS total_amount
FROM combined_compressed;

-- Check
SELECT * FROM transformed_sales LIMIT 10;
USE your_database_name;

-- Drop if exists
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;

-- Fact table
CREATE TABLE fact_sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_no VARCHAR(20),
    product_id VARCHAR(20),
    customer_id BIGINT,
    order_date DATETIME,
    quantity INT,
    price DECIMAL(10,2),
    total_amount DECIMAL(12,2)
);

-- Customer dimension
CREATE TABLE dim_customer (
    customer_id BIGINT PRIMARY KEY,
    country VARCHAR(100)
);

-- Product dimension
CREATE TABLE dim_product (
    product_id VARCHAR(20) PRIMARY KEY,
    description VARCHAR(255)
);
USE your_database_name;

-- Insert into fact table
INSERT INTO fact_sales (
    invoice_no,
    product_id,
    customer_id,
    order_date,
    quantity,
    price,
    total_amount
)
SELECT 
    InvoiceNo,
    StockCode,
    CustomerID,
    order_date,
    Quantity,
    Price,
    total_amount
FROM transformed_sales;

-- Insert into customer dimension
INSERT INTO dim_customer (customer_id, country)
SELECT DISTINCT
    CustomerID,
    Country
FROM transformed_sales;

-- Insert into product dimension
INSERT INTO dim_product (product_id, description)
SELECT DISTINCT
    StockCode,
    Description
FROM transformed_sales;
