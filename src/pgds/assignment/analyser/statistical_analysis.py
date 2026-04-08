import pandas as pd

def advanced_statistical_analysis(df, branches=None, defaults=None):
    print("\n📈 ADVANCED STATISTICAL ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. CORRELATION (DEFAULT RISK)
    # -----------------------------------
    cols = [
        'CREDIT_SCORE',
        'LOAN_AMOUNT',
        'INTEREST_RATE',
        'OVERDUE_AMOUNT',
        'DEFAULT_FLAG'
    ]

    cols = [c for c in cols if c in df.columns]

    if len(cols) >= 2:
        corr = df[cols].corr()
        results['default_risk_corr'] = corr
        print("\nDefault Risk Correlation:\n", corr)

    # -----------------------------------
    # 2. PAIRWISE CORRELATION (ADVANCED)
    # -----------------------------------
    if defaults is not None:
        defaults['RECOVERY_RATE'] = (
            defaults['RECOVERY_AMOUNT'] / defaults['DEFAULT_AMOUNT']
        )

        pair_cols = [
            'EMI_AMOUNT',
            'RECOVERY_RATE',
            'DEFAULT_AMOUNT'
        ]

        merged = df.merge(defaults, on='LOAN_ID', how='left')

        pair_cols = [c for c in pair_cols if c in merged.columns]

        if len(pair_cols) >= 2:
            pair_corr = merged[pair_cols].corr()
            results['pairwise_corr'] = pair_corr
            print("\nPairwise Correlation:\n", pair_corr)

    # -----------------------------------
    # 3. BRANCH-LEVEL CORRELATION
    # -----------------------------------
    if branches is not None:
        if 'BRANCH_ID' not in df.columns:
            print("⚠️ ********** BRANCH_ID not available in dataset → skipping branch-level correlation")
        else:
             print("######################")
             branch_cols = [
            'DELINQUENT_LOANS',
            'LOAN_DISBURSEMENT_AMOUNT'
            ]

             merged = df.merge(branches, on='BRANCH_ID', how='left')

             merged['RECOVERY_RATE'] = merged.get('RECOVERY_AMOUNT', 0) / merged.get('DEFAULT_AMOUNT', 1)

             branch_cols = [c for c in branch_cols if c in merged.columns]

             branch_cols.append('RECOVERY_RATE')

             if len(branch_cols) >= 2:
                 branch_corr = merged[branch_cols].corr()
                 results['branch_corr'] = branch_corr

                 print("\nBranch-Level Correlation:\n", branch_corr)

    return results