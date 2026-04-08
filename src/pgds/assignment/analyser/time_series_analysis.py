"""
TASK 16: Time-Series Analysis
- Analyse monthly loan disbursement trends over the full dataset period
- Identify seasonal patterns in loan applications and disbursements
- Compare monthly default rates across regions
"""

import pandas as pd


def time_series(df, applications=None, defaults=None):
    """
    Perform time-series decomposition and seasonal analysis on
    disbursements, applications, and defaults.

    Returns
    -------
    dict with keys: monthly_disbursement, yearly_disbursement,
                    seasonal_applications, monthly_defaults,
                    regional_monthly_defaults, peak_disbursement_month
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 16 — Time-Series Analysis")
    print("="*55)

    # ── 1. Monthly loan disbursement trend ────────────────────────────────────
    if 'DISBURSAL_DATE' in df.columns:
        df = df.copy()
        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')

        monthly_disb = df.groupby(df['DISBURSAL_DATE'].dt.to_period('M')).agg(
            Total_Disbursed=('LOAN_AMOUNT', 'sum'),
            Loan_Count=('LOAN_ID', 'count'),
            Avg_Loan=('LOAN_AMOUNT', 'mean')
        ).round(2)
        results['monthly_disbursement'] = monthly_disb
        print(f"\n📌 Monthly Disbursement Trend (last 6 periods):")
        print(monthly_disb.tail(6).to_string())

        # Yearly
        yearly_disb = df.groupby(df['DISBURSAL_DATE'].dt.year).agg(
            Total_Disbursed=('LOAN_AMOUNT', 'sum'),
            Loan_Count=('LOAN_ID', 'count')
        ).round(2)
        results['yearly_disbursement'] = yearly_disb
        print("\n📌 Yearly Disbursement Summary:")
        print(yearly_disb.to_string())

        # Peak month (seasonal)
        monthly_seasonal = df.groupby(df['DISBURSAL_DATE'].dt.month)['LOAN_AMOUNT'].sum()
        peak_month = monthly_seasonal.idxmax()
        results['peak_disbursement_month'] = int(peak_month)
        print(f"\n📌 Peak Disbursement Month (1=Jan): Month {peak_month}")
        print(monthly_seasonal.to_string())

    # ── 2. Seasonal pattern in applications ───────────────────────────────────
    src_apps = applications if applications is not None else df
    src_apps = src_apps.copy()

    if 'APPLICATION_DATE' in src_apps.columns:
        src_apps['APPLICATION_DATE'] = pd.to_datetime(src_apps['APPLICATION_DATE'], errors='coerce')

        # By calendar month (aggregated across all years)
        seasonal = src_apps.groupby(src_apps['APPLICATION_DATE'].dt.month).size().rename('Application_Count')
        seasonal.index.name = 'Month'
        results['seasonal_applications'] = seasonal
        print("\n📌 Seasonal Pattern — Applications by Month:")
        print(seasonal.to_string())

        # By year-month
        monthly_apps = src_apps.groupby(
            src_apps['APPLICATION_DATE'].dt.to_period('M')
        ).size().rename('Application_Count')
        results['monthly_applications'] = monthly_apps
        print(f"\n📌 Monthly Applications (last 6 periods):")
        print(monthly_apps.tail(6).to_string())

    # ── 3. Monthly default rate ───────────────────────────────────────────────
    src_def = defaults if defaults is not None else df[df['DEFAULT_FLAG'] == 1]
    src_def = src_def.copy()

    if 'DEFAULT_DATE' in src_def.columns:
        src_def['DEFAULT_DATE'] = pd.to_datetime(src_def['DEFAULT_DATE'], errors='coerce')

        monthly_def = src_def.groupby(
            src_def['DEFAULT_DATE'].dt.to_period('M')
        ).size().rename('Default_Count')
        results['monthly_defaults'] = monthly_def
        print(f"\n📌 Monthly Default Count (last 6 periods):")
        print(monthly_def.tail(6).to_string())

    # ── 4. Monthly defaults by region ────────────────────────────────────────
    if 'REGION' in df.columns and 'DISBURSAL_DATE' in df.columns:
        df['YEAR'] = df['DISBURSAL_DATE'].dt.year
        reg_monthly = df.groupby(['YEAR', 'REGION'])['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Default_Count='sum'
        ).round(4)
        reg_monthly['Default_Rate_%'] = (reg_monthly['Default_Rate'] * 100).round(2)
        results['regional_monthly_defaults'] = reg_monthly
        print("\n📌 Yearly Default Rate by Region:")
        print(reg_monthly[['Default_Count', 'Default_Rate_%']].to_string())

    print("\n✅ Task 16 complete")
    return results
