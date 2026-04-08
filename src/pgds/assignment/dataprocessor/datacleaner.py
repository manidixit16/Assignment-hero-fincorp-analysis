"""
datacleaner.py
Legacy camelCase cleaning module retained for compatibility with reference repo.
Full Task 1 implementation is in dataprocessor/data_cleaning.py
"""

import pandas as pd


def cleanData(data):
    """
    Basic cleaning pass on all datasets.
    - Remove duplicates from customers
    - Drop loans with null Customer_ID or Loan_Amount <= 0
    - Parse Application_Date in applications
    - Standardise all column names to uppercase

    Returns
    -------
    dict of cleaned DataFrames
    """
    # Standardise column names across all tables
    for key in data:
        data[key].columns = data[key].columns.str.strip().str.upper()

    # Customers — remove duplicates
    data['customers'] = data['customers'].drop_duplicates()

    # Loans — drop nulls on key columns, enforce positive amount
    loans = data['loans']
    loans = loans.dropna(subset=['CUSTOMER_ID'])
    loans = loans[loans['LOAN_AMOUNT'] > 0]
    data['loans'] = loans

    # Applications — parse date
    if 'APPLICATION_DATE' in data['applications'].columns:
        data['applications']['APPLICATION_DATE'] = pd.to_datetime(
            data['applications']['APPLICATION_DATE'], errors='coerce'
        )

    # Defaults — parse date
    if 'DEFAULT_DATE' in data['defaults'].columns:
        data['defaults']['DEFAULT_DATE'] = pd.to_datetime(
            data['defaults']['DEFAULT_DATE'], errors='coerce'
        )

    # Transactions — parse date
    if 'TRANSACTION_DATE' in data['transactions'].columns:
        data['transactions']['TRANSACTION_DATE'] = pd.to_datetime(
            data['transactions']['TRANSACTION_DATE'], errors='coerce'
        )

    print("✅ cleanData complete")
    return data
