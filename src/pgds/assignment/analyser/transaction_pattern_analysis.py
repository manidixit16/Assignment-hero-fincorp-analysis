import pandas as pd

def transaction_pattern_analysis(df, transactions):

    print("\n TRANSACTION PATTERN ANALYSIS")

    results = {}

    # -----------------------------------
    # STANDARDIZE COLUMNS
    # -----------------------------------
    transactions.columns = [col.upper() for col in transactions.columns]

    print("Columns:", transactions.columns)

    # -----------------------------------
    # 1. IRREGULAR REPAYMENT PATTERNS
    # -----------------------------------
    if 'CUSTOMER_ID' in transactions.columns and 'AMOUNT' in transactions.columns:

        txn_variation = transactions.groupby('CUSTOMER_ID')['AMOUNT'].std()

        irregular = txn_variation[txn_variation > txn_variation.median()]

        print("\nIrregular Customers:", len(irregular))

        results['irregular'] = irregular

    else:
        print("Missing CUSTOMER_ID or AMOUNT")

    # -----------------------------------
    # 2. PENALTY PROPORTION
    # -----------------------------------
    if 'PAYMENT_TYPE' in transactions.columns:

        total = len(transactions)

        penalty = transactions[
            transactions['PAYMENT_TYPE'].astype(str).str.upper() == 'PENALTY'
        ]

        ratio = len(penalty) / total if total > 0 else 0

        print(f"\n Penalty Ratio: {ratio:.2%}")

        results['penalty_ratio'] = ratio

    else:
        print("PAYMENT_TYPE missing")

    # -----------------------------------
    # 3. OVERDUE vs NON-OVERDUE
    # -----------------------------------
    if 'OVERDUE_AMOUNT' in df.columns and 'LOAN_AMOUNT' in df.columns:

        overdue = df[df['OVERDUE_AMOUNT'] > 0]
        non_overdue = df[df['OVERDUE_AMOUNT'] == 0]

        print("\n Overdue Avg:", overdue['LOAN_AMOUNT'].mean())
        print(" Non-Overdue Avg:", non_overdue['LOAN_AMOUNT'].mean())

        results['overdue_vs_non'] = {
            'overdue': overdue['LOAN_AMOUNT'].mean(),
            'non_overdue': non_overdue['LOAN_AMOUNT'].mean()
        }

    return results