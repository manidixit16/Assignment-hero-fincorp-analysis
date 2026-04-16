def transaction_recovery_analysis(df, transactions):

    print("\n TRANSACTION & RECOVERY ANALYSIS")

    results = {}

    # -----------------------------------
    # 7.1 PENALTY ANALYSIS
    # -----------------------------------
    if 'TRANSACTION_TYPE' in transactions.columns:

        penalty = transactions[
            transactions['TRANSACTION_TYPE'].str.upper() == 'PENALTY'
        ]

        penalty_count = len(penalty)
        total_txn = len(transactions)

        penalty_ratio = penalty_count / total_txn if total_txn > 0 else 0

        print("\n Penalty Ratio:", penalty_ratio)

        results['penalty_ratio'] = penalty_ratio

    # -----------------------------------
    # OVERDUE TREND
    # -----------------------------------
    if 'OVERDUE_AMOUNT' in df.columns:

        overdue_trend = df['OVERDUE_AMOUNT'].describe()

        print("\n Overdue Summary:\n", overdue_trend)

        results['overdue'] = overdue_trend

    # -----------------------------------
    # 7.2 RECOVERY BY REASON
    # -----------------------------------
    if 'DEFAULT_REASON' in df.columns:

        recovery_reason = df.groupby('DEFAULT_REASON')['RECOVERY_RATE'].mean()

        print("\n Recovery by Default Reason:\n", recovery_reason)

        results['recovery_reason'] = recovery_reason

    # -----------------------------------
    # RECOVERY BY LEGAL ACTION
    # -----------------------------------
    if 'LEGAL_ACTION' in df.columns:

        recovery_legal = df.groupby('LEGAL_ACTION')['RECOVERY_RATE'].mean()

        print("\n Recovery by Legal Action:\n", recovery_legal)

        results['recovery_legal'] = recovery_legal

    # -----------------------------------
    # 7.3 REGION COMPARISON
    # -----------------------------------
    if 'REGION' in df.columns:

        region_recovery = df.groupby('REGION')['RECOVERY_RATE'].mean()

        print("\n Recovery by Region:\n", region_recovery)

        results['region_recovery'] = region_recovery

    # -----------------------------------
    #  BRANCH LIMITATION
    # -----------------------------------
    print("\n Branch-level recovery comparison NOT possible")
    print("Reason: No linkage between branch dataset and loan/default data")

    return results