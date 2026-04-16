import pandas as pd

def advanced_statistical_analysis(df, branches):

    print("\n ADVANCED STATISTICAL ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. DEFAULT RISK CORRELATION
    # -----------------------------------
    cols = [
        'CREDIT_SCORE',
        'LOAN_AMOUNT',
        'INTEREST_RATE',
        'OVERDUE_AMOUNT',
        'DEFAULT_FLAG'
    ]

    available_cols = [col for col in cols if col in df.columns]

    if len(available_cols) >= 2:

        corr = df[available_cols].corr()
        results['default_corr'] = corr

        print("\n Default Risk Correlation:\n", corr)

    else:
        print("  Missing columns for correlation")

    # -----------------------------------
    # 2. PAIRWISE CORRELATION
    # -----------------------------------
    pair_cols = ['EMI_AMOUNT', 'RECOVERY_RATE', 'DEFAULT_AMOUNT']

    available_pair = [col for col in pair_cols if col in df.columns]

    if len(available_pair) >= 2:

        corr_pair = df[available_pair].corr()
        results['pairwise_corr'] = corr_pair

        print("\n Pairwise Correlation:\n", corr_pair)

    # -----------------------------------
    # 3. BRANCH LEVEL (LIMITED)
    # -----------------------------------
    print("\n  Branch-Level Analysis Limitation:")
    print("Branch dataset is NOT linked with loan dataset.")
    print("→ Cannot compute true branch-level recovery or efficiency.")

    print("\n Performing limited branch analysis using available data...")

    branch_corr = branches[['DELINQUENT_LOANS', 'LOAN_DISBURSEMENT_AMOUNT']].corr()

    results['branch_corr'] = branch_corr

    print("\n Branch Internal Correlation:\n", branch_corr)

    return results