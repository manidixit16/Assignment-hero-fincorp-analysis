"""
Loan Default Scorer
Identifies correlation patterns between loan attributes and default risk.
"""
import pandas as pd


def loan_default_scorer(df, branches):
    """
    Analyse default risk across loan attributes such as credit score,
    loan amount, and interest rate. Also examines branch-level patterns.
    """
    print("\n[TASK 3] Loan Default Scoring")

    summary = {}

    # --------------------------------------------------
    # 1. CREDIT SCORE vs DEFAULT
    # --------------------------------------------------
    if 'CREDIT_SCORE' in df.columns and 'DEFAULT_FLAG' in df.columns:
        score_vs_default = df.groupby(
            pd.cut(df['CREDIT_SCORE'], bins=5)
        )['DEFAULT_FLAG'].mean()

        summary['score_vs_default'] = score_vs_default
        print("\nDefault Rate by Credit Score Band:\n", score_vs_default)

    # --------------------------------------------------
    # 2. LOAN AMOUNT vs DEFAULT
    # --------------------------------------------------
    if 'LOAN_AMOUNT' in df.columns and 'DEFAULT_FLAG' in df.columns:
        amount_vs_default = df.groupby(
            pd.cut(df['LOAN_AMOUNT'], bins=5)
        )['DEFAULT_FLAG'].mean()

        summary['amount_vs_default'] = amount_vs_default
        print("\nDefault Rate by Loan Amount Band:\n", amount_vs_default)

    # --------------------------------------------------
    # 3. INTEREST RATE vs DEFAULT
    # --------------------------------------------------
    if 'INTEREST_RATE' in df.columns and 'DEFAULT_FLAG' in df.columns:
        rate_vs_default = df.groupby(
            pd.cut(df['INTEREST_RATE'], bins=5)
        )['DEFAULT_FLAG'].mean()

        summary['rate_vs_default'] = rate_vs_default
        print("\nDefault Rate by Interest Rate Band:\n", rate_vs_default)

    # --------------------------------------------------
    # 4. CORRELATION MATRIX
    # --------------------------------------------------
    numeric_cols = ['LOAN_AMOUNT', 'INTEREST_RATE', 'CREDIT_SCORE', 'DEFAULT_FLAG']
    available = [c for c in numeric_cols if c in df.columns]
    if available:
        corr_matrix = df[available].corr()
        summary['corr_matrix'] = corr_matrix
        print("\nCorrelation Matrix:\n", corr_matrix)

    # --------------------------------------------------
    # 5. DEFAULT AMOUNT PAIRWISE
    # --------------------------------------------------
    pair_cols = ['EMI_AMOUNT', 'DEFAULT_AMOUNT', 'RECOVERY_RATE']
    available_pair = [c for c in pair_cols if c in df.columns]
    if available_pair:
        pairwise = df[available_pair].corr()
        summary['pairwise_corr'] = pairwise
        print("\nEMI / Default Pairwise Correlation:\n", pairwise)

    return summary
