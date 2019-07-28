#!/usr/bin/env python
# coding: utf-8

# # Banking and Unemployment
# ---
# The below script explores the relationship between states with high unemployment rates and bank counts per state.
# 
# In this script, we retrieved and plotted data from the 2013 US Census and Google Places API to show the relationship between various socioeconomic parameters and bank count across 700 randomly selected zip codes. We used Pandas, Numpy, Matplotlib, Requests, Census API, and Google API to accomplish our task.

# In[3]:


# Dependencies
from census import Census
from config import (census_key, gkey)
import gmaps
import numpy as np
import pandas as pd
import requests
import time
import us
import matplotlib.pyplot as plt
import seaborn as sns

# Census API Key
c = Census(census_key, year=2016)


# In[4]:


c.acs5.get(('NAME', 'B25034_010E'),
          {'for': 'state:{}'.format(us.states.MD.fips)})


# ## Data Retrieval

# In[6]:


# Run Census Search to retrieve data on all states (2016 ACS5 Census)
# See: https://github.com/CommerceDataService/census-wrapper for library documentation
# See: https://gist.github.com/afhaque/60558290d6efd892351c4b64e5c01e9b for labels
census_data = c.acs5.get(('NAME'          #state name
                          ,'B01003_001E'  #population total
                          ,'B17001_001E'  #poverty status total
                          ,'B17001_002E'  #poverty status below poverty level
                          ,'B19301_001E'  #total per capita income
                          ,'B23025_001E'  #total labor force 16 years and over
                          ,'B23025_004E'  #total Civilian force 16 years and over, employed
                          ,'B23025_005E'  #Unemployment Civilian Count
                          ,'B23025_006E'  #total Armed forces 16 years and over, employed
                          ,'B23025_007E'  #total not labor force
                          ,'B25003_001E'  #total houses
                          ,'B25003_002E'  #Total!!Owner occupied
                          ,'B25003_003E'  #Total!!Renter occupied
                          ,'B25081_002E'  #Houses with mortgage
                          ,'B992701_001E' #total people
                          ,'B992701_002E' #people with medical coverage
                          ,'B992701_003E' #people without medical coverage
                          ), {
                         'for': 'state:*'})

# Convert to DataFrame
census_pd = pd.DataFrame(census_data)

# # # Column Reordering
census_pd = census_pd.rename(columns={ 'NAME': 'State'        #state name
                                      ,'B01003_001E':'Total Population'  #population total
                                      ,'B17001_001E':'Total Poverty'  #poverty status total
                                      ,'B17001_002E':'People Below Poverty Level'  #poverty status below poverty level
                                      ,'B19301_001E':'Per Capita Income'  #total per capita income
                                      ,'B23025_001E':'Total Labor Force'  #total labor force 16 years and over
                                      ,'B23025_004E':'Total Employed Civilian'  #total Civilian force 16 years and over, employed
                                      ,'B23025_005E':'Unemployment Civilian'  #Unemployment Civilian Count
                                      ,'B23025_006E':'Armed Forces Employment'  #total Armed forces 16 years and over, employed
                                      ,'B23025_007E':'Total Not Labor Force'  #total not labor force
                                      ,'B25003_001E':'Total Houses'  #total houses
                                      ,'B25003_002E':'Houses with owners'  #Total!!Owner occupied
                                      ,'B25003_003E':'Houses with renters'  #Total!!Renter occupied
                                      ,'B25081_002E':'Houses with mortgage'  #Houses with mortgage
                                      ,'B992701_001E':'Total People' #total people
                                      ,'B992701_002E':'Total People with insurance' #people with medical coverage
                                      ,'B992701_003E':'Total People withou insurance'}) #people without medical coverage

# # Add in Employment Rate (Employment Count / Population)
# census_pd["Unemployment Rate"] = 100 * \
#     census_pd["Unemployment Count"].astype(
#         int) / census_pd["Population"].astype(int)

# # Final DataFrame
# census_pd = census_pd[["Zipcode", "Population", "Unemployment Rate"]]


# In[7]:


# Visualize
print(len(census_pd))
census_pd.head()


# ## Combine Data

# In[8]:


# Import the original data we analyzed earlier. Use dtype="object" to match other
samhsa_data = pd.read_csv(
    '../Resources/SAMHSA/Any_Mental_Illness_2016.csv', dtype="object", encoding="utf-8")

# Visualize
samhsa_data.head()

samhsa_data.drop(['Unnamed: 10', 'Unnamed: 11',
       'Unnamed: 12', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15'], axis=1, inplace=True)


# In[9]:


samhsa_data.head()


# In[10]:


# # Merge the two data sets along zip code
census_data_complete = pd.merge(
    samhsa_data, census_pd, how="outer", on=["State", "State"])

# Save the revised Data Frame as a csv
census_data_complete.to_csv(
    "../Resources/Census_Data/census_merged.csv", encoding="utf-8", index=False)

# Visualize
census_data_complete.head()
# census_data_complete.columns


# In[12]:


# Import the data analyzed earlier.

final_data_df = pd.read_csv(
    '../Resources/Census_Data/final_data.csv', encoding="utf-8")

# # final_data_df.columns
final_data_df['18 or Older % MI\nEstimate'] = final_data_df['18 or Older % MI\nEstimate']*100

final_data_df.head()


# In[13]:


# poverty and mi correlation

poverty_df = final_data_df[['State','People Below Poverty %','18 or Older % MI\nEstimate']]
poverty_df = poverty_df.sort_values(by=['People Below Poverty %'])
poverty_df = poverty_df.reset_index(drop=True)
poverty_df.head()


# In[15]:


# Mental Ilness X Poverty Level
sns.set()
plt.figure(figsize=(20,18))
plt.barh(poverty_df['State'], poverty_df['18 or Older % MI\nEstimate']
        , align='center', alpha=0.5, )
plt.yticks(poverty_df['State'])
plt.ylabel('States With More People Below Poverty Level')
plt.xlabel('Mental Ilness By State Population %')
plt.title('Mental Ilness X Poverty Level')
plt.savefig('../Resources/Census_Data/mental_poverty.png')

plt.show()


# In[16]:


# Unemployment and mi correlation

unemployment_df = final_data_df[['State','Unemployment Civilian %','18 or Older % MI\nEstimate']]
unemployment_df = unemployment_df.sort_values(by=['Unemployment Civilian %'])
unemployment_df = unemployment_df.reset_index(drop=True)
unemployment_df.head()


# In[18]:


# Mental Ilness X Employment
sns.set()
plt.figure(figsize=(20,18))
plt.barh(unemployment_df['State'], unemployment_df['18 or Older % MI\nEstimate']
        , align='center', alpha=0.5, color='red')
plt.yticks(unemployment_df['State'])
plt.ylabel('States By Unemployment Level')
plt.xlabel('Mental Ilness By State Population %')
plt.title('Mental Ilness X Unemployment Status')
plt.savefig('../Resources/Census_Data/mental_unemployment.png')

plt.show()


# In[19]:


# Health Insurance and mi correlation

insurance_df = final_data_df[['State','Total People without insurance %','18 or Older % MI\nEstimate']]
insurance_df = insurance_df.sort_values(by=['Total People without insurance %'])
insurance_df = insurance_df.reset_index(drop=True)
insurance_df.head()


# In[20]:


# Mental Ilness X Health Insurance
sns.set()
plt.figure(figsize=(20,18))
plt.barh(insurance_df['State'], insurance_df['18 or Older % MI\nEstimate']
        , align='center', alpha=0.5, color='green')
plt.yticks(insurance_df['State'])
plt.ylabel('States By Health Care Insurance Coverage')
plt.xlabel('Mental Ilness By State Population %')
plt.title('Mental Ilness X Health Insurance Coverage')
plt.savefig('../Resources/Census_Data/mental_insurance.png')
 
plt.show()

