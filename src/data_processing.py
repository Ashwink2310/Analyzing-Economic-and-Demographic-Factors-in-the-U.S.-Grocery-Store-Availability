"""
Data loading and preprocessing functions for grocery desert analysis
"""

import pandas as pd
import numpy as np
from simpledbf import Dbf5
import glob


def load_population_data(filepath):
    """
    Load and preprocess county population data.
    """
    population_data = pd.read_csv(filepath, encoding='latin1')
    
    selected_columns = ['STATE', 'COUNTY', 'STNAME', 'CTYNAME', 'YEAR', 'AGEGRP',
                       'TOT_POP', 'TOT_MALE', 'TOT_FEMALE', 'WA_MALE', 'WA_FEMALE', 
                       'BA_MALE', 'BA_FEMALE', 'IA_MALE', 'IA_FEMALE', 'AA_MALE', 
                       'AA_FEMALE', 'NA_MALE', 'NA_FEMALE', 'H_MALE', 'H_FEMALE']
    
    population_data = population_data[selected_columns]
    
    population_data = population_data[population_data['YEAR'].isin([1, 2, 3, 4])]
    
    year_mapping = {1: 2019, 2: 2020, 3: 2021, 4: 2022}
    population_data['YEAR'] = population_data['YEAR'].map(year_mapping)
    
    age_mapping = {
        0: ('Total', 'Total'),        
        1: (0, 4), 2: (5, 9), 3: (10, 14), 4: (15, 19), 5: (20, 24),
        6: (25, 29), 7: (30, 34), 8: (35, 39), 9: (40, 44), 10: (45, 49),
        11: (50, 54), 12: (55, 59), 13: (60, 64), 14: (65, 69), 15: (70, 74),
        16: (75, 79), 17: (80, 84), 18: (85, None)
    }
    
    population_data[['AGERANGE_LOWER', 'AGERANGE_UPPER']] = population_data['AGEGRP'].apply(
        lambda x: pd.Series(age_mapping[x])
    )
    
    population_data.rename(columns={
        'WA_MALE': 'White_Alone_MALE', 'WA_FEMALE': 'White_Alone_FEMALE',
        'BA_MALE': 'Black_Alone_MALE', 'BA_FEMALE': 'Black_Alone_FEMALE',
        'IA_MALE': 'Native_India_Alone_MALE', 'IA_FEMALE': 'Native_India_Alone_FEMALE',
        'AA_MALE': 'Asian_Alone_MALE', 'AA_FEMALE': 'Asian_Alone_FEMALE',
        'NA_MALE': 'Native_Hawaiian_Alone_MALE', 'NA_FEMALE': 'Native_Hawaiian_Alone_FEMALE',
        'H_MALE': 'Hispanic_Alone_MALE', 'H_FEMALE': 'Hispanic_Alone_FEMALE',
    }, inplace=True)
    
    population_data = population_data[['STATE', 'COUNTY', 'YEAR', 'AGERANGE_LOWER', 'AGERANGE_UPPER',
                                       'TOT_POP', 'TOT_MALE', 'TOT_FEMALE',
                                       'White_Alone_MALE', 'White_Alone_FEMALE',
                                       'Black_Alone_MALE', 'Black_Alone_FEMALE',
                                       'Native_India_Alone_MALE', 'Native_India_Alone_FEMALE',
                                       'Asian_Alone_MALE', 'Asian_Alone_FEMALE',
                                       'Native_Hawaiian_Alone_MALE', 'Native_Hawaiian_Alone_FEMALE',
                                       'Hispanic_Alone_MALE', 'Hispanic_Alone_FEMALE']]
    
    return population_data


