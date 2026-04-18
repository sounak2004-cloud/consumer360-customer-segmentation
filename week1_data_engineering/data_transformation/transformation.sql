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
CREATE TABLE dim_customer (
    customer_id BIGINT PRIMARY KEY,
    country VARCHAR(100)
);
CREATE TABLE dim_product (
    product_id VARCHAR(20) PRIMARY KEY,
    description VARCHAR(255)
);
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
INSERT INTO dim_customer (customer_id, country)
SELECT DISTINCT
    CustomerID,
    Country
FROM transformed_sales;
INSERT INTO dim_product (product_id, description)
SELECT DISTINCT
    StockCode,
    Description
FROM transformed_sales;
