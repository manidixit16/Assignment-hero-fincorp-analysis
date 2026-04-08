import pandas as pd

def profitability_analysis(df, branches=None):
    print("\n💰 PROFITABILITY ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. INTEREST INCOME CALCULATION
    # -----------------------------------
    if 'LOAN_AMOUNT' in df.columns and 'INTEREST_RATE' in df.columns:
        df['INTEREST_INCOME'] = df['LOAN_AMOUNT'] * df['INTEREST_RATE']

        total_income = df['INTEREST_INCOME'].sum()
        results['total_income'] = total_income

        print(f"\nTotal Interest Income: {total_income:.2f}")

    # -----------------------------------
    # 2. PROFIT BY LOAN PURPOSE
    # -----------------------------------
    if 'LOAN_PURPOSE' in df.columns:
        purpose_profit = df.groupby('LOAN_PURPOSE')['INTEREST_INCOME'].sum()

        results['purpose_profit'] = purpose_profit

        print("\nProfit by Loan Purpose:\n", purpose_profit)

    # -----------------------------------
    # 3. BRANCH PROFITABILITY
    # -----------------------------------
    if 'BRANCH_ID' in df.columns:
        branch_profit = df.groupby('BRANCH_ID')['INTEREST_INCOME'].sum()

        results['branch_profit'] = branch_profit

        print("\nBranch Profitability:\n", branch_profit.head())

    # -----------------------------------
    # 4. REGION PROFITABILITY
    # -----------------------------------
    if branches is not None:
        # merged = df.merge(branches, on='BRANCH_ID', how='left')

        if 'REGION' in df.columns and 'INTEREST_INCOME' in df.columns:
            region_profit = df.groupby('REGION')['INTEREST_INCOME'].sum()

            results['region_profit'] = region_profit

            print("\nRegion Profitability:\n", region_profit)

    return results