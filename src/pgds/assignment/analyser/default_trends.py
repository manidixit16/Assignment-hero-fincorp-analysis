import pandas as pd

def default_trends_analysis(df, defaults):
    print("\n📉 DEFAULT TRENDS ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. DEFAULTS OVER TIME
    # -----------------------------------
    if 'DEFAULT_DATE' in defaults.columns:
        defaults['DEFAULT_DATE'] = pd.to_datetime(defaults['DEFAULT_DATE'], errors='coerce')

        trend = defaults.groupby(
            defaults['DEFAULT_DATE'].dt.to_period('M')
        ).size()

        results['default_trend'] = trend

        print("\nDefaults Over Time:\n", trend.head())

    # -----------------------------------
    # 2. AVG DEFAULT AMOUNT BY LOAN PURPOSE
    # -----------------------------------
    merged = df.merge(defaults, on='LOAN_ID', how='left')

    if 'LOAN_PURPOSE' in merged.columns and 'DEFAULT_AMOUNT' in merged.columns:
        avg_default = merged.groupby('LOAN_PURPOSE')['DEFAULT_AMOUNT'].mean()

        results['avg_default_by_purpose'] = avg_default

        print("\nAvg Default Amount by Loan Purpose:\n", avg_default)

    # -----------------------------------
    # 3. DEFAULT RATE BY INCOME CATEGORY
    # -----------------------------------
    if 'ANNUAL_INCOME' in df.columns:
        df['INCOME_GROUP'] = pd.qcut(
            df['ANNUAL_INCOME'],
            q=3,
            labels=['Low', 'Medium', 'High']
        )

        income_default = df.groupby('INCOME_GROUP')['DEFAULT_FLAG'].mean()

        results['income_default'] = income_default

        print("\nDefault Rate by Income Group:\n", income_default)

    return results