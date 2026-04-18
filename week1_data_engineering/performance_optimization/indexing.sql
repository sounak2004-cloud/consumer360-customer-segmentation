USE your_database_name;

-- Indexes for fact table 

CREATE INDEX idx_fact_customer 
ON fact_sales(customer_id);

CREATE INDEX idx_fact_product 
ON fact_sales(product_id);

CREATE INDEX idx_fact_date 
ON fact_sales(order_date);

CREATE INDEX idx_fact_invoice 
ON fact_sales(invoice_no);

-- Indexes for dimension tables

CREATE INDEX idx_customer_id 
ON dim_customer(customer_id);

CREATE INDEX idx_product_id 
ON dim_product(product_id);
