#!/usr/bin/env python
# coding: utf-8

# In[109]:


#import dependencies
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from scipy.stats.stats import pearsonr
from statsmodels.formula.api import ols
from scipy.stats import linregress

# import plotly.plotly as py
# import plotly.graph_objs as go


# In[110]:


#import and read excel file on mental health
excelfile=("../Resources/SAMHDA/SAMHDA_MentalIllnessbyState/Combined_mentalillness_2010-17.xlsx")
df_illness=pd.read_excel(excelfile)
df_illness['estimate']=df_illness['estimate']*100
df_illness.head()


# In[111]:


#import and read excel file on suicides
excelfile=("../Resources/CDC/SuicideRates/Suicide_combined_byState.xlsx")
df_suicide=pd.read_excel(excelfile)
df_suicide.head()


# In[112]:


#merging 2 files based on year and state

#add a new column year-state to mental illness data
df_illness['year-state']=df_illness['year'].map(str)+df_illness['state']
df_illness.head()


#add a new column year-state to suicide data
df_suicide['year-state']=df_suicide['year'].map(str)+df_suicide['State']
df_suicide.head()

#merging files
df_illness_suicide=pd.merge(df_illness, df_suicide, on="year-state", how="left",suffixes=('_ill','_sui'))
df_illness_suicide.head()

#suicide data available 2014 onwards, filtering data frame accordingly
df_ill_sui_201417=df_illness_suicide.loc[df_illness_suicide['year_ill']>2013,:]
df_ill_sui_201417=df_ill_sui_201417.loc[df_ill_sui_201417['state']!='District of Columbia',:]
df_ill_sui_201417.head()

# df_ill_sui_201417.to_csv("Test.csv")


# In[113]:


#scatter plot-all years together

scatter_ill_sui=df_ill_sui_201417.plot.scatter(x='estimate',
                                               y='RATE',
                                               grid=True,
                                               title='Mental Illness vs. Suicide Rate',
                                               color='deepskyblue',
                                               edgecolor='grey',
                                               s=40,
                                               alpha=.8
                                               )
plt.xlabel('% Population with any Mental Illness')
plt.ylabel('Suicide Rate per 100,000 individuals')

# z = np.polyfit(df_ill_sui_201417['estimate'], df_ill_sui_201417['RATE'], 1)
# p = np.poly1d(z)
# plt.plot(df_ill_sui_201417['estimate'],p(df_ill_sui_201417['estimate']),"r--")

# Trend line
(slope, intercept, _, _, _) = linregress(df_ill_sui_201417['estimate'], df_ill_sui_201417['RATE'])
fit = slope * df_ill_sui_201417['estimate'] + intercept
plt.plot(df_ill_sui_201417['estimate'], fit, 'r--')


plt.savefig("../Images/Mental Illness vs. Suicide Rate.png")
plt.show()


# In[114]:


#correlation coefficient between mental illness and suicide rate
print(np.corrcoef(df_ill_sui_201417['estimate'], df_ill_sui_201417['RATE']))


# In[115]:


#Regression analysis - mental illness and suicide rate
mod = ols(formula='RATE~estimate', data=df_ill_sui_201417)
res = mod.fit()
print(res.summary())


# In[116]:


#for line chart

plt.subplot

df_ill_sui_grpby=df_ill_sui_201417.groupby(['year_ill'])
sui_rate=df_ill_sui_grpby['RATE'].mean()
ill_rate=df_ill_sui_grpby['estimate'].mean()

line_chart=sui_rate.plot(kind='line',
                         marker='o',
                         label='Suicide Rate per 100,000 individuals',
                         title='Mental Illness vs. Suicide Rate (2014-2017)')

line_chart=ill_rate.plot(kind='line',
                         marker='x',
                         label='%Population with any mental illness')

line_chart.set_ylim(12.5,20)
line_chart.legend()

plt.xlabel('Year')


# In[117]:


#import and read excel file on income
csvfile=("../Resources/BEA/PersonalIncome_reformatted.csv")
df_income=pd.read_csv(csvfile)
df_income.head()


# In[118]:



#add a new column year-state to income data
df_income['year-state']=df_income['Year'].map(str)+df_income['GeoName']
df_income.head()

#filtering the data frame to get Per capita disposable personal income
df_income_percapita=df_income.loc[df_income['Description']=='Per capita disposable personal income (dollars) 2/',:]
df_income_percapita.head()

