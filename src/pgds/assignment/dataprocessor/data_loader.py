import pandas as pd
from config import DATA_PATH


def load_data():
    """Load all six Hero FinCorp datasets from CSV files."""
    return {
        "customers":    pd.read_csv(DATA_PATH + "customers.csv",    low_memory=False),
        "loans":        pd.read_csv(DATA_PATH + "loans.csv",        low_memory=False),
        "applications": pd.read_csv(DATA_PATH + "applications.csv", low_memory=False),
        "transactions": pd.read_csv(DATA_PATH + "transactions.csv", low_memory=False),
        "defaults":     pd.read_csv(DATA_PATH + "defaults.csv",     low_memory=False),
        "branches":     pd.read_csv(DATA_PATH + "branches.csv",     low_memory=False),
    }
