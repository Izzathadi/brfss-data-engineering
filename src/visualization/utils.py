# src/visualization/utils.py

import numpy as np
import pandas as pd
from scipy import stats
import os
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

def calculate_data_statistics(df, parquet_path=None):
    """
    Calculate comprehensive statistics for the entire dataset.

    Args:
        df (pd.DataFrame): DataFrame to analyze
        parquet_path (str, optional): Path to the original parquet file

    Returns:
        dict: Dictionary containing various dataset statistics
    """
    stats = {}

    expected_columns = ['Diabetes_01', 'HighBP', 'HighChol', 'BMI', 'Smoker', 'PhysActivity', 'Fruits', 'Veggies', 'DiffWalk', 'Sex', 'Age']
    df = df[expected_columns].reset_index(drop=True)

    stats['total_rows'] = len(df)
    stats['total_columns'] = len(df.columns)
    stats['total_missing'] = df.isnull().sum().sum()
    stats['missing_percentage'] = (stats['total_missing'] / (stats['total_rows'] * stats['total_columns'])) * 100

    numeric_columns = ['BMI']
    categorical_columns = [col for col in df.columns if 
                           (df[col].dropna().isin([0, 1]).all()) or
                           (df[col].dropna().isin(range(1, 14)).all())]
    stats['numeric_columns'] = len(numeric_columns)
    stats['categorical_columns'] = len(categorical_columns)

    # Ganti memory_usage dengan ukuran file asli
    if parquet_path and os.path.exists(parquet_path):
        stats['file_size_mb'] = os.path.getsize(parquet_path) / 1024 
    else:
        stats['file_size_mb'] = None  # Atau 0, atau tampilkan pesan jika file tidak ditemukan

    stats['duplicate_rows'] = df.duplicated().sum()

    return stats

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