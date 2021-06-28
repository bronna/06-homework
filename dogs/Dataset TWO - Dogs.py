#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[36]:


pd.set_option("display.max_rows", None, "display.max_columns", None)


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[37]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", nrows=30000, na_values=["Unknown", "UNKNOWN"])
df.head()


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[38]:


df.info(verbose=True)


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# Each row is a dog in New York City. `Primary Breed` gives the dog's breed and `License Issued Date` gives the date the pet became registered.

# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# 1. What is the most popular breed?
# 2. What is the average dog age?
# 3. What are the 3 most common dog colors?
# 4. What percentage of dogs are spayed and neutered?

# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[39]:


df_breeds = df['Primary Breed'].value_counts().head(10)
df_breeds


# In[40]:


df_breeds.sort_values(ascending=True).plot(kind='barh', x='Primary Breed')


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[41]:


# Added 'na_values=["Unknown"]' to read_csv above
df_breeds.sort_values(ascending=True).plot(kind='barh', x='Primary Breed')


# ## What are the most popular dog names?

# In[42]:


df['Animal Name'].value_counts().head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[43]:


df[df['Animal Name'] == 'Brianna'].shape


# In[44]:


df[df['Animal Name'] == 'Max'].shape


# In[45]:


df[df['Animal Name'] == 'Maxwell'].shape


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[46]:


df['Guard or Trained'].value_counts(normalize=True)*100


# ## What are the actual numbers?

# In[47]:


df['Guard or Trained'].value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[48]:


df['Guard or Trained'].value_counts(dropna=False)


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[49]:


df['Guard or Trained'] = df['Guard or Trained'].fillna("No")


# In[50]:


df["Guard or Trained"].value_counts()


# ## What are the top dog breeds for guard dogs? 

# In[51]:


df_guard = df[df["Guard or Trained"] == "Yes"]


# In[52]:


df_guard["Primary Breed"].value_counts()


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[53]:


df["year"] = df["Animal Birth"].apply(lambda birth: birth.year)
df.head()


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[54]:


df["age"] = pd.datetime.now().year - df["year"]


# In[55]:


df.age.mean().round(2)


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[56]:


df_neighborhoods = pd.read_csv("zipcodes-neighborhoods.csv")
df_neighborhoods


# In[57]:


df = df.merge(df_neighborhoods, left_on='Owner Zip Code', right_on='zip')


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[58]:


df[df['borough'] == "Bronx"]["Animal Name"].value_counts().head(1)


# In[59]:


df[df['borough'] == "Brooklyn"]["Animal Name"].value_counts().head(1)


# In[60]:


df[df['neighborhood'] == "Upper East Side"]["Animal Name"].value_counts().head(1)


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[61]:


df_new = pd.DataFrame(df.groupby('neighborhood')['Primary Breed'].value_counts().groupby(level=0).nlargest(1))
df_new


# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[62]:


df.groupby(by="Animal Gender")["Spayed or Neut"].value_counts(normalize=True)


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[63]:


df['monochrome'] = np.where((df["Animal Dominant Color"].str.upper() == "BLACK") | (df["Animal Dominant Color"].str.upper() == "WHITE") | (df["Animal Dominant Color"].str.upper() == "GREY") | (df["Animal Dominant Color"].str.upper() == "GRAY"), True, False)

df['monochrome'].value_counts()


# ## How many dogs are in each borough? Plot it in a graph.

# In[64]:


df_number_borough = pd.DataFrame(df['borough'].value_counts(ascending=True))
df_number_borough


# In[65]:


df_number_borough


# In[66]:


df_number_borough.plot(kind='barh')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[67]:


df_boro_pop = pd.read_csv("boro_population.csv")
df_boro_pop


# In[68]:


df_number_borough.merge(df_boro_pop, left_index=True, right_on='borough')
df_number_borough


# In[69]:


df_number_borough["dogs_per_cap"] = df_number_borough["borough_x"] / df_number_borough["population"]
df_number_borough.sort_values("dogs_per_cap", ascending=False).head(1)


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[ ]:





# ## What percentage of dogs are not guard dogs?

# In[ ]:


df["Guard or Trained"].value_counts(normalize=True)

