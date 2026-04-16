# Dataset Overview – Online Retail

## 1. Dataset Description

This dataset contains transactional data from an online retail store. Each row represents a product purchased within a transaction (invoice). A single invoice can contain multiple products.

---

## 2. Columns Description

| Column Name | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| InvoiceNo   | Unique transaction ID (prefix 'C' indicates cancellation)    |
| StockCode   | Unique product identifier                                    |
| Description | Name of the product                                          |
| Quantity    | Number of units purchased (negative values indicate returns) |
| InvoiceDate | Date and time of transaction                                 |
| UnitPrice   | Price per unit                                               |
| CustomerID  | Unique customer identifier                                   |
| Country     | Customer location                                            |

---

## 3. Data Issues Identified

### 3.1 Cancelled Transactions

* Invoice numbers starting with 'C' represent cancelled orders
* Example: C536379
* These transactions include negative quantities

---

### 3.2 Negative Quantity Values

* Quantity < 0 indicates returned or cancelled items
* Example: Discount or product return rows
* These should NOT be treated as normal sales

---

### 3.3 Special StockCodes (Non-Product Entries)

* Some StockCodes do not represent actual products:

  * POST → Shipping/Postage
  * D → Discount
* Example:

  * POST, POSTAGE
  * D, Discount

---

### 3.4 Mixed Transaction Types

* Dataset contains:

  * Sales transactions
  * Returns
  * Discounts
* Requires filtering for accurate analysis

---

### 3.5 Data Type Issues

* InvoiceDate contains both date and time
* Needs conversion to DATE format for aggregation

---

### 3.6 Potential Missing Values

* CustomerID may contain NULL values (common in this dataset)
* These records cannot be used for customer-level analysis

---

## 4. Key Observations

* One InvoiceNo can contain multiple products → suitable for market basket analysis
* Dataset is transactional → supports RFM, CLV, and cohort analysis
* CustomerID is essential for segmentation
* Majority of transactions belong to the United Kingdom 

---

## 5. Cleaning Strategy (Planned)

* Remove cancelled transactions (InvoiceNo starting with 'C')
* Remove rows where Quantity ≤ 0
* Remove non-product StockCodes (POST, D)
* Remove rows with NULL CustomerID
* Convert InvoiceDate to standard DATE format
* Create derived column: Revenue = Quantity × UnitPrice
