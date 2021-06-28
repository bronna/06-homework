#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part One: Lots and lots of questions about beer

# ### Do your importing and your setup

# In[36]:


import pandas as pd
import matplotlib.pyplot as plt
import altair as alt


# In[37]:


pd.set_option("display.max_rows", None, "display.max_columns", None)


# ## Read in the file `craftcans.csv`, and look at the first first rows

# In[38]:


df = pd.read_csv("craftcans.csv", na_values=["Does not apply"])


# In[39]:


df.head()


# ## How many rows do you have in the data? What are the column types?

# In[40]:


df.shape


# In[41]:


df.info(verbose=True)


# # Checking out our alcohol

# ## What are the top 10 producers of cans of beer?

# In[42]:


df.Brewery.value_counts().head(10)


# ## What is the most common ABV? (alcohol by volume)

# In[43]:


df.ABV.value_counts().head(1)


# ## Oh, weird, ABV isn't a number. Convert it to a number for me, please.
# 
# It's going to take a few steps!
# 
# ### First, let's just look at the ABV column by itself

# In[44]:


df.ABV


# ### Hm, `%` isn't part of  a number. Let's remove it.
# 
# When you're confident you got it right, save the results back into the `ABV` column.
# 
# - *Tip: In programming the easiest way to remove something is to *replacing it with nothing*.
# - *Tip: "nothing" might seem like `NaN` sinc we talked about it a lot in class, but in this case it isn't! It's just an empty string, like ""*
# - *Tip: `.replace` is used for replacing ENTIRE cells, while `.str.replace` is useful for replacing PARTS of cells (see my New York example)*

# In[45]:


df.ABV = df.ABV.str.replace('%','')


# ### Now let's turn `ABV` into a numeric data type
# 
# Save the results back into the `ABV` column (again), and then check `df.dtypes` to make sure it worked.
# 
# - *Tip: We used `.astype(int)` during class, but this has a decimal in it...*

# In[46]:


df.ABV = df.ABV.astype(float)


# ## What's the ABV of the average beer look like?
# 
# ### Show me in two different ways: one command to show the `median`/`mean`/etc, and secondly show me a chart

# In[47]:


df.ABV.describe()


# In[48]:


plt.figure(figsize=(8,6))
plt.hist(df.ABV, bins=50, alpha=1, label="ABV")
plt.xlabel('ABV',size=16)
plt.ylabel('# types of beer',size=16)
plt.title("What's the ABV of the average beer?",size=18)


# In[49]:


alt.Chart(df).mark_bar().encode(
    alt.X("ABV", bin = alt.BinParams(maxbins = 30)),
    y='count()',
)


# ### We don't have ABV for all of the beers, how many are we missing them from?
# 
# - *Tip: You can use `isnull()` or `notnull()` to see where a column is missing data.*
# - *Tip: You just want to count how many `True`s and `False`s there are.*
# - *Tip: It's a weird trick involving something we usually use to count things in a column*

# In[50]:


df['ABV'].isnull().sum()


# # Looking at location
# 
# Brooklyn used to produce 80% of the country's beer! Let's see if it's still true.

# ## What are the top 10 cities in the US for canned craft beer?

# In[51]:


df['Location'].value_counts().head(10)


# ## List all of the beer from Brooklyn, NY

# In[52]:


df_brooklyn = df[df['Location'] == 'Brooklyn, NY']
df_brooklyn


# ## What brewery in Brooklyn puts out the most cans of beer?

# In[53]:


df_brooklyn['Brewery'].value_counts().head(1)


# ## What are the five most popular styles of beer produced by Sixpoint?

# In[54]:


df[df['Brewery'] == 'Sixpoint Craft Ales'].head(5)


# ## List all of the breweries in New York state.
# 
# - *Tip: We want to match *part* of the `Location` column, but not all of it.*
# - *Tip: Watch out for `NaN` values! You might be close, but you'll need to pass an extra parameter to make it work without an error.*

# In[55]:


df_ny = df[df['Location'].str.contains(', NY', na=False)]
df_ny['Brewery'].value_counts()


# ### Now *count* all of the breweries in New York state

# In[56]:


df_ny['Brewery'].value_counts().count()


# # Measuring International Bitterness Units
# 
# ## Display all of the IPAs
# 
# Include American IPAs, Imperial IPAs, and anything else with "IPA in it."
# 
# IPA stands for [India Pale Ale](https://www.bonappetit.com/story/ipa-beer-styles), and is probably the most popular kind of beer in the US for people who are drinking [craft beer](https://www.craftbeer.com/beer/what-is-craft-beer).

# In[57]:


df_ipa = df[df['Style'].str.contains('IPA', na=False)]
df_ipa['Style'].value_counts()


# IPAs are usually pretty hoppy and bitter. IBU stands for [International Bitterness Unit](http://www.thebrewenthusiast.com/ibus/), and while a lot of places like to brag about having the most bitter beer (it's an American thing!), IBUs don't necessary *mean anything*.
# 
# Let's look at how different beers have different IBU measurements.

# ## Try to get the average IBU measurement across all beers

# In[58]:


df['IBUs'].median()


# ### Oh no, it doesn't work!
# 
# It looks like some of those values *aren't numbers*. There are two ways to fix this:
# 
# 1. Do the `.replace` and `np.nan` thing we did in class. Then convert the column to a number. This is boring.
# 2. When you're reading in your csv, there [is an option called `na_values`](http://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.read_csv.html). You can give it a list of **numbers or strings to count as `NaN`**. It's a lot easier than doing the `np.nan` thing, although you'll need to go add it up top and run all of your cells again.
# 
# - *Tip: Make sure you're giving `na_values` a LIST, not just a string*
# 
# ### Now try to get the average IBUs again

