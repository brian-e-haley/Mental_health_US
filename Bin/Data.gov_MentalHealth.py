#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Initialising and importing
get_ipython().run_line_magic('autosave', '300')
import pandas as pd


# In[2]:


# Saving file path for csv file to clean
csv_path = '../Resources/Data.gov/US_CDI.csv'


# In[3]:


data_gov_raw = pd.read_csv(csv_path)


# In[14]:


#data_gov_raw.head()


# In[5]:


#data_gov_raw.columns


# In[6]:


#data_gov_raw.dtypes


# In[7]:


# Take only Recent mentally unhealthy...
data_gov_MentalHealth = data_gov_raw.loc[(data_gov_raw['Topic'] == 'Mental Health')
                                          & (data_gov_raw['Question'] == 'Recent mentally unhealthy days among adults aged >= 18 years')]


# In[8]:


# Taking relevant columns
data_gov_MentalHealth = data_gov_MentalHealth.iloc[:, [0, 2, 3, 10, 11, 14, 15, 22, 24, 28]]


# In[9]:


data_gov_MentalHealth.columns = ['Year', 'Location Short', 'Location', 'Data Value 1',
       'Data Value 2', 'Low Confidence Limit', 'High Confidence Limit',
       'Lat and Long', 'Location ID', 'Category']


# In[10]:


data_gov_MentalHealth['Data Value 1'] = pd.to_numeric(data_gov_MentalHealth['Data Value 1'])


# In[15]:


data_gov_MentalHealth.head()


# In[18]:


data_gov_MentalHealth = data_gov_MentalHealth.loc[data_gov_MentalHealth['Category'] == 'GENDER']


# In[19]:


data_gov_MentalHealth.to_csv(path_or_buf = '../Resources/Data.gov/US_CDI_MentalHealth_map.csv')


# In[ ]:




