"""
Feature engineering functions for demographic and economic metrics

"""

import pandas as pd
import numpy as np


def calculate_demographic_percentages(data):
    """
    Calculate demographic percentages for race and ethnicity groups
    """
    male_alone_columns = ['White_Alone_MALE', 'Black_Alone_MALE', 'Native_India_Alone_MALE', 
                         'Asian_Alone_MALE', 'Native_Hawaiian_Alone_MALE', 'Hispanic_Alone_MALE']
    
    female_alone_columns = ['White_Alone_FEMALE', 'Black_Alone_FEMALE', 'Native_India_Alone_FEMALE', 
                           'Asian_Alone_FEMALE', 'Native_Hawaiian_Alone_FEMALE', 'Hispanic_Alone_FEMALE']
    
    percentage_columns = []
    
    for col in male_alone_columns + female_alone_columns:
        data[f"{col}_PERCENT"] = (data[col] / data['TOT_POP']) * 100
        percentage_columns.append(f"{col}_PERCENT")
    
    return data, percentage_columns


def calculate_area_normalized_metrics(data):
    """
    Normalize economic metrics by county land area
    """
    area_columns = []
    
    emp_col_index = data.columns.tolist().index('EMP')
    
    for col in data.columns[emp_col_index:-1]:
        if col != 'ALAND':
            data[f"{col}/Area"] = data[col] / data['ALAND']
            area_columns.append(f"{col}/Area")
    
    return data, area_columns


def calculate_gender_percentages(data):
    """
    Calculate male and female percentages of total population
    """
    data['MALE_PERCENT'] = data['TOT_MALE'] / data['TOT_POP']
    data['FEMALE_PERCENT'] = data['TOT_FEMALE'] / data['TOT_POP']
    
    return data


def calculate_combined_race_percentages(data):
    """
    Combine male and female percentages for each race/ethnicity group
    """
    data['White_Alone_PERCENT'] = data['White_Alone_MALE_PERCENT'] + data['White_Alone_FEMALE_PERCENT']
    data['Black_Alone_PERCENT'] = data['Black_Alone_MALE_PERCENT'] + data['Black_Alone_FEMALE_PERCENT']
    data['Native_India_Alone_PERCENT'] = data['Native_India_Alone_MALE_PERCENT'] + data['Native_India_Alone_FEMALE_PERCENT']
    data['Asian_Alone_PERCENT'] = data['Asian_Alone_MALE_PERCENT'] + data['Asian_Alone_FEMALE_PERCENT']
    data['Native_Hawaiian_Alone_PERCENT'] = data['Native_Hawaiian_Alone_MALE_PERCENT'] + data['Native_Hawaiian_Alone_FEMALE_PERCENT']
    data['Hispanic_Alone_PERCENT'] = data['Hispanic_Alone_MALE_PERCENT'] + data['Hispanic_Alone_FEMALE_PERCENT']
    
    return data


def calculate_temporal_changes(data, group_cols, value_col, start_year=2019, end_year=2022):
    """
    Calculate absolute and percentage changes over time
    """
    change_data = []

    for group_vals, group_df in data.groupby(group_cols):
        val_start = group_df.loc[group_df['YEAR'] == start_year, value_col].values
        val_end = group_df.loc[group_df['YEAR'] == end_year, value_col].values

        if len(val_start) == 0 or len(val_end) == 0:
            continue

        val_start = val_start[0]
        val_end = val_end[0]

        absolute_change = val_end - val_start
        
        if val_start != 0:
            pct_change = (absolute_change / val_start) * 100
        else:
            pct_change = np.nan

        result = {col: val for col, val in zip(group_cols, group_vals if isinstance(group_vals, tuple) else [group_vals])}
        result[f'{value_col}_CHANGE'] = absolute_change
        result[f'{value_col}_PCT_CHANGE'] = pct_change
        
        change_data.append(result)

    return pd.DataFrame(change_data)


def create_at_risk_indicator(data, metric_col, threshold):
    """
    Create binary indicator for counties at risk of becoming food deserts
    """
    data['At_Risk'] = data[metric_col] < threshold
    
    return data


def prepare_clustering_features(data, percentage_cols, area_cols):
    """
    Prepare feature matrix for clustering analysis
    """
    filtered_data = data[
        (data['AGERANGE_LOWER'] == 'Total') & 
        (data['AGERANGE_UPPER'] == 'Total')
    ]

    columns_of_interest = ['TOT_POP', 'TOT_MALE', 'TOT_FEMALE'] + percentage_cols + area_cols
    grouped_data = filtered_data.groupby(['STATE', 'COUNTY', 'YEAR'])[columns_of_interest].mean()

    flattened_data = grouped_data.unstack(level=2)
    flattened_data.columns = ['{}_{}'.format(col, year) for col, year in flattened_data.columns]

    return flattened_data