# In[59]:


df['IBUs'].median()


# ## Draw the distribution of IBU measurements, but with *twenty* bins instead of the default of 10
# 
# - *Tip: Every time I ask for a distribution, I'm looking for a histogram*
# - *Tip: Use the `?` to get all of the options for building a histogram*
# - *Tip: Make sure your `matplotlib` thing is set up right!*

# In[60]:


df['IBUs'].hist(bins=20)


# ## Hm, Interesting distribution. List all of the beers with IBUs above the 75th percentile
# 
# - *Tip: There's a single that gives you the 25/50/75th percentile*
# - *Tip: You can just manually type the number when you list those beers*

# In[61]:


df['IBUs'].describe()


# In[62]:


df_high = df[df['IBUs'] > 64]
df_high


# ## List all of the beers with IBUs below the 25th percentile

# In[28]:


df_low = df[df['IBUs'] < 21]
df_low


# ## List the median IBUs of each type of beer. Graph it.
# 
# Put the highest at the top, and the missing ones at the bottom.
# 
# - Tip: Look at the options for `sort_values` to figure out the `NaN` thing. The `?` probably won't help you here.

# In[29]:


df_median = pd.DataFrame(df.groupby("Style")["IBUs"].median())
df_median


# In[30]:


df_median.sort_values(by="IBUs", ascending=True, na_position='first').plot(kind="barh", figsize=(8, 20))


# ## Hmmmm, it looks like they are generally different styles. What are the most common 5 styles of high-IBU beer vs. low-IBU beer?
# 
# - *Tip: You'll want to think about it in three pieces - filtering to only find the specific beers beers, then finding out what the most common styles are, then getting the top 5.*
# - *Tip: You CANNOT do this in one command. It's going to be one command for the high and one for the low.*
# - *Tip: "High IBU" means higher than 75th percentile, "Low IBU" is under 25th percentile*

# In[31]:


df_high.value_counts("Style").head()


# In[32]:


df_low.value_counts("Style").head()


# ## Get the average IBU of "Witbier", "Hefeweizen" and "American Pale Wheat Ale" styles
# 
# I'm counting these as wheat beers. If you see any other wheat beer categories, feel free to include them. I want ONE measurement and ONE graph, not three separate ones. And 20 to 30 bins in the histogram, please.
# 
# - *Tip: I hope that `isin` is in your toolbox*

# In[67]:


df[df['Style'].isin(["Witbier", "Hefeweizen", "American Pale Wheat Ale"])].IBUs.median()


# ## Draw a histogram of the IBUs of those beers

# In[34]:


df[df['Style'].isin(["Witbier", "Hefeweizen", "American Pale Wheat Ale"])].IBUs.hist(bins=25)


# ## Get the average IBU of any style with "IPA" in it (also draw a histogram)

# In[71]:


df[df.Style.str.contains("IPA", na=False)].IBUs.median()


# In[73]:


df[df.Style.str.contains("IPA", na=False)].IBUs.hist(bins=25)


# ## Plot those two histograms on top of one another
# 
# To plot two plots on top of one another, you do two steps.
# 
# 1. First, you make a plot using `plot` or `hist`, and you save it into a variable called `ax`.
# 2. You draw your second graph using `plot` or `hist`, and send `ax=ax` to it as a parameter.
# 
# It would look something like this:
# 
# ```python
# ax = df.plot(....)
# df.plot(ax=ax, ....)
# ``` 
# 
# (...except totally different)

# In[78]:


plt.figure(figsize=(8,6))

plt.hist(df[df['Style'].isin(["Witbier", "Hefeweizen", "American Pale Wheat Ale"])].IBUs, bins=20, alpha=0.5, label="Wheat Beers")
plt.hist(df[df.Style.str.contains("IPA", na=False)].IBUs, bins=30, alpha=0.5, label="IPA Beers")

plt.xlabel('IBUs',size=16)
plt.ylabel('# of beer types',size=16)
plt.title('IBUs of Wheat and IPA Beers',size=18)
plt.legend(loc='upper left')


# ## Compare the ABV of wheat beers vs. IPAs : their IBUs were really different, but how about their alcohol percentage?
# 
# Wheat beers might include witbier, hefeweizen, American Pale Wheat Ale, and anything else you think is wheaty. IPAs probably have "IPA" in their name.

# In[76]:


df[df['Style'].isin(["Witbier", "Hefeweizen", "American Pale Wheat Ale"])].ABV.median()


# In[77]:


df[df.Style.str.contains("IPA", na=False)].ABV.median()


# In[79]:


plt.figure(figsize=(8,6))

plt.hist(df[df['Style'].isin(["Witbier", "Hefeweizen", "American Pale Wheat Ale"])].ABV, bins=20, alpha=0.5, label="Wheat Beers")
plt.hist(df[df.Style.str.contains("IPA", na=False)].ABV, bins=30, alpha=0.5, label="IPA Beers")

plt.xlabel('ABV',size=16)
plt.ylabel('# of beer types',size=16)
plt.title('ABV of Wheat and IPA Beers',size=18)
plt.legend(loc='upper left')


# ## Good work!
# 
# If you made it this far you deserve a drink.

# In[ ]:


get_ipython().getoutput('!!')

