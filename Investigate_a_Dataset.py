#!/usr/bin/env python
# coding: utf-8

# > **Tip**: Welcome to the Investigate a Dataset project! You will find tips in quoted sections like this to help organize your approach to your investigation. Once you complete this project, remove these **Tip** sections from your report before submission. First things first, you might want to double-click this Markdown cell and change the title so that it reflects your dataset and investigation.
# 
# # Project: Investigate a Dataset - No-show appointments
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# 
# This dataset collects information from 100k medical appointments in Brazil and is focused on the question of **whether or not patients show up for their appointment**. A dataset contain 14 colum.
# #### Colums:
# * **PatientId** : dentification of a patient
# * **AppointmentID**: Identification of each appointment
# * **Gender** :Male or Female
# * **ScheduledDay** :tells us on what day the patient set up their appointment
# * **AppointmentDay**:The day of the actual appointment
# * **Age** : The age of patient
# * **Neighbourhood** :indicates the location of the hospital
# * **Scholarship** : dicates whether or not the patient is enrolled in Brasilian welfare program
# * **Hipertension** : True if the patient suffring from Hipertension or False
# * **Diabetes** :True if the patient suffring from Diabetes or False
# * **Alcoholism** :True if the patient suffring from Alcoholism or False
# * **Handcap** :True or False
# * **SMS_received** :  number of messages sent to the patient
# * **No-show** : it says ‘No’ if the patient showed up to their appointment, and ‘Yes’ if they did not show up.
# ### Question(s) for Analysis      
# 1- What is the distribution of patients according to gender? Is gender related to attendance?    
# 2- How many patinet suffring from Hipertension and  what is the percenege?    3-Dose older patient suffering from Hypertension more than younger people?   
# 
# 
# 
# 

# In[25]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# 
# 
# ### General Properties
# 

# In[3]:


pathh = 'Database_No_show_appointments/noshowappointments-kagglev2-may-2016.csv'
df = pd.read_csv(pathh)
print(df.head())


# In[9]:


print(df.shape)


# In[10]:


print(df.info())


# In[4]:


df.head()


# In[12]:


print(df.nunique())


# In[11]:


print(df.describe())


# In[13]:


print(df.isnull().sum())


# In[14]:


print(df.sample(5))


# In[5]:


print(df.dtypes)


# In[7]:


print(df.tail(2))


# In[15]:


df.duplicated().sum()  


# In[11]:


def columns_unique_value(col) :
  print(df[col].unique())

def columns_count_value(col) :
 print(df[col].value_counts())


# In[13]:


columns_unique_value('Age')


# In[28]:


columns_unique_value('Handcap')


# In[14]:


columns_count_value('Age')


# 
# ### Data Cleaning
# 
# **issue1**:fix data type    
# **issue2**: Age colum has outlier values 
# 
#  

# In[19]:


df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])


# In[20]:


df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])


# In[21]:


df.PatientId=df.PatientId.astype('int64')


# In[22]:


df.Age=df.Age.astype('int8')


# In[26]:


np.iinfo('int8') 


# In[27]:


df.Age=df.Age.astype('int8')


# In[18]:


df = df.dropna()


# In[19]:


df.info()


# In[20]:


df.describe()


# In[7]:


df.duplicated()


# In[8]:


sum(df.duplicated())


# In[10]:


df.drop_duplicates(inplace=True)


# In[11]:


df


# In[12]:


df.info()


# In[21]:


df['Age'] = df['Age'].apply(lambda x: df['Age'].median() if x < 0 else x)


# In[22]:


df['Handcap'].value_counts()


# In[23]:


df['WaitingDays'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days


# In[30]:


df=df.astype({'Gender':'category','No-show':'category'})


# In[31]:


df=df.astype({'Scholarship':bool,'Hipertension':bool,'Diabetes':bool,'Alcoholism':bool,'SMS_received':bool})


# In[32]:


df.rename(columns={'PatientId':'Patient_ID', 'AppointmentID':'Appointment_ID', 'Hipertension':'Hypertension', 'Handcap':'Handicap', 'No-show':'No_Show'}, inplace=True)


# In[33]:


df.info()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# 
# 
# ### Research 
# Question 1 What is the distribution of patients according to gender? Is gender related to attendance?

# In[38]:


def plot_pie(col,title):
 df[col].value_counts().plot(kind='pie',title=f'Distribution of {title}',legend=True);


# In[34]:


columns_count_value('Gender')



# In[39]:


plot_pie('Gender',title='Gender')


# In[41]:


df_show=df[df['No_Show']=='No']
df_notshow=df[df['No_Show']=='Yes']


# In[42]:


df_show['Gender'].value_counts()


# In[43]:


df_notshow['Gender'].value_counts()


# In[45]:


df.groupby('Gender')['No_Show'].value_counts(normalize=True)


# In[48]:


The percentage is so Similar    
if the patient is Male so the percent to attendence appointment is 80%   
if the patient is Female so the percent to attendence appointment is 79.6%
if the patient is Male so the percent to  not attendence appointment is 19.9%   
if the patient is Female so the percent to  not attendence appointment is 20.3%   
Therefore, I cannot say that if the gender is female, she will commit to attending more than the male


# In[49]:


df.groupby('Gender',observed=True)['No_Show'].value_counts(normalize=True).unstack().plot(kind='bar',xlabel='Gender',ylabel='Percent',title='The  percentege of patient show and not show based on Gender');


# In[50]:


get_ipython().run_line_magic('pinfo', 'percentage')


# In[51]:


columns_count_value('Hypertension')


# In[53]:


df['Hypertension'].value_counts(normalize=True)


# ### Research Question 2  Dose older patient suffering from Hypertension more than younger people?

# In[55]:


df[df['Hypertension']==True]['Age'].hist(legend=True);


# In[57]:


df.corr(numeric_only=True)['Hypertension']['Age']


# In[58]:


df_Hypertension=df.groupby('Age',as_index=False)['Hypertension'].value_counts(normalize=True)


# In[59]:


df_Hypertension[df_Hypertension['Hypertension']==True].plot(kind='scatter',x='Age',y='proportion',title='Relation between Age and suffring from Hypertension ');


# <a id='conclusions'></a>
# ## Conclusions
# 
# The age distribution shows that the older people suffer from  Hypertension more than young
# 
# ## Submitting your Project 
# 
# > **Tip**: Before you submit your project, you need to create a .html or .pdf version of this notebook in the workspace here. To do that, run the code cell below. If it worked correctly, you should see output that starts with `NbConvertApp] Converting notebook`, and you should see the generated .html file in the workspace directory (click on the orange Jupyter icon in the upper left).
# 
# > **Tip**: Alternatively, you can download this report as .html via the **File** > **Download as** submenu, and then manually upload it into the workspace directory by clicking on the orange Jupyter icon in the upper left, then using the Upload button.
# 
# > **Tip**: Once you've done this, you can submit your project by clicking on the "Submit Project" button in the lower right here. This will create and submit a zip file with this .ipynb doc and the .html or .pdf version you created. Congratulations!

# In[ ]:


# Running this cell will execute a bash command to convert this notebook to an .html file
get_ipython().system('python -m nbconvert --to html Investigate_a_Dataset.ipynb')

