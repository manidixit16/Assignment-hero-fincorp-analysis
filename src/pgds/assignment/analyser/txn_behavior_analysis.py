"""
Transaction Behaviour Analysis
Examines transaction patterns to surface customer payment habits
and identify anomalous activity.
"""
import pandas as pd


def txn_behavior_analysis(df, transactions):
    """
    Analyse transaction type frequencies, payment behaviour, and
    their relationship to default outcomes.
    """
    print("\n[TASK 20] Transaction Behaviour Analysis")

    behaviour = {}

    # --------------------------------------------------
    # 1. TRANSACTION TYPE FREQUENCY
    # --------------------------------------------------
    if 'TRANSACTION_TYPE' in transactions.columns:
        txn_freq = transactions['TRANSACTION_TYPE'].value_counts()
        behaviour['txn_freq'] = txn_freq
        print("\nTransaction Frequency by Type:\n", txn_freq)

    # --------------------------------------------------
    # 2. PAYMENT TYPE FREQUENCY
    # --------------------------------------------------
    if 'PAYMENT_TYPE' in transactions.columns:
        pay_freq = transactions['PAYMENT_TYPE'].value_counts()
        behaviour['pay_freq'] = pay_freq
        print("\nPayment Frequency by Type:\n", pay_freq)

    # --------------------------------------------------
    # 3. TRANSACTION AMOUNT SUMMARY
    # --------------------------------------------------
    if 'TRANSACTION_AMOUNT' in transactions.columns:
        amt_summary = transactions['TRANSACTION_AMOUNT'].describe()
        behaviour['amt_summary'] = amt_summary
        print("\nTransaction Amount Summary:\n", amt_summary)

    # --------------------------------------------------
    # 4. DEFAULT LINKAGE
    # --------------------------------------------------
    if 'DEFAULT_FLAG' in df.columns and 'TRANSACTION_TYPE' in transactions.columns:
        print("\n  Note: Linking transaction patterns to defaults requires LOAN_ID join")

    return behaviour
