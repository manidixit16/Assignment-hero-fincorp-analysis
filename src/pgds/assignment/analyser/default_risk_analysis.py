import pandas as pd

def default_risk_analysis(df, branches):

    print("\n DEFAULT RISK ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. CORRELATION (LOAN ATTRIBUTES)
    # -----------------------------------
    cols = ['LOAN_AMOUNT', 'INTEREST_RATE', 'CREDIT_SCORE', 'DEFAULT_FLAG']

    analysis_df = df[cols].dropna()

    corr_main = analysis_df.corr()
    results['loan_correlation'] = corr_main

    print("\n Loan Attribute Correlation:\n", corr_main)

    # -----------------------------------
    # 2. PAIRWISE CORRELATION
    # -----------------------------------
    pair_cols = ['EMI_AMOUNT', 'OVERDUE_AMOUNT', 'DEFAULT_AMOUNT']

    pair_df = df[pair_cols].dropna()

    corr_pair = pair_df.corr()
    results['pairwise_correlation'] = corr_pair

    print("\n📊 Pairwise Correlation:\n", corr_pair)

    # -----------------------------------
    # 3. BRANCH vs DEFAULT
    # -----------------------------------
    if 'REGION' in df.columns:

        # Default rate by region
        region_default = df.groupby('REGION')['DEFAULT_FLAG'].mean()

        # Merge with branch metrics
        branch_analysis = branches.merge(
            region_default,
            on='REGION',
            how='left'
        )

        branch_corr = branch_analysis[
            ['DELINQUENT_LOANS', 'LOAN_DISBURSEMENT_AMOUNT', 'DEFAULT_FLAG']
        ].corr()

        results['branch_correlation'] = branch_corr

        print("\nBranch vs Default Correlation:\n", branch_corr)

    return results