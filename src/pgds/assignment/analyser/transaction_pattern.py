import pandas as pd

def transaction_pattern_analysis(df, transactions):
    print("\n💥 TRANSACTION PATTERN ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. IRREGULAR REPAYMENT PATTERNS
    # -----------------------------------
    if 'CUSTOMER_ID' in transactions.columns:
        txn_count = transactions.groupby('CUSTOMER_ID').size()

        # Calculate variation (std dev proxy)
        txn_variation = transactions.groupby('CUSTOMER_ID')['TRANSACTION_AMOUNT'].std()

        irregular = txn_variation[txn_variation > txn_variation.median()]

        results['irregular_customers'] = irregular

        print("\nIrregular Customers:", len(irregular))

    # -----------------------------------
    # 2. PENALTY PROPORTION
    # -----------------------------------
    if 'TRANSACTION_TYPE' in transactions.columns:
        total_txn = len(transactions)

        penalty_txn = transactions[
            transactions['TRANSACTION_TYPE'].str.upper() == 'PENALTY'
        ]

        penalty_ratio = len(penalty_txn) / total_txn if total_txn > 0 else 0

        results['penalty_ratio'] = penalty_ratio

        print(f"\nPenalty Proportion: {penalty_ratio:.2%}")

    # -----------------------------------
    # 3. OVERDUE vs NON-OVERDUE
    # -----------------------------------
    if 'OVERDUE_AMOUNT' in df.columns:
        overdue = df[df['OVERDUE_AMOUNT'] > 0]
        non_overdue = df[df['OVERDUE_AMOUNT'] == 0]

        overdue_avg = overdue['LOAN_AMOUNT'].mean()
        non_overdue_avg = non_overdue['LOAN_AMOUNT'].mean()

        results['overdue_vs_non'] = {
            'overdue_avg': overdue_avg,
            'non_overdue_avg': non_overdue_avg
        }

        print("\nOverdue vs Non-Overdue:")
        print("Overdue Avg Loan:", overdue_avg)
        print("Non-Overdue Avg Loan:", non_overdue_avg)

    return results