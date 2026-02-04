"""
Configuration file for grocery desert analysis
Modify these parameters to customize the analysis
"""

DATA_PATHS = {
    'population': 'data/cc-est2023-alldata.csv',
    'grocery_directory': 'data/merged Data',
    'county_area': 'data/tl_2021_us_county.dbf',
    'county_shapefile': 'data/tl_2018_us_county.shp'
}

ANALYSIS_YEARS = [2019, 2020, 2021, 2022]

CLUSTERING_PARAMS = {
    'n_clusters': 4,
    'random_state': 42,
    'k_range': range(2, 10)
}

AT_RISK_THRESHOLD = {
    'establishment_density': 0.001
}

VISUALIZATION_PARAMS = {
    'figsize_standard': (12, 6),
    'figsize_wide': (14, 6),
    'dpi': 300,
    'style': 'seaborn-v0_8-darkgrid'
}

OUTPUT_PATHS = {
    'results': 'results/',
    'visualizations': 'visualizations/'
}

DEMOGRAPHIC_FEATURES = {
    'race': [
        'White_Alone_PERCENT',
        'Black_Alone_PERCENT',
        'Native_India_Alone_PERCENT',
        'Asian_Alone_PERCENT',
        'Native_Hawaiian_Alone_PERCENT',
        'Hispanic_Alone_PERCENT'
    ],
    'gender': ['MALE_PERCENT', 'FEMALE_PERCENT']
}

TARGET_METRICS = [
    'ESTAB_All_establishments/Area',
    'EMP/Area',
    'PAYANN/Area'
]
