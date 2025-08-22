"""
Netflix Data Preprocessing & ETL Script
---------------------------------------
This script performs:
1. Data loading (CSV/Excel)
2. Preprocessing & cleaning
3. Loading cleaned data into MS SQL Server
"""

import pandas as pd
import numpy as np
import pyodbc

# Step 1: Load Data

DATA_PATH = "data/netflix_reviews.csv"

df = pd.read_csv(DATA_PATH)

# Step 2: Preprocessing

# Drop missing values
df.dropna(subset=["review", "rating"], inplace=True)

# Convert review text to lowercase
df["review_cleaned"] = df["review"].astype(str).str.lower()

# Remove special characters
df["review_cleaned"] = df["review_cleaned"].str.replace(r"[^a-zA-Z0-9\s]", "", regex=True)


# Step 3: Connect to SQL Server
CONN_STR = (
    "DRIVER={SQL SERVER};"
    "SERVER=...;"
    "DATABASE=...;"
    "UID=...;"
    "PWD=...;"
)

conn = pyodbc.connect(CONN_STR)
cursor = conn.cursor()


# Step 4: Create Table (if not exists)

print("Creating table if not exists...")

cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='netflix_reviews' AND xtype='U')
CREATE TABLE netflix_reviews (
    id INT IDENTITY(1,1) PRIMARY KEY,
    review NVARCHAR(MAX),
    review_cleaned NVARCHAR(MAX),
    rating INT
)
""")
conn.commit()

# Step 5: Insert Data into SQL

print("Inserting data into SQL Server...")

for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO netflix_reviews (review, review_cleaned, rating)
        VALUES (?, ?, ?)
    """, row["review"], row["review_cleaned"], int(row["rating"]))

conn.commit()
print("Data successfully loaded into SQL Server!")

# Close connection
cursor.close()
conn.close()
