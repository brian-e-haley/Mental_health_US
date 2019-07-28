#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Initialising and importing
get_ipython().run_line_magic('autosave', '300')
import pandas as pd
import folium as fol


# In[2]:


# Saving file path for csv file
csv_path = '../Resources/Data.gov/US_CDI_MentalHealth_map.csv'

# Reading csv mental health data
data_gov = pd.read_csv(csv_path)

states = '../Resources/US_States/us-states.json'


# In[12]:


# Generating the map
m = fol.Map(location=[40, -100], zoom_start=3)

fol.Choropleth(
    geo_data=states,
    name='choropleth',
    data=data_gov,
    columns=['Location Short', 'Data Value 1'],
    key_on='feature.id',
    fill_color='OrRd',
    fill_opacity=0.5,
    line_opacity=0.4,
    legend_name='Severity of Mental Health Issues'
).add_to(m)


# In[13]:


m


# In[14]:


m.save('../Output/map_MentalHealth.html')


# In[ ]:




