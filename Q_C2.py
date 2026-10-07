import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sales = pd.DataFrame({
    'order_date': ['2026-01-05', '2026-01-18', '2026-02-02', '2026-02-14', '2026-03-01', '2026-03-20'],
    'region': ['North', 'south', 'North', 'East', 'SOUTH', 'east'],
    'products': ["Pen", "Notebook", "Pen", "Bag", "Bag", "Notebook"],
    'units': [10, 5, np.nan, 2, 4, 8],
    'price': [20, 60, 20, 500, 500, 60],
    'Rep': ['Ravi', 'Sita', 'Ravi', 'Kiran', 'Sita', 'Kiran']
})

# a) clean region: strip spaces, Title Case
sales['region'] = sales['region'].str.strip().str.title()

# b) fill missing units with the median of units
sales['units'] = sales['units'].fillna(sales['units'].median())

# c) revenue, datetime conversion, month name
sales['revenue'] = sales['units'] * sales['price']
sales['order_date'] = pd.to_datetime(sales['order_date'])
sales['month'] = sales['order_date'].dt.month_name()

# d) total revenue per region, highest first
region_revenue = sales.groupby('region')['revenue'].sum().sort_values(ascending=False)
print(region_revenue)

# e) pivot table: region x product, total revenue, missing = 0
pivot = sales.pivot_table(index='region', columns='products', values='revenue',
                          aggfunc='sum', fill_value=0)
print(pivot)

sns.barplot(data=sales, x='region', y='revenue', estimator='sum', errorbar=None)
plt.title('Revenue by Region')
plt.xlabel('Region')
plt.ylabel('Revenue')
plt.show()

# Output of d):
'''
region
South    2300.0
East     1480.0
North     300.0
Name: revenue, dtype: float64

Pivot table from e):
products     Bag  Notebook    Pen
region
East      1000.0     480.0    0.0
North        0.0       0.0  300.0
 South     2000.0     300.0    0.0'''
