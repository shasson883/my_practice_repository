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
from wordcloud import WordCloud
import folium


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

# Create new columns to support visualisation
df_mns['Subscribers (mn.)'] = (df_mns['Subscribers'] / 1000000).astype(int)
df_mns['Video Views (bn.)'] = (df_mns['Video Views'] / 1000000000).astype(int)
df_mns['Uploads (k.)'] = (df_mns['Uploads'] / 1000)

# Create new df for scatter plot
df_sub_pop = df_mns[['Subscribers (mn.)', 'Video Views (bn.)']]
df_sub_pop

# Calculate the correlation coefficient
correlation = df_sub_pop['Subscribers (mn.)'].corr(df_sub_pop['Video Views (bn.)'])

# Create linear regression for trend line
m, b = np.polyfit(df_sub_pop['Subscribers (mn.)'], df_sub_pop['Video Views (bn.)'], 1)

# Set scaling factor of circle size
scaling_factor = 4

# Calculate the size of circles 
sizes = df_sub_pop['Subscribers (mn.)'] * scaling_factor

# Set figuresize
plt.figure(figsize=(16, 12))

# Plot df as a scatter
plt.scatter(df_sub_pop['Subscribers (mn.)'], df_sub_pop['Video Views (bn.)'], s = sizes, color = '#FF0000', alpha=0.6)

# Plot trendline
plt.plot(df_sub_pop['Subscribers (mn.)'], m * df_sub_pop['Subscribers (mn.)'] + b, color='#FF0000')

# Adjust chart formatting 
plt.title('Correlation Between No. Subscribers & No. Video Views (2023)', fontsize = 25, weight = 'bold')
plt.xlabel('No. Subscribers (mn.)', fontsize = 16,  weight = 'bold')
plt.ylabel('No. Video Views (mn.)', fontsize = 16,  weight = 'bold')
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid(True, which = 'both', linestyle = '--', linewidth = 0.5)

plt.annotate(f'Correlation: {correlation:.2f}', 
             xy = (0.85, 0.025), 
             xycoords = 'axes fraction', 
             fontsize = 15, 
             weight = 'bold')

plt.show()

# Strong positive correlation

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

# Create new variable for expressing values in millions
df_mns = df

# Create new df for scatter plot
df_sub_pop_2 = df_mns[['Subscribers (mn.)', 'Uploads (k.)']]
df_sub_pop_2

# Calculate the correlation coefficient
correlation = df_sub_pop_2['Subscribers (mn.)'].corr(df_sub_pop_2['Uploads (k.)'])

# Create linear regression for trend line
m, b = np.polyfit(df_sub_pop_2['Subscribers (mn.)'], df_sub_pop_2['Uploads (k.)'], 1)

# Set scaling factor of circle size
scaling_factor = 4 

# Calculate the size of circles 
sizes = df_sub_pop_2['Subscribers (mn.)'] * scaling_factor

# Set figuresize
plt.figure(figsize = (16, 12))

# Plot df as a scatter
plt.scatter(df_sub_pop_2['Subscribers (mn.)'], df_sub_pop_2['Uploads (k.)'], s = sizes, color = '#FF0000', alpha = 0.6)

# Plot trendline
plt.plot(df_sub_pop_2['Subscribers (mn.)'], m * df_sub_pop_2['Subscribers (mn.)'] + b, color = '#FF0000')

# Adjust chart formatting 
plt.title('Correlation Between No. Subscribers & No. Video Uploads (2023)', fontsize = 25, weight = 'bold')
plt.xlabel('No. Subscribers (mn.)', fontsize = 16, weight = 'bold')
plt.ylabel('No. Video Uploads (k.)', fontsize = 16, weight = 'bold')
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid(True, which = 'both', linestyle = '--', linewidth = 0.5)

plt.annotate(f'Correlation: {correlation:.2f}', 
             xy = (0.85, 0.025), 
             xycoords = 'axes fraction', 
             fontsize = 15, 
             weight = 'bold')

plt.show()

# Weak positive correlation



## Are certain categories more correlated with high view or subscriber counts?

# Create new df to group by category & aggregate columns
category_sum = df.groupby('Category').agg({
    'Subscribers (mn.)': 'sum',
    'Video Views (bn.)': 'sum'
}).reset_index()

# Validate results of new df
print(category_sum)

# Sort categories by no. Subscribers (mn.)
category_sum_subs = category_sum.sort_values(by = 'Subscribers (mn.)', ascending = False)
category_sum_subs

