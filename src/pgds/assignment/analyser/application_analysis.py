import pandas as pd

def application_insights(applications):
    print("\n LOAN APPLICATION INSIGHTS")

    results = {}

    # -----------------------------------
    # 1. APPROVAL / REJECTION RATE
    # -----------------------------------
    if 'APPROVAL_STATUS' in applications.columns:
        approval_rate = applications['APPROVAL_STATUS'].value_counts(normalize=True)

        results['approval_rate'] = approval_rate

        print("\nApproval / Rejection Rates:\n", approval_rate)

    # -----------------------------------
    # 2. REJECTION REASONS
    # -----------------------------------
    if 'REJECTION_REASON' in applications.columns:
        rejection = applications[
            applications['APPROVAL_STATUS'].str.upper() == 'REJECTED'
        ]

        reason_counts = rejection['REJECTION_REASON'].value_counts()

        results['rejection_reasons'] = reason_counts

        print("\nTop Rejection Reasons:\n", reason_counts.head())

    # -----------------------------------
    # 3. PROCESSING FEE COMPARISON
    # -----------------------------------
    if 'PROCESSING_FEE' in applications.columns:
        fee_comparison = applications.groupby('APPROVAL_STATUS')['PROCESSING_FEE'].mean()

        results['fee_comparison'] = fee_comparison

        print("\nProcessing Fee Comparison:\n", fee_comparison)

    return results