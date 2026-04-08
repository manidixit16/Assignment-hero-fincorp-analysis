import pandas as pd

def time_series_analysis(df, loans, applications, defaults, branches):
    print("\n📅 TIME SERIES ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. LOAN DISBURSEMENT TREND
    # -----------------------------------
    if 'DISBURSEMENT_DATE' in loans.columns:
        loans['DISBURSEMENT_DATE'] = pd.to_datetime(
            loans['DISBURSEMENT_DATE'], errors='coerce'
        )

        disbursement_trend = loans.groupby(
            loans['DISBURSEMENT_DATE'].dt.to_period('M')
        ).size()

        results['disbursement_trend'] = disbursement_trend

        print("\nMonthly Disbursement Trend:\n", disbursement_trend.head())

    # -----------------------------------
    # 2. SEASONAL PATTERN (APPLICATIONS)
    # -----------------------------------
    if 'APPLICATION_DATE' in applications.columns:
        applications['APPLICATION_DATE'] = pd.to_datetime(
            applications['APPLICATION_DATE'], errors='coerce'
        )

        seasonal = applications.groupby(
            applications['APPLICATION_DATE'].dt.month
        ).size()

        results['seasonal_pattern'] = seasonal

        print("\nSeasonal Pattern (Month-wise):\n", seasonal)

    # -----------------------------------
    # 3. MONTHLY DEFAULT RATE (REGION)
    # -----------------------------------
    if 'DEFAULT_DATE' in defaults.columns:
        defaults['DEFAULT_DATE'] = pd.to_datetime(
            defaults['DEFAULT_DATE'], errors='coerce'
        )

        merged = df.merge(branches, on='BRANCH_ID', how='left') \
                   .merge(defaults, on='LOAN_ID', how='left')

        merged['MONTH'] = merged['DEFAULT_DATE'].dt.to_period('M')

        region_default = merged.groupby(
            ['REGION', 'MONTH']
        )['DEFAULT_FLAG'].mean()

        results['region_default'] = region_default

        print("\nMonthly Default Rate by Region:\n", region_default.head())

    return results