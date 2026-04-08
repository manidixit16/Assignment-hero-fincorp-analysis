import pandas as pd

def branch_efficiency_analysis(applications, loans, branches):
    print("\n🏢 BRANCH EFFICIENCY ANALYSIS")

    results = {}

    # -----------------------------------
    # MERGE DATA
    # -----------------------------------
    applications['APPLICATION_DATE'] = pd.to_datetime(applications['APPLICATION_DATE'], errors='coerce')
    loans['DISBURSEMENT_DATE'] = pd.to_datetime(loans['DISBURSEMENT_DATE'], errors='coerce')

    merged = applications.merge(loans, on='APPLICATION_ID', how='left') \
                         .merge(branches, on='BRANCH_ID', how='left')

    # -----------------------------------
    # 1. PROCESSING TIME PER BRANCH
    # -----------------------------------
    merged['PROCESSING_DAYS'] = (
        merged['DISBURSEMENT_DATE'] - merged['APPLICATION_DATE']
    ).dt.days

    if 'BRANCH_ID' in merged.columns:
        processing = merged.groupby('BRANCH_ID')['PROCESSING_DAYS'].mean()
        results['processing_time'] = processing

        print("\nAvg Processing Time per Branch:\n", processing.head())

    # -----------------------------------
    # 2. REJECTED APPLICATIONS
    # -----------------------------------
    if 'APPROVAL_STATUS' in applications.columns:
        rejected = applications[
            applications['APPROVAL_STATUS'].str.upper() == 'REJECTED'
        ]

        rejected_counts = rejected.groupby('BRANCH_ID').size()
        results['rejected_counts'] = rejected_counts

        print("\nRejected Applications per Branch:\n", rejected_counts.head())

    # -----------------------------------
    # 3. CUSTOMER SATISFACTION (IF EXISTS)
    # -----------------------------------
    if 'CUSTOMER_SATISFACTION' in applications.columns:
        satisfaction = applications.groupby('BRANCH_ID')['CUSTOMER_SATISFACTION'].mean()
        results['satisfaction'] = satisfaction

        print("\nCustomer Satisfaction by Branch:\n", satisfaction.head())

    return results