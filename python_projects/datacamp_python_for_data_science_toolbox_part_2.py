# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 14:45:27 2023

@author: shass
"""

# =============================================================================
# DataCamp - Python Data Science Toolbox (Part 2) Case Study
# =============================================================================

# Import packages
import pandas as pd
import numpy as np

# Set the display.max_columns option to None to display all columns of the df
pd.set_option('display.max_columns', None)


# Import excel datasets
df_curr = pd.read_excel(r"C:\Users\shass\my_github\my_practice_repository\datasets\world_bank\world_bank_current_classification_by_income_20230821.xlsx")
df_hist = pd.read_excel(r"C:\Users\shass\my_github\my_practice_repository\datasets\world_bank\world_bank_historical_classification_by_income_20230630.xlsx") 

# Create copies of the df's before any review or changes are made to the originals
df_curr = df_curr.copy()
df_hist = df_hist.copy()

# Review the number of rows & columns of the df
df_curr.shape
df_hist.shape

# Review first 15 rows
df_curr.head(15)
df_hist.head(15)

# Display concise info about the df's
df_curr.info
df_hist.info

# Provide descriptive statistics for numerical values in the df's
df_curr.describe
df_hist.describe


