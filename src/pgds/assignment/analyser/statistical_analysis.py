"""
TASK 6: Advanced Statistical Analysis
1. Correlation Analysis for Default Risks:
   Credit_Score, Loan_Amount, Interest_Rate, Overdue_Amount, Default_Flag
2. Pairwise Correlation Heatmap:
   EMI_Amount, Recovery_Rate, Default_Amount
3. Branch-Level Correlation:
   Delinquent_Loans, Loan_Disbursement_Amount, Recovery_Rate vs efficiency
"""

import pandas as pd


def correlation_analysis(df, branches=None, defaults=None):
    """Alias — calls advanced_statistical_analysis."""
    return advanced_statistical_analysis(df, branches=branches, defaults=defaults)


def advanced_statistical_analysis(df, branches=None, defaults=None):
    """
    Compute advanced correlation matrices for default risk, pairwise
    financial variables, and branch-level operational metrics.

    Returns
    -------
    dict with keys: default_risk_corr, pairwise_corr, branch_corr,
                    branch_region_corr
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 6 — Advanced Statistical Analysis")
    print("="*55)

    # ── 1. Default risk correlation ───────────────────────────────────────────
    risk_cols = ['CREDIT_SCORE', 'LOAN_AMOUNT', 'INTEREST_RATE',
                 'OVERDUE_AMOUNT', 'DEFAULT_FLAG']
    risk_cols = [c for c in risk_cols if c in df.columns]

    if len(risk_cols) >= 2:
        corr = df[risk_cols].corr()
        results['default_risk_corr'] = corr
        print("\n📌 Default Risk Correlation Matrix:")
        print(corr.round(4).to_string())
        if 'DEFAULT_FLAG' in corr.columns:
            print("\n  Correlation with DEFAULT_FLAG:")
            print(corr['DEFAULT_FLAG'].drop('DEFAULT_FLAG').round(4).to_string())

    # ── 2. Pairwise correlation: EMI / Recovery / Default Amount ──────────────
    if defaults is not None:
        defaults = defaults.copy()
        if 'RECOVERY_RATE' not in defaults.columns:
            defaults['RECOVERY_RATE'] = (
                defaults['RECOVERY_AMOUNT'] /
                defaults['DEFAULT_AMOUNT'].replace(0, pd.NA)
            ).clip(0, 1)

        merged = df.merge(defaults[['LOAN_ID', 'RECOVERY_RATE', 'DEFAULT_AMOUNT']],
                          on='LOAN_ID', how='left', suffixes=('', '_DEF'))

        pair_cols = ['EMI_AMOUNT', 'RECOVERY_RATE', 'DEFAULT_AMOUNT']
        pair_cols = [c for c in pair_cols if c in merged.columns]

        if len(pair_cols) >= 2:
            pair_corr = merged[pair_cols].corr()
            results['pairwise_corr'] = pair_corr
            print("\n📌 Pairwise Correlation (EMI / Recovery Rate / Default Amount):")
            print(pair_corr.round(4).to_string())

    # ── 3. Branch-level correlation (using branches table directly) ───────────
    if branches is not None:
        merged_b = branches.copy()

        branch_cols = ['DELINQUENT_LOANS', 'LOAN_DISBURSEMENT_AMOUNT',
                       'AVG_PROCESSING_TIME', 'TOTAL_ACTIVE_LOANS']
        branch_cols = [c for c in branch_cols if c in merged_b.columns]

        if len(branch_cols) >= 2:
            branch_corr = merged_b[branch_cols].corr()
            results['branch_corr'] = branch_corr
            print("\n📌 Branch-Level Correlation Matrix:")
            print(branch_corr.round(4).to_string())

        # Regional aggregation
        if 'REGION' in merged_b.columns:
            agg_cols = {c: 'mean' for c in branch_cols}
            region_agg = merged_b.groupby('REGION').agg(agg_cols).round(4)
            results['branch_region_corr'] = region_agg
            print("\n📌 Branch Metrics by Region (mean):")
            print(region_agg.to_string())

    print("\n✅ Task 6 complete")
    return results
