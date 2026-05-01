# 1. IMPORT LIBRARIES

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

sns.set(style="whitegrid")


# 2. LOAD DATA

df = pd.read_csv("D:\Zaalima\Week 2\week2_logic_core\data_pipeline\cleaned_data.csv", encoding='latin1')

print("Shape:", df.shape)
print(df.head())


# 3. DATA CLEANING

df = df.dropna(subset=['CustomerID'])

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

# Create TotalAmount if not exists
if 'TotalAmount' not in df.columns:
    df['TotalAmount'] = df['Quantity'] * df['Price']


# 4. CREATE RFM TABLE

snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'Invoice': 'nunique',
    'TotalAmount': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

print(rfm.head())


# 5. RFM SCORING

rfm['R_score'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1,2,3,4])
rfm['M_score'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4])

rfm['RFM_Score'] = (
    rfm['R_score'].astype(str) +
    rfm['F_score'].astype(str) +
    rfm['M_score'].astype(str)
)


# 6. SEGMENTATION

def segment(row):
    if row['RFM_Score'] == '444':
        return 'Champions'
    elif row['F_score'] == 4:
        return 'Loyal Customers'
    elif row['R_score'] == 1:
        return 'At Risk'
    else:
        return 'Others'

rfm['Segment'] = rfm.apply(segment, axis=1)

print(rfm['Segment'].value_counts())


# 7. LOG TRANSFORMATION

rfm['Log_Recency'] = np.log1p(rfm['Recency'])
rfm['Log_Frequency'] = np.log1p(rfm['Frequency'])
rfm['Log_Monetary'] = np.log1p(rfm['Monetary'])


# 8. CUSTOMER LIFETIME VALUE

rfm['CLV'] = rfm['Monetary'] * rfm['Frequency']


# 9. VISUALIZATIONS


# Segment Count
plt.figure()
sns.countplot(data=rfm, x="Segment")
plt.title("Customer Segment Distribution")
plt.xticks(rotation=30)
plt.show()


# Recency vs Monetary
plt.figure()
sns.scatterplot(data=rfm, x="Recency", y="Monetary", hue="Segment")
plt.title("Recency vs Monetary")
plt.show()


# Frequency vs Monetary
plt.figure()
sns.scatterplot(data=rfm, x="Frequency", y="Monetary", hue="Segment")
plt.title("Frequency vs Monetary")
plt.show()


# Correlation Heatmap
plt.figure()
sns.heatmap(rfm[['Recency','Frequency','Monetary']].corr(), annot=True)
plt.title("RFM Correlation")
plt.show()


# Boxplot
plt.figure()
sns.boxplot(data=rfm, x="Segment", y="Monetary")
plt.xticks(rotation=30)
plt.title("Monetary by Segment")
plt.show()


# Distribution plots
plt.figure(figsize=(12,4))

plt.subplot(1,3,1)
sns.histplot(rfm['Recency'], kde=True)

plt.subplot(1,3,2)
sns.histplot(rfm['Frequency'], kde=True)

plt.subplot(1,3,3)
sns.histplot(rfm['Monetary'], kde=True)

plt.show()


# 10. TOP CUSTOMERS

top_customers = rfm.sort_values(by="Monetary", ascending=False).head(10)
print("Top Customers:\n", top_customers)


# 11. K-MEANS CLUSTERING

X = rfm[['Recency', 'Frequency', 'Monetary']]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42)
rfm['Cluster'] = kmeans.fit_predict(X_scaled)


# Cluster Visualization
plt.figure()
sns.scatterplot(data=rfm, x='Recency', y='Monetary', hue='Cluster')
plt.title("Customer Clusters")
plt.show()


# 12. SAVE OUTPUT

rfm.to_csv("rfm_final_output.csv")

print("DONE: Full RFM + ML pipeline executed")
