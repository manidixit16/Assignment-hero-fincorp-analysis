def loan_application_analysis(applications):

    print("\n LOAN APPLICATION INSIGHTS")

    results = {}

    # -----------------------------------
    # STANDARDIZE COLUMN NAMES
    # -----------------------------------
    applications.columns = [col.upper() for col in applications.columns]

    # -----------------------------------
    # 1. APPROVAL / REJECTION RATE
    # -----------------------------------
    if 'APPROVAL_STATUS' in applications.columns:

        status_counts = applications['APPROVAL_STATUS'].value_counts(normalize=True)

        print("\n Approval/Rejection Rate:\n", status_counts)

        results['approval_rate'] = status_counts

    else:
        print(" APPROVAL_STATUS missing")

    # -----------------------------------
    # 2. REJECTION REASONS
    # -----------------------------------
    reason_col = None

    for col in applications.columns:
        if 'REASON' in col:
            reason_col = col
            break

    if reason_col:

        rejected = applications[
            applications['APPROVAL_STATUS'].str.upper() == 'REJECTED'
        ]

        reason_counts = rejected[reason_col].value_counts()

        print(f"\n Rejection Reasons ({reason_col}):\n", reason_counts)

        results['rejection_reason'] = reason_counts

    else:
        print(" No rejection reason column found")

    # -----------------------------------
    # 3. PROCESSING FEE ANALYSIS
    # -----------------------------------
    fee_col = None

    for col in applications.columns:
        if 'FEE' in col:
            fee_col = col
            break

    if fee_col:

        fee_analysis = applications.groupby('APPROVAL_STATUS')[fee_col].mean()

        print(f"\n Avg Processing Fee ({fee_col}):\n", fee_analysis)

        results['fee_analysis'] = fee_analysis

    else:
        print(" No processing fee column found")

    return results