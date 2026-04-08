"""
DefaultRiskAnalysis.py
Legacy-style module retained for compatibility with reference repo structure.
Full Task 3 implementation is in analyser/default_analysis.py
"""

import pandas as pd


def correlationWithDefault(df):
    """Compute correlation of key loan attributes with DEFAULT_FLAG."""
    cols = ['LOAN_AMOUNT', 'INTEREST_RATE', 'CREDIT_SCORE', 'DEFAULT_FLAG']
    cols = [c for c in cols if c in df.columns]
    corr = df[cols].corr()
    print("\n📌 Correlation with DEFAULT_FLAG:")
    if 'DEFAULT_FLAG' in corr.columns:
        print(corr['DEFAULT_FLAG'].drop('DEFAULT_FLAG').round(4).to_string())
    return corr


def pairwiseCorrelation(df):
    """Pairwise correlation: EMI_Amount, Overdue_Amount, Default_Amount."""
    pair_cols = ['EMI_AMOUNT', 'OVERDUE_AMOUNT', 'DEFAULT_AMOUNT']
    pair_cols = [c for c in pair_cols if c in df.columns]
    if len(pair_cols) < 2:
        return None
    pair_corr = df[pair_cols].corr()
    print("\n📌 Pairwise Correlation (EMI / Overdue / Default Amount):")
    print(pair_corr.round(4).to_string())
    return pair_corr


def defaultRateBySegment(df):
    """Default rate broken down by credit score bucket."""
    if 'CREDIT_SCORE' not in df.columns:
        return None
    df = df.copy()
    df['CREDIT_BUCKET'] = pd.cut(
        df['CREDIT_SCORE'],
        bins=[0, 300, 580, 670, 740, 900],
        labels=['Very Poor', 'Poor', 'Fair', 'Good', 'Excellent']
    )
    result = df.groupby('CREDIT_BUCKET', observed=True)['DEFAULT_FLAG'].agg(
        Default_Rate='mean', Count='count'
    )
    result['Default_Rate_%'] = (result['Default_Rate'] * 100).round(2)
    print("\n📌 Default Rate by Credit Score Bucket:")
    print(result[['Count', 'Default_Rate_%']].to_string())
    return result
