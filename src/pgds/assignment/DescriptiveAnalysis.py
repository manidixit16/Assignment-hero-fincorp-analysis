"""
DescriptiveAnalysis.py
Legacy-style module retained for compatibility with reference repo structure.
Full Task 2 implementation is in analyser/descriptive_analysis.py
"""

import pandas as pd


def loanAmountDistribution(df):
    """Return descriptive stats for Loan Amount."""
    stats = df['LOAN_AMOUNT'].describe()
    print("\n📌 Loan Amount Distribution:")
    print(stats.to_string())
    return stats


def emiDistribution(df):
    """Return descriptive stats for EMI Amount."""
    if 'EMI_AMOUNT' not in df.columns:
        print("  EMI_AMOUNT column not found.")
        return None
    stats = df['EMI_AMOUNT'].describe()
    print("\n📌 EMI Amount Distribution:")
    print(stats.to_string())
    return stats


def creditScoreDistribution(df):
    """Return descriptive stats for Credit Score."""
    stats = df['CREDIT_SCORE'].describe()
    print("\n📌 Credit Score Distribution:")
    print(stats.to_string())
    return stats


def regionalTrends(df):
    """Summarise loan disbursement and default rate by region."""
    if 'REGION' not in df.columns:
        return None
    regional = df.groupby('REGION').agg(
        Total_Disbursement=('LOAN_AMOUNT', 'sum'),
        Loan_Count=('LOAN_ID', 'count'),
        Default_Rate=('DEFAULT_FLAG', 'mean')
    )
    regional['Default_Rate'] = (regional['Default_Rate'] * 100).round(2)
    print("\n📌 Regional Trends:")
    print(regional.to_string())
    return regional


def monthlyTrends(applications):
    """Count loan applications by month."""
    applications = applications.copy()
    applications['APPLICATION_DATE'] = pd.to_datetime(
        applications['APPLICATION_DATE'], errors='coerce'
    )
    monthly = applications.groupby(
        applications['APPLICATION_DATE'].dt.to_period('M')
    ).size().rename('Application_Count')
    print("\n📌 Monthly Applications (last 5):")
    print(monthly.tail(5).to_string())
    return monthly
