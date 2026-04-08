import pandas as pd

def recovery_effectiveness(df, defaults, branches):
    print("\n💊 RECOVERY EFFECTIVENESS ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. RECOVERY RATE CALCULATION
    # -----------------------------------
    defaults['RECOVERY_RATE'] = (
        defaults['RECOVERY_AMOUNT'] / defaults['DEFAULT_AMOUNT']
    )

    overall_recovery = defaults['RECOVERY_RATE'].mean()
    results['overall_recovery'] = overall_recovery

    print(f"\nOverall Recovery Rate: {overall_recovery:.2%}")

    # -----------------------------------
    # 2. LEGAL ACTION COMPARISON
    # -----------------------------------
    if 'LEGAL_ACTION' in defaults.columns:
        legal_comparison = defaults.groupby('LEGAL_ACTION')['RECOVERY_RATE'].mean()
        results['legal_comparison'] = legal_comparison

        print("\nRecovery by Legal Action:\n", legal_comparison)

    # -----------------------------------
    # 3. BRANCH-WISE RECOVERY
    # -----------------------------------
    # merged = defaults.merge(df[['LOAN_ID', 'REGION']], on='LOAN_ID', how='left') \
    #
    #                  .merge(branches, on='REGION', how='left')
    # -----------------------------------
    # 3. REGION-WISE RECOVERY (REPLACES BRANCH)
    # -----------------------------------

    # Merge REGION from df (comes from customers)
    if 'REGION' in df.columns:

        merged = defaults.merge(
            df[['LOAN_ID', 'REGION']],
            on='LOAN_ID',
            how='left'
        )

        # Recovery Rate
        if 'RECOVERY_AMOUNT' in merged.columns and 'DEFAULT_AMOUNT' in merged.columns:
            merged['RECOVERY_RATE'] = (
                    merged['RECOVERY_AMOUNT'] / merged['DEFAULT_AMOUNT']
            )

        region_recovery = merged.groupby('REGION')['RECOVERY_RATE'].mean()

        results['region_recovery'] = region_recovery

        print("\nRegion-wise Recovery:\n", region_recovery.head())

    else:
        print("⚠️ REGION not available → skipping recovery segmentation")

    # -----------------------------------
    # 4. REGION-WISE RECOVERY (BONUS)
    # -----------------------------------
    if 'REGION' in merged.columns:
        region_recovery = merged.groupby('REGION')['RECOVERY_RATE'].mean()
        results['region_recovery'] = region_recovery

        print("\nRegion-wise Recovery:\n", region_recovery)

    return results