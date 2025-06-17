# src/visualization/data_loader.py

import os
import pandas as pd
from .config import PROCESSED_DIR

def load_data(processed_dir=PROCESSED_DIR):
    """
    Load and combine all BRFSS data files from the processed directory.
    
    Args:
        processed_dir (str): Path to the directory containing processed parquet files
        
    Returns:
        pd.DataFrame: Combined dataframe with all years of data
    """
    data_frames = []
    
    if not os.path.exists(processed_dir):
        raise FileNotFoundError(f"Processed data directory not found: {processed_dir}")
    
    parquet_files = [f for f in os.listdir(processed_dir) if f.endswith(".parquet")]
    
    if not parquet_files:
        raise FileNotFoundError(f"No parquet files found in {processed_dir}")
    
    for file in parquet_files:
        try:
            df = pd.read_parquet(os.path.join(processed_dir, file))
            # Extract year from filename (assuming format like 'BRFSS2015.parquet')
            year = int(file.split("BRFSS")[-1].split(".")[0])
            df["Year"] = year
            data_frames.append(df)
            print(f"Loaded data for year {year}: {len(df)} records")
        except Exception as e:
            print(f"Error loading file {file}: {e}")
            continue
    
    if not data_frames:
        raise ValueError("No valid data files could be loaded")
    
    combined_df = pd.concat(data_frames, ignore_index=True)
    print(f"Total combined data: {len(combined_df)} records across {len(data_frames)} years")
    
    return combined_df

def get_available_years(df):
    """
    Get sorted list of available years in the dataset.
    
    Args:
        df (pd.DataFrame): DataFrame containing Year column
        
    Returns:
        list: Sorted list of available years
    """
    return sorted(df["Year"].unique())
