def profitability_analysis(df):

    print("\n PROFITABILITY ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. TOTAL INTEREST INCOME
    # -----------------------------------
    if 'LOAN_AMOUNT' in df.columns and 'INTEREST_RATE' in df.columns:

        df['INTEREST_INCOME'] = df['LOAN_AMOUNT'] * df['INTEREST_RATE']

        total_income = df['INTEREST_INCOME'].sum()

        print(f"\n Total Interest Income: {total_income:,.2f}")

        results['total_income'] = total_income

    else:
        print(" Missing loan or interest data")

    # -----------------------------------
    # 2. PROFIT BY LOAN PURPOSE
    # -----------------------------------
    if 'LOAN_PURPOSE' in df.columns:

        purpose_profit = df.groupby('LOAN_PURPOSE')['INTEREST_INCOME'].sum()

        print("\n Profit by Loan Purpose:\n", purpose_profit)

        results['purpose_profit'] = purpose_profit

    else:
        print("LOAN_PURPOSE missing")

    # -----------------------------------
    # 3. REGION PROFITABILITY (ALTERNATIVE)
    # -----------------------------------
    if 'REGION' in df.columns:

        region_profit = df.groupby('REGION')['INTEREST_INCOME'].sum()

        print("\n Profit by Region:\n", region_profit)

        results['region_profit'] = region_profit

    # -----------------------------------
    # BRANCH LIMITATION
    # -----------------------------------
    print("\n Branch profitability analysis NOT possible")
    print("Reason: No linkage between branch dataset and loan data")

    return results