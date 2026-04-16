import pandas as pd

def time_series_analysis(df):

    print("\n TIME SERIES ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. MONTHLY DISBURSEMENT TREND
    # -----------------------------------
    if 'DISBURSAL_DATE' in df.columns:

        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')

        disb_trend = df.groupby(
            df['DISBURSAL_DATE'].dt.to_period('M')
        ).size()

        print("\n Monthly Disbursement Trend:\n", disb_trend.head())

        results['disbursement'] = disb_trend

    else:
        print(" DISBURSAL_DATE missing")

    # -----------------------------------
    # 2. SEASONAL PATTERN (APPLICATIONS)
    # -----------------------------------
    if 'APPLICATION_DATE' in df.columns:

        df['APPLICATION_DATE'] = pd.to_datetime(df['APPLICATION_DATE'], errors='coerce')

        seasonal_app = df.groupby(
            df['APPLICATION_DATE'].dt.month
        ).size()

        print("\n Seasonal Pattern (Applications):\n", seasonal_app)

        results['seasonal_app'] = seasonal_app

    # -----------------------------------
    # SEASONAL PATTERN (DISBURSEMENT)
    # -----------------------------------
    if 'DISBURSAL_DATE' in df.columns:

        seasonal_disb = df.groupby(
            df['DISBURSAL_DATE'].dt.month
        ).size()

        print("\n Seasonal Pattern (Disbursement):\n", seasonal_disb)

        results['seasonal_disb'] = seasonal_disb

        # -----------------------------------
        # 3. MONTHLY DEFAULT RATE BY REGION
        # -----------------------------------
        if 'DISBURSAL_DATE' in df.columns and 'REGION' in df.columns and 'DEFAULT_FLAG' in df.columns:

            df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')

            df_valid = df[df['DISBURSAL_DATE'].notna()].copy()

            if df_valid.empty:
                print(" No valid DISBURSAL_DATE data")
            else:
                df_valid['MONTH'] = df_valid['DISBURSAL_DATE'].dt.to_period('M')

                region_default = df_valid.groupby(
                    ['REGION', 'MONTH']
                )['DEFAULT_FLAG'].mean()

                print("\nMonthly Default Rate by Region:\n", region_default.head())

                results['region_default'] = region_default

        else:
            print("Required columns missing for default rate")

    return results