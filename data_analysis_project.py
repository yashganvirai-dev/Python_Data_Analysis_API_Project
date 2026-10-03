# Day 16–20: Python Data Analysis & API Application
# Author: Yash Ganvir

# =========================
# 1. Import Libraries
# =========================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
from datetime import datetime

# =========================
# 2. Load Dataset
# =========================
df = pd.read_csv("sales_data.csv")

print("First 5 rows:")
display(df.head())

print("\nDataset shape:", df.shape)
print("\nData types:")
print(df.dtypes)

# =========================
# 3. Data Cleaning
# =========================
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Fill missing customer ratings with the mean rating
df["Customer_Rating"] = df["Customer_Rating"].fillna(df["Customer_Rating"].mean())

# Remove duplicate rows if any
df = df.drop_duplicates()

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# =========================
# 4. Data Analysis
# =========================
print("\nSummary statistics:")
display(df.describe())

total_revenue = df["Total_Sales"].sum()
total_quantity = df["Quantity"].sum()
average_rating = df["Customer_Rating"].mean()

print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Total Quantity Sold: {total_quantity}")
print(f"Average Customer Rating: {average_rating:.2f}")

product_sales = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
category_sales = df.groupby("Category")["Total_Sales"].sum().sort_values(ascending=False)

print("\nSales by Product:")
display(product_sales)

print("\nSales by Category:")
display(category_sales)

# =========================
# 5. Visualizations
# =========================
sns.set_theme(style="whitegrid")

plt.figure(figsize=(10,5))
product_sales.plot(kind="bar")
plt.title("Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Sales (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,5))
category_sales.plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Sales Distribution by Category")
plt.ylabel("")
plt.show()

plt.figure(figsize=(10,5))
sns.lineplot(data=df, x="Date", y="Total_Sales", marker="o")
plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Sales (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,5))
sns.scatterplot(data=df, x="Quantity", y="Total_Sales", hue="Category", s=100)
plt.title("Quantity vs Total Sales")
plt.tight_layout()
plt.show()

# =========================
# 6. REST API + JSON
# =========================
# Public demo API: JSONPlaceholder
api_url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    api_data = response.json()

    print("\nAPI Status Code:", response.status_code)
    print("\nAPI JSON Response:")
    print(json.dumps(api_data, indent=4))

    api_df = pd.DataFrame([api_data])
    print("\nAPI data as Pandas DataFrame:")
    display(api_df)

except requests.RequestException as e:
    print("API request failed:", e)

# =========================
# 7. Generate Final Report
# =========================
top_product = product_sales.index[0]
top_product_sales = product_sales.iloc[0]
top_category = category_sales.index[0]

report = f"""
PYTHON DATA ANALYSIS REPORT
===========================

Dataset: Sales Data
Records analyzed: {len(df)}

Key Metrics
-----------
Total Revenue: ₹{total_revenue:,.2f}
Total Quantity Sold: {total_quantity}
Average Customer Rating: {average_rating:.2f}

Top Performing Product
----------------------
Product: {top_product}
Sales: ₹{top_product_sales:,.2f}

Top Performing Category
-----------------------
Category: {top_category}
Sales: ₹{category_sales.iloc[0]:,.2f}

Technologies Used
-----------------
Python
NumPy
Pandas
Matplotlib
Seaborn
Requests
JSON

Conclusion
----------
The dataset was loaded, cleaned, analyzed and visualized using Python.
A REST API was also consumed and its JSON response was converted into
a Pandas DataFrame. The project demonstrates basic data analysis,
visualization, API consumption and automated report generation.
"""

print(report)

with open("final_report.txt", "w", encoding="utf-8") as f:
    f.write(report)

print("Final report saved as final_report.txt")
