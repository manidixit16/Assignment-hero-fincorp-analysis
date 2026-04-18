"""
Default Trend Tracker
Tracks default patterns over time, by income segment and loan
purpose to surface where risk is concentrating.
"""
import pandas as pd


def default_trend_analysis(df):
    """
    Compute default trend over time, broken down by income segment
    and loan purpose.
    """
    print("\n[TASK 14] Default Trend Tracker")

    trend_data = {}

    # --------------------------------------------------
    # 1. DEFAULT TREND OVER TIME
    # --------------------------------------------------
    if 'DISBURSAL_DATE' in df.columns and 'DEFAULT_FLAG' in df.columns:
        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')
        time_series = df.groupby(df['DISBURSAL_DATE'].dt.to_period('M'))['DEFAULT_FLAG'].sum()
        trend_data['monthly_defaults'] = time_series
        print("\nMonthly Default Count:\n", time_series.head())

    # --------------------------------------------------
    # 2. DEFAULT BY LOAN PURPOSE
    # --------------------------------------------------
    if 'LOAN_PURPOSE' in df.columns and 'DEFAULT_AMOUNT' in df.columns:
        purpose_defaults = df.groupby('LOAN_PURPOSE')['DEFAULT_AMOUNT'].mean()
        trend_data['purpose_defaults'] = purpose_defaults
        print("\nAverage Default Amount by Loan Purpose:\n", purpose_defaults)

    # --------------------------------------------------
    # 3. DEFAULT BY INCOME SEGMENT
    # --------------------------------------------------
    if 'ANNUAL_INCOME' in df.columns and 'DEFAULT_FLAG' in df.columns:
        income_bins   = [0, 300000, 700000, float('inf')]
        income_labels = ['Low', 'Medium', 'High']
        df['INCOME_TIER'] = pd.cut(df['ANNUAL_INCOME'], bins=income_bins, labels=income_labels)

        income_defaults = df.groupby('INCOME_TIER')['DEFAULT_FLAG'].mean()
        trend_data['income_defaults'] = income_defaults
        print("\nDefault Rate by Income Tier:\n", income_defaults)

    return trend_data
