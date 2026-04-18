"""
Recovery Effectiveness Analysis
Evaluates how well the organisation recovers defaulted loan amounts,
and whether legal action significantly improves outcomes.
"""
import pandas as pd


def recovery_effectiveness(df):
    """
    Assess recovery rate distribution, impact of legal action on
    recovery, and average rates per loan type.
    """
    print("\n[TASK 10] Recovery Effectiveness Analysis")

    recovery = {}

    # --------------------------------------------------
    # 1. RECOVERY RATE DISTRIBUTION
    # --------------------------------------------------
    if 'RECOVERY_RATE' in df.columns:
        recovery['rate_summary'] = df['RECOVERY_RATE'].describe()
        print("\nRecovery Rate Summary:\n", recovery['rate_summary'])

    # --------------------------------------------------
    # 2. RECOVERY BY LEGAL ACTION
    # --------------------------------------------------
    if 'LEGAL_ACTION' in df.columns and 'RECOVERY_RATE' in df.columns:
        legal_impact = df.groupby('LEGAL_ACTION')['RECOVERY_RATE'].mean()
        recovery['legal_impact'] = legal_impact
        print("\nRecovery Rate by Legal Action:\n", legal_impact)

    # --------------------------------------------------
    # 3. RECOVERY BY LOAN PURPOSE
    # --------------------------------------------------
    if 'LOAN_PURPOSE' in df.columns and 'RECOVERY_RATE' in df.columns:
        purpose_recovery = df.groupby('LOAN_PURPOSE')['RECOVERY_RATE'].mean()
        recovery['purpose_recovery'] = purpose_recovery
        print("\nRecovery Rate by Loan Purpose:\n", purpose_recovery)

    return recovery
