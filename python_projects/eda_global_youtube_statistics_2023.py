# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 09:44:38 2023

@author: shass
"""


### 1. Import packages, dataset & set df parameters

# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Import csv dataset & convert to pandas dataframe (df)
df = pd.read_csv(r'C:\Users\shass\my_github\my_practice_repository\datasets\global_youtube_statistics_2023.csv')
df

# Set the display.max_columns option to None to display all columns of the df
pd.set_option('display.max_columns', None)


### 2. Initial data exploration

# Display concise info about the df
df.info()

# Review the top 10 rows of the df
df.head(10)

# Review descriptive statistics of the df of numerical datatypes
df.describe()


### 3. Data cleaning & transformation

## Column review

# Review columns names for naming convention consistency & if all are required
print(df.columns)

# Replace '_' with ' ' and capitalize the first letter of each word in column name
df.columns = df.columns.str.replace('_', ' ').str.title()
print(df.columns)

# Rank column dropped as not required
df = df.drop(columns = 'Rank')

# Confirm that 'Rank' has been dropped
print(df.columns)


## Duplicate review

# Duplicate check using the duplicated() method to mark duplicate rows
duplicates = df.duplicated()

# Filter the df using the boolean series to examine the duplicates
duplicate_rows = df[duplicates]

# No duplicate rows exist in the df
print(duplicate_rows)


## Missing value review

# Count the number of missing values in the df
missing_values_count = df.isnull().sum()

# Display the count of missing values for incomplete columns
missing_values_count[missing_values_count > 0]

# Select object datatype columns from df
categorical_columns = df.select_dtypes(include = ['object']).columns

# Replace object datatype column missing values with 'Unknown'
df[categorical_columns] = df[categorical_columns].fillna('Unknown')

# Select numerical datatype columns from df
numerical_columns = df.select_dtypes(include = ['float', 'int64']).columns

# Exclude 'Latitude' & 'Longitude' columns from selection
numerical_columns = numerical_columns.difference(['Latitude', 'Longitude'])

# Replace numerical datatype column missing values with 'Unknown'
df[numerical_columns] = df[numerical_columns].fillna(0)

# Recalculate the number of missing values in the df
missing_values_count = df.isnull().sum()

# Valiate only 'Latitude' & 'Longitude' have missing values
missing_values_count[missing_values_count > 0]


## Datatype review

# Display concise info about the df
df.info()

# Convert several float data typescolumns to integars
df = df.astype({
    'Video Views': 'int64',
    'Video Views Rank': 'int64',
    'Country Rank': 'int64',
    'Channel Type Rank': 'int64',
    'Video Views For The Last 30 Days': 'int64',
    'Subscribers For Last 30 Days': 'int64',
    'Created Year': 'int64',
    'Population': 'int64',
    'Urban Population': 'int64'
})

# Validate results of datatype change
df.info()


## Remove & replace unwanted characters

# Define remove & replace logic as replacing any non-alphanumeric characters
pattern = r'[^a-zA-Z0-9\s.,!?&\'-]'

# Replace characters 'Youtuber' & 'Title' with an empty string
df['Youtuber'] = df['Youtuber'].str.replace(pattern, '')
df['Title'] = df['Title'].str.replace(pattern, '')

# Remove any trailing/ leading whitespace
df['Youtuber'] = df['Youtuber'].str.strip()
df['Title'] = df['Title'].str.strip()

# Create filtered views of df to validate remove & replace
filter_youtuber_rows = df['Youtuber'].str.contains(pattern, regex = True)
filter_title_rows = df['Title'].str.contains(pattern, regex = True)

# Validate results of string remove & replace
filter_youtuber_rows_results = filter_youtuber_rows[filter_youtuber_rows == True]
print(filter_youtuber_rows_results)

filter_title_rows_results = filter_title_rows[filter_title_rows == True]
print(filter_title_rows_results)


## Removing unwanted rows

# Remove rows from with 0 'Video Views' as these are Topics not valid channels
for x in df.index:
    if df.loc[x, 'Video Views'] == 0:
        df.drop(x, inplace = True)
       
# Validate the results        
filtered_df = df[df['Video Views'] == 0]
filtered_df

# For analysis purposes only 'Youtubers' with valid names are being included
# Remove rows from with blank 'Youtuber' as these are channels with only special characters
for x in df.index:
    if df.loc[x, 'Youtuber'] == '':
        df.drop(x, inplace = True)

# Validate the results
filtered_df = df[df['Youtuber'] == '']
filtered_df


## Sorting the df

# Sort values by number of 'Subscribers' descending from highest to lowest
df.sort_values(by = 'Subscribers', ascending = False)
df

## Resetting the index

# Resetting the index due to rows which have been dropped from the df
df = df.reset_index(drop = True)
df


### 4. Summary statistics        

# Generate summary statistics for numerical columns, rounded to 0 decimal places
numerical_summary = df.describe().round().astype(int)
print(numerical_summary)
    
# Generate summary statistics for object columns
object_summary = df[categorical_columns].describe(include = ['object'])
print(object_summary)

### 5. Data output

# Output the DataFrame to a CSV file
df.to_csv(r'C:\Users\shass\my_github\my_practice_repository\datasets\global_youtube_statistics_2023_cleaned_py.csv', 
          index = False)
        
### 6. Data visualisation                  

# Apply plot style 'seaborn' for visualisations                  
plt.style.use('seaborn')

## Correlation matrix heatmap

# Adjust the default figure size for matplotlib plots
plt.rcParams['figure.figsize'] = (16, 12)

# Generate correlation matrix heatmap
sns.heatmap(df.corr(), annot = True)

## What are the top 10 YouTube channels by no. subscribers?

# Select columns to show in output
selected_columns = ['Youtuber', 'Subscribers']

# Filter df for top 10 most subscribed YouTube channels 
top_10_channels = df.loc[0:9, selected_columns]

# Validate filtered df output
print(top_10_channels)

# Sort values so that highest output is descending
top_10_channels_desc = top_10_channels.sort_values(by = 'Subscribers', ascending = True)

# Reflect 'Subscriber' in millions
top_10_channels['Subscribers (mn.)'] = (top_10_channels['Subscribers'] / 1000000).astype(int)
top_10_channels_desc['Subscribers (mn.)'] = (top_10_channels_desc['Subscribers'] / 1000000).astype(int)

top_10_channels_desc = top_10_channels_desc[['Youtuber', 'Subscribers (mn.)']]

# Validate sorted output
print(top_10_channels_desc)

# Plot df as a horizontal bar chart
top_10_channels_desc.plot.barh(x = 'Youtuber', y = 'Subscribers (mn.)', stacked = True, color = '#FF0000', width = 0.75)

# Adjust chart formatting 
plt.title('Top 10 YouTube Channels by No. Subscribers (2023)', fontsize = 25, weight = 'bold')
plt.xlabel('No. Subscribers (mn.)', fontsize = 16,  weight = 'bold')
plt.ylabel('YouTube Channel', fontsize = 15, weight = 'bold')
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.tight_layout()


## Which are the top 10 channel categories by no. YouTube channels?

# Calculate the number of YouTube channels in each category
category_counts_asc = df['Category'].value_counts(ascending = True)
print(category_counts_asc)

# Select the top 10 categories based on the number of YouTuber channels
top_10_categories_asc = category_counts_asc.tail(10)
print(top_10_categories_asc)

# Plot df as a horizontal bar chart
top_10_categories_asc.plot.barh(x = 'No. YouTube Channels', y = 'Category', stacked = True, color = '#FF0000', width = 0.75)

# Adjust chart formatting 
plt.title('Top 10 YouTube Channels Categories (2023)', fontsize = 25, weight = 'bold')
plt.xlabel('No. YouTube Channels', fontsize = 16,  weight = 'bold')
plt.ylabel('Channel Category', fontsize = 16, weight = 'bold')
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.tight_layout()

## Which countries have the highest number of YouTubers?

# Calculate the number of YouTuber channels in each country
country_counts_asc = df['Country'].value_counts(ascending = True)
print(country_counts_asc)

# Select the top 10 countries based on the number of YouTube channels
top_10_countries = country_counts_asc.tail(10)
print(top_10_countries)

# Data for the top 10 categories and the sum of the remaining categories
data = top_10_countries.tolist()
data += [country_counts_asc[:-10].sum()]

# Labels for the top 10 categories and 'Others' for the remaining categories
labels = top_10_countries.index.tolist() + ['Others']
         
# Set colour palette for the top 10 categories & a seperate colour for 'Others'
colors = sns.color_palette("pastel", 10)

# Gray color for 'Others'
colors += [(0.8, 0.8, 0.8)]  

# create a pie chart using Matplotlib with adjusted start angle and larger font size
wedges, texts, autotexts = plt.pie(data, labels = labels, autopct = '%1.0f%%', colors = colors, startangle = 150, textprops = {'fontsize': 15})

# equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')

# increase the font size of the pie chart labels and percentage values
for text in texts:
    text.set_fontsize(15)
for autotext in autotexts:
    autotext.set_fontsize(15)

# Adjust chart formatting 
plt.title('% Distribution of YouTube Channels by Country (2023)', fontsize = 25, weight = 'bold')
plt.tight_layout()


## Is there a correlation between the number of subscribers and the number of views?

# Create new variable for expressing values in millions
df_mns = df

# Reflect 'Subscriber' & 'Video Views' in millions
df_mns['Subscribers (mn.)'] = (df_mns['Subscribers'] / 1000000).astype(int)
df_mns['Video Views (bn.)'] = (df_mns['Video Views'] / 1000000000).astype(int)

# Create new df for scatter plot
df_sub_pop = df_mns[['Subscribers (mn.)', 'Video Views (bn.)']]
df_sub_pop

# Create linear regression for trend line
m, b = np.polyfit(df_sub_pop['Subscribers (mn.)'], df_sub_pop['Video Views (bn.)'], 1)

# Set figuresize
plt.figure(figsize=(16, 12))

# Plot df as a scatter
plt.scatter(df_sub_pop['Subscribers (mn.)'], df_sub_pop['Video Views (bn.)'], color='#FF0000', alpha=0.6)

# Plot trendline
plt.plot(df_sub_pop['Subscribers (mn.)'], m * df['Subscribers (mn.)'] + b, color='#FF0000')

# Adjust chart formatting 
plt.title('Correlation Between Subscribers & Video Views (2023)', fontsize = 25, weight = 'bold')
plt.xlabel('Number of Subscribers', fontsize = 16,  weight = 'bold')
plt.ylabel('Number of Video Views', fontsize = 16,  weight = 'bold')
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid(True, which = 'both', linestyle = '--', linewidth = 0.5)
plt.show()

"""
np.polyfit(): This is a function from the numpy library. It's used to fit a polynomial (of a specified degree) 
# to a set of data points using a least-squares approach. The result is the coefficients of the polynomial.

Inputs:

df['Subscribers']: This is the x-values (or independent variable) of the data points you're trying to fit a polynomial to.
df['Video_Views']: This is the y-values (or dependent variable) of the data points.
1: This is the degree of the polynomial. In this case, it's 1, which means we're fitting a linear polynomial 
# (i.e., a straight line) to the data points. 
# This line is represented by the equation y = mx + b, where m is the slope and b is the y-intercept.

Outputs:
m: This is the slope of the fitted line.
b: This is the y-intercept of the fitted line. In other words, it's the value of y when x is 0.
In essence, this line of code is using a linear regression to find the best-fitting straight line 
# (in a least-squares sense) that describes the relationship between 'Subscribers' and 'Video_Views' in the given dataset. 
# The resulting line is represented by the equation y = mx + b.

"""




## Is there a correlation between the number of subscribers and the number of videos?

## Are certain categories more correlated with high view or subscriber counts?

## What is the average view-to-subscriber ratio across different categories?

## Which categories have the most engaged audiences, as measured by views per subscriber?

## What are the most common words in high-view channel descriptions?

## Which categories are potentially the most lucrative, based on views and subscriber counts?

## Is there a correlation between the number of views and estimated revenue?

 








