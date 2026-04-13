import pandas as pd


def time_series_analysis(df, loans, applications, defaults, branches):

    print("TIME SERIES ANALYSIS")

    results = {}

    # -----------------------------------
    # STANDARDIZE COLUMN NAMES (IMPORTANT)
    # -----------------------------------
    df.columns = [col.upper() for col in df.columns]
    loans.columns = [col.upper() for col in loans.columns]
    applications.columns = [col.upper() for col in applications.columns]
    defaults.columns = [col.upper() for col in defaults.columns]

    # -----------------------------------
    # 1. LOAN DISBURSEMENT TREND
    # -----------------------------------
    if 'DISBURSAL_DATE' in loans.columns:
        loans['DISBURSAL_DATE'] = pd.to_datetime(
            loans['DISBURSAL_DATE'], errors='coerce'
        )

        disbursement_trend = loans.groupby(
            loans['DISBURSAL_DATE'].dt.to_period('M')
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

        # ✅ Merge ONLY with defaults (NOT branches)
        merged = df.merge(defaults, on='LOAN_ID', how='left')

        # Ensure REGION exists (from customers)
        if 'REGION' not in merged.columns:
            if 'Region' in merged.columns:
                merged['REGION'] = merged['Region']
            else:
                print("⚠️ REGION missing → skipping regional default analysis")
                return results

        # Create DEFAULT_FLAG if missing
        if 'DEFAULT_FLAG' not in merged.columns:
            merged['DEFAULT_FLAG'] = merged['DEFAULT_AMOUNT'].notnull().astype(int)

        # Create MONTH
        # Ensure DEFAULT_DATE exists after merge
        if 'DEFAULT_DATE' not in merged.columns:
            print("DEFAULT_DATE missing after merge → skipping")
            return results

        # Ensure datetime
        merged['DEFAULT_DATE'] = pd.to_datetime(merged['DEFAULT_DATE'], errors='coerce')

        # Remove invalid dates
        merged = merged[merged['DEFAULT_DATE'].notna()]

        # Create MONTH
        merged['MONTH'] = merged['DEFAULT_DATE'].dt.to_period('M')

        region_default = merged.groupby(
            ['REGION', 'MONTH']
        )['DEFAULT_FLAG'].mean()

        results['region_default'] = region_default

        print("\nMonthly Default Rate by Region:\n", region_default.head())

    return results