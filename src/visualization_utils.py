"""
Visualization utilities for consistent plotting across the project
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def set_plotting_style():
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12


def save_figure(fig, filename, output_dir='visualizations', dpi=300):
    """
    Save figure with consistent settings
    """
    filepath = f"{output_dir}/{filename}"
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"Saved: {filepath}")


def plot_bar_chart(data, x_col, y_col, title, xlabel, ylabel, 
                   color='steelblue', figsize=(12, 6), rotation=45, save_path=None):
    """
    Create a standardized bar chart
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(data[x_col], data[y_col], color=color, alpha=0.8)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.tick_params(axis='x', rotation=rotation)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax


def plot_scatter_with_trend(x_data, y_data, title, xlabel, ylabel,
                           trend_line=True, figsize=(10, 6), save_path=None):
    """
    Create scatter plot with optional trend line
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.scatter(x_data, y_data, alpha=0.5, s=30, color='steelblue')
    
    if trend_line:
        z = np.polyfit(x_data, y_data, 1)
        p = np.poly1d(z)
        ax.plot(x_data, p(x_data), "r-", linewidth=2, label=f'y={z[0]:.4f}x+{z[1]:.4f}')
        ax.legend()
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax


def plot_heatmap(data, title, figsize=(12, 10), cmap='coolwarm', save_path=None):
    """
    Create a correlation heatmap
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if isinstance(data, pd.DataFrame):
        sns.heatmap(data, annot=False, cmap=cmap, center=0, 
                   square=True, linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
    else:
        sns.heatmap(data, annot=False, cmap=cmap, center=0,
                   square=True, linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax


def plot_time_series(data, time_col, value_cols, title, xlabel, ylabel,
                    figsize=(14, 6), save_path=None):
    """
    Create time series plot for multiple variables
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for col in value_cols:
        ax.plot(data[time_col], data[col], marker='o', linewidth=2, label=col)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.legend(loc='best')
    ax.grid(alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax


def plot_distribution(data, column, title, xlabel, bins=30, 
                     figsize=(10, 6), save_path=None):
    """
    Create histogram with density curve
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.hist(data[column].dropna(), bins=bins, alpha=0.7, color='steelblue', edgecolor='black')
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax


def plot_boxplot_by_group(data, group_col, value_col, title, xlabel, ylabel,
                         figsize=(12, 6), save_path=None):
    """
    Create boxplot grouped by category
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    data.boxplot(column=value_col, by=group_col, ax=ax)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    plt.suptitle('')
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax
