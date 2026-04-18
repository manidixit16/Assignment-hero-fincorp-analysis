"""
Advanced Metrics
Runs deeper statistical correlation analysis across loan, default,
and branch-level variables.
"""
import pandas as pd


def advanced_statistical_analysis(df, branches):
    """
    Compute extended correlation heatmaps and pairwise analysis
    for EMI, overdue, and default amount variables.
    """
    print("\n[TASK 6] Advanced Statistical Metrics")

    metrics = {}

    # --------------------------------------------------
    # 1. LOAN ATTRIBUTE CORRELATION
    # --------------------------------------------------
    loan_cols = ['LENI_AMOUNT', 'INTEREST_RATE', 'CREDIT_SCORE', 'DEFAULT_FLAG']
    available = [c for c in loan_cols if c in df.columns]
    if available:
        corr_loans = df[available].corr()
        metrics['corr_loans'] = corr_loans
        print("\nLoan Attribute Correlation:\n", corr_loans)

    # --------------------------------------------------
    # 2. EMI / OVERDUE / DEFAULT CORRELATION
    # --------------------------------------------------
    emi_cols = ['EMI_AMOUNT', 'DEFAULT_AMOUNT', 'RECOVERY_RATE']
    avail_emi = [c for c in emi_cols if c in df.columns]
    if avail_emi:
        corr_emi = df[avail_emi].corr()
        metrics['corr_emi'] = corr_emi
        print("\nEMI / Default Correlation:\n", corr_emi)

    # --------------------------------------------------
    # 3. DEFAULT RISK CORRELATION
    # --------------------------------------------------
    risk_cols = ['CREDIT_SCORE', 'LOAN_AMOUNT', 'INTEREST_RATE', 'DEFAULT_AMOUNT', 'DEFAULT_FLAG']
    avail_risk = [c for c in risk_cols if c in df.columns]
    if avail_risk:
        corr_risk = df[avail_risk].corr()
        metrics['corr_risk'] = corr_risk
        print("\nDefault Risk Correlation:\n", corr_risk)

    return metrics