#merging files
df_illness_income=pd.merge(df_illness, df_income_percapita, on="year-state", how="left",suffixes=('_ill','_inc'))
df_illness_income.head()


# In[119]:


#scatter plot-all years together

scatter_ill_inc=df_illness_income.plot.scatter(x='value',
                                               y='estimate',
                                               grid=True,
                                               title='% Population with any mental illness vs Disposable Income',
                                               color='lightcoral',
                                               edgecolor='grey',
                                               s=40,
                                               alpha=.8)
plt.xlabel('Per capita disposable income')
plt.ylabel('% Population with any mental illness')

#Trend line
# z = np.polyfit(df_illness_income['value'], df_illness_income['estimate'], 1)
# p = np.poly1d(z)
# plt.plot(df_illness_income['value'],p(df_illness_income['value']),"g--")

(slope, intercept, _, _, _) = linregress(df_illness_income['value'], df_illness_income['estimate'])
fit = slope * df_illness_income['value'] + intercept
plt.plot(df_illness_income['value'], fit, 'g--')


plt.savefig("../Images/Mental Illness vs. Income.png")

plt.show()


# In[120]:


#correlation coefficient between mental illness and income
print(np.corrcoef(df_illness_income['value'], df_illness_income['estimate']))


# In[121]:


#Regression analysis - mental illness and income
mod = ols(formula='estimate~value', data=df_illness_income)
res = mod.fit()
print(res.summary())


# In[122]:


#import and read excel file on income
csvfile=("../Resources/BEA/GDPbyStateMn_reformatted.csv")
df_gdp=pd.read_csv(csvfile)
df_gdp.head()


# In[123]:


#add a new column year-state to gdp data
df_gdp['year-state']=df_gdp['year'].map(str)+df_gdp['GeoName']
df_gdp.head()


#merging files
df_illness_gdp=pd.merge(df_illness, df_gdp, on="year-state", how="left",suffixes=('_ill','_gdp'))
df_illness_gdp.head()


# In[124]:


#scatter plot-all years together

scatter_ill_gdp=df_illness_gdp.plot.scatter(x='estimate',
                                            y='value',
                                            grid=True,
                                            title='% Population with any mental illness vs GDP',
                                            color='deepskyblue',
                                            edgecolor='grey',
                                            s=40,
                                            alpha=.8
                                            )

plt.xlabel('% Population with any mental illness')
plt.ylabel('GDP ($ Mn)')

plt.ylim(0,1000000)

z = np.polyfit(df_illness_gdp['estimate'], df_illness_gdp['value'], 1)
p = np.poly1d(z)
plt.plot(df_illness_gdp['estimate'],p(df_illness_gdp['estimate']),"r--")



plt.savefig("../Images/Mental Illness vs. GDP.png")

plt.show()


# In[125]:


#correlation coefficient between mental illness and gdp
print(np.corrcoef(df_illness_gdp['estimate'], df_illness_gdp['value']))


# In[126]:


#Regression analysis - mental illness and gdp
mod = ols(formula='estimate~value', data=df_illness_gdp)
res = mod.fit()
print(res.summary())


# In[183]:


# mental illness trend
df_illness_yr=df_illness.groupby(['year'])
df_illness_yr['estimate'].mean().plot(kind='line',
                                      marker='o',
                                      color='red',
                                      grid=True,
                                      title='% Population with Mental Illness in US')
plt.ylim(17,20)
plt.ylabel('% Population with any mental illness')

plt.savefig("../Images/Trend: % Population with any mental illness.png")


# In[186]:


# mental illness distribution-2017
df_illness_2017=df_illness.loc[df_illness['year']==2017,:]

bins=[15,16,17,18,19,20,21,22,23,24,25,26]
groups=['15%-16%','16%-17%','17%-18%','18%-19%','19%-20%','20%-21%','21%-22%','22%-23%','23%-24%','24%-25%','25%-26%']

df_illness_2017['bins']=pd.cut(df_illness_2017['estimate'],bins,labels=groups)

df_illness_2017_bins=df_illness_2017.groupby(['bins'])

df_illness_2017_bins['state'].count().plot(kind='bar',
                                           figsize=(7,5),
                                           color='skyblue',
                                           title='# States vs. % Population with Mental Illness in 2017',
                                           )

plt.xlabel('% Population with mental illness')
plt.ylabel('Number of states in US')

plt.savefig("../Images/# States vs. % Population with Mental Illness in 2017.png")


# In[ ]:




