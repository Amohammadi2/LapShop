import pandas as pd
import matplotlib.pyplot as plt
import os
from file_manager import load_sales_log, load_products

# Load sales data
sales_data = load_sales_log()

# Load products data
products_data = load_products()

# Create the 'reports' directory if it doesn't exist
if not os.path.exists('reports'):
    os.makedirs('reports')

# Graph 1: Which brand has the most sales
brand_sales = sales_data['brand'].value_counts()
plt.figure(figsize=(10, 6))
brand_sales.plot(kind='bar')
plt.title('Brand with the Most Sales')
plt.xlabel('Brand')
plt.ylabel('Number of Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('reports/brand_most_sales.png')
plt.close()

# Graph 2: Which range of price has the most sales
bins = [0, 20000000, 40000000, 60000000, 80000000, 100000000, float('inf')]
labels = ['0-20M', '20M-40M', '40M-60M', '60M-80M', '80M-100M', '100M+']
sales_data['price_range'] = pd.cut(sales_data['price'], bins=bins, labels=labels)
price_range_sales = sales_data['price_range'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
price_range_sales.plot(kind='bar')
plt.title('Price Range with the Most Sales')
plt.xlabel('Price Range (Tomans)')
plt.ylabel('Number of Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('reports/price_range_most_sales.png')
plt.close()

# Graph 3: How many of the sold products with price under 80,000,000 Tomans were ASUS laptops

under_80m = sales_data[sales_data['price'] < 80000000]
total_under_80m = len(under_80m)
asus_under_80m = under_80m[under_80m['brand'] == 'asus']
asus_sales_count = len(asus_under_80m)
asus_percentage = (asus_sales_count / total_under_80m) * 100
plt.figure(figsize=(6, 4))
plt.bar('ASUS', asus_percentage, color='orange')
plt.title('Percentage of ASUS Laptops Sold Under 80,000,000 Tomans')
plt.xlabel('Brand')
plt.ylabel('Percentage of Sales (%)')
plt.ylim(0, 100)  # Set y-axis limit to 0-100 for percentage
plt.tight_layout()

# Save the plot
plt.savefig('reports/asus_under_80m_percentage.png')
plt.close()

# Graph 4: Distribution of sales across brands
brand_sales_distribution = sales_data['brand'].value_counts()
plt.figure(figsize=(10, 6))
brand_sales_distribution.plot(kind='bar')
plt.title('Distribution of Sales Across Brands')
plt.xlabel('Brand')
plt.ylabel('Number of Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('reports/brand_sales_distribution.png')
plt.close()

# Graph 5: Distribution of average prices across brands
average_prices = products_data.groupby('brand')['price'].mean()
plt.figure(figsize=(10, 6))
average_prices.plot(kind='bar')
plt.title('Average Price Across Brands')
plt.xlabel('Brand')
plt.ylabel('Average Price (Tomans)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('reports/average_price_across_brands.png')
plt.close()