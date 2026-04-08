"""
TASK 12: Profitability Analysis
- Calculate total interest income generated across all loans
- Identify the most profitable loan purposes based on interest earnings
- Compare profitability metrics for branches across regions
"""

import pandas as pd


def profitability(df, branches=None):
    """
    Compute interest income and profitability metrics across
    loan purposes, regions, and branches.

    Returns
    -------
    dict with keys: total_interest_income, income_by_purpose,
                    income_by_region, income_by_branch, income_by_term,
                    net_profitability (income minus default loss estimate)
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 12 — Profitability Analysis")
    print("="*55)

    df = df.copy()

    # ── 1. Compute interest income ────────────────────────────────────────────
    if 'INTEREST_INCOME' not in df.columns:
        if 'INTEREST_RATE' in df.columns and 'LOAN_TERM' in df.columns:
            df['INTEREST_INCOME'] = (
                df['LOAN_AMOUNT'] * (df['INTEREST_RATE'] / 100) * (df['LOAN_TERM'] / 12)
            )

    if 'INTEREST_INCOME' not in df.columns:
        print("  ⚠️  Cannot compute INTEREST_INCOME — skipping Task 12")
        return results

    total_income = df['INTEREST_INCOME'].sum()
    results['total_interest_income'] = round(total_income, 2)
    print(f"\n📌 Total Estimated Interest Income : ₹{total_income:,.0f}")
    print(f"   (₹{total_income/1e9:.2f} Billion)")

    # ── 2. Income by loan purpose ─────────────────────────────────────────────
    if 'LOAN_PURPOSE' in df.columns:
        income_purpose = df.groupby('LOAN_PURPOSE').agg(
            Total_Interest_Income=('INTEREST_INCOME', 'sum'),
            Avg_Interest_Income=('INTEREST_INCOME', 'mean'),
            Loan_Count=('LOAN_ID', 'count'),
            Avg_Interest_Rate=('INTEREST_RATE', 'mean')
        ).round(2).sort_values('Total_Interest_Income', ascending=False)
        income_purpose['Income_Share_%'] = (
            income_purpose['Total_Interest_Income'] / total_income * 100
        ).round(2)
        results['income_by_purpose'] = income_purpose
        print("\n📌 Interest Income by Loan Purpose (ranked):")
        print(income_purpose.to_string())

    # ── 3. Income by region ───────────────────────────────────────────────────
    if 'REGION' in df.columns:
        income_region = df.groupby('REGION').agg(
            Total_Interest_Income=('INTEREST_INCOME', 'sum'),
            Total_Disbursement=('LOAN_AMOUNT', 'sum'),
            Avg_Interest_Rate=('INTEREST_RATE', 'mean'),
            Loan_Count=('LOAN_ID', 'count')
        ).round(2).sort_values('Total_Interest_Income', ascending=False)
        income_region['Yield_%'] = (
            income_region['Total_Interest_Income'] / income_region['Total_Disbursement'] * 100
        ).round(2)
        results['income_by_region'] = income_region
        print("\n📌 Interest Income by Region:")
        print(income_region.to_string())

    # ── 4. Income by region (detailed) ───────────────────────────────────────
    if branches is not None and 'REGION' in df.columns:
        br_income = branches.groupby('REGION').agg(
            Branch_Count=('BRANCH_ID', 'count'),
            Total_Disbursement=('LOAN_DISBURSEMENT_AMOUNT', 'sum')
        )
        region_inc = df.groupby('REGION')['INTEREST_INCOME'].sum().reset_index()
        region_inc.columns = ['REGION', 'Interest_Income']
        br_inc_merged = br_income.merge(region_inc, on='REGION', how='left')
        results['income_by_branch'] = br_inc_merged.sort_values('Interest_Income', ascending=False)
        print("\n📌 Interest Income by Region (with branch data):")
        print(br_inc_merged.to_string())

    # ── 5. Net profitability (income minus estimated default loss) ────────────
    if 'DEFAULT_AMOUNT' in df.columns and 'DEFAULT_FLAG' in df.columns:
        total_default_loss = df['DEFAULT_AMOUNT'].sum()
        net_profit = total_income - total_default_loss
        results['net_profitability'] = round(net_profit, 2)
        results['total_default_loss'] = round(total_default_loss, 2)
        print(f"\n📌 Estimated Net Profitability:")
        print(f"   Interest Income  : ₹{total_income:,.0f}")
        print(f"   Default Loss     : ₹{total_default_loss:,.0f}")
        print(f"   Net (est.)       : ₹{net_profit:,.0f}")

    # ── 6. Income by loan term ────────────────────────────────────────────────
    if 'LOAN_TERM' in df.columns:
        inc_term = df.groupby('LOAN_TERM').agg(
            Avg_Interest_Income=('INTEREST_INCOME', 'mean'),
            Count=('LOAN_ID', 'count')
        ).round(2)
        results['income_by_term'] = inc_term
        print("\n📌 Avg Interest Income by Loan Term (months):")
        print(inc_term.to_string())

    print("\n✅ Task 12 complete")
    return results
