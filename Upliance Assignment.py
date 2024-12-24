#!/usr/bin/env python
# coding: utf-8

# # Loading the Data

# In[1]:


import pandas as pd

user_details = pd.read_excel("C:/Users/manis/Downloads/Data Analyst Intern Assignment - Excel.xlsx", sheet_name='UserDetails.csv')
cooking_sessions = pd.read_excel("C:/Users/manis/Downloads/Data Analyst Intern Assignment - Excel.xlsx", sheet_name='CookingSessions.csv')
order_details = pd.read_excel("C:/Users/manis/Downloads/Data Analyst Intern Assignment - Excel.xlsx", sheet_name='OrderDetails.csv')


# # Inspecting and Cleaning the Data

# In[2]:


print(user_details.isnull().sum())
print(cooking_sessions.isnull().sum())
print(order_details.isnull().sum())


# In[3]:


order_details['Rating'].fillna(order_details['Rating'].mean(), inplace=True)


# In[4]:


order_details['Order Date'] = pd.to_datetime(order_details['Order Date'])
cooking_sessions['Session Start'] = pd.to_datetime(cooking_sessions['Session Start'])
cooking_sessions['Session End'] = pd.to_datetime(cooking_sessions['Session End'])


# # Merging the Datasets

# In[5]:


user_details = user_details.drop_duplicates(subset=['User ID'])
cooking_sessions = cooking_sessions.drop_duplicates(subset=['User ID'])
order_details = order_details.drop_duplicates(subset=['User ID'])


# In[6]:


user_details['User ID'] = user_details['User ID'].str.strip().str.upper()
cooking_sessions['User ID'] = cooking_sessions['User ID'].str.strip().str.upper()
order_details['User ID'] = order_details['User ID'].str.strip().str.upper()


# In[7]:


# Check for missing User IDs
missing_in_user_details = set(order_details['User ID']) - set(user_details['User ID'])
print("Missing in User Details:", missing_in_user_details)

missing_in_cooking_sessions = set(order_details['User ID']) - set(cooking_sessions['User ID'])
print("Missing in Cooking Sessions:", missing_in_cooking_sessions)


# In[8]:


merged_data = pd.merge(order_details, cooking_sessions, on='User ID', how='outer')
merged_data = pd.merge(merged_data, user_details, on='User ID', how='outer')


# In[9]:


print("Merged Data Preview:")
print(merged_data.head())

print("Columns in Merged Data:", merged_data.columns)
print("Total Rows in Merged Data:", len(merged_data))


# # Analyzing the Relationships

# In[10]:


print("Columns in merged_data:", merged_data.columns)


# In[11]:


print(merged_data[['Dish Name_x', 'Dish Name_y']].drop_duplicates())


# In[12]:


merged_data = merged_data.rename(columns={'Dish Name_x': 'Dish Name'})
merged_data = merged_data.drop(columns=['Dish Name_y'])


# In[13]:


# Group by 'User ID' and 'Dish Name' to count occurrences
cooking_order_relation = merged_data.groupby(['User ID', 'Dish Name']).size().reset_index(name='Count')

# Display the result
print(cooking_order_relation)


# In[14]:


popular_dishes = merged_data['Dish Name'].value_counts()
print(popular_dishes)


# In[15]:


age_analysis = merged_data.groupby('Age')['Total Orders'].sum()
location_analysis = merged_data.groupby('Location')['Total Orders'].sum()
print(age_analysis, location_analysis)


# # Visualizations

# In[18]:


import matplotlib.pyplot as plt

popular_dishes.head(10).plot(kind='bar')
plt.title('Top Popular Dishes')
plt.xlabel('Dish Name')
plt.ylabel('Frequency')
plt.show()


# In[17]:


import seaborn as sns

sns.barplot(x=merged_data['Age'], y=merged_data['Total Orders'])
plt.title('User Activity by Age')
plt.show()


# In[ ]:




