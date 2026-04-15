import pandas as pd
import numpy as np

# LOADING DATA
df = pd.read_csv("Sales_Data.csv")
print(f"Loaded: {df.shape[0]} rows and {df.shape[1]} columns")

# CHANGING DATA TYPE OF ORDER DATE and Extracting Date parts
df['Order Date'] = pd.to_datetime(df['Order Date'], format="%m/%d/%Y")

df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Month Name'] = df['Order Date'].dt.strftime('%B')
df['Order Quarter'] = df['Order Date'].dt.quarter.map({1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'})
df['Order Day'] = df['Order Date'].dt.day
df['Day of Week'] = df['Order Date'].dt.day_name()

for col in ['Category', 'Sub Category', 'Region', 'State', 'City', 'Order Month', 'Day of Week', 'Order Quarter']:
    df[col] = df[col].astype('category')

# NULL HANDLING IF ANY OCCURS
for col in ['Sales', 'Discount', 'Profit']:
    null_count = df[col].isnull().sum()
    if null_count > 0:
        mean_val = df[col].mean()
        df[col].fillna(mean_val, inplace=True)
        print(f"Filled {null_count} nulls in {col} with mean {mean_val:,.2f}")

# DERIVED BUSINESS COLUMNS
df['Revenue After Discount'] = (df['Sales'] * (1 - df['Discount'])).round(2)
df['Profit Margin %'] = ((df['Profit'] / df['Sales']) * 100).round(2)
df['Discount %'] = (df['Discount'] * 100).round(2)

bins = [0, 100, 300, 600, float('inf')]
labels = ['Low', 'Medium', 'High', 'Very High']
df['Profit Category'] = pd.cut(df['Profit'], bins=bins, labels=labels)

# CONVERTING ORDER ID INTO 5 DIGITS
df['Order ID'] = 'OD' + df['Order ID'].str.extract(r'(\d+)')[0].str.zfill(5)

# SAVING FILE
output_path = 'Sales_Data_Cleaned.csv'
df.to_csv(output_path, index=False)
print(f"\nCleaned Data saved to {output_path}")
print(f"Final Shape: {df.shape[0]} rows and {df.shape[1]} columns")

