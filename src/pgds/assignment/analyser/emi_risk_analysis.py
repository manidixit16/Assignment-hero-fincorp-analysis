"""
EMI Risk Analysis
Investigates how EMI amount levels relate to default probability,
identifying threshold ranges with elevated risk.
"""
import pandas as pd


def emi_risk_analysis(df):
    """
    Segment EMI amounts into quantile bands and measure default probability
    per band to surface high-risk EMI thresholds.
    """
    print("\n[TASK 8] EMI Risk Analysis")

    findings = {}

    # --------------------------------------------------
    # 1. DEFAULT PROBABILITY BY EMI BAND
    # --------------------------------------------------
    if 'EMI_AMOUNT' in df.columns and 'DEFAULT_FLAG' in df.columns:
        emi_bands = pd.qcut(df['EMI_AMOUNT'], 5, duplicates='drop')
        default_by_band = df.groupby(emi_bands)['DEFAULT_FLAG'].mean()

        findings['default_by_band'] = default_by_band
        print("\nDefault Probability by EMI Band:\n", default_by_band)

    else:
        print(" EMI_AMOUNT or DEFAULT_FLAG column not found — skipping")

    # --------------------------------------------------
    # 2. EMI THRESHOLD ANALYSIS
    # --------------------------------------------------
    if 'EMI_AMOUNT' in df.columns:
        df['EMI_BIN'] = pd.qcut(df['EMI_AMOUNT'], 5, duplicates='drop')
        threshold_risk = df.groupby('EMI_BIN')['DEFAULT_FLAG'].mean()

        findings['threshold_risk'] = threshold_risk
        print("\nEMI Threshold Risk Profile:\n", threshold_risk)

    # --------------------------------------------------
    # 3. LOAN TYPE (NOTE)
    # --------------------------------------------------
    print("\n  Note: Loan type breakdown not feasible — LOAN_TYPE column absent in dataset")

    return findings