def combine_grocery_data_by_year(year, data_directory='merged Data'):
    """
    Combine multiple grocery establishment files for a single year
    """
    
    csv_files = glob.glob(f"{data_directory}/merged_data_{year}_EMPSIZE_*.csv")
    
    common_columns = ['STATE', 'COUNTY', 'YEAR', 'Total_Population', 'MedianFamilyIncome_County',
                      'PovertyRate_County', 'Total_LowIncomeTracts',
                      'Total_LILATracts_1And10', 'Total_LILATracts_halfAnd10',
                      'Total_LILATracts_1And20', 'Total_LILATracts_Vehicle']

    dataframes = []
    column_order = []
    EMP_column = None 
    PAYANN_column = None 

    for i, file in enumerate(csv_files):
        df = pd.read_csv(file)

        df['STATE'] = df['State_County_ID'].astype(str).str[:-3].astype(int)
        df['COUNTY'] = df['State_County_ID'].astype(str).str[-3:].astype(int)
        df.drop(columns=['State_County_ID'], inplace=True)

        df['YEAR'] = df['YEAR'].fillna(year)

        most_common_label = df['EMPSIZES_LABEL'].mode()[0]
        df['EMPSIZES_LABEL'] = df['EMPSIZES_LABEL'].fillna(most_common_label)

        if i == 0:
            EMP_column = df[['EMP']] 
            PAYANN_column = df[['PAYANN']]             

        common_data = df[common_columns]

        emp_size_label = most_common_label.replace(' ', '_')
        rename_dict = {'ESTAB': f'ESTAB_{emp_size_label}'}
        df.rename(columns=rename_dict, inplace=True)

        dataframes.append(df.drop(columns=common_columns))
        column_order.extend(rename_dict.values())

    combined_df = pd.concat([common_data] + dataframes, axis=1)

    if EMP_column is not None:
        combined_df['EMP'] = EMP_column['EMP']
    if PAYANN_column is not None:    
        combined_df['PAYANN'] = PAYANN_column['PAYANN']

    fixed_columns = ['STATE', 'COUNTY', 'YEAR', 'EMP', 'PAYANN']
    column_order = sorted(set(column_order))  
    desired_order = fixed_columns + column_order

    combined_df = combined_df[desired_order]
    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()].fillna(0)

    return combined_df


def load_all_grocery_data(years=[2019, 2020, 2021, 2022], data_directory='merged Data'):
    """
    Load and combine grocery data across multiple years
    """
    all_years_data = []
    
    for year in years:
        year_data = combine_grocery_data_by_year(year, data_directory)
        all_years_data.append(year_data)
    
    grocery_data = pd.concat(all_years_data, ignore_index=True)
    grocery_data.fillna(0, inplace=True)
    
    return grocery_data


def load_county_area_data(shapefile_path='tl_2021_us_county.dbf'):
    """
    Load county land area from TIGER/Line shapefile
    """
    county_area = Dbf5(shapefile_path)
    county_area = county_area.to_dataframe()
    
    county_area.rename(columns={'STATEFP': 'STATE', 'COUNTYFP': 'COUNTY'}, inplace=True)
    county_area['STATE'] = county_area['STATE'].astype(int)
    county_area['COUNTY'] = county_area['COUNTY'].astype(int)
    
    county_area = county_area[['STATE', 'COUNTY', 'ALAND']].sort_values(['STATE', 'COUNTY'])
    county_area['ALAND'] = county_area['ALAND'] / 1_000_000
    
    return county_area


def load_and_merge_data(population_file='cc-est2023-alldata.csv',
                       grocery_years=[2019, 2020, 2021, 2022],
                       grocery_directory='Merged Data',
                       area_file='tl_2021_us_county.dbf'):
    """
    Load all datasets and merge into single analysis-ready dataframe
    """
    population_data = load_population_data(population_file)
    grocery_data = load_all_grocery_data(grocery_years, grocery_directory)
    area_data = load_county_area_data(area_file)
    
    grocery_data = pd.merge(grocery_data, area_data, on=['STATE', 'COUNTY'], how='inner')
    
    final_data = pd.merge(population_data, grocery_data, 
                         on=['STATE', 'COUNTY', 'YEAR'], 
                         how='inner')
    
    return final_data
