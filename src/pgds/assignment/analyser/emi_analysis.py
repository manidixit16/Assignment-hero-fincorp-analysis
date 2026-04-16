import pandas as pd

def emi_analysis(df):

    print("\n EMI ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. EMI vs DEFAULT PROBABILITY
    # -----------------------------------
    if 'EMI_AMOUNT' in df.columns and 'DEFAULT_FLAG' in df.columns:

        emi_default = df.groupby(pd.qcut(df['EMI_AMOUNT'], 5))['DEFAULT_FLAG'].mean()

        print("\n Default Probability by EMI Segment:\n", emi_default)

        results['emi_default'] = emi_default

    else:
        print(" EMI or DEFAULT_FLAG missing")

    # -----------------------------------
    # 2. EMI THRESHOLD ANALYSIS
    # -----------------------------------
    if 'EMI_AMOUNT' in df.columns:

        df['EMI_BIN'] = pd.qcut(df['EMI_AMOUNT'], 5)

        threshold = df.groupby('EMI_BIN')['DEFAULT_FLAG'].mean()

        print("\n EMI Threshold Analysis:\n", threshold)

        results['emi_threshold'] = threshold

    # -----------------------------------
    # 3. LOAN TYPE ANALYSIS (NOT POSSIBLE)
    # -----------------------------------
    print("\n Loan Type Comparison NOT possible")
    print("Reason: LOAN_TYPE column not available in dataset")

    return results