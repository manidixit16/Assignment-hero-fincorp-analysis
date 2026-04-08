import pandas as pd

def transaction_and_recovery_analysis(df, transactions, defaults, branches):
    print("\n💸 TRANSACTION & RECOVERY ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. PENALTY PAYMENTS ANALYSIS
    # -----------------------------------
    if 'TRANSACTION_TYPE' in transactions.columns:
        penalty = transactions[
            transactions['TRANSACTION_TYPE'].str.upper() == 'PENALTY'
        ]

        penalty_count = len(penalty)
        total_transactions = len(transactions)

        penalty_ratio = penalty_count / total_transactions if total_transactions > 0 else 0

        results['penalty_ratio'] = penalty_ratio

        print(f"\nPenalty Transaction Ratio: {penalty_ratio:.2%}")

    # -----------------------------------
    # 2. OVERDUE TRENDS
    # -----------------------------------
    if 'OVERDUE_AMOUNT' in df.columns:
        overdue_trend = df.groupby('LOAN_ID')['OVERDUE_AMOUNT'].mean()

        results['overdue_trend'] = overdue_trend

        print("\nOverdue Trend Sample:\n", overdue_trend.head())

    # -----------------------------------
    # 3. RECOVERY RATE
    # -----------------------------------
    defaults['RECOVERY_RATE'] = (
        defaults['RECOVERY_AMOUNT'] / defaults['DEFAULT_AMOUNT']
    )

    # -----------------------------------
    # 4. BY DEFAULT REASON
    # -----------------------------------
    if 'DEFAULT_REASON' in defaults.columns:
        reason_recovery = defaults.groupby('DEFAULT_REASON')['RECOVERY_RATE'].mean()
        results['recovery_by_reason'] = reason_recovery

        print("\nRecovery by Default Reason:\n", reason_recovery)

    # -----------------------------------
    # 5. BY LEGAL ACTION
    # -----------------------------------
    if 'LEGAL_ACTION' in defaults.columns:
        legal_recovery = defaults.groupby('LEGAL_ACTION')['RECOVERY_RATE'].mean()
        results['recovery_by_legal'] = legal_recovery

        print("\nRecovery by Legal Action:\n", legal_recovery)

    # -----------------------------------
    # 6. REGION COMPARISON
    # -----------------------------------
    # merged = df.merge(branches, on='BRANCH_ID', how='left') \
    #            .merge(defaults, on='LOAN_ID', how='left')
    merged = df.merge(defaults, on='LOAN_ID', how='left')

    if 'REGION' in merged.columns:
        region_recovery = merged.groupby('REGION')['RECOVERY_RATE'].mean()
        results['region_recovery'] = region_recovery

        print("\nRecovery by Region:\n", region_recovery)

    # -----------------------------------
    # 7. BRANCH COMPARISON
    # -----------------------------------
    if 'REGION' in merged.columns:
        region_recovery = merged.groupby('REGION')['RECOVERY_RATE'].mean()
        results['region_recovery'] = region_recovery

        print("\nRecovery by Region:\n", region_recovery)
    # branch_recovery = merged.groupby('BRANCH_ID')['RECOVERY_RATE'].mean()
    # results['branch_recovery'] = branch_recovery
    #
    # print("\nRecovery by Branch:\n", branch_recovery.head())

    return results