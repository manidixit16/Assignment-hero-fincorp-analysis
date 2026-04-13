import pandas as pd

def branch_efficiency_analysis(applications, loans, branches):

    print("\n🏢 BRANCH EFFICIENCY ANALYSIS")

    results = {}

    # -----------------------------------
    # STANDARDIZE COLUMNS
    # -----------------------------------
    applications.columns = [col.upper() for col in applications.columns]
    loans.columns = [col.upper() for col in loans.columns]
    branches.columns = [col.upper() for col in branches.columns]

    # -----------------------------------
    # CORRECT MERGE (FIXED)
    # -----------------------------------
    merged = applications.merge(loans, on='LOAN_ID', how='left')

    # -----------------------------------
    # DATE CONVERSION
    # -----------------------------------
    if 'APPLICATION_DATE' in merged.columns and 'DISBURSAL_DATE' in merged.columns:

        merged['PROCESSING_DAYS'] = (
            merged['DISBURSAL_DATE'] - merged['APPLICATION_DATE']
        ).dt.days

        merged = merged[merged['PROCESSING_DAYS'].notna()]

    else:
        print("⚠️ Missing date columns")
        return results

    # -----------------------------------
    # 1. PROCESSING TIME (NO BRANCH_ID → USE REGION)
    # -----------------------------------
    if 'REGION' in merged.columns:
        processing = merged.groupby('REGION')['PROCESSING_DAYS'].mean()
        results['processing_time'] = processing

        print("\nAvg Processing Time per Region:\n", processing.head())
    else:
        print("⚠️ REGION missing")

    # -----------------------------------
    # 2. REJECTED APPLICATIONS
    # -----------------------------------
    if 'APPROVAL_STATUS' in applications.columns:

        rejected = applications[
            applications['APPROVAL_STATUS'].str.upper() == 'REJECTED'
        ]

        if 'REGION' in rejected.columns:
            rejected_counts = rejected.groupby('REGION').size()
            results['rejected_counts'] = rejected_counts

            print("\nRejected Applications per Region:\n", rejected_counts.head())
        else:
            print("⚠️ REGION missing in applications")

    # -----------------------------------
    # 3. CUSTOMER SATISFACTION
    # -----------------------------------
    if 'CUSTOMER_SATISFACTION' in applications.columns:

        if 'REGION' in applications.columns:
            satisfaction = applications.groupby('REGION')['CUSTOMER_SATISFACTION'].mean()
            results['satisfaction'] = satisfaction

            print("\nCustomer Satisfaction by Region:\n", satisfaction.head())

    return results