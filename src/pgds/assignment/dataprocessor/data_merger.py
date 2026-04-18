"""
Data Merger
Joins all cleaned datasets into a single master DataFrame used
throughout the analysis pipeline.
"""
import pandas as pd


def merge_all(data):
    """
    Build a unified analysis frame by left-joining loans with
    customers, defaults, and applications on shared keys.

    Returns
    -------
    pd.DataFrame
        Master frame with loan, customer, default, and application columns.
    """
    master = data['loans'].copy()

    # --------------------------------------------------
    # 1. ATTACH CUSTOMER ATTRIBUTES
    # --------------------------------------------------
    customer_cols = [c for c in ['CUSTOMER_ID', 'CREDIT_SCORE', 'ANNUAL_INCOME', 'REGION']
                     if c in data['customers'].columns]
    master = master.merge(data['customers'][customer_cols], on='CUSTOMER_ID', how='left')

    # --------------------------------------------------
    # 2. ATTACH DEFAULT & RECOVERY INFO
    # --------------------------------------------------
    default_cols = [c for c in [
        'LOAN_ID', 'DEFAULT_AMOUNT', 'RECOVERY_AMOUNT',
        'DEFAULT_REASON', 'LEGAL_ACTION', 'DEFAULT_DATE'
    ] if c in data['defaults'].columns]
    master = master.merge(data['defaults'][default_cols], on='LOAN_ID', how='left')

    # --------------------------------------------------
    # 3. ATTACH APPLICATION ATTRIBUTES
    # --------------------------------------------------
    app_cols = [c for c in ['LOAN_ID', 'APPLICATION_DATE', 'LOAN_PURPOSE']
                if c in data['applications'].columns]
    master = master.merge(data['applications'][app_cols], on='LOAN_ID', how='left')

    # --------------------------------------------------
    # 4. FILL MISSING FINANCIAL COLUMNS
    # --------------------------------------------------
    for col in ['DEFAULT_AMOUNT', 'RECOVERY_AMOUNT']:
        if col in master.columns:
            master[col] = master[col].fillna(0)

    # --------------------------------------------------
    # 5. COMPUTE RECOVERY RATE
    # --------------------------------------------------
    if 'RECOVERY_AMOUNT' in master.columns and 'DEFAULT_AMOUNT' in master.columns:
        master['RECOVERY_RATE'] = (
            master['RECOVERY_AMOUNT'] / master['DEFAULT_AMOUNT'].replace(0, 1)
        )

    # --------------------------------------------------
    # 6. RESOLVE DUPLICATE REGION COLUMNS
    # --------------------------------------------------
    if 'REGION_x' in master.columns:
        master['REGION'] = master['REGION_x']
    elif 'REGION_y' in master.columns:
        master['REGION'] = master['REGION_y']
    master.drop(columns=['REGION_x', 'REGION_y'], errors='ignore', inplace=True)

    print(f"[Merger] Master frame ready — {len(master):,} rows, {master.shape[1]} columns")
    return master
