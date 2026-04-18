"""
Temporal Analysis
Examines loan disbursement, application, and default trends over
time using monthly and seasonal breakdowns.
"""
import pandas as pd


def time_series_analysis(df):
    """
    Generate time-series views for monthly disbursement, seasonal
    applications, and per-region default rate fluctuations.
    """
    print("\n[TASK 16] Temporal (Time-Series) Analysis")

    time_data = {}

    # --------------------------------------------------
    # 1. MONTHLY LOAN DISBURSEMENT
    # --------------------------------------------------
    if 'DISBURSAL_DATE' in df.columns:
        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')
        monthly_disb = df.groupby(df['DISBURSAL_DATE'].dt.to_period('M')).size()
        time_data['monthly_disb'] = monthly_disb
        print("\nMonthly Loan Disbursement:\n", monthly_disb.head())

    # --------------------------------------------------
    # 2. SEASONAL APPLICATION PATTERN
    # --------------------------------------------------
    if 'APPLICATION_DATE' in df.columns:
        df['APPLICATION_DATE'] = pd.to_datetime(df['APPLICATION_DATE'], errors='coerce')
        seasonal_apps = df.groupby(df['APPLICATION_DATE'].dt.month).size()
        time_data['seasonal_apps'] = seasonal_apps
        print("\nSeasonal Application Pattern (by month):\n", seasonal_apps)

    # --------------------------------------------------
    # 3. SEASONAL DISBURSEMENT PATTERN
    # --------------------------------------------------
    if 'DISBURSAL_DATE' in df.columns:
        seasonal_disb = df.groupby(df['DISBURSAL_DATE'].dt.month).size()
        time_data['seasonal_disb'] = seasonal_disb
        print("\nSeasonal Disbursement Pattern (by month):\n", seasonal_disb)

    # --------------------------------------------------
    # 4. MONTHLY DEFAULT RATE BY REGION
    # --------------------------------------------------
    if 'DISBURSAL_DATE' in df.columns and 'DEFAULT_FLAG' in df.columns and 'REGION' in df.columns:
        df['MONTH'] = df['DISBURSAL_DATE'].dt.to_period('M')
        region_default_ts = df.groupby(['MONTH', 'REGION'])['DEFAULT_FLAG'].mean().unstack()
        time_data['region_default_ts'] = region_default_ts
        print("\nMonthly Default Rate by Region (sample):\n", region_default_ts.head())

    return time_data
