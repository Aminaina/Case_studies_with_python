#!/usr/bin/env python
# coding: utf-8

# In[2]:


# identify customer segments based on purchasing behavior.


# In[3]:


#Load required libraries and datasets


# In[1]:


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df_customer = pd.read_csv(r'C:\Users\Käyttäjä\OneDrive - LUT University\Documents 1\data_analytics\Projects\Quantium_chips_retail analytics\QVI_purchase_behaviour.csv')


# In[3]:


df_transaction = pd.read_excel(r'C:\Users\Käyttäjä\OneDrive - LUT University\Documents 1\data_analytics\Projects\Quantium_chips_retail analytics\QVI_transaction_data.xlsx')


# In[1]:


#Exploratory data analysis
#Examining customer data


# In[4]:


df_customer


# In[5]:


df_customer.isnull().sum()


# In[6]:


df_customer['LIFESTAGE'].unique()


# In[7]:


df_customer['PREMIUM_CUSTOMER'].unique()


# In[8]:


df_customer.duplicated().any()


# In[4]:


#Examining transaction data


# In[9]:


df_transaction


# In[10]:


df_transaction.info()


# In[15]:


df_transaction.duplicated().any()


# In[13]:


df_transaction[df_transaction.duplicated()]


# In[14]:


df_transaction = df_transaction.drop_duplicates()


# In[11]:


# change type of date to date using  pd.to_datetime() function '
#('1899-12-30' base date) and the unit as 'D' (days)
df_transaction['DATE'] = pd.to_datetime( df_transaction['DATE'], origin='1899-12-30', unit='D')


# In[16]:


sorted(df_transaction['PROD_NAME'].unique())


# In[22]:


# List of product names to remove which is not chips product
product_names_to_remove = [
    'Woolworths Medium   Salsa 300g',
    'Woolworths Mild     Salsa 300g',
    'Old El Paso Salsa   Dip Chnky Tom Ht300g',
    'Old El Paso Salsa   Dip Tomato Med 300g',
    'Old El Paso Salsa   Dip Tomato Mild 300g',
    'Doritos Salsa       Medium 300g',
    'Doritos Salsa Mild  300g'
]

# Filter out rows where PROD_NAME is in the list
df_transaction = df_transaction[~df_transaction['PROD_NAME'].isin(product_names_to_remove)]


# In[23]:


# extract_brand_and_size
import re

def extract_brand_and_size(prod_name):
    """
    Extracts the brand (first word by default) and size (e.g., '175g') from the product name.
    """
    # Extract brand as the first word
    brand = prod_name.split()[0]
    
    # Look for size pattern (e.g., '175g', '200G', etc.)
    size_match = re.search(r'\d+\s*[gG]', prod_name)
    size = size_match.group() if size_match else None  # If no match, return None
    
    return brand, size

# Apply the function to the 'PROD_NAME' column and create new columns
df_transaction[['Brand', 'Size']] = df_transaction['PROD_NAME'].apply(
    lambda x: pd.Series(extract_brand_and_size(x))
)

# Display the updated DataFrame
print(df_transaction[['PROD_NAME', 'Brand', 'Size']])





# In[24]:


sorted(df_transaction['Brand'].unique())


# In[26]:


# Define a dictionary with old values as keys and new values as values
replace_dict = {
    'Burger': 'Burger Ring', 
    'Dorito': 'Doritos', 
    'French': 'French Fries',
    'Grain':'Grain Waves',
    'GrnWves': 'Grain Waves',
    'Infzns': 'Infuzions',
    'Red': 'Red Rock Deli',
    'RRD': 'Red Rock Deli',
    'Smith': 'Smiths',
    'Snbts': 'Sunbites Whlegrn',
    'NCC': 'Natural Chip Co', 
    'Natural': 'Natural Chip Co',
    'Sunbites':'Sunbites Whlegrn',
    'WW': 'Woolworths'
     
}

# Replace values in the 'PROD_NAME' column based on the dictionary
df_transaction['Brand'] = df_transaction['Brand'].replace(replace_dict)

# Check the modified dataframe
print(sorted(df_transaction['Brand'].unique()))


# In[86]:


sorted(df_transaction['Size'].unique())


# In[76]:


df_transaction['Size'] = df_transaction['Size'].str.replace(r'[gG]', '', regex=True)


# In[85]:


df_transaction['Size'] = df_transaction['Size'].astype(int)


# In[80]:


df_transaction.describe()


# In[81]:


