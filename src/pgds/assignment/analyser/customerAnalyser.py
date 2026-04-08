"""
customerAnalyser.py
Legacy camelCase module retained for compatibility with reference repo.
Full Task 5 implementation is in analyser/customer_analysis.py
"""

import pandas as pd


def segment_customers(df):
    """
    Segment customers by credit score into risk tiers.
    Returns DataFrame with Customer_ID and Segment columns.
    """
    df = df.copy()
    df['SEGMENT'] = pd.cut(
        df['CREDIT_SCORE'],
        bins=[0, 500, 650, 750, 900],
        labels=['High Risk', 'Medium', 'Good', 'Excellent']
    )

    summary = df['SEGMENT'].value_counts().rename('Count')
    print("\n📌 Customer Segments by Credit Score:")
    print(summary.to_string())

    id_col = 'CUSTOMER_ID' if 'CUSTOMER_ID' in df.columns else df.columns[0]
    return df[[id_col, 'SEGMENT']]


def highValueCustomers(df):
    """Identify high-value customers: no default, good/excellent credit, high income."""
    mask = df['DEFAULT_FLAG'] == 0
    if 'CREDIT_SCORE' in df.columns:
        mask = mask & (df['CREDIT_SCORE'] >= 700)
    if 'ANNUAL_INCOME' in df.columns:
        mask = mask & (df['ANNUAL_INCOME'] >= df['ANNUAL_INCOME'].quantile(0.75))
    hv = df[mask]
    print(f"\n📌 High-Value Customers: {len(hv):,}")
    return hv


def highRiskCustomers(df):
    """Identify high-risk customers: defaulted or very low credit score."""
    mask = (df['DEFAULT_FLAG'] == 1)
    if 'CREDIT_SCORE' in df.columns:
        mask = mask | (df['CREDIT_SCORE'] < 500)
    hr = df[mask]
    print(f"\n📌 High-Risk Customers: {len(hr):,}")
    return hr
