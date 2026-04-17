SET SQL_SAFE_UPDATES = 0;

select * from combined_compressed ;

--- Check duplicates first

SELECT StockCode, COUNT(*) AS dup_count
FROM combined_compressed
GROUP BY StockCode, CustomerID
HAVING COUNT(*) > 1;

--- Permit
SET SQL_SAFE_UPDATES = 0;

--- Delete duplicates using CTE
DELETE c
FROM combined_compressed c
JOIN (
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY StockCode, Quantity, Price
                   ORDER BY CustomerID
               ) AS rn
        FROM combined_compressed
    ) t
    WHERE rn > 1
) dup
ON c.CustomerID = dup.CustomerID
AND c.StockCode = dup.StockCode
AND c.Quantity = dup.Quantity
AND c.Price = dup.Price;


--- Missing Customer Name
SELECT COUNT(*) AS missing_customers
FROM combined_compressed
WHERE CustomerID IS NULL OR CustomerID = '';

DELETE FROM combined_compressed
WHERE CustomerID IS NULL OR CustomerID = '';

--- Clean & Convert InvoiceDate
--- Add new column

ALTER TABLE combined_compressed
ADD InvoiceDate_clean DATETIME;

--- Convert text → datetime
UPDATE combined_compressed
SET InvoiceDate_clean = STR_TO_DATE(InvoiceDate, '%d-%m-%Y %H:%i');

--- Check if conversion worked
SELECT InvoiceDate, InvoiceDate_clean
FROM combined_compressed
LIMIT 10;

--- Remove Invalid Transactions
--- Remove negative / zero Quantity

DELETE FROM combined_compressed
WHERE Quantity <= 0;

--- Remove zero / negative Price
DELETE FROM combined_compressed
WHERE Price <= 0;

--- Validate
SELECT MIN(Quantity), MIN(Price)
FROM combined_compressed;

--- Text Cleaning
--- Trim spaces

UPDATE combined_compressed
SET Description = TRIM(Description);

--- Remove empty descriptions
DELETE FROM combined_compressed
WHERE Description IS NULL OR Description = '';

--- Fix Data Types
--- Convert CustomerID properly
ALTER TABLE combined_compressed
MODIFY CustomerID BIGINT;

--- Add Business Column
--- Total Amount = Quantity × Price
ALTER TABLE combined_compressed
ADD TotalAmount DECIMAL(12,2);

UPDATE combined_compressed
SET TotalAmount = Quantity * Price;

--- FINAL CHECK
SELECT COUNT(*) FROM combined_compressed;

SELECT * FROM combined_compressed LIMIT 10;
