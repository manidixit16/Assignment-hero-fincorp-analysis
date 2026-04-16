def branch_performance_analysis(branches):

    print("\n BRANCH PERFORMANCE ANALYSIS (USING BRANCH DATA ONLY)")

    results = {}

    # -----------------------------------
    # AVAILABLE METRICS
    # -----------------------------------
    print("\n Available Metrics:")
    print("- LOAN_DISBURSEMENT_AMOUNT")
    print("- DELINQUENT_LOANS")
    print("- REGION")

    # -----------------------------------
    # 1. LOAN DISBURSEMENT RANKING
    # -----------------------------------
    loan_rank = branches.sort_values(
        'LOAN_DISBURSEMENT_AMOUNT',
        ascending=False
    )

    results['loan_ranking'] = loan_rank

    print("\n Top Branches by Loan Disbursement:\n", loan_rank.head())

    # -----------------------------------
    # 2. DELINQUENCY (RISK PROXY)
    # -----------------------------------
    delinquency_rank = branches.sort_values(
        'DELINQUENT_LOANS',
        ascending=False
    )

    results['delinquency_ranking'] = delinquency_rank

    print("\n High Delinquency Branches:\n", delinquency_rank.head())

    # -----------------------------------
    # 3. REGION COMPARISON
    # -----------------------------------
    region_perf = branches.groupby('REGION').agg({
        'LOAN_DISBURSEMENT_AMOUNT': 'sum',
        'DELINQUENT_LOANS': 'sum'
    })

    results['region_performance'] = region_perf

    print("\n Region-wise Branch Performance:\n", region_perf)

    # -----------------------------------
    # LIMITATIONS (IMPORTANT)
    # -----------------------------------
    print("\n LIMITATIONS:")

    print("\n Processing Time Efficiency cannot be calculated")
    print("Reason: APPLICATION_DATE and DISBURSAL_DATE are not available in branch dataset")

    print("\n Default Rate cannot be calculated")
    print("Reason: DEFAULT_FLAG or default-level data is not available in branch dataset")

    print("\n Recovery Rate cannot be calculated")
    print("Reason: RECOVERY_AMOUNT is not available in branch dataset")

    print("\n Direct branch-to-loan mapping not available")
    print("Reason: No common key (e.g., BRANCH_ID) linking branch and loan datasets")

    return results