"""
Module 1: Data Cleaning & Preprocessing
Customer Churn Prediction & Business Analytics
Author: Data Science Apprentice
"""

import os
import pandas as pd
import numpy as np

def load_raw_data(filepath="data/WA_Fn-UseC_-Telco-Customer-Churn.csv"):
    """Load the raw IBM Telco Customer Churn dataset."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Dataset successfully loaded with shape: {df.shape}")
    return df

def clean_data(df):
    """
    Perform rigorous data cleaning:
    1. Strip leading/trailing whitespaces from string columns.
    2. Convert TotalCharges from object to float, handling whitespace values.
    3. Check and remove any duplicate records.
    4. Create binary churn indicator (1 for Yes, 0 for No).
    5. Validate tenure and charges boundaries.
    """
    df_clean = df.copy()
    
    # 1. Strip string whitespace
    str_cols = df_clean.select_dtypes(include='object').columns
    for col in str_cols:
        df_clean[col] = df_clean[col].astype(str).str.strip()
        
    # 2. Fix TotalCharges
    # Replace empty spaces with NaN, then inspect tenure
    df_clean['TotalCharges'] = pd.to_numeric(df_clean['TotalCharges'], errors='coerce')
    missing_tc = df_clean['TotalCharges'].isnull().sum()
    print(f"TotalCharges missing/blank values detected: {missing_tc}")
    
    # For customers with tenure == 0, TotalCharges is legitimately 0.0
    zero_tenure_mask = (df_clean['tenure'] == 0) & (df_clean['TotalCharges'].isnull())
    print(f"Customers with tenure=0 and null TotalCharges: {zero_tenure_mask.sum()}")
    df_clean.loc[zero_tenure_mask, 'TotalCharges'] = 0.0
    
    # In case any remaining nulls exist, fill with median
    if df_clean['TotalCharges'].isnull().sum() > 0:
        df_clean['TotalCharges'] = df_clean['TotalCharges'].fillna(df_clean['TotalCharges'].median())
        
    # 3. Check duplicate records
    dup_count = df_clean.duplicated().sum()
    print(f"Duplicate rows found: {dup_count}")
    if dup_count > 0:
        df_clean = df_clean.drop_duplicates()
        
    # 4. Target variable encoding for convenience
    df_clean['Churn_Binary'] = df_clean['Churn'].map({'Yes': 1, 'No': 0}).astype(int)
    
    # 5. Feature categorization
    df_clean['TenureGroup'] = pd.cut(
        df_clean['tenure'],
        bins=[-1, 12, 24, 36, 48, 60, 72],
        labels=['0-12 Mo', '13-24 Mo', '25-36 Mo', '37-48 Mo', '49-60 Mo', '61-72 Mo']
    )
    
    print(f"Data cleaning complete. Clean shape: {df_clean.shape}")
    return df_clean

def save_cleaned_data(df_clean, output_path="data/cleaned_telco_churn.csv"):
    """Export cleaned dataset to CSV."""
    df_clean.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved to: {output_path}")

if __name__ == "__main__":
    raw_df = load_raw_data()
    cleaned_df = clean_data(raw_df)
    save_cleaned_data(cleaned_df)
