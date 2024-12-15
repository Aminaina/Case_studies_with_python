#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
 


# Load the Dataset: 

# In[2]:


df = pd.read_csv(r'C:\Users\Käyttäjä\OneDrive - LUT University\Documents 1\data_analytics\Projects\Elisa_Marketing Campaign and Customer Insights Data\marketing_campaign_data.csv')


# Understand the Data

# In[3]:


df.describe()


# In[4]:


df.info()


# In[5]:


df.isnull().sum()


# In[6]:


pd.set_option('display.max_rows', None )


# In[7]:


df


# ###Customer Segmentation

# In[8]:


##lest create segment depends on age 
##Demographics  Age_Group, Gender, Region


# In[9]:


# Define age groups using pd.cut
bins = [0, 25, 35, 50, 65, 100]  # Bin edges
labels = ["Young Adults", "Early Career", "Mid-Career Professionals", "Late-Career Professionals", "Retired"]  # Age group labels
#labels = ["18-25", "26-35", "36-50", "51-65", "65+"]
# Create the Age_Group column
df["Age_Group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)

# Display the first few rows



# In[10]:


df[["Age", "Age_Group"]].sort_values(by= "Age")


# In[11]:


# Plot 1: Age Group Distribution
plt.figure(figsize=(8, 5))
df["Age_Group"].value_counts().sort_index().plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Age Group Distribution")
plt.xlabel("Age Group")
plt.ylabel("Count of Customers")
plt.xticks(rotation= 30)
plt.show()

# Plot 2: Gender Distribution
plt.figure(figsize=(6, 5))
df["Gender"].value_counts().plot(kind="pie", autopct="%1.1f%%", startangle=90, colors=["lightcoral", "lightskyblue", "orange"])
plt.title("Gender Distribution")
plt.ylabel("")  # Hide y-axis label
plt.show()

# Plot 3: Region Distribution
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x="Region", palette="viridis", order=df["Region"].value_counts().index)
plt.title("Customer Distribution by Region")
plt.xlabel("Region")
plt.ylabel("Count of Customers")
plt.xticks(rotation=45)
plt.show()


# In[12]:


##behavior


# In[17]:


#Bin Monthly Spend
# Calculate percentiles
bins = [0, df["Monthly_Spend"].quantile(0.25), df["Monthly_Spend"].quantile(0.50), 
        df["Monthly_Spend"].quantile(0.75), df["Monthly_Spend"].max()]
labels = ["Low Spend", "Medium Spend", "High Spend", "Very High Spend"]

# Create binned column
df["Spend_Bin"] = pd.cut(df["Monthly_Spend"], bins=bins, labels=labels, include_lowest=True)


# In[18]:


#Campaign Engagement
Engagement_bins = [0, 4, 8, 15]
Engagement_labels = ["Low Engagement",  "Medium Engagement", "High Engagement"]
# Create binned column
df["Engagement_bin"] = pd.cut(df["Campaign_Engagement"], bins=Engagement_bins, labels=Engagement_labels,  right=True )


# In[23]:


#Last Interaction Date:
import datetime as dt
df["Last_Interaction_Date"] = pd.to_datetime(df["Last_Interaction_Date"])
today = dt.datetime.now()
df["Last_Interaction_period"] = ((today - df["Last_Interaction_Date"]).dt.days )/ 30

conditions = [
    df["Last_Interaction_period"] <= 3,
    df["Last_Interaction_period"] <= 6,
    df["Last_Interaction_period"] > 6
]
choices = ["Active", "Moderately Active", "Inactive"]
df["Interaction_Segment"] = np.select(conditions, choices, default="Unknown")



# In[31]:


#Products Purchased
Products_bins = [0, 0.99, 3, 4, 5]
Products_labels = ['no Purchased', '1-2 Products', '3-4 Products', '5 Products']

df["Products_Purchased_Bin"] = pd.cut(df["Products_Purchased"] , bins=Products_bins, labels=Products_labels,  include_lowest=True,  right=True)


# In[38]:


# Set consistent style
sns.set_style("whitegrid")

# Plot 1: Spend vs. Engagement Level (Scatter plot)
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Monthly_Spend", y="Campaign_Engagement", hue="Engagement_bin", palette="viridis")
plt.title("Spend vs. Campaign Engagement")
plt.xlabel("Monthly Spend")
plt.ylabel("Campaign Engagement")
plt.show()

# Plot 2: Interaction Segment by Engagement Level (Bar plot)
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Interaction_Segment", hue="Engagement_bin", palette="Set2")
plt.title("Interaction Segment by Engagement Level")
plt.xlabel("Interaction Segment")
plt.ylabel("Count of Customers")
plt.show()

# Plot 3: Products Purchased vs. Spend Bin (Bar plot)
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Products_Purchased_Bin", hue="Spend_Bin", palette="coolwarm")
plt.title("Product Purchases by Spend Bin")
plt.xlabel("Products Purchased")
plt.ylabel("Count of Customers")
plt.xticks(rotation=45)
plt.show()



