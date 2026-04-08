"""Build the master merged DataFrame used by all analysis tasks."""

import pandas as pd


def merge_all(data):
    """
    Merge loans ← customers ← applications ← defaults into one master DataFrame.

    Returns
    -------
    pd.DataFrame : master dataset with columns from all tables
    """
    loans        = data['loans']
    customers    = data['customers']
    applications = data['applications']
    defaults     = data['defaults']

    # Loans + Customers
    df = loans.merge(customers, on='CUSTOMER_ID', how='left', suffixes=('', '_CUST'))

    # + Applications (keep key fields only to avoid column explosion)
    app_cols = ['LOAN_ID', 'LOAN_PURPOSE', 'APPROVAL_STATUS',
                'PROCESSING_DAYS', 'PROCESSING_FEE', 'SOURCE_CHANNEL']
    app_cols = [c for c in app_cols if c in applications.columns]
    df = df.merge(applications[app_cols], on='LOAN_ID', how='left', suffixes=('', '_APP'))

    # + Defaults
    def_cols = ['LOAN_ID', 'DEFAULT_AMOUNT', 'RECOVERY_AMOUNT',
                'DEFAULT_REASON', 'RECOVERY_STATUS', 'LEGAL_ACTION',
                'DEFAULT_DATE', 'RECOVERY_RATE']
    def_cols = [c for c in def_cols if c in defaults.columns]
    df = df.merge(defaults[def_cols], on='LOAN_ID', how='left', suffixes=('', '_DEF'))

    print(f"\n✅ Master merge complete: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df
