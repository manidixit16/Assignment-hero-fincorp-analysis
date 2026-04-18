"""
Borrower Segmentation
Segments customers by income and credit score to identify high-value
and high-risk borrower groups.
"""
import pandas as pd


def borrower_segmentation(df):
    """
    Classify borrowers into Low / Medium / High tiers based on
    income level and credit score, then assess loan status distribution.
    """
    print("\n[TASK 5] Borrower Segmentation")

    segments = {}

    # --------------------------------------------------
    # 1. INCOME SEGMENTATION
    # --------------------------------------------------
    if 'ANNUAL_INCOME' in df.columns:
        income_bins   = [0, 300000, 700000, float('inf')]
        income_labels = ['Low', 'Medium', 'High']

        df['INCOME_TIER'] = pd.cut(
            df['ANNUAL_INCOME'], bins=income_bins, labels=income_labels
        )
        income_dist = df['INCOME_TIER'].value_counts()

        segments['income_dist'] = income_dist
        print("\nBorrower Count by Income Tier:\n", income_dist)

    # --------------------------------------------------
    # 2. CREDIT SCORE SEGMENTATION
    # --------------------------------------------------
    if 'CREDIT_SCORE' in df.columns:
        score_bins   = [0, 580, 720, float('inf')]
        score_labels = ['Low', 'Medium', 'High']

        df['SCORE_TIER'] = pd.cut(
            df['CREDIT_SCORE'], bins=score_bins, labels=score_labels
        )
        score_dist = df['SCORE_TIER'].value_counts()

        segments['score_dist'] = score_dist
        print("\nBorrower Count by Credit Score Tier:\n", score_dist)

    # --------------------------------------------------
    # 3. LOAN STATUS DISTRIBUTION
    # --------------------------------------------------
    if 'LOAN_STATUS' in df.columns:
        status_dist = df['LOAN_STATUS'].value_counts()
        segments['loan_status'] = status_dist
        print("\nLoan Status Distribution:\n", status_dist)

    # --------------------------------------------------
    # 4. HIGH-RISK vs HIGH-VALUE PROFILING
    # --------------------------------------------------
    if 'INCOME_TIER' in df.columns and 'SCORE_TIER' in df.columns:
        high_risk  = df[(df['INCOME_TIER'] == 'Low') & (df['SCORE_TIER'] == 'Low')]
        high_value = df[(df['INCOME_TIER'] == 'High') & (df['SCORE_TIER'] == 'High')]

        print(f"\nHigh-Risk Borrowers  (Low Income + Low Score): {len(high_risk)}")
        print(f"High-Value Borrowers (High Income + High Score): {len(high_value)}")

        segments['high_risk_count']  = len(high_risk)
        segments['high_value_count'] = len(high_value)

    return segments
