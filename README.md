


## Project: Consumer360 – Customer Segmentation & CLV Engine

# Week 1 – Data Engineering & Schema Design

---

## 📌 Objective

The goal of Week 1 was to build a strong data foundation by transforming raw transactional data into a structured format suitable for analytics, including customer segmentation and lifetime value modeling.

---

## 🗂️ Dataset

* Source: Online Retail Dataset (Kaggle)
* Type: Transactional (Invoice-level data)
* Each row represents a product within a transaction

---

## ⚙️ Work Completed

### 1. Data Inspection

* Analyzed dataset structure and columns
* Identified key issues:

  * Missing Customer IDs
  * Negative quantities (returns/cancellations)
  * Special StockCodes (POST, D)
  * Mixed transaction types (sales, returns, discounts)

---

### 2. Data Cleaning

* Removed invalid records:

  * Transactions with missing CustomerID
  * Rows with non-positive Quantity and UnitPrice
* Standardized date format using SQL
* Trimmed and cleaned text fields
* Created derived column:

  * **TotalAmount = Quantity × UnitPrice**

---

### 3. Data Transformation

* Converted raw transactional data into structured format
* Prepared dataset for downstream analytics (RFM, CLV, Cohort Analysis)

---

### 4. Star Schema Design

Designed a star schema to support analytical queries:

* **Fact Table:** `fact_sales`

  * Contains transactional data (line-item level)
* **Dimension Tables:**

  * `dim_customer`
  * `dim_product`

---

### 5. ERD (Entity Relationship Diagram)

* Established relationships between fact and dimension tables
* Enabled structured querying and scalability

---

### 6. Indexing & Optimization

* Created indexes on frequently used columns:

  * CustomerID
  * InvoiceNo
  * InvoiceDate
  * StockCode
* Goal: Ensure query performance under 2 seconds

---

## 🧠 Key Learnings

* Importance of data quality before analysis
* Handling real-world issues like cancellations and returns
* Designing scalable data models using star schema
* Basics of query optimization using indexing

---

## 📁 Folder Structure

```bash
week1_data_engineering/
│
├── data_inspection/
│   └── dataset_overview.md
│
├── data_cleaning/
│   └── cleaning.sql
│
├── data_transformation/
│   └── transformation.sql
│
├── star_schema_design/
│   ├── schema.sql
│   └── schema_explanation.md
│   └── erd_diagram.png
│
├── performance_optimization/
│   └── indexing.sql
│
```

---

## 🚀 Outcome

By the end of Week 1:

* Raw data was cleaned and structured
* A scalable schema was designed
* Data is ready for advanced analytics in Week 2

---

## 🔜 Next Steps (Week 2)

* RFM Segmentation
* Cohort Analysis
* Customer Lifetime Value (CLV) Modeling
* Market Basket Analysis
