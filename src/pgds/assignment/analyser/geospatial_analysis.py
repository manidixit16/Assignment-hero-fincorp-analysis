import pandas as pd

def geospatial_analysis(df, branches):
    print("\n🌍 GEOSPATIAL ANALYSIS")

    results = {}

    # -----------------------------------
    # MERGE WITH BRANCH DATA
    # -----------------------------------
    merged = df.merge(branches, on='BRANCH_ID', how='left')

    # -----------------------------------
    # 1. LOAN DISTRIBUTION (REGION)
    # -----------------------------------
    if 'REGION' in merged.columns:
        loan_dist = merged['REGION'].value_counts()

        results['loan_distribution'] = loan_dist

        print("\nLoan Distribution by Region:\n", loan_dist)

    # -----------------------------------
    # 2. DEFAULT RATE BY REGION
    # -----------------------------------
    if 'REGION' in merged.columns:
        default_rate = merged.groupby('REGION')['DEFAULT_FLAG'].mean()

        results['default_rate'] = default_rate

        print("\nDefault Rate by Region:\n", default_rate)

    # -----------------------------------
    # 3. RURAL vs URBAN ANALYSIS
    # -----------------------------------
    if 'AREA_TYPE' in merged.columns:
        area_analysis = merged.groupby('AREA_TYPE').agg({
            'LOAN_AMOUNT': 'sum',
            'DEFAULT_FLAG': 'mean'
        }).rename(columns={
            'LOAN_AMOUNT': 'TOTAL_DISBURSEMENT',
            'DEFAULT_FLAG': 'DEFAULT_RATE'
        })

        results['area_analysis'] = area_analysis

        print("\nRural vs Urban Analysis:\n", area_analysis)

    return results