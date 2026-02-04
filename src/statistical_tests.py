"""
Statistical hypothesis testing for demographic and economic relationships
"""

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, f_oneway, pearsonr
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def calculate_correlations(data, target_col, feature_cols):
    """
    Calculate Pearson correlations between target and multiple features
    """
    correlation_results = []
    
    for col in feature_cols:
        valid_data = data[[target_col, col]].dropna()
        
        if len(valid_data) > 0:
            correlation = valid_data[target_col].corr(valid_data[col])
            correlation_results.append({
                'Feature': col, 
                'Correlation': correlation
            })
    
    df_correlations = pd.DataFrame(correlation_results)
    df_correlations = df_correlations.sort_values(by='Correlation', ascending=False)
    
    return df_correlations


def plot_correlation_bar_chart(correlation_df, target_col, save_path=None):
    """
    Create bar chart of correlation coefficients
    """
    plt.figure(figsize=(14, 6))
    plt.bar(correlation_df['Feature'], correlation_df['Correlation'], color='lightgreen')
    plt.xlabel('Features', fontsize=12)
    plt.ylabel('Correlation Coefficient', fontsize=12)
    plt.title(f'Correlation with {target_col}', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def t_test_at_risk_vs_safe(data, group_col, metric_col):
    """
    Perform independent t-test between at-risk and safe counties
    """
    at_risk = data[data[group_col] == True][metric_col].dropna()
    safe = data[data[group_col] == False][metric_col].dropna()
    
    t_stat, p_value = ttest_ind(at_risk, safe, equal_var=False)
    
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'at_risk_mean': at_risk.mean(),
        'safe_mean': safe.mean(),
        'at_risk_n': len(at_risk),
        'safe_n': len(safe)
    }


def anova_test_across_groups(data, group_col, metric_col):
    """
    Perform one-way ANOVA to test for differences across groups
    """
    groups = [
        data[data[group_col] == group][metric_col].dropna()
        for group in data[group_col].unique()
    ]
    
    groups = [g for g in groups if len(g) > 0]
    
    f_stat, p_value = f_oneway(*groups)
    
    return {
        'f_statistic': f_stat,
        'p_value': p_value,
        'n_groups': len(groups)
    }


def calculate_temporal_change_correlation(data, pop_col='TOT_POP', target_col=None, 
                                         start_year=2019, end_year=2022):
    """
    Calculate correlation between population change and target metric change
    """
    change_data = []
    
    for (state, county), group in data.groupby(['STATE', 'COUNTY']):
        pop_start = group.loc[group['YEAR'] == start_year, pop_col].values
        pop_end = group.loc[group['YEAR'] == end_year, pop_col].values
        target_start = group.loc[group['YEAR'] == start_year, target_col].values
        target_end = group.loc[group['YEAR'] == end_year, target_col].values
        
        if len(pop_start) == 0 or len(pop_end) == 0 or len(target_start) == 0 or len(target_end) == 0:
            continue
        
        pop_change = (pop_end[0] - pop_start[0]) / pop_start[0] if pop_start[0] != 0 else np.nan
        target_change = (target_end[0] - target_start[0]) / target_start[0] if target_start[0] != 0 else np.nan
        
        change_data.append({
            'STATE': state,
            'COUNTY': county,
            'POP_PCT_CHANGE': pop_change,
            'TARGET_PCT_CHANGE': target_change
        })
    
    df_changes = pd.DataFrame(change_data).dropna()
    df_changes = df_changes.replace([np.inf, -np.inf], np.nan).dropna()
    
    if len(df_changes) > 0:
        correlation = df_changes['POP_PCT_CHANGE'].corr(df_changes['TARGET_PCT_CHANGE'])
    else:
        correlation = np.nan
    
    return df_changes, correlation


def plot_scatter_with_regression(df_changes, x_col, y_col, x_label, y_label, save_path=None):
    """
    Create scatter plot with regression line
    """
    X = df_changes[x_col].values.reshape(-1, 1)
    y = df_changes[y_col].values.reshape(-1, 1)
    
    reg_model = LinearRegression().fit(X, y)
    slope = reg_model.coef_[0][0]
    intercept = reg_model.intercept_[0]
    r_squared = reg_model.score(X, y)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df_changes[x_col], df_changes[y_col], alpha=0.5, label='Data points')
    plt.plot(df_changes[x_col], reg_model.predict(X), color='red', linewidth=2, label='Regression Line')
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title(f'{y_label} vs {x_label}', fontsize=14)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared
    }


def age_group_correlation_analysis(data, target_col, start_year=2019, end_year=2022):
    """
    Calculate correlations between population change and target metric by age group
    """
    all_age_data = data[data['AGERANGE_LOWER'] != "Total"]
    
    change_data = []
    
    for (state, county, age_lower, age_upper), group in all_age_data.groupby(
        ['STATE', 'COUNTY', 'AGERANGE_LOWER', 'AGERANGE_UPPER']
    ):
        pop_start = group.loc[group['YEAR'] == start_year, 'TOT_POP'].values
        pop_end = group.loc[group['YEAR'] == end_year, 'TOT_POP'].values
        target_start = group.loc[group['YEAR'] == start_year, target_col].values
        target_end = group.loc[group['YEAR'] == end_year, target_col].values
        
        if len(pop_start) == 0 or len(pop_end) == 0 or len(target_start) == 0 or len(target_end) == 0:
            continue
        
        pop_change = pop_end[0] - pop_start[0]
        target_change = target_end[0] - target_start[0]
        
        change_data.append({
            'STATE': state,
            'COUNTY': county,
            'AGERANGE_LOWER': age_lower,
            'AGERANGE_UPPER': age_upper,
            'POP_CHANGE': pop_change,
            'TARGET_CHANGE': target_change
        })
    
    df_changes = pd.DataFrame(change_data)
    
    correlations = []
    
    for _, row in df_changes[['AGERANGE_LOWER', 'AGERANGE_UPPER']].drop_duplicates().iterrows():
        age_lower = row['AGERANGE_LOWER']
        age_upper = row['AGERANGE_UPPER']
        
        df_age = df_changes[
            (df_changes['AGERANGE_LOWER'] == age_lower) & 
            (df_changes['AGERANGE_UPPER'] == age_upper)
        ]
        
        if len(df_age) > 1:
            correlation = df_age['POP_CHANGE'].corr(df_age['TARGET_CHANGE'])
            correlations.append({
                'Age_Range': f'{age_lower}-{age_upper}',
                'Correlation': correlation
            })
    
    return pd.DataFrame(correlations)


def plot_age_correlation_bar_chart(correlation_df, target_col, years, save_path=None):
    """
    Plot correlations by age group
    """
    plt.figure(figsize=(12, 6))
    plt.bar(correlation_df['Age_Range'], correlation_df['Correlation'], color='skyblue')
    plt.xlabel('Age Range', fontsize=12)
    plt.ylabel('Correlation Coefficient', fontsize=12)
    plt.title(
        f'Population Change vs {target_col} Change by Age Group ({years[0]}-{years[1]})',
        fontsize=14
    )
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
