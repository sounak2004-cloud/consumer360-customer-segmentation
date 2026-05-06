import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(
    "../data_pipeline/cleaned_data.csv",
    sep='\t',
    on_bad_lines='skip',
    encoding='utf-8'
)

print("📌 Data Loaded Successfully")
print(df.head())

# =========================
# CLEAN COLUMN NAMES
# =========================
df.columns = df.columns.str.strip()

print("\n📌 Columns:")
print(df.columns)

# =========================
# KEEP REQUIRED COLUMNS
# =========================
df = df[['InvoiceNo', 'Description']]

# =========================
# REMOVE NULL VALUES
# =========================
df.dropna(inplace=True)

# =========================
# REMOVE CANCELLED INVOICES
# =========================
df = df[
    ~df['InvoiceNo']
    .astype(str)
    .str.startswith('C')
]

# =========================
# CLEAN PRODUCT NAMES
# =========================
df['Description'] = df['Description'].str.strip()

# =========================
# KEEP ONLY TOP 100 PRODUCTS
# (improves performance)
# =========================
top_products = (
    df['Description']
    .value_counts()
    .head(100)
    .index
)

df = df[
    df['Description']
    .isin(top_products)
]

print("\n📌 Filtered Top Products")
print(df.head())

# =========================
# CREATE BASKET MATRIX
# =========================
basket = (
    df.groupby(['InvoiceNo', 'Description'])['Description']
    .count()
    .unstack()
    .fillna(0)
)

# Convert to boolean
basket = basket.map(
    lambda x: True if x > 0 else False
)

print("\n📌 Basket Matrix Created")
print(basket.head())

print("\n📌 Basket Shape:")
print(basket.shape)

# =========================
# APPLY APRIORI
# =========================
frequent_itemsets = apriori(
    basket,
    min_support=0.05,
    use_colnames=True,
    max_len=2
)

print("\n📌 Frequent Itemsets")
print(frequent_itemsets.head())

print("\n📌 Total Frequent Itemsets:")
print(len(frequent_itemsets))

# =========================
# GENERATE ASSOCIATION RULES
# =========================
rules = association_rules(
    frequent_itemsets,
    metric="lift",
    min_threshold=1
)

# =========================
# KEEP IMPORTANT COLUMNS
# =========================
rules = rules[[
    'antecedents',
    'consequents',
    'support',
    'confidence',
    'lift'
]]

# =========================
# CONVERT FROZENSET TO STRING
# =========================
rules['antecedents'] = rules[
    'antecedents'
].apply(
    lambda x: ', '.join(list(x))
)

rules['consequents'] = rules[
    'consequents'
].apply(
    lambda x: ', '.join(list(x))
)

# =========================
# SORT RULES
# =========================
rules = rules.sort_values(
    by='lift',
    ascending=False
)

print("\n📌 Top Association Rules")
print(rules.head(10))

print("\n📌 Total Rules Generated:")
print(len(rules))

# =========================
# SAVE OUTPUT
# =========================
rules.to_csv(
    "association_rules.csv",
    index=False
)

print("\n✅ association_rules.csv generated successfully")
