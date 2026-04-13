import pandas as pd
def time_to_default(df):
    df['TIME_TO_DEFAULT']=(pd.to_datetime(df['DEFAULT_DATE'])-pd.to_datetime(df['LOAN_START_DATE'])).dt.days
    return df['TIME_TO_DEFAULT'].mean()


import pandas as pd

def time_to_default_analysis(df, loans, defaults):
    print("\n⏳ TIME TO DEFAULT ANALYSIS")

    results = {}

    # -----------------------------------
    # CONVERT DATES
    # -----------------------------------
    loans['DISBURSAL_DATE'] = pd.to_datetime(
        loans['DISBURSAL_DATE'], errors='coerce'
    )

    defaults['DEFAULT_DATE'] = pd.to_datetime(
        defaults['DEFAULT_DATE'], errors='coerce'
    )

    # -----------------------------------
    # MERGE DATA
    # -----------------------------------
    merged = loans.merge(defaults, on='LOAN_ID', how='inner') \
                  .merge(df[['LOAN_ID', 'LOAN_PURPOSE', 'CREDIT_SCORE', 'ANNUAL_INCOME']],
                         on='LOAN_ID', how='left')

    # -----------------------------------
    # CALCULATE TIME TO DEFAULT
    # -----------------------------------
    merged['TIME_TO_DEFAULT'] = (
        merged['DEFAULT_DATE'] - merged['DISBURSAL_DATE']
    ).dt.days

    # Remove invalid values
    merged = merged[merged['TIME_TO_DEFAULT'] > 0]

    # -----------------------------------
    # 1. AVERAGE TIME TO DEFAULT
    # -----------------------------------
    avg_time = merged['TIME_TO_DEFAULT'].mean()
    results['avg_time'] = avg_time

    print(f"\nAverage Time to Default: {avg_time:.2f} days")

    # -----------------------------------
    # 2. BY LOAN PURPOSE
    # -----------------------------------
    if 'LOAN_PURPOSE' in merged.columns:
        purpose_time = merged.groupby('LOAN_PURPOSE')['TIME_TO_DEFAULT'].mean()

        results['purpose_time'] = purpose_time

        print("\nTime to Default by Loan Purpose:\n", purpose_time)

    # -----------------------------------
    # 3. BY DEMOGRAPHICS
    # -----------------------------------
    if 'ANNUAL_INCOME' in merged.columns:
        merged['INCOME_GROUP'] = pd.qcut(
            merged['ANNUAL_INCOME'],
            q=3,
            labels=['Low', 'Medium', 'High']
        )

        income_time = merged.groupby('INCOME_GROUP')['TIME_TO_DEFAULT'].mean()

        results['income_time'] = income_time

        print("\nTime to Default by Income Group:\n", income_time)

    if 'CREDIT_SCORE' in merged.columns:
        merged['CREDIT_SEGMENT'] = pd.cut(
            merged['CREDIT_SCORE'],
            bins=[0, 500, 650, 750, 900],
            labels=['High Risk', 'Medium', 'Good', 'Excellent']
        )

        credit_time = merged.groupby('CREDIT_SEGMENT')['TIME_TO_DEFAULT'].mean()

        results['credit_time'] = credit_time

        print("\nTime to Default by Credit Score:\n", credit_time)

    return results