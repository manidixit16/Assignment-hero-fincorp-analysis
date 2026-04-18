"""
Repayment Behaviour Analysis
Profiles customer repayment habits segmented by age group,
gender, and approval status to identify risk patterns early.
"""
import pandas as pd


def customer_behavior_analysis(df, applications, customers):
    """
    Analyse approval rates by gender and age group, and evaluate
    customer repayment behaviour (on-time vs frequent vs occasional).
    """
    print("\n[TASK 17] Repayment Behaviour Analysis")

    behaviour = {}

    # --------------------------------------------------
    # 1. APPROVAL BY GENDER
    # --------------------------------------------------
    if 'GENDER' in customers.columns and 'APPROVAL_STATUS' in applications.columns:
        merged = applications.merge(customers, on='CUSTOMER_ID', how='left')
        approval_gender = merged.groupby(['GENDER', 'APPROVAL_STATUS']).size().unstack(fill_value=0)
        behaviour['approval_gender'] = approval_gender
        print("\nApproval by Gender:\n", approval_gender)

    # --------------------------------------------------
    # 2. APPROVAL BY AGE GROUP
    # --------------------------------------------------
    if 'AGE' in customers.columns and 'APPROVAL_STATUS' in applications.columns:
        if 'merged' not in dir():
            merged = applications.merge(customers, on='CUSTOMER_ID', how='left')

        age_bins   = [0, 30, 50, float('inf')]
        age_labels = ['Young', 'Middle', 'Senior']
        merged['AGE_GROUP'] = pd.cut(merged['AGE'], bins=age_bins, labels=age_labels)

        approval_age = merged.groupby(['AGE_GROUP', 'APPROVAL_STATUS']).size().unstack(fill_value=0)
        behaviour['approval_age'] = approval_age
        print("\nApproval by Age Group:\n", approval_age)

    # --------------------------------------------------
    # 3. REPAYMENT BEHAVIOUR DISTRIBUTION
    # --------------------------------------------------
    if 'REPAYMENT_BEHAVIOUR' in df.columns:
        repay_dist = df['REPAYMENT_BEHAVIOUR'].value_counts()
        behaviour['repay_dist'] = repay_dist
        print("\nRepayment Behaviour Distribution:\n", repay_dist)

    return behaviour
