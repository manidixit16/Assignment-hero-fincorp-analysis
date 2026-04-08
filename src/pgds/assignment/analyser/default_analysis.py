"""
TASK 3: Default Risk Analysis
- Correlation between Loan_Amount, Interest_Rate, Credit_Score and Default_Flag
- Pairwise correlation heatmap: EMI_Amount, Overdue_Amount, Default_Amount
- Correlation between branch performance metrics and default rates
"""

import pandas as pd


def default_risk_analysis(df, branches=None):
    """
    Analyse key factors driving loan defaults.

    Returns
    -------
    dict with keys: loan_correlation, pairwise_correlation,
                    branch_correlation, default_by_credit_bucket,
                    default_by_employment, default_by_purpose
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 3 — Default Risk Analysis")
    print("="*55)

    # ── 1. Loan attribute correlations ────────────────────────────────────────
    corr_cols = ['LOAN_AMOUNT', 'INTEREST_RATE', 'CREDIT_SCORE', 'DEFAULT_FLAG']
    corr_cols = [c for c in corr_cols if c in df.columns]

    if len(corr_cols) >= 2:
        corr = df[corr_cols].corr()
        results['loan_correlation'] = corr
        print("\n📌 Loan Attribute Correlation with DEFAULT_FLAG:")
        if 'DEFAULT_FLAG' in corr.columns:
            print(corr['DEFAULT_FLAG'].drop('DEFAULT_FLAG').to_string())

    # ── 2. Pairwise correlation: EMI / Overdue / Default ─────────────────────
    pair_cols = ['EMI_AMOUNT', 'OVERDUE_AMOUNT', 'DEFAULT_AMOUNT']
    pair_cols = [c for c in pair_cols if c in df.columns]

    if len(pair_cols) >= 2:
        pair_corr = df[pair_cols].corr()
        results['pairwise_correlation'] = pair_corr
        print("\n📌 Pairwise Correlation (EMI / Overdue / Default):")
        print(pair_corr.to_string())

    # ── 3. Branch-level default analysis ──────────────────────────────────────
    if branches is not None and 'REGION' in df.columns:
        branch_cols = ['DEFAULT_FLAG', 'DELINQUENT_LOANS', 'LOAN_DISBURSEMENT_AMOUNT']

        # Aggregate df by REGION then join branches metrics
        df_region = df.groupby('REGION')['DEFAULT_FLAG'].mean().reset_index()
        br_region  = branches.groupby('REGION')[['DELINQUENT_LOANS', 'LOAN_DISBURSEMENT_AMOUNT']].mean().reset_index()
        branch_corr = df_region.merge(br_region, on='REGION', how='left').set_index('REGION').round(4)
        results['branch_correlation'] = branch_corr
        print("\n📌 Branch-Level Default Metrics by Region:")
        print(branch_corr.to_string())

    # ── 4. Default rate by credit score bucket ────────────────────────────────
    if 'CREDIT_SCORE' in df.columns:
        df = df.copy()
        df['CREDIT_BUCKET'] = pd.cut(
            df['CREDIT_SCORE'],
            bins=[0, 300, 580, 670, 740, 900],
            labels=['Very Poor (<300)', 'Poor (300-580)',
                    'Fair (580-670)', 'Good (670-740)', 'Excellent (>740)']
        )
        cs_def = df.groupby('CREDIT_BUCKET', observed=True)['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Count='count'
        )
        cs_def['Default_Rate'] = (cs_def['Default_Rate'] * 100).round(2)
        results['default_by_credit_bucket'] = cs_def
        print("\n📌 Default Rate by Credit Score Bucket:")
        print(cs_def.to_string())

    # ── 5. Default by employment status ───────────────────────────────────────
    if 'EMPLOYMENT_STATUS' in df.columns:
        emp_def = df.groupby('EMPLOYMENT_STATUS')['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Count='count'
        )
        emp_def['Default_Rate'] = (emp_def['Default_Rate'] * 100).round(2)
        results['default_by_employment'] = emp_def
        print("\n📌 Default Rate by Employment Status:")
        print(emp_def.to_string())

    # ── 6. Default by loan purpose ────────────────────────────────────────────
    if 'LOAN_PURPOSE' in df.columns:
        purp_def = df.groupby('LOAN_PURPOSE')['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Count='count'
        )
        purp_def['Default_Rate'] = (purp_def['Default_Rate'] * 100).round(2)
        results['default_by_purpose'] = purp_def.sort_values('Default_Rate', ascending=False)
        print("\n📌 Default Rate by Loan Purpose:")
        print(results['default_by_purpose'].to_string())

    print("\n✅ Task 3 complete")
    return results
