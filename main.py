import pandas as pd
import matplotlib.pyplot as plt
import math

# Load data from CSV files, skipping the first column, setting field format as string, and removing NA values
customers_zip = pd.read_csv("customers_zip.csv", usecols=["customer_id", "zip_cust"], dtype=str).dropna()
delivery_zip = pd.read_csv("delivery_zip.csv", usecols=["customer_id", "zip_del"], dtype=str).dropna()
sports = pd.read_csv("sports.csv",  usecols=["customer_id", "sport"], dtype=str).dropna()
orders = pd.read_csv("orders.csv", dtype={"order_id": str, "value": float}).dropna()
customer_orders = pd.read_csv("customer_orders.csv", usecols=["customer_id", "order_id"], dtype=str).dropna()

#filter out incorrect values
orders = orders[(orders['value'] >= 0) & (orders['value'] <= 500000)]



# Add the "id_zip" column to both tables
customers_zip["id_zip"] = customers_zip["customer_id"] + ";" + customers_zip["zip_cust"]
delivery_zip["id_zip"] = delivery_zip["customer_id"] + ";" + delivery_zip["zip_del"]

# Merge tables on the "id_zip" column
merged_table = pd.merge(delivery_zip, customers_zip, on="id_zip", how="left")

#count of customers with orders
count_customers_with_orders = merged_table["customer_id_x"].nunique()

# Nan means customer doesnt have such zip. we remove Nan values
merged_table = merged_table[merged_table['customer_id_y'].notna()]

count_cust_home_zip = merged_table['customer_id_x'].nunique()

percentage_remaining = (count_cust_home_zip / count_customers_with_orders) * 100

print(f"Percentage of customers with order at home zip : {percentage_remaining:.2f}%")

sport_counts = sports['sport'].value_counts()

most_common_sport = sport_counts.idxmax()

least_common_sport = sport_counts.idxmin()

print(f"most popular: {most_common_sport}")

print(f"least popular: {least_common_sport}")

user_sports_count = sports.groupby('customer_id')['sport'].nunique()

users_with_more_than_two_sports = (user_sports_count > 2).sum()

print(f"Count of customers with more than 2 sports : {users_with_more_than_two_sports}")

average_value = orders['value'].mean()
median_value = orders['value'].median()

print(f"average order value : {average_value:.2f}")
print(f"median order value : {median_value}")

filtered_orders = orders.sort_values(by='value', ascending=True)


merged_df = pd.merge(customer_orders, sports, on="customer_id")
merged_df = pd.merge(merged_df, filtered_orders, on="order_id")

filtered_df = merged_df[merged_df['sport'] == 'jeYdziectwo']

average_order_by_user = filtered_df['value'].mean()
median_order_by_user = filtered_df['value'].median()

print(f"average value for customers that love 'jeYdziectwo': {average_order_by_user:.2f}")
print(f"median value for customers that love 'jeYdziectwo': {median_order_by_user}")
