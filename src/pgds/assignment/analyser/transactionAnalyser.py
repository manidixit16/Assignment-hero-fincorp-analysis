"""
transactionAnalyser.py
Legacy camelCase module retained for compatibility with reference repo.
Full Task 7 & 20 implementation is in analyser/transaction_analysis.py
and analyser/transaction_pattern.py
"""


def transaction_summary(transactions):
    """
    Summarise transaction types and compute the penalty ratio.

    Returns
    -------
    dict with penalty_ratio, emi_count, penalty_count
    """
    type_col = next(
        (c for c in ['PAYMENT_TYPE', 'TRANSACTION_TYPE'] if c in transactions.columns),
        None
    )

    if type_col is None:
        print("  ⚠️  No transaction type column found")
        return {}

    counts       = transactions[type_col].value_counts()
    penalty_count = transactions[type_col].str.upper().eq('PENALTY').sum()
    emi_count     = transactions[type_col].str.upper().eq('EMI').sum()
    total         = len(transactions)
    penalty_ratio = penalty_count / total if total else 0

    print(f"\n📌 Transaction Type Breakdown:")
    print(counts.to_string())
    print(f"\n  Penalty Ratio : {penalty_ratio:.2%}  ({penalty_count:,} of {total:,})")

    return {
        "penalty_ratio":  round(penalty_ratio, 4),
        "penalty_count":  int(penalty_count),
        "emi_count":      int(emi_count),
        "total":          int(total),
    }


def overdueTransactions(df, transactions):
    """Compare transaction amounts for overdue vs non-overdue loans."""
    if 'OVERDUE_AMOUNT' not in df.columns:
        return None

    amt_col  = next((c for c in ['AMOUNT', 'TRANSACTION_AMOUNT'] if c in transactions.columns), None)
    if amt_col is None:
        return None

    tx = transactions.copy()
    overdue_ids  = set(df[df['OVERDUE_AMOUNT'] > 0]['LOAN_ID'].dropna())
    tx['IS_OVERDUE'] = tx['LOAN_ID'].isin(overdue_ids).map({True: 'Overdue', False: 'Non-Overdue'})

    comparison = tx.groupby('IS_OVERDUE')[amt_col].agg(
        Mean='mean', Median='median', Count='count'
    ).round(2)
    print("\n📌 Transaction Amounts — Overdue vs Non-Overdue:")
    print(comparison.to_string())
    return comparison
