# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 10:46:42 2023

@author: shass
"""

"""
DataCamp - Python Data Science Toolbox (Part 1)
"""

### Return a dictionary with counts of occurrences as value for each key

# # Define count_entries()
# def count_entries(df, *args):
#     """Return a dictionary with counts of occurrences as value for each key."""
    
#     #Initialize an empty dictionary: cols_count
#     cols_count = {}
    
#     # Iterate over column names in args
#     for col_name in args:
    
#         # Extract column from DataFrame: col
#         col = df[col_name]
    
#         # Iterate over the column in DataFrame
#         for entry in col:
    
#             # If entry is in cols_count, add 1
#             if entry in cols_count.keys():
#                 cols_count[entry] += 1
    
#             # Else add the entry to cols_count, set the value to 1
#             else:
#                 cols_count[entry] = 1

#     # Return the cols_count dictionary
#     return cols_count

# # Call count_entries(): result1
# result1 = count_entries(tweets_df, 'lang')

# # Call count_entries(): result2
# result2 = count_entries(tweets_df, 'lang', 'source')

# # Print result1 and result2
# print(result1)
# print(result2)


# """
# DataCamp - Python Data Science Toolbox (Part 1)
# """

# ### Create list from filter object

# # Select retweets from the Twitter DataFrame: result
# result = filter(lambda x: x[0:2] == 'RT', tweets_df['text'])

# # Create list from filter object result: res_list
# res_list = list(result)

# # Print all retweets in res_list
# for tweet in res_list:
#     print(tweet)
    
    
    
    
"""
DataCamp - Python Data Science Toolbox (Part 2)
"""

### List comprehension

## List example

nums = [12, 8, 21, 3, 16]
new_nums = [num + 1 for num in nums]
print(new_nums)

## Range example

result = [num for num in range(11)]
print(result)
































