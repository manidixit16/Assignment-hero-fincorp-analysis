"""
Revenue Analysis
Measures profitability across regions, loan amount brackets,
and loan purposes to guide portfolio strategy.
"""
import pandas as pd


def profitability_analysis(df):
    """
    Estimate revenue contribution from interest income by region,
    loan amount bracket, and loan purpose.
    """
    print("\n[TASK 12] Revenue & Profitability Analysis")

    revenue = {}

    # --------------------------------------------------
    # 1. PROFIT BY REGION
    # --------------------------------------------------
    if 'REGION' in df.columns and 'INTEREST_INCOME' in df.columns:
        region_revenue = df.groupby('REGION')['INTEREST_INCOME'].sum()
        revenue['region_revenue'] = region_revenue
        print("\nRevenue by Region:\n", region_revenue)

    # --------------------------------------------------
    # 2. PROFIT BY LOAN AMOUNT BRACKET
    # --------------------------------------------------
    if 'LOAN_AMOUNT' in df.columns and 'INTEREST_INCOME' in df.columns:
        amount_bins   = [0, 10000, 20000, 30000, float('inf')]
        amount_labels = ['<10k', '10k-20k', '20k-30k', '>30k']
        df['AMOUNT_BRACKET'] = pd.cut(df['LOAN_AMOUNT'], bins=amount_bins, labels=amount_labels)

        bracket_revenue = df.groupby('AMOUNT_BRACKET')['INTEREST_INCOME'].sum()
        revenue['bracket_revenue'] = bracket_revenue
        print("\nRevenue by Loan Amount Bracket:\n", bracket_revenue)

    # --------------------------------------------------
    # 3. PROFIT BY LOAN PURPOSE
    # --------------------------------------------------
    if 'LOAN_PURPOSE' in df.columns and 'INTEREST_INCOME' in df.columns:
        purpose_revenue = df.groupby('LOAN_PURPOSE')['INTEREST_INCOME'].sum()
        revenue['purpose_revenue'] = purpose_revenue
        print("\nRevenue by Loan Purpose:\n", purpose_revenue)

    return revenue