# Sort categories by no. Video Views (bn.)
category_sum_views = category_sum.sort_values(by = 'Video Views (bn.)', ascending = False)
category_sum_views

# Plot df as a bar chart
ax = category_sum_subs.plot(kind = 'bar', stacked = True, x = 'Category', y = 'Subscribers (mn.)', color = '#FF0000')

# Add data labels above the bars
for bar in ax.containers:
    ax.bar_label(bar, label_type='edge', color='black', fontsize = 15, padding = 5)

# Adjusting the chart formatting
plt.title('No. Subscribers by Channel Category (2023)', fontsize = 25, weight = 'bold')
plt.xlabel('Channel Category', fontsize = 16,  weight = 'bold')
plt.ylabel('Subscribers (mn.)', fontsize = 16, weight = 'bold')
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.tight_layout()

# Create new df for bar chart, Category vs Video Views (bn.)

# Plot df as a bar chart
ax = category_sum_views.plot(kind = 'bar', stacked = True, x = 'Category', y = 'Video Views (bn.)', color = '#FF0000')

# Add data labels above the bars
for bar in ax.containers:
    ax.bar_label(bar, label_type='edge', color='black', fontsize = 15, padding = 5)

# Adjusting the chart formatting
plt.title('No. Video Views by Channel Category (2023)', fontsize = 25, weight = 'bold')
plt.xlabel('Channel Category', fontsize = 16,  weight = 'bold')
plt.ylabel('Video Views (bn.)', fontsize = 16, weight = 'bold')
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.tight_layout()



## What is the average view-to-subscriber ratio across different categories?
## Which categories have the most engaged audiences, as measured by views per subscriber?

# Create new dataframe using raw values
category_sum_raw = df.groupby('Category').agg({
    'Subscribers': 'sum',
    'Video Views': 'sum'
}).reset_index()

# Create new variable to calculate the 'Subscriber to View Ratio'
category_sum_raw['View-to-Subscriber Ratio'] = category_sum_raw['Video Views'] / category_sum_raw['Subscribers']
category_sum_raw['View-to-Subscriber Ratio'] = category_sum_raw['View-to-Subscriber Ratio'].astype(float)

# Sort df by 'Subscriber to View Ratio' descending
category_sum_raw = category_sum_raw.sort_values(by = 'View-to-Subscriber Ratio', ascending = False)

# Plot df as a bar chart
ax = category_sum_raw.plot(kind = 'bar', stacked = True, x = 'Category', y = 'View-to-Subscriber Ratio', color = '#FF0000')

# Add data labels above the bars
for bar in ax.containers:
    ax.bar_label(bar, label_type='edge', labels=[f'{int(val)}' for val in bar.datavalues], color='black', fontsize=15, padding=5)

# Adjusting the chart formatting
plt.title('Avg. View-to-Subscriber Ratio by Channel Category (2023)', fontsize = 25, weight = 'bold')
plt.xlabel('Channel Category', fontsize = 16,  weight = 'bold')
plt.ylabel('Avg. View-to-Subscriber Ratio', fontsize = 16, weight = 'bold')
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.tight_layout()

"""
Explained - the 'View-to-Subscriber Ratio' show indicates on avg. how many views are correlated per additional Subscriber
e.g. for every additional subscriber gained on a Pets & Animals category you can expect to get on average 619 additional views
across videos

"""


## What are the most common words in high-view channel descriptions?

# Determine the 75th percentile of video views
percentile_75th = df['Video Views'].quantile(0.75)

# Filter channels with views above the 75th percentile
high_view_channels = df[df['Video Views'] > percentile_75th]

# Combine the names of high-view channels into a single string
text = ' '.join(high_view_channels['Youtuber'])

# Create the word cloud
wordcloud = WordCloud(background_color = 'white', width = 800, height = 400).generate(text)

# Plot the word cloud
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')
plt.title('Word Cloud of High-View YouTube Channel Descriptions', fontsize = 25, weight = 'bold')
plt.show()



## Which categories are potentially the most lucrative based on avg. monthly earnings

# Calculate avg. monthly averages per category rounded to 0 decimal places
df['Avg. Monthly Earnings'] = (df['Lowest Monthly Earnings'] + df['Highest Monthly Earnings']) / 2

# Create new df to group by category & calculate mean avg. monthly earnings by category
category_avg_earnings = df.groupby('Category').agg({
    'Avg. Monthly Earnings': 'mean',
    }).reset_index()

# Create new column to reflect avg. monthly earnings in thousands, rounded down to nearest whole number 
category_avg_earnings['Avg. Monthly Earnings ($000s)'] = (category_avg_earnings['Avg. Monthly Earnings'] / 1000).astype(int)
category_avg_earnings

# Sort categories by no. Subscribers (mn.)
category_avg_earnings = category_avg_earnings.sort_values(by = 'Avg. Monthly Earnings ($000s)', ascending = False)

# Plot df as a bar chart
ax = category_avg_earnings.plot(kind = 'bar', stacked = True, x = 'Category', y = 'Avg. Monthly Earnings ($000s)', color = '#FF0000')

# Add data labels above the bars
for bar in ax.containers:
    ax.bar_label(bar, label_type = 'edge', color = 'black', fontsize = 15, padding = 5)

# Adjusting the chart formatting
plt.title('Avg. Monthly Earnings by Channel Category (2023)', fontsize = 25, weight = 'bold')
plt.xlabel('Channel Category', fontsize = 16,  weight = 'bold')
plt.ylabel('Avg. Monthly Earnings ($000s)', fontsize = 16, weight = 'bold')
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.tight_layout()



## Is there a correlation between the number of views and estimated revenue?

df_sub_pop_4 = df[['Video Views', 'Avg. Monthly Earnings']].copy()

df_sub_pop_4['Video Views (bn.)'] = df_sub_pop_4['Video Views'] / 1000000000
df_sub_pop_4['Avg. Monthly Earnings ($000s)'] = df_sub_pop_4['Avg. Monthly Earnings'] / 1000


# Calculate the correlation coefficient
correlation = df_sub_pop_4['Video Views (bn.)'].corr(df_sub_pop_4['Avg. Monthly Earnings ($000s)'])

# Create linear regression for trend line
m, b = np.polyfit(df_sub_pop_4['Video Views (bn.)'], df_sub_pop_4['Avg. Monthly Earnings ($000s)'], 1)

# Sort data by 'Video Views (bn.)'
df_sub_pop_4 = df_sub_pop_4.sort_values(by='Video Views (bn.)')

# Set scaling factor of circle size
scaling_factor = 4 

# Set figuresize
plt.figure(figsize = (16, 12))

# Calculate the size of circles 
sizes = df_sub_pop_4['Video Views (bn.)'] * scaling_factor

# Plot df as a scatter
plt.scatter(df_sub_pop_4['Video Views (bn.)'], df_sub_pop_4['Avg. Monthly Earnings ($000s)'], color = '#FF0000', alpha = 0.6)

# Plot trendline
plt.plot(df_sub_pop_4['Video Views (bn.)'], m * df_sub_pop_4['Video Views (bn.)'] + b, color = '#FF0000')

# Adjust chart formatting 
plt.title('Correlation Between Video Views & Avg. Monthly Earnings (2023)', fontsize = 25, weight = 'bold')
plt.xlabel('Video Views (bn.)', fontsize = 16, weight = 'bold')
plt.ylabel('Avg. Monthly Earnings ($000s)', fontsize = 16, weight = 'bold')
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid(True, which = 'both', linestyle = '--', linewidth = 0.5)

plt.annotate(f'Correlation: {correlation:.2f}', 
             xy = (0.85, 0.025), 
             xycoords = 'axes fraction', 
             fontsize = 15, 
             weight = 'bold')

plt.show()

# Moderate positive correlation
 
"""

## Geographic map

# Calculate the number of YouTuber channels in each country
country_counts = df['Country'].value_counts()

# Convert the series to a df
country_counts = country_counts.reset_index()

# Create column headers
country_counts.columns = ['Country', 'Youtuber Count']

# Validate new df
country_counts

world_map = folium.Map(location = [20,0], tiles = "cartodbpositron", zoom_start = 2)

world_map.choropleth(
    geo_data = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json',
    name = 'choropleth',
    data = country_counts,
    columns = ['Country', 'Youtuber Count'],
    key_on = 'feature.properties.name',
    fill_color = 'YlOrRd', 
    fill_opacity = 0.7, 
    line_opacity = 0.2,
    legend_name = 'Country Counts'
)

folium.LayerControl().add_to(world_map)

world_map.save('world_map.html')

world_map

"""


"""
df_country = df.groupby('Country').agg({
    'Youtuber': 'sum',
    'Subscribers': 'sum',
    'Video Views': 'sum',
}).reset_index()
"""










