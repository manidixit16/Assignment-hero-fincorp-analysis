"""
profitabilityAnalyser.py
Legacy camelCase module retained for compatibility with reference repo.
Full Task 12 implementation is in analyser/profitability_analysis.py
"""


def profitability(df):
    """
    Compute total interest income and break it down by loan purpose.

    Returns
    -------
    dict with total_interest and by_purpose summary
    """
    if 'INTEREST_INCOME' not in df.columns:
        if 'INTEREST_RATE' in df.columns and 'LOAN_TERM' in df.columns:
            df = df.copy()
            df['INTEREST_INCOME'] = (
                df['LOAN_AMOUNT'] * (df['INTEREST_RATE'] / 100) * (df['LOAN_TERM'] / 12)
            )
        else:
            print("  ⚠️  Cannot compute INTEREST_INCOME — missing columns")
            return {}

    total_interest = df['INTEREST_INCOME'].sum()
    print(f"\n📌 Total Interest Income: ₹{total_interest:,.0f}")

    by_purpose = None
    if 'LOAN_PURPOSE' in df.columns:
        by_purpose = df.groupby('LOAN_PURPOSE')['INTEREST_INCOME'].sum() \
                       .sort_values(ascending=False)
        print("\n📌 Interest Income by Loan Purpose:")
        print(by_purpose.round(0).to_string())

    by_region = None
    if 'REGION' in df.columns:
        by_region = df.groupby('REGION')['INTEREST_INCOME'].sum() \
                      .sort_values(ascending=False)
        print("\n📌 Interest Income by Region:")
        print(by_region.round(0).to_string())

    return {
        "total_interest": round(total_interest, 2),
        "by_purpose":     by_purpose,
        "by_region":      by_region,
    }