# we notice there outlier in  product quantity, and TOT_SALES  which we should investigate
df_transaction[df_transaction['PROD_QTY'] == 200.000000]


# In[37]:


#there  two transactions where PROD_QTY = 200 and TOT_SALES = 650 with samw customer
#let's see if totalsales outliers with same transcation 
[dfdf_transaction_transaction['TOT_SALES'] == 650.0]


# In[39]:


#same case where customer 226000 bought same quantity. let see if he other purchase
df_transaction[df_transaction['LYLTY_CARD_NBR'] == 226000]


# In[41]:


#He has only two previous transactions, and his purchases are different from others. 
#We could say it is better to remove the outliers and remove rows related to customer 226000.
df_transaction = df_transaction[df_transaction['LYLTY_CARD_NBR'] != 226000]
df_transaction.describe()


# In[87]:


# Merge using a left join
merged_df = pd.merge(df_transaction, df_customer, on='LYLTY_CARD_NBR', how='left')
merged_df.info()


# In[43]:


# List of related columns
columns_to_select = ['DATE', 'STORE_NBR', 'LYLTY_CARD_NBR', 'TXN_ID', 'PROD_NBR', 'PROD_QTY', 'LIFESTAGE', 'PREMIUM_CUSTOMER'
                     ,'Brand', 'Size','TOT_SALES']

# Selecting only the desired columns from df_transaction
merged_df = merged_df[columns_to_select]


# In[83]:


merged_df 


# In[47]:


#Data analysis on customer segments 
#frame question :
#customer segments
#What are the total sales for each customer segment?
# how many customers are in each segment?
# how many purchase are in each segment?



# In[59]:


#What are the total sales for each customer segment?
# Step 1: Calculate total sales by LIFESTAGE and PREMIUM_CUSTOMER
sales_by_segment = merged_df.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['TOT_SALES'].sum().reset_index()

# Step 2: Calculate total sales across all segments (this is the total for the entire dataset)
total_sales = sales_by_segment['TOT_SALES'].sum()

# Step 3: Calculate the proportion of total sales for each LIFESTAGE and PREMIUM_CUSTOMER combination
sales_by_segment['Proportion of Total Sales'] = sales_by_segment['TOT_SALES'] / total_sales

# Step 4: Create a pivot table to reshape the data (LIFESTAGE vs PREMIUM_CUSTOMER)
sales_pivot = sales_by_segment.pivot_table(index='LIFESTAGE', columns='PREMIUM_CUSTOMER',
                                           values='Proportion of Total Sales', aggfunc='sum')

# Step 5: Plotting the stacked column chart with custom colors and adding labels
fig, ax = plt.subplots(figsize=(10, 6))

# Custom color palette for PREMIUM_CUSTOMER (you can modify the colors here)
colors = sns.color_palette("Set2", n_colors=sales_pivot.shape[1])

# Plot the stacked bar chart
sales_pivot.plot(kind='bar', stacked=True, ax=ax, color=colors)

# Add labels on top of each stack segment
for p in ax.patches:
    height = p.get_height()
    width = p.get_width()
    x = p.get_x() + width / 2  # Position the label in the center of the bar
    y = p.get_y() + height / 2  # Position the label in the center of the stack
    
    # Display the label (percentage of total sales)
    ax.text(x, y, f'{height:.2%}', ha='center', va='center', fontsize=10, color='black')

# Add labels and title
plt.title('Proportion of Total Sales by LIFESTAGE and PREMIUM_CUSTOMER', fontsize=16)
plt.xlabel('LIFESTAGE', fontsize=12)

# Hide y-axis
ax.yaxis.set_visible(False)

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45, ha='right')

# Add legend title
plt.legend(title='Premium Customer', title_fontsize='13')

# Show the plot
plt.tight_layout()
plt.show()


# In[60]:


# the top 3 segments  contributing the most to total sales are Budget - older families, 
# Mainstream - young singles/couples, and Mainstream- retirees



# In[61]:


## how many customers are in each segment?
 

# Step 1: Calculate the number of customers by LIFESTAGE and PREMIUM_CUSTOMER
cus_by_segment = merged_df.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['LYLTY_CARD_NBR'].nunique().reset_index()

# Step 2: Calculate the total number of customers across all segments
total_cus = cus_by_segment['LYLTY_CARD_NBR'].sum()

# Step 3: Calculate the proportion of customers in each segment
cus_by_segment['Proportion of Total cus'] = cus_by_segment['LYLTY_CARD_NBR'] / total_cus