# Here are actionable **recommendations** based on the detailed analysis of the report:
# 
# ---
# 
# ### **1. Product Purchases Analysis**  
# **Key Findings**:  
# - The **1-2 Products** category has the highest frequency among **High Spend** and **Very High Spend** customers.  
# - Customers who did **not purchase any products** mostly belong to **High Spend** and **Medium Spend** groups.
# 
# **Recommendations**:  
# 1. **Upselling Opportunities**:  
#    - Target customers who purchased **1-2 products** with personalized recommendations for related products to encourage **cross-selling**.  
#    - Use bundled offers (e.g., "Buy 2, get 1 free") or loyalty points to push more purchases.  
# 
# 2. **Re-engagement Campaigns**:  
#    - Focus on the **No Purchase** group in **High Spend** and **Medium Spend** categories. These customers have spending capacity but haven’t made purchases.  
#    - Use tailored email campaigns, exclusive discounts, and limited-time offers to encourage purchases.  
#    - Investigate why they haven’t purchased—are there gaps in product variety, price, or marketing strategy?  
# 
# ---
# 
# ### **2. Interaction Segment by Engagement Level**  
# **Key Findings**:  
# - **Highly Engaged** customers dominate the **Inactive** segment.  
# - **Medium Engagement** and **Low Engagement** customers are spread across **Moderately Active** and **Active** groups.  
# 
# **Recommendations**:  
# 1. **Activate the Inactive Group**:  
#    - Since many **Inactive** customers are **Highly Engaged**, it’s essential to **reignite their interaction** with targeted campaigns. Examples include:  
#       - Offering exclusive rewards for activity (e.g., logging in, reviewing products).  
#       - Sending personalized messages based on past engagement data.  
# 
# 2. **Improve Engagement for Medium/Low Segments**:  
#    - **Interactive Campaigns**: Use quizzes, surveys, or gamified content to engage Medium/Low customers.  
#    - Highlight customer testimonials, success stories, or product reviews to build trust and interest.  
#    - Use behavioral triggers (e.g., abandoned cart emails) for Medium Engagement customers to encourage further interaction.  
# 
# 3. **Segmented Campaigns**:  
#    - Break the customer base into **Inactive, Moderately Active, and Active** segments, and personalize messaging for each:  
#       - Inactive: Awareness campaigns to rebuild interest.  
#       - Moderately Active: Offers to move them to Active.  
#       - Active: Reward their loyalty with exclusive discounts or early access to products.  
# 
# ---
# 
# ### **3. Spend vs Campaign Engagement**  
# **Key Findings**:  
# - Higher Monthly Spend customers show **Medium to High Engagement**.  
# - Some **High Spend customers** still have **Low Engagement**, presenting a contradiction.  
# 
# **Recommendations**:  
# 1. **Focus on High Spenders with Low Engagement**:  
#    - Identify why these customers have low engagement despite high spending (e.g., dissatisfaction, lack of connection with marketing).  
#    - Use loyalty programs, personalized surveys, and targeted communications to increase their engagement.  
# 
# 2. **Reward High Engagement**:  
#    - Develop a rewards program for **Highly Engaged** customers to retain their activity and encourage future purchases.  
#    - Provide exclusive benefits, such as sneak peeks of new products or invitations to events.  
# 
# 3. **Improve Campaign Quality for Medium Engagement**:  
#    - Evaluate which campaigns are most effective for **Medium Engagement** customers and replicate those strategies.  
#    - Test different marketing channels (e.g., social media ads, influencer marketing, newsletters) to boost engagement.  
# 
# ---
# 
# ### **4. General Recommendations**  
# 1. **Customer Segmentation**:  
#    - Continue to segment customers into **Spend Bins** (Low, Medium, High, Very High Spend) and **Engagement Levels** (Low, Medium, High).  
#    - Use these insights to deliver **targeted messaging** and campaigns.  
# 
# 2. **Analyze Non-Purchase Behavior**:  
#    - Investigate why customers in the **High Spend** and **Medium Spend** groups haven’t made purchases. Potential factors include product availability, price sensitivity, or ineffective communication.  
# 
# 3. **Personalized Communication**:  
#    - Use data-driven personalization to tailor marketing efforts. Examples include personalized product recommendations, dynamic pricing, or messaging based on past behavior.  
# 
# 4. **Track Key Metrics**:  
#    - Continuously monitor:  
#       - Customer churn rate.  
#       - Engagement rates across segments.  
#       - Conversion rates from campaigns targeting inactive and non-purchase groups.  
# 
# 5. **Feedback Loop**:  
#    - Collect feedback from **No Purchase** customers and those with **Low Engagement** to identify improvement areas in your campaigns, product offerings, or user experience.
# 
# ---
# 
# ### Summary of Action Points:  
# | **Objective**                        | **Recommendation**                               |  
# |--------------------------------------|-----------------------------------------------|  
# | Increase Purchases for High Spenders | Focus on upselling and cross-selling strategies. |  
# | Re-engage Inactive Customers         | Offer exclusive rewards, discounts, and campaigns. |  
# | Boost Engagement for Low/Medium Users| Use interactive content, gamification, and personalized offers. |  
# | Retain Highly Engaged Customers      | Launch loyalty programs and exclusive rewards.   |  
# | Convert No Purchase Customers        | Run reactivation campaigns with targeted messaging. |  
# 
# ---
# 
# Let me know if you need detailed campaign examples or further segmentation! 😊
# 

# In[ ]:





# In[ ]:




