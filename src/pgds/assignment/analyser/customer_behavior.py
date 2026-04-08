"""
TASK 17: Customer Behavior Analysis
- Categorise customers based on repayment behaviour
  (always on time, occasional defaulters, frequent defaulters)
- Analyse patterns in loan approval/rejection by customer demographics
- Identify high-value customers with consistent repayment histories
"""

import pandas as pd


def customer_behavior(df, applications=None, transactions=None):
    """
    Profile customer repayment behaviour and link it to demographic
    and application-level characteristics.

    Returns
    -------
    dict with keys: repayment_categories, behavior_by_demographics,
                    high_value_customers, approval_by_age_group,
                    approval_by_gender, rejection_by_demographics
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 17 — Customer Behavior Analysis")
    print("="*55)

    df = df.copy()

    # ── 1. Repayment behaviour categorisation ─────────────────────────────────
    # Overdue amount and loan status used as proxies for repayment behaviour
    conditions = []
    choices    = []

    if 'OVERDUE_AMOUNT' in df.columns and 'DEFAULT_FLAG' in df.columns:
        # Always On Time: no overdue, no default
        df['REPAYMENT_CATEGORY'] = 'Always On Time'
        df.loc[df['OVERDUE_AMOUNT'] > 0, 'REPAYMENT_CATEGORY']   = 'Occasional Defaulter'
        df.loc[df['DEFAULT_FLAG'] == 1, 'REPAYMENT_CATEGORY']     = 'Defaulted'
    elif 'DEFAULT_FLAG' in df.columns:
        df['REPAYMENT_CATEGORY'] = df['DEFAULT_FLAG'].map(
            {0: 'Non-Defaulter', 1: 'Defaulter'}
        )

    if 'REPAYMENT_CATEGORY' in df.columns:
        cat_summary = df['REPAYMENT_CATEGORY'].value_counts().rename('Count')
        cat_pct = (cat_summary / len(df) * 100).round(2).rename('Pct_%')
        repayment_df = pd.concat([cat_summary, cat_pct], axis=1)
        results['repayment_categories'] = repayment_df
        print("\n📌 Customer Repayment Categories:")
        print(repayment_df.to_string())

    # ── 2. Behaviour by demographics ─────────────────────────────────────────
    if 'GENDER' in df.columns:
        gender_def = df.groupby('GENDER')['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Count='count'
        )
        gender_def['Default_Rate_%'] = (gender_def['Default_Rate'] * 100).round(2)
        results['default_by_gender'] = gender_def
        print("\n📌 Default Rate by Gender:")
        print(gender_def[['Count', 'Default_Rate_%']].to_string())

    if 'AGE' in df.columns:
        df['AGE_GROUP'] = pd.cut(
            df['AGE'],
            bins=[18, 25, 35, 45, 55, 100],
            labels=['18-25', '26-35', '36-45', '46-55', '55+']
        )
        age_def = df.groupby('AGE_GROUP', observed=True)['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Count='count'
        )
        age_def['Default_Rate_%'] = (age_def['Default_Rate'] * 100).round(2)
        results['default_by_age'] = age_def
        print("\n📌 Default Rate by Age Group:")
        print(age_def[['Count', 'Default_Rate_%']].to_string())

    if 'EMPLOYMENT_STATUS' in df.columns:
        emp_def = df.groupby('EMPLOYMENT_STATUS')['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Count='count'
        )
        emp_def['Default_Rate_%'] = (emp_def['Default_Rate'] * 100).round(2)
        results['default_by_employment'] = emp_def
        print("\n📌 Default Rate by Employment Status:")
        print(emp_def[['Count', 'Default_Rate_%']].to_string())

    # ── 3. Approval / rejection patterns by demographics ─────────────────────
    if applications is not None and 'APPROVAL_STATUS' in applications.columns:
        apps = applications.merge(
            df[['CUSTOMER_ID', 'AGE', 'GENDER', 'EMPLOYMENT_STATUS',
                'ANNUAL_INCOME', 'CREDIT_SCORE']].drop_duplicates(subset='CUSTOMER_ID'),
            on='CUSTOMER_ID', how='left'
        )

        if 'GENDER' in apps.columns:
            appr_gender = apps.groupby('GENDER')['APPROVAL_STATUS'].apply(
                lambda x: (x == 'Approved').mean() * 100
            ).round(2).rename('Approval_Rate_%')
            results['approval_by_gender'] = appr_gender
            print("\n📌 Approval Rate by Gender:")
            print(appr_gender.to_string())

        if 'EMPLOYMENT_STATUS' in apps.columns:
            appr_emp = apps.groupby('EMPLOYMENT_STATUS')['APPROVAL_STATUS'].apply(
                lambda x: (x == 'Approved').mean() * 100
            ).round(2).rename('Approval_Rate_%')
            results['approval_by_employment'] = appr_emp
            print("\n📌 Approval Rate by Employment Status:")
            print(appr_emp.to_string())

    # ── 4. High-value customers ───────────────────────────────────────────────
    hv_mask = (df['DEFAULT_FLAG'] == 0)
    if 'CREDIT_SCORE' in df.columns:
        hv_mask = hv_mask & (df['CREDIT_SCORE'] >= 700)
    if 'ANNUAL_INCOME' in df.columns:
        income_75 = df['ANNUAL_INCOME'].quantile(0.75)
        hv_mask = hv_mask & (df['ANNUAL_INCOME'] >= income_75)

    high_value = df[hv_mask]
    results['high_value_customers'] = high_value

    hv_cols = ['CUSTOMER_ID', 'CREDIT_SCORE', 'ANNUAL_INCOME', 'LOAN_AMOUNT']
    hv_cols = [c for c in hv_cols if c in high_value.columns]
    print(f"\n📌 High-Value Customers (no default, CS≥700, income top 25%): {len(high_value):,}")
    if not high_value.empty:
        print(high_value[hv_cols].head(10).to_string(index=False))

    print("\n✅ Task 17 complete")
    return results
