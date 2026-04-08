"""
common.py
Shared data loading and merging utilities.
Retained for compatibility with reference repo structure.
"""

import pandas as pd


def loadAllData():
    """Load all six Hero FinCorp datasets from data/raw/."""
    return {
        "applications": pd.read_csv("data/raw/applications.csv", low_memory=False),
        "customers":    pd.read_csv("data/raw/customers.csv",     low_memory=False),
        "loans":        pd.read_csv("data/raw/loans.csv",         low_memory=False),
        "defaults":     pd.read_csv("data/raw/defaults.csv",      low_memory=False),
        "transactions": pd.read_csv("data/raw/transactions.csv",  low_memory=False),
        "branches":     pd.read_csv("data/raw/branches.csv",      low_memory=False),
    }


def mergeAll(data):
    """
    Merge loans + customers (+ branches if BRANCH_ID present).
    Returns master DataFrame.
    """
    loans     = data['loans']
    customers = data['customers']

    df = loans.merge(customers, on='CUSTOMER_ID', how='left')

    if 'BRANCH_ID' in loans.columns and 'BRANCH_ID' in data['branches'].columns:
        df = df.merge(data['branches'], on='BRANCH_ID', how='left')

    return df
