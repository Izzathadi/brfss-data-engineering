# src/visualization/utils.py

import numpy as np
import pandas as pd
from scipy import stats
from .config import AGE_DESCRIPTIONS

def calculate_bmi_statistics(bmi_data):
    """
    Calculate comprehensive statistics for BMI data.
    
    Args:
        bmi_data (pd.Series): BMI values
        
    Returns:
        dict: Dictionary containing various statistics
    """
    clean_data = bmi_data.dropna()
    
    if len(clean_data) == 0:
        return {}
    
    return {
        'mean': np.mean(clean_data),
        'std': np.std(clean_data),
        'skewness': stats.skew(clean_data),
        'kurtosis': stats.kurtosis(clean_data),
        'min': np.min(clean_data),
        'max': np.max(clean_data),
        'count': len(clean_data)
    }

def format_age_labels(age_counts):
    """
    Format age category labels with descriptions.
    
    Args:
        age_counts (pd.Series): Value counts of age categories
        
    Returns:
        tuple: (labels, values) formatted for plotting
    """
    # Sort by age category (ascending)
    sorted_counts = age_counts.sort_index()
    
    labels = []
    values = []
    
    for age_cat, count in sorted_counts.items():
        description = AGE_DESCRIPTIONS.get(age_cat, f"Age Category {age_cat}")
        labels.append(description)
        values.append(count)
    
    return labels, values

def create_feature_description_table(feature_descriptions):
    """
    Create a formatted table for feature descriptions.
    
    Args:
        feature_descriptions (dict): Dictionary mapping features to descriptions
        
    Returns:
        list: List of HTML table rows
    """
    rows = []
    
    for feature, description in feature_descriptions.items():
        rows.append([feature, description])
    
    return rows

def format_correlation_values(corr_matrix):
    """
    Format correlation matrix values to show maximum 6 decimal places.
    
    Args:
        corr_matrix (pd.DataFrame): Correlation matrix
        
    Returns:
        pd.DataFrame: Formatted correlation matrix
    """
    return corr_matrix.round(6)
