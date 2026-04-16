import pandas as pd

def default_trend_analysis(df):

    print("\n DEFAULT TREND ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. DEFAULT TREND OVER TIME
    # -----------------------------------
    date_col = None

    if 'DEFAULT_DATE' in df.columns:
        date_col = 'DEFAULT_DATE'
    elif 'DISBURSAL_DATE' in df.columns:
        print(" DEFAULT_DATE not available → using DISBURSAL_DATE")
        date_col = 'DISBURSAL_DATE'

    if date_col:

        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        trend = df.groupby(
            df[date_col].dt.to_period('M')
        )['DEFAULT_FLAG'].sum()

        print("\n Default Trend:\n", trend.head())

        results['trend'] = trend

    else:
        print(" No valid date column")

    # -----------------------------------
    # 2. DEFAULT AMOUNT BY LOAN PURPOSE
    # -----------------------------------
    if 'LOAN_PURPOSE' in df.columns:

        purpose_default = df.groupby('LOAN_PURPOSE')['DEFAULT_AMOUNT'].mean()

        print("\n Avg Default Amount by Purpose:\n", purpose_default)

        results['purpose_default'] = purpose_default

    else:
        print(" LOAN_PURPOSE missing")

    # -----------------------------------
    # 3. DEFAULT RATE BY INCOME SEGMENT 
    # -----------------------------------

    if 'ANNUAL_INCOME' in df.columns:

        df['INCOME_SEGMENT'] = pd.qcut(
            df['ANNUAL_INCOME'],
            3,
            labels=['Low', 'Medium', 'High']
        )

        income_default = df.groupby('INCOME_SEGMENT')['DEFAULT_FLAG'].mean()

        print("\n Default Rate by Income Segment:\n", income_default)

        results['income_default'] = income_default

    else:
        print(" ANNUAL_INCOME missing")

    return results