"""
DataQualityAndPreparation.py
Legacy-style module retained for compatibility with reference repo structure.
Full Task 1 implementation is in dataprocessor/data_cleaning.py
"""

import pandas as pd


def loadData():
    """Load all six Hero FinCorp datasets from data/raw/."""
    customers    = pd.read_csv("data/raw/customers.csv",    low_memory=False)
    applications = pd.read_csv("data/raw/applications.csv", low_memory=False)
    loans        = pd.read_csv("data/raw/loans.csv",        low_memory=False)
    defaults     = pd.read_csv("data/raw/defaults.csv",     low_memory=False)
    transactions = pd.read_csv("data/raw/transactions.csv", low_memory=False)
    branches     = pd.read_csv("data/raw/branches.csv",     low_memory=False)
    return customers, applications, loans, defaults, transactions, branches


def checkMissingValues(dfs):
    """Print missing value counts for each DataFrame in the list."""
    names = ['customers', 'applications', 'loans', 'defaults', 'transactions', 'branches']
    for name, df in zip(names, dfs):
        print(f"\n--- {name.upper()} ---")
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if missing.empty:
            print("  No missing values")
        else:
            print(missing.to_string())


def checkDuplicates(dfs):
    """Print duplicate row counts for each DataFrame."""
    names = ['customers', 'applications', 'loans', 'defaults', 'transactions', 'branches']
    for name, df in zip(names, dfs):
        dups = df.duplicated().sum()
        print(f"  {name:15s}: {dups} duplicates")


def standardizeDates(df, date_cols):
    """Parse date columns to datetime."""
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


def removeOutliers(df, col):
    """Cap outliers in a numeric column using IQR method."""
    import numpy as np
    Q1    = df[col].quantile(0.25)
    Q3    = df[col].quantile(0.75)
    IQR   = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df[col] = df[col].clip(lower=lower, upper=upper)
    return df
