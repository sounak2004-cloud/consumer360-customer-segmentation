import pandas as pd

# =========================
# LOAD DATA
# =========================
file_path = "../segmentation/rfm_segments.csv"

try:
    df = pd.read_csv(file_path)
    print("\n📌 Data Loaded Successfully\n")
except FileNotFoundError:
    print(f"❌ File not found: {file_path}")
    exit()

# =========================
# CLEAN COLUMN NAMES
# =========================
df.columns = df.columns.str.lower()

# =========================
# BASIC INFO
# =========================
print("🔍 BASIC INFO")
print(df.info())

print("\n🔍 SAMPLE DATA")
print(df.head())

print("\n🔍 SEGMENT DISTRIBUTION")
print(df['segment'].value_counts())

# =========================
# CHECK REQUIRED COLUMNS
# =========================
required_cols = ['segment', 'recency', 'frequency', 'monetary']

for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Missing column: {col}")

# =========================
# CORE VALIDATION
# =========================

print("\n==============================")
print("📊 MONETARY ANALYSIS")
print("==============================")

monetary_check = df.groupby('segment')['monetary'].mean().sort_values(ascending=False)
print(monetary_check)


print("\n==============================")
print("📊 FREQUENCY ANALYSIS")
print("==============================")

frequency_check = df.groupby('segment')['frequency'].mean().sort_values(ascending=False)
print(frequency_check)


print("\n==============================")
print("📊 RECENCY ANALYSIS")
print("==============================")

recency_check = df.groupby('segment')['recency'].mean().sort_values()
print(recency_check)


# =========================
# TOP CUSTOMERS CHECK
# =========================
print("\n==============================")
print("🏆 TOP CUSTOMERS CHECK")
print("==============================")

top_customers = df.sort_values(by='monetary', ascending=False).head(10)
print(top_customers[['customerid', 'monetary', 'segment']])


# =========================
# EDGE CASE CHECK
# =========================
print("\n==============================")
print("⚠️ LOW FREQUENCY CUSTOMERS (freq=1)")
print("==============================")

low_freq = df[df['frequency'] == 1]
print(low_freq[['customerid', 'frequency', 'segment']].head())


# =========================
# FINAL VALIDATION LOGIC
# =========================
print("\n==============================")
print("✅ FINAL VALIDATION RESULT")
print("==============================")

top_segment = monetary_check.index[0]

if top_segment.lower() == "champions":
    print("✔ VALID: Champions are highest spenders")
else:
    print(f"❌ ISSUE: {top_segment} is highest spender, NOT Champions")


# =========================
# SEGMENT BALANCE CHECK
# =========================
print("\n==============================")
print("📊 SEGMENT PERCENTAGE")
print("==============================")

segment_percent = df['segment'].value_counts(normalize=True) * 100
print(segment_percent.round(2))


# =========================
# SAVE REPORT
# =========================
with open("validation_summary.txt", "w") as f:
    f.write("Monetary Analysis:\n")
    f.write(str(monetary_check))
    f.write("\n\nFrequency Analysis:\n")
    f.write(str(frequency_check))
    f.write("\n\nRecency Analysis:\n")
    f.write(str(recency_check))
    f.write("\n\nSegment Distribution (%):\n")
    f.write(str(segment_percent.round(2)))

print("\n📄 Validation summary saved as validation_summary.txt")
