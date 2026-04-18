"""
Regional Analysis
Maps loan distribution and default rates across geographic regions
to identify high-volume and high-risk areas.
"""
import pandas as pd


def geospatial_analysis(df):
    """
    Summarise active loan counts, default rates, and total loan
    amounts per region.
    """
    print("\n[TASK 13] Regional (Geospatial) Analysis")

    geo = {}

    # --------------------------------------------------
    # 1. ACTIVE LOANS BY REGION
    # --------------------------------------------------
    if 'REGION' in df.columns:
        active_loans = df.groupby('REGION').size()
        geo['active_loans'] = active_loans
        print("\nActive Loans by Region:\n", active_loans)

    # --------------------------------------------------
    # 2. DEFAULT RATE BY REGION
    # --------------------------------------------------
    if 'REGION' in df.columns and 'DEFAULT_FLAG' in df.columns:
        default_rate = df.groupby('REGION')['DEFAULT_FLAG'].mean()
        geo['default_rate'] = default_rate
        print("\nDefault Rate by Region:\n", default_rate)

    # --------------------------------------------------
    # 3. TOTAL LOAN AMOUNT BY REGION
    # --------------------------------------------------
    if 'REGION' in df.columns and 'LOAN_AMOUNT' in df.columns:
        loan_total = df.groupby('REGION')['LOAN_AMOUNT'].sum()
        geo['loan_total'] = loan_total
        print("\nTotal Loan Amount by Region:\n", loan_total)

    return geo
