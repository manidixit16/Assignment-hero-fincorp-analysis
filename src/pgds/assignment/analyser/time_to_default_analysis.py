import pandas as pd

def time_to_default_analysis(df):

    print("\n TIME TO DEFAULT ANALYSIS")

    results = {}

    # -----------------------------------
    # CHECK REQUIRED COLUMNS
    # -----------------------------------
    if 'DEFAULT_DATE' in df.columns and 'DISBURSAL_DATE' in df.columns:

        df['DEFAULT_DATE'] = pd.to_datetime(df['DEFAULT_DATE'], errors='coerce')
        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')

        # Calculate time to default
        df['TIME_TO_DEFAULT'] = (
            df['DEFAULT_DATE'] - df['DISBURSAL_DATE']
        ).dt.days

        # Keep valid values only
        df = df[df['TIME_TO_DEFAULT'] >= 0]

        # -----------------------------------
        # 1. AVG TIME TO DEFAULT
        # -----------------------------------
        avg_time = df['TIME_TO_DEFAULT'].mean()

        print(f"\n Avg Time to Default: {avg_time:.2f} days")

        results['avg_time'] = avg_time

        # -----------------------------------
        # 2. PURPOSE-WISE
        # -----------------------------------
        if 'LOAN_PURPOSE' in df.columns:

            purpose_time = df.groupby('LOAN_PURPOSE')['TIME_TO_DEFAULT'].mean()

            print("\n Time to Default by Purpose:\n", purpose_time)

            results['purpose'] = purpose_time

        # -----------------------------------
        # 3. DEMOGRAPHIC COMPARISON
        # -----------------------------------
        # Detect income column
        income_col = None
        for col in df.columns:
            if 'INCOME' in col.upper():
                income_col = col
                break

        if 'CREDIT_SCORE' in df.columns:

            df['CREDIT_SEGMENT'] = pd.cut(
                df['CREDIT_SCORE'],
                bins=[300, 600, 750, 900],
                labels=['Low', 'Medium', 'High']
            )

            if income_col:

                df['INCOME_SEGMENT'] = pd.qcut(
                    df[income_col],
                    3,
                    labels=['Low', 'Medium', 'High']
                )

                demo_time = df.groupby(
                    ['CREDIT_SEGMENT', 'INCOME_SEGMENT']
                )['TIME_TO_DEFAULT'].mean()

                print("\ Time to Default by Customer Segment:\n", demo_time)

                results['demographic'] = demo_time

    else:
        print(" Required date columns missing")

    return results