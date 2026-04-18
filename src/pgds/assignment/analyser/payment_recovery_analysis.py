"""
Payment & Recovery Analysis
Examines transaction types, payment patterns, and recovery rates by region
to understand customer repayment behaviour.
"""
import pandas as pd


def payment_recovery_analysis(df, transactions):
    """
    Analyse transaction distribution, recovery rates by region,
    and default reasons to gauge collection efficiency.
    """
    print("\n[TASK 7] Payment & Recovery Analysis")

    findings = {}

    # --------------------------------------------------
    # 1. TRANSACTION TYPE BREAKDOWN
    # --------------------------------------------------
    if 'TRANSACTION_TYPE' in transactions.columns:
        txn_counts = transactions['TRANSACTION_TYPE'].value_counts()
        findings['txn_counts'] = txn_counts
        print("\nTransaction Type Distribution:\n", txn_counts)

    # --------------------------------------------------
    # 2. PAYMENT TYPE BREAKDOWN
    # --------------------------------------------------
    if 'PAYMENT_TYPE' in transactions.columns:
        payment_counts = transactions['PAYMENT_TYPE'].value_counts()
        findings['payment_counts'] = payment_counts
        print("\nPayment Type Distribution:\n", payment_counts)

    # --------------------------------------------------
    # 3. RECOVERY RATE BY REGION
    # --------------------------------------------------
    if 'RECOVERY_RATE' in df.columns and 'REGION' in df.columns:
        region_recovery = df.groupby('REGION')['RECOVERY_RATE'].mean()
        findings['region_recovery'] = region_recovery
        print("\nAverage Recovery Rate by Region:\n", region_recovery)

    # --------------------------------------------------
    # 4. RECOVERY BY DEFAULT REASON
    # --------------------------------------------------
    if 'DEFAULT_REASON' in df.columns and 'RECOVERY_RATE' in df.columns:
        reason_recovery = df.groupby('DEFAULT_REASON')['RECOVERY_RATE'].mean()
        findings['reason_recovery'] = reason_recovery
        print("\nRecovery Rate by Default Reason:\n", reason_recovery)

    return findings
