"""
Loan Disbursement Analysis
Analyses processing time efficiency across regions, loan amounts,
and loan purposes to surface operational bottlenecks.
"""
import pandas as pd


def disbursement_efficiency(df):
    """
    Compute processing time (application to disbursal) broken down
    by region, loan amount bracket, and loan purpose.
    """
    print("\n[TASK 11] Loan Disbursement Efficiency")

    efficiency = {}

    # --------------------------------------------------
    # 1. COMPUTE PROCESSING TIME
    # --------------------------------------------------
    if 'APPLICATION_DATE' in df.columns and 'DISBURSAL_DATE' in df.columns:
        df['APPLICATION_DATE'] = pd.to_datetime(df['APPLICATION_DATE'], errors='coerce')
        df['DISBURSAL_DATE']   = pd.to_datetime(df['DISBURSAL_DATE'],   errors='coerce')

        df['PROCESSING_DAYS'] = (df['DISBURSAL_DATE'] - df['APPLICATION_DATE']).dt.days

        valid = df[df['PROCESSING_DAYS'].between(0, 365)]
        efficiency['processing_summary'] = valid['PROCESSING_DAYS'].describe()
        print("\nProcessing Time Summary:\n", efficiency['processing_summary'])

        # BY REGION
        if 'REGION' in valid.columns:
            by_region = valid.groupby('REGION')['PROCESSING_DAYS'].mean()
            efficiency['by_region'] = by_region
            print("\nAvg Processing Days by Region:\n", by_region)

        # BY LOAN PURPOSE
        if 'LOAN_PURPOSE' in valid.columns:
            by_purpose = valid.groupby('LOAN_PURPOSE')['PROCESSING_DAYS'].mean()
            efficiency['by_purpose'] = by_purpose
            print("\nAvg Processing Days by Loan Purpose:\n", by_purpose)

        # BY LOAN AMOUNT BRACKET
        if 'LOAN_AMOUNT' in valid.columns:
            amount_bins   = [0, 10000, 20000, 30000, float('inf')]
            amount_labels = ['<10k', '10k-20k', '20k-30k', '>30k']
            valid['AMOUNT_BRACKET'] = pd.cut(
                valid['LOAN_AMOUNT'], bins=amount_bins, labels=amount_labels
            )
            by_amount = valid.groupby('AMOUNT_BRACKET')['PROCESSING_DAYS'].mean()
            efficiency['by_amount'] = by_amount
            print("\nAvg Processing Days by Loan Amount Bracket:\n", by_amount)
    else:
        print(" APPLICATION_DATE or DISBURSAL_DATE missing — cannot compute processing time")

    return efficiency
