"""
Exploratory Summary Analysis
Generates descriptive statistics and distribution overviews for the Hero FinCorp dataset.
"""
import pandas as pd


def exploratory_summary(df, applications):
    """
    Compute distribution summaries for loans, EMI, credit scores,
    regional breakdown, and monthly application/approval trends.
    """
    print("\n[TASK 2] Exploratory Summary Analysis")

    output = {}

    # --------------------------------------------------
    # 1. LOAN AMOUNT DISTRIBUTION
    # --------------------------------------------------
    if 'LOAN_AMOUNT' in df.columns:
        output['loan_stats'] = df['LOAN_AMOUNT'].describe()
        print("\nLoan Amount Statistics:\n", output['loan_stats'])

    # --------------------------------------------------
    # 2. EMI DISTRIBUTION
    # --------------------------------------------------
    if 'EMI_AMOUNT' in df.columns:
        output['emi_stats'] = df['EMI_AMOUNT'].describe()
        print("\nEMI Statistics:\n", output['emi_stats'])

    # --------------------------------------------------
    # 3. CREDIT SCORE DISTRIBUTION
    # --------------------------------------------------
    if 'CREDIT_SCORE' in df.columns:
        output['credit_stats'] = df['CREDIT_SCORE'].describe()
        print("\nCredit Score Statistics:\n", output['credit_stats'])

    # --------------------------------------------------
    # 4. REGIONAL LOAN & DEFAULT OVERVIEW
    # --------------------------------------------------
    if 'REGION' in df.columns:
        region_loan_totals  = df.groupby('REGION')['LOAN_AMOUNT'].sum()
        region_default_rates = df.groupby('REGION')['DEFAULT_FLAG'].mean()

        output['region_loan_totals']   = region_loan_totals
        output['region_default_rates'] = region_default_rates

        print("\nTotal Loan Amount by Region:\n",  region_loan_totals.head())
        print("\nDefault Rate by Region:\n",        region_default_rates.head())

    # --------------------------------------------------
    # 5. MONTHLY APPLICATION TREND
    # --------------------------------------------------
    if 'APPLICATION_DATE' in applications.columns:
        applications['APPLICATION_DATE'] = pd.to_datetime(
            applications['APPLICATION_DATE'], errors='coerce'
        )
        applications = applications[applications['APPLICATION_DATE'].notna()]

        app_trend = applications.groupby(
            applications['APPLICATION_DATE'].dt.to_period('M')
        ).size()

        if len(app_trend) > 1:
            app_trend = app_trend.iloc[:-1]

        output['app_trend'] = app_trend
        print("\nMonthly Application Trend:\n", app_trend.head())

    # --------------------------------------------------
    # 6. MONTHLY DISBURSEMENT TREND
    # --------------------------------------------------
    if 'DISBURSAL_DATE' in df.columns:
        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')
        df = df[df['DISBURSAL_DATE'].notna()]

        disbursal_trend = df.groupby(
            df['DISBURSAL_DATE'].dt.to_period('M')
        ).size()

        if len(disbursal_trend) > 1:
            disbursal_trend = disbursal_trend.iloc[:-1]

        output['disbursal_trend'] = disbursal_trend
        print("\nMonthly Disbursement Trend:\n", disbursal_trend.head())

    # --------------------------------------------------
    # 7. MONTHLY APPROVAL TREND
    # --------------------------------------------------
    if 'APPROVAL_STATUS' in applications.columns:
        approved_apps = applications[
            applications['APPROVAL_STATUS'].str.upper() == 'APPROVED'
        ]
        approval_trend = approved_apps.groupby(
            approved_apps['APPLICATION_DATE'].dt.to_period('M')
        ).size()

        if len(approval_trend) > 1:
            approval_trend = approval_trend.iloc[:-1]

        output['approval_trend'] = approval_trend
        print("\nMonthly Approved Loans:\n", approval_trend.head())

    return output
