"""
TASK 2: Descriptive Analysis
- Distribution of Loan_Amount, EMI_Amount, and Credit_Score
- Regional trends in loan disbursement and defaults
- Monthly trends in loan approvals and disbursements
"""

import pandas as pd


def descriptive_analysis(df, applications=None):
    """
    Summarise key metrics across the merged dataset.

    Parameters
    ----------
    df : pd.DataFrame  — master merged dataset
    applications : pd.DataFrame, optional — raw applications (for monthly trend)

    Returns
    -------
    dict with keys: loan_amount_stats, emi_stats, credit_score_stats,
                    regional_trends, monthly_applications, monthly_disbursements
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 2 — Descriptive Analysis")
    print("="*55)

    # ── 1. Distributions ──────────────────────────────────────────────────────
    results['loan_amount_stats'] = df['LOAN_AMOUNT'].describe()
    print("\n📌 Loan Amount Statistics:")
    print(results['loan_amount_stats'].to_string())

    if 'EMI_AMOUNT' in df.columns:
        results['emi_stats'] = df['EMI_AMOUNT'].describe()
        print("\n📌 EMI Amount Statistics:")
        print(results['emi_stats'].to_string())

    if 'CREDIT_SCORE' in df.columns:
        results['credit_score_stats'] = df['CREDIT_SCORE'].describe()
        print("\n📌 Credit Score Statistics:")
        print(results['credit_score_stats'].to_string())

    # ── 2. Regional trends ────────────────────────────────────────────────────
    if 'REGION' in df.columns:
        regional = df.groupby('REGION').agg(
            Total_Disbursement=('LOAN_AMOUNT', 'sum'),
            Loan_Count=('LOAN_ID', 'count'),
            Default_Rate=('DEFAULT_FLAG', 'mean'),
            Avg_Credit_Score=('CREDIT_SCORE', 'mean')
        )
        regional['Default_Rate'] = (regional['Default_Rate'] * 100).round(2)
        regional['Avg_Credit_Score'] = regional['Avg_Credit_Score'].round(1)
        results['regional_trends'] = regional
        print("\n📌 Regional Trends:")
        print(regional.to_string())

    # ── 3. Monthly trends ─────────────────────────────────────────────────────
    if applications is not None and 'APPLICATION_DATE' in applications.columns:
        applications = applications.copy()
        applications['APPLICATION_DATE'] = pd.to_datetime(
            applications['APPLICATION_DATE'], errors='coerce'
        )
        monthly_apps = applications.groupby(
            applications['APPLICATION_DATE'].dt.to_period('M')
        ).size().rename('Application_Count')
        results['monthly_applications'] = monthly_apps
        print(f"\n📌 Monthly Applications — sample (last 5 periods):")
        print(monthly_apps.tail(5).to_string())

    if 'DISBURSAL_DATE' in df.columns:
        df = df.copy()
        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')
        monthly_disb = df.groupby(
            df['DISBURSAL_DATE'].dt.to_period('M')
        )['LOAN_AMOUNT'].sum().rename('Total_Disbursed')
        results['monthly_disbursements'] = monthly_disb
        print(f"\n📌 Monthly Disbursements — sample (last 5 periods):")
        print(monthly_disb.tail(5).to_string())

    print("\n✅ Task 2 complete")
    return results
