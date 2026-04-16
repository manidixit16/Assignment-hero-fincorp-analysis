
import pandas as pd
from config import DATA_PATH
import os

def load_data():
    return {
        "customers": pd.read_csv(DATA_PATH + "customers.csv", low_memory=False),
        "loans": pd.read_csv(DATA_PATH + "loans.csv", low_memory=False),
        "applications": pd.read_csv(DATA_PATH + "applications.csv", low_memory=False),
        "transactions": pd.read_csv(DATA_PATH + "transactions.csv", low_memory=False),
        "defaults": pd.read_csv(DATA_PATH + "defaults.csv", low_memory=False),
        "branches": pd.read_csv(DATA_PATH + "branches.csv", low_memory=False),
    }

def load_cleaned_data():
    cleaned_data = {}
    path = "data/cleaned"

    for file in os.listdir(path):
        if file.endswith(".csv"):
            name = file.replace(".csv", "")
            cleaned_data[name] = pd.read_csv(os.path.join(path, file))

    print("Loaded cleaned datasets")
    return cleaned_data
