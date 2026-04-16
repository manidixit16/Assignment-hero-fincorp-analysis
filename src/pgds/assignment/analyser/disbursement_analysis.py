import pandas as pd

def disbursement_efficiency(df):

    print("\n LOAN DISBURSEMENT EFFICIENCY")

    results = {}

    # -----------------------------------
    # 1. PROCESSING TIME
    # -----------------------------------
    if 'APPLICATION_DATE' in df.columns and 'DISBURSAL_DATE' in df.columns:

        df['APPLICATION_DATE'] = pd.to_datetime(df['APPLICATION_DATE'], errors='coerce')
        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')

        df['PROCESSING_DAYS'] = (
            df['DISBURSAL_DATE'] - df['APPLICATION_DATE']
        ).dt.days

        # print("\ BEFORE CLEANING:")
        # print(df['PROCESSING_DAYS'].describe())

        # -----------------------------------
        # DATA CLEANING
        # -----------------------------------
        df_clean = df[
            (df['PROCESSING_DAYS'].notna()) &   # remove NaN
            (df['PROCESSING_DAYS'] >= 0) &      # remove negative
            (df['PROCESSING_DAYS'] <= 120)      # remove unrealistic values
        ].copy()

        # print("\AFTER CLEANING:")
        # print(df_clean['PROCESSING_DAYS'].describe())

        # -----------------------------------
        # AVERAGE + MEDIAN (BETTER)
        # -----------------------------------
        avg_time = df_clean['PROCESSING_DAYS'].mean()
        median_time = df_clean['PROCESSING_DAYS'].median()

        print(f"\n Average Processing Time: {avg_time:.2f} days")
        print(f" Median Processing Time: {median_time:.2f} days")

        results['avg_time'] = avg_time
        results['median_time'] = median_time

    else:
        print(" Missing date columns")
        return results   # stop if dates missing

    # -----------------------------------
    # 2. REGION COMPARISON (FIXED → USE CLEAN DATA)
    # -----------------------------------
    if 'REGION' in df_clean.columns:

        region_time = df_clean.groupby('REGION')['PROCESSING_DAYS'].mean()

        print("\n Processing Time by Region:\n", region_time)

        results['region_time'] = region_time

    else:
        print(" REGION missing")

    # -----------------------------------
    # 3. LOAN PURPOSE ANALYSIS (FIXED)
    # -----------------------------------
    if 'LOAN_PURPOSE' in df_clean.columns:

        purpose_time = df_clean.groupby('LOAN_PURPOSE')['PROCESSING_DAYS'].mean()

        print("\n Processing Time by Loan Purpose:\n", purpose_time)

        results['purpose'] = purpose_time

    else:
        print(" LOAN_PURPOSE not available")

    # -----------------------------------
    # BRANCH LIMITATION
    # -----------------------------------
    print("\n Branch comparison NOT possible")
    print("Reason: No BRANCH_ID linkage in dataset")

    return results



# import pandas as pd
#
# def disbursement_efficiency(df):
#
#     print("\n LOAN DISBURSEMENT EFFICIENCY")
#
#     results = {}
#
#     # -----------------------------------
#     # 1. PROCESSING TIME
#     # -----------------------------------
#     if 'APPLICATION_DATE' in df.columns and 'DISBURSAL_DATE' in df.columns:
#
#         df['APPLICATION_DATE'] = pd.to_datetime(df['APPLICATION_DATE'], errors='coerce')
#         df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')
#
#         df['PROCESSING_DAYS'] = (
#             df['DISBURSAL_DATE'] - df['APPLICATION_DATE']
#         ).dt.days
#         print("CHECK++++++")
#         print(df['PROCESSING_DAYS'].describe())
#         avg_time = df['PROCESSING_DAYS'].mean()
#
#         print(f"\n Average Processing Time: {avg_time:.2f} days")
#
#         results['avg_time'] = avg_time
#
#     else:
#         print(" Missing date columns")
#
#     # -----------------------------------
#     # 2. REGION COMPARISON (ALTERNATIVE)
#     # -----------------------------------
#     if 'REGION' in df.columns:
#
#         region_time = df.groupby('REGION')['PROCESSING_DAYS'].mean()
#
#         print("\n Processing Time by Region:\n", region_time)
#
#         results['region_time'] = region_time
#
#     # -----------------------------------
#     # 3. LOAN PURPOSE ANALYSIS
#     # -----------------------------------
#     if 'LOAN_PURPOSE' in df.columns:
#
#         purpose_time = df.groupby('LOAN_PURPOSE')['PROCESSING_DAYS'].mean()
#
#         print("\n Processing Time by Loan Purpose:\n", purpose_time)
#
#         results['purpose'] = purpose_time
#
#     else:
#         print(" LOAN_PURPOSE not available")
#
#     # -----------------------------------
#     #  BRANCH LIMITATION
#     # -----------------------------------
#     print("\n Branch comparison NOT possible")
#     print("Reason: No BRANCH_ID linkage in dataset")
#
#     return results