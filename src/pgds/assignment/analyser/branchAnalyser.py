"""
branchAnalyser.py
Legacy camelCase module retained for compatibility with reference repo.
Full Task 4 implementation is in analyser/branch_analysis.py
"""


def branch_performance(df):
    """
    Rank branches (or regions, since no BRANCH_ID in data) by
    disbursement volume and default rate.
    """
    group_col = 'BRANCH_ID' if 'BRANCH_ID' in df.columns else 'REGION'

    branch = df.groupby(group_col).agg(
        Loan_Amount=('LOAN_AMOUNT', 'sum'),
        Default_Rate=('DEFAULT_FLAG', 'mean')
    )
    branch['Default_Rate'] = (branch['Default_Rate'] * 100).round(2)

    print(f"\n📌 Branch Performance (grouped by {group_col}):")
    print(branch.sort_values('Loan_Amount', ascending=False).head(10).to_string())

    return branch.sort_values('Loan_Amount', ascending=False)