# Step 4: Create a pivot table to reshape the data (LIFESTAGE vs PREMIUM_CUSTOMER)
cus_pivot = cus_by_segment.pivot_table(index='LIFESTAGE', columns='PREMIUM_CUSTOMER',
                                           values='Proportion of Total cus', aggfunc='sum')

# Step 5: Plotting the stacked column chart with custom colors and adding labels
fig, ax = plt.subplots(figsize=(10, 6))

# Custom color palette for PREMIUM_CUSTOMER (you can modify the colors here)
colors = sns.color_palette("Set2", n_colors=cus_pivot.shape[1])

# Plot the stacked bar chart
cus_pivot.plot(kind='bar', stacked=True, ax=ax, color=colors)

# Add labels on top of each stack segment
for p in ax.patches:
    height = p.get_height()
    width = p.get_width()
    x = p.get_x() + width / 2  # Position the label in the center of the bar
    y = p.get_y() + height / 2  # Position the label in the center of the stack
    
    # Display the label (percentage of total customers)
    ax.text(x, y, f'{height:.2%}', ha='center', va='center', fontsize=10, color='black')

# Add labels and title
plt.title('Proportion of Total Customers by LIFESTAGE and PREMIUM_CUSTOMER', fontsize=16)
plt.xlabel('LIFESTAGE', fontsize=12)

# Hide y-axis
ax.yaxis.set_visible(False)

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45, ha='right')

# Add legend title
plt.legend(title='Premium Customer', title_fontsize='13')

# Show the plot
plt.tight_layout()
plt.show()


# In[63]:


#Mainstream - Young Singles/Couples  have the largest customer numbers, which means more people are buying chips.
#Budget - Older Families has high total sales, but the number of customers in this segment
#is relatively smaller (6.46% of the total customer base).
#This insight suggests that:
#Budget - Older Families may have a higher average spend per customer, making this segment very valuable
#in terms of sales despite having fewer customers.
#To better understand the relationship between total sales and number of customers, 
#we can calculate the average sales per customer for each segment.

#How to Calculate Average Sales per Customer:
#  we have the total sales and number of unique customers by LIFESTAGE and PREMIUM_CUSTOMER
#sales_by_segment, cus_by_segment

# Step 1: Merge the two dataframes to get total sales and number of customers in one table
merged_segment = pd.merge(sales_by_segment, cus_by_segment, on=['LIFESTAGE', 'PREMIUM_CUSTOMER'])

# Step 2: Calculate average sales per customer
merged_segment['Avg_Sales_Per_Customer'] = merged_segment['TOT_SALES'] / merged_segment['LYLTY_CARD_NBR']

# Step 3: View the segments with the highest average sales per customer
merged_segment = merged_segment.sort_values(by='Avg_Sales_Per_Customer', ascending=False)

# Display the top 10 segments with the highest average sales per customer
print(merged_segment[['LIFESTAGE', 'PREMIUM_CUSTOMER', 'Avg_Sales_Per_Customer']])



# In[68]:


#Older Families tend to spend significantly more on average compared to other customer segments, this segment could be
#multi-pack buying behavior
# let's investigate if customers are purchasing more than one unit of chips in a single transaction
# Group by LIFESTAGE and PREMIUM_CUSTOMER to analyze average quantity
avg_qty_segment_analysis = merged_df.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER']).agg(
    avg_qty=('PROD_QTY', 'mean')
).reset_index()

# Sort by average quantity in descending order for better readability
avg_qty_segment_analysis = avg_qty_segment_analysis.sort_values(by='avg_qty', ascending=False)

# Display the result
avg_qty_segment_analysis


# In[102]:


#This analysis highlights that Older Families across all premium customer categories
#(Budget, Mainstream, Premium) have the highest average quantity per transaction, with values close to 1.95.
#This strongly suggests that Older Families are likely engaging in multi-pack buying behavior.
#now let's focus on deep diving into specific customer segments to gather more insights,
#particularly on the Mainstream - Young Singles/Couples and Older Families (Budget)
#1. Mainstream - Young Singles/Couples
M_young_Singles_Couples = merged_df[(merged_df['LIFESTAGE']=='YOUNG SINGLES/COUPLES')& (merged_df['PREMIUM_CUSTOMER']=='Mainstream')]
M_young_Singles_Couples.groupby('Brand').agg( tot = ('TOT_SALES', 'sum' ),  qun= ('PROD_QTY', 'sum') ).sort_values(by='tot', ascending=False)


# In[115]:


#Kettle chips dominate both in sales and quantity purchased, making it the top-performing brand in this segment.
#It could indicate that Mainstream - Young Singles/Couples prefer this brand significantly more than others.
#let figureout that with Analysis of Affinity to Brand:
#let understand how strongly Mainstream - Young Singles/Couples prefer a brand relative to other segments
 # Group by Brand to get total product quantity for the Mainstream - Young Singles/Couples segment
brand_qty_segment = M_young_Singles_Couples.groupby('Brand').agg(
    segment_qty=('PROD_QTY', 'sum')
).reset_index()

# Group by Brand to get total product quantity for all customers
total_qty_all = merged_df.groupby('Brand').agg(
    total_qty_all=('PROD_QTY', 'sum')
).reset_index()

# Merge the two dataframes on 'Brand'
brand_qty_affinity = pd.merge(brand_qty_segment, total_qty_all, on='Brand', how='left')

# Calculate affinity as the ratio of segment's quantity to total quantity
brand_qty_affinity['affinity'] = brand_qty_affinity['segment_qty'] / brand_qty_affinity['total_qty_all']
brand_qty_affinity_sorted = brand_qty_affinity.sort_values(by='affinity', ascending=False)
# Display the result
print(brand_qty_affinity_sorted)


# In[121]:


#Tyrrells, Twisties,Doritos, and  Kettle are the top 4 brands with the highest affinity scores.
#This means the Mainstream - Young Singles/Couples segment buys these brands more frequently
#than the overall customer base.
#The affinity scores for these brands range from 0.0929 to 0.092.
#Lower Affinity Brands:

#Burger Ring, CCs, and Woolworths have the lowest affinity scores,
#suggesting that these brands are less popular within the Mainstream - Young Singles/Couples segment compared to
#the total customer base.
#Now we want to looking for prefered size to Mainstream - Young Singles/Couples  relative to other segments
 # Group by size to get total product quantity for the Mainstream - Young Singles/Couples segment
Size_qty_segment = M_young_Singles_Couples.groupby('Size').agg(
    segment_qty=('PROD_QTY', 'sum')
).reset_index()

# Group by Brand to get total product quantity for all customers
total_qty_alls = merged_df.groupby('Size').agg(
    total_qty_all=('PROD_QTY', 'sum')
).reset_index()

# Merge the two dataframes on 'Brand'
Size_qty_affinity = pd.merge(Size_qty_segment, total_qty_alls, on='Size', how='left')

# Calculate affinity as the ratio of segment's quantity to total quantity
Size_qty_affinity['affinity'] = Size_qty_affinity['segment_qty'] / Size_qty_affinity['total_qty_all']
Size_qty_affinity_sorted = Size_qty_affinity.sort_values(by='affinity', ascending=False)
# Display the result
print(Size_qty_affinity_sorted)


# In[125]:


#The most popular pack size for Tyrrells in this segment is 270g with a quantity of 1,153 sold
# let's find out which brands offer the most preferred sizes 
M_young_Singles_Couples[M_young_Singles_Couples['Size'] == 270]['Brand'].unique()


# In[126]:


#Twisties is the only brand has the size 270.
#and also it is the second preferd brand at young_Singles_Couples
# let drive to totalsale and quanity of Twisties
# Filter the data for Twisties in the Mainstream - Young Singles/Couples segment
twisties_data = M_young_Singles_Couples[M_young_Singles_Couples['Brand'] == 'Twisties']

# Calculate the total sales and quantity for Twisties in the segment
twisties_sales = twisties_data.groupby('Size').agg(
    total_sales=('TOT_SALES', 'sum'),
    total_qty=('PROD_QTY', 'sum')
).reset_index()

# Display the result for Twisties sales by size
print(twisties_sales)



# Key Insights:
# The Mainstream - Young Singles/Couples segment has distinct preferences for certain brands and sizes, particularly Tyrrells 165g and Twisties 270g.
# 
# This segment has significant sales, making it a crucial target for future marketing, product placements, and promotions.
# 
# Recommendations for Management:
# Increase Visibility and Promotions for Tyrrells 165g: Focus on the Tyrrells 165g size as it is the top-performing pack in this segment.
# Capitalize on Twisties 270g: Use the popularity of Twisties 270g in marketing campaigns and stock it accordingly.
# Customer Engagement: Leverage targeted campaigns to maintain loyalty and encourage repeat purchases in this key segment.

# In[ ]:




