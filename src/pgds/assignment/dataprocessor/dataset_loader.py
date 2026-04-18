"""
Dataset Loader
Responsible for reading raw and cleaned CSV datasets from disk
into a dictionary of Pandas DataFrames.
"""
import os
import pandas as pd
from config import DATA_PATH


def load_data():
    """
    Read all six raw CSV files (customers, loans, applications,
    transactions, defaults, branches) and return as a dict.
    """
    print("[Loader] Reading raw datasets from:", DATA_PATH)
    datasets = {
        "customers":    pd.read_csv(DATA_PATH + "customers.csv",    low_memory=False),
        "loans":        pd.read_csv(DATA_PATH + "loans.csv",        low_memory=False),
        "applications": pd.read_csv(DATA_PATH + "applications.csv", low_memory=False),
        "transactions": pd.read_csv(DATA_PATH + "transactions.csv", low_memory=False),
        "defaults":     pd.read_csv(DATA_PATH + "defaults.csv",     low_memory=False),
        "branches":     pd.read_csv(DATA_PATH + "branches.csv",     low_memory=False),
    }
    for name, frame in datasets.items():
        print(f"  {name}: {len(frame):,} rows, {frame.shape[1]} cols")
    return datasets


def load_cleaned_data():
    """
    Load all cleaned CSV files from the data/cleaned directory
    and return as a dict keyed by filename (without extension).
    """
    cleaned_dir = "data/cleaned"
    cleaned = {}

    for fname in os.listdir(cleaned_dir):
        if fname.endswith(".csv"):
            key = fname.replace(".csv", "")
            cleaned[key] = pd.read_csv(os.path.join(cleaned_dir, fname), low_memory=False)

    print(f"[Loader] Loaded {len(cleaned)} cleaned datasets from {cleaned_dir}")
    return cleaned
