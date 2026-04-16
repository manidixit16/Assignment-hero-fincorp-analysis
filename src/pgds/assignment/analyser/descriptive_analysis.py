import pandas as pd

def descriptive_analysis(df, applications):

    print("\ DESCRIPTIVE ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. DISTRIBUTION ANALYSIS
    # -----------------------------------
    if 'LOAN_AMOUNT' in df.columns:
        results['loan_stats'] = df['LOAN_AMOUNT'].describe()
        print("\nLoan Amount Summary:\n", results['loan_stats'])

    if 'EMI_AMOUNT' in df.columns:
        results['emi_stats'] = df['EMI_AMOUNT'].describe()
        print("\nEMI Summary:\n", results['emi_stats'])

    if 'CREDIT_SCORE' in df.columns:
        results['credit_score_stats'] = df['CREDIT_SCORE'].describe()
        print("\nCredit Score Summary:\n", results['credit_score_stats'])

    # -----------------------------------
    # 2. REGIONAL ANALYSIS
    # -----------------------------------
    if 'REGION' in df.columns:

        regional_loans = df.groupby('REGION')['LOAN_AMOUNT'].sum()
        regional_defaults = df.groupby('REGION')['DEFAULT_FLAG'].mean()

        results['regional_loans'] = regional_loans
        results['regional_defaults'] = regional_defaults

        print("\nLoan Distribution by Region:\n", regional_loans.head())
        print("\nDefault Rate by Region:\n", regional_defaults.head())

    # -----------------------------------
    # 3. MONTHLY APPLICATIONS
    # -----------------------------------
    if 'APPLICATION_DATE' in applications.columns:

        applications['APPLICATION_DATE'] = pd.to_datetime(
            applications['APPLICATION_DATE'], errors='coerce'
        )

        applications = applications[applications['APPLICATION_DATE'].notna()]

        monthly_apps = applications.groupby(
            applications['APPLICATION_DATE'].dt.to_period('M')
        ).size()

        if len(monthly_apps) > 1:
            monthly_apps = monthly_apps.iloc[:-1]

        results['monthly_applications'] = monthly_apps

        print("\nMonthly Applications:\n", monthly_apps.head())

    # -----------------------------------
    # 4. MONTHLY DISBURSEMENT
    # -----------------------------------
    if 'DISBURSAL_DATE' in df.columns:

        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')
        df = df[df['DISBURSAL_DATE'].notna()]

        monthly_disb = df.groupby(
            df['DISBURSAL_DATE'].dt.to_period('M')
        ).size()

        if len(monthly_disb) > 1:
            monthly_disb = monthly_disb.iloc[:-1]

        results['monthly_disbursement'] = monthly_disb

        print("\nMonthly Disbursement:\n", monthly_disb.head())

    # -----------------------------------
    # 5. MONTHLY APPROVAL TREND (NEW FIX)
    # -----------------------------------
    if 'APPROVAL_STATUS' in applications.columns:

        approved = applications[
            applications['APPROVAL_STATUS'].str.upper() == 'APPROVED'
        ]

        monthly_approved = approved.groupby(
            approved['APPLICATION_DATE'].dt.to_period('M')
        ).size()

        if len(monthly_approved) > 1:
            monthly_approved = monthly_approved.iloc[:-1]

        results['monthly_approved'] = monthly_approved

        print("\nMonthly Approved Loans:\n", monthly_approved.head())

    return results