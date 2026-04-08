import pandas as pd

def disbursement_efficiency(applications, loans, branches):
    print("\n⏱️ LOAN DISBURSEMENT EFFICIENCY")

    results = {}
    merged = applications.merge(loans, on='LOAN_ID', how='left')

    # -----------------------------------
    # CREATE PROCESSING DAYS SAFELY
    # -----------------------------------
    if 'APPLICATION_DATE' in merged.columns and 'DISBURSEMENT_DATE' in merged.columns:
        merged['PROCESSING_DAYS'] = (
                merged['DISBURSEMENT_DATE'] - merged['APPLICATION_DATE']
        ).dt.days
    else:
        print("⚠️ Missing date columns → PROCESSING_DAYS not created")

    # -----------------------------------
    # 1. PROCESSING TIME
    # -----------------------------------
    applications['APPLICATION_DATE'] = pd.to_datetime(
        applications['APPLICATION_DATE'], errors='coerce'
    )

    if 'DISBURSEMENT_DATE' in loans.columns:
        loans['DISBURSEMENT_DATE'] = pd.to_datetime(
            loans['DISBURSEMENT_DATE'], errors='coerce'
        )

        merged = applications.merge(loans, on='APPLICATION_ID', how='left')

        merged['PROCESSING_DAYS'] = (
            merged['DISBURSEMENT_DATE'] - merged['APPLICATION_DATE']
        ).dt.days

        avg_processing = merged['PROCESSING_DAYS'].mean()
        results['avg_processing_time'] = avg_processing

        print(f"\nAverage Processing Time: {avg_processing:.2f} days")

    # -----------------------------------
    # 2. REGION COMPARISON
    # -----------------------------------
    if 'REGION' in merged.columns:
        region_time = merged.groupby('REGION')['PROCESSING_DAYS'].mean()
        results['branch_processing'] = region_time

        print("\nProcessing Time by Branch:\n", region_time.head())

    # -----------------------------------
    # 3. LOAN PURPOSE ANALYSIS
    # -----------------------------------
    if 'LOAN_PURPOSE' in merged.columns and 'PROCESSING_DAYS' in merged.columns:
        purpose_trend = merged.groupby('LOAN_PURPOSE')['PROCESSING_DAYS'].mean()
        results['purpose_trend'] = purpose_trend

        print("\nProcessing Time by Loan Purpose:\n", purpose_trend)
    else:
        print("⚠️ Missing LOAN_PURPOSE or PROCESSING_DAYS")
    # if 'LOAN_PURPOSE' in merged.columns:
    #     purpose_trend = merged.groupby('LOAN_PURPOSE')['PROCESSING_DAYS'].mean()
    #     results['purpose_trend'] = purpose_trend
    #
    #     print("\nProcessing Time by Loan Purpose:\n", purpose_trend)

    # -----------------------------------
    # 4. REGION ANALYSIS
    # -----------------------------------
    # merged = merged.merge(branches, on='REGION', how='left')

    if 'REGION' in merged.columns and 'PROCESSING_DAYS' in merged.columns:
        region_trend = merged.groupby('REGION')['PROCESSING_DAYS'].mean()
        results['region_trend'] = region_trend

        print("\nProcessing Time by Region:\n", region_trend)

    return results