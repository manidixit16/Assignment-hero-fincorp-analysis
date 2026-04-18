"""
Credit Risk Profiler
Profiles risk across credit score tiers, loan purposes, and repayment
behaviour categories to support underwriting decisions.
"""
import pandas as pd


def credit_risk_profiler(df):
    """
    Build a risk profile by credit score tier and loan purpose.
    Also evaluates repayment behaviour against default outcomes.
    """
    print("\n[TASK 18] Credit Risk Profiler")

    risk_profile = {}

    # --------------------------------------------------
    # 1. RISK BY CREDIT SCORE TIER
    # --------------------------------------------------
    if 'CREDIT_SCORE' in df.columns and 'DEFAULT_FLAG' in df.columns:
        score_bins   = [0, 580, 720, float('inf')]
        score_labels = ['Low', 'Medium', 'High']
        df['SCORE_TIER'] = pd.cut(df['CREDIT_SCORE'], bins=score_bins, labels=score_labels)

        risk_by_tier = df.groupby('SCORE_TIER')['DEFAULT_FLAG'].mean()
        risk_profile['risk_by_tier'] = risk_by_tier
        print("\nDefault Rate by Credit Score Tier:\n", risk_by_tier)

    # --------------------------------------------------
    # 2. RISK BY LOAN PURPOSE
    # --------------------------------------------------
    if 'LOAN_PURPOSE' in df.columns and 'DEFAULT_FLAG' in df.columns:
        risk_by_purpose = df.groupby('LOAN_PURPOSE')['DEFAULT_FLAG'].sum()
        risk_profile['risk_by_purpose'] = risk_by_purpose
        print("\nDefault Count by Loan Purpose:\n", risk_by_purpose)

    # --------------------------------------------------
    # 3. REPAYMENT BEHAVIOUR
    # --------------------------------------------------
    if 'REPAYMENT_BEHAVIOUR' in df.columns:
        behaviour_dist = df['REPAYMENT_BEHAVIOUR'].value_counts()
        risk_profile['behaviour_dist'] = behaviour_dist
        print("\nRepayment Behaviour Distribution:\n", behaviour_dist)

    return risk_profile
