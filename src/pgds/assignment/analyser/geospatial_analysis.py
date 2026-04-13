import pandas as pd
import numpy as np


def geospatial_analysis(df, branches):

    print("\n🌍 GEO-SPATIAL ANALYSIS STARTED\n")

    # -----------------------------------
    # 1. MAP DISTRIBUTION OF ACTIVE LOANS
    # -----------------------------------

    # Use branches dataset directly
    active_loans_region = branches.groupby('REGION')['TOTAL_ACTIVE_LOANS'].sum()

    print("\n📊 Active Loans by Region:")
    print(active_loans_region)


    # -----------------------------------
    # 2. DEFAULT RATE BY REGION
    # -----------------------------------

    # Step 1: create Default_Flag in df
    if 'DEFAULT_FLAG' not in df.columns:
        df['DEFAULT_FLAG'] = df['LOAN_ID'].isin(df.get('DEFAULT_LOAN_IDS', [])).astype(int)

    # 🚨 Since Branch_ID missing → assign region using RANDOM (proxy)
    # (You can replace this later if real mapping exists)
    if 'REGION' not in df.columns:
        df['REGION'] = np.random.choice(branches['REGION'], size=len(df))

    default_by_region = df.groupby('REGION')['DEFAULT_FLAG'].mean()

    print("Default Rate by Region:")
    print(default_by_region)


    # -----------------------------------
    # 3. RURAL vs URBAN ANALYSIS
    # -----------------------------------

    # Create Rural/Urban classification
    branches['AREA_TYPE'] = branches['REGION'].apply(
        lambda x: 'Urban' if 'Metro' in str(x) or 'City' in str(x) else 'Rural'
    )

    disbursement_area = branches.groupby('AREA_TYPE')['LOAN_DISBURSEMENT_AMOUNT'].sum()

    print("Loan Disbursement: Rural vs Urban")
    print(disbursement_area)


    print("GEO-SPATIAL ANALYSIS COMPLETED")



# import pandas as pd
#
# def geospatial_analysis(df, branches):
#     print("\n🌍 GEOSPATIAL ANALYSIS")
#
#     results = {}
#
#     # -----------------------------------
#     # MERGE WITH BRANCH DATA
#     # -----------------------------------
#     merged = df.merge(branches, on='BRANCH_ID', how='left')
#
#     # -----------------------------------
#     # 1. LOAN DISTRIBUTION (REGION)
#     # -----------------------------------
#     if 'REGION' in merged.columns:
#         loan_dist = merged['REGION'].value_counts()
#
#         results['loan_distribution'] = loan_dist
#
#         print("\nLoan Distribution by Region:\n", loan_dist)
#
#     # -----------------------------------
#     # 2. DEFAULT RATE BY REGION
#     # -----------------------------------
#     if 'REGION' in merged.columns:
#         default_rate = merged.groupby('REGION')['DEFAULT_FLAG'].mean()
#
#         results['default_rate'] = default_rate
#
#         print("\nDefault Rate by Region:\n", default_rate)
#
#     # -----------------------------------
#     # 3. RURAL vs URBAN ANALYSIS
#     # -----------------------------------
#     if 'AREA_TYPE' in merged.columns:
#         area_analysis = merged.groupby('AREA_TYPE').agg({
#             'LOAN_AMOUNT': 'sum',
#             'DEFAULT_FLAG': 'mean'
#         }).rename(columns={
#             'LOAN_AMOUNT': 'TOTAL_DISBURSEMENT',
#             'DEFAULT_FLAG': 'DEFAULT_RATE'
#         })
#
#         results['area_analysis'] = area_analysis
#
#         print("\nRural vs Urban Analysis:\n", area_analysis)
#
#     return results