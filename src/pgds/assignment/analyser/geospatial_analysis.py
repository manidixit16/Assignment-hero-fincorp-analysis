"""
TASK 13: Geospatial Analysis
- Map the distribution of active loans across regions
- Compare default rates across different geographic regions
- Visualise loan disbursement trends for different area types (region categories)
"""

import pandas as pd


def geo_analysis(df, branches=None):
    """
    Regional/geographic distribution analysis of loans, defaults,
    and disbursement trends.

    Returns
    -------
    dict with keys: active_loans_by_region, default_rate_by_region,
                    disbursement_by_region, branch_count_by_region,
                    region_risk_profile, loan_status_by_region
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 13 — Geospatial Analysis")
    print("="*55)

    if 'REGION' not in df.columns:
        print("  ⚠️  REGION column not found — skipping Task 13")
        return results

    # ── 1. Active loans by region ─────────────────────────────────────────────
    status_col = 'LOAN_STATUS' if 'LOAN_STATUS' in df.columns else None

    if status_col:
        active = df[df[status_col].str.upper() == 'ACTIVE']
        active_by_region = active.groupby('REGION').agg(
            Active_Loans=('LOAN_ID', 'count'),
            Total_Disbursed=('LOAN_AMOUNT', 'sum')
        ).sort_values('Active_Loans', ascending=False)
        results['active_loans_by_region'] = active_by_region
        print("\n📌 Active Loans by Region:")
        print(active_by_region.to_string())

    # ── 2. Default rate by region ─────────────────────────────────────────────
    default_region = df.groupby('REGION').agg(
        Total_Loans=('LOAN_ID', 'count'),
        Defaults=('DEFAULT_FLAG', 'sum'),
        Default_Rate=('DEFAULT_FLAG', 'mean'),
        Avg_Credit_Score=('CREDIT_SCORE', 'mean')
    ).round(4)
    default_region['Default_Rate_%'] = (default_region['Default_Rate'] * 100).round(2)
    default_region = default_region.drop(columns='Default_Rate').sort_values(
        'Default_Rate_%', ascending=False
    )
    results['default_rate_by_region'] = default_region
    print("\n📌 Default Rate by Region:")
    print(default_region.to_string())

    # ── 3. Disbursement by region ─────────────────────────────────────────────
    disb_region = df.groupby('REGION').agg(
        Total_Disbursed=('LOAN_AMOUNT', 'sum'),
        Avg_Loan_Amount=('LOAN_AMOUNT', 'mean'),
        Loan_Count=('LOAN_ID', 'count')
    ).round(2).sort_values('Total_Disbursed', ascending=False)
    results['disbursement_by_region'] = disb_region
    print("\n📌 Loan Disbursement by Region:")
    print(disb_region.to_string())

    # ── 4. Branch distribution by region ─────────────────────────────────────
    if branches is not None and 'REGION' in branches.columns:
        branch_region = branches.groupby('REGION').agg(
            Branch_Count=('BRANCH_ID', 'count'),
            Total_Disbursement=('LOAN_DISBURSEMENT_AMOUNT', 'sum'),
            Avg_Delinquency=('DELINQUENT_LOANS', 'mean')
        ).round(2)
        results['branch_count_by_region'] = branch_region
        print("\n📌 Branch Distribution by Region:")
        print(branch_region.to_string())

    # ── 5. Loan status by region ──────────────────────────────────────────────
    if status_col:
        status_region = df.groupby(['REGION', status_col]).size().unstack(fill_value=0)
        results['loan_status_by_region'] = status_region
        print("\n📌 Loan Status by Region:")
        print(status_region.to_string())

    # ── 6. Region risk profile ────────────────────────────────────────────────
    risk_profile = df.groupby('REGION').agg(
        Avg_Interest_Rate=('INTEREST_RATE', 'mean'),
        Avg_Credit_Score=('CREDIT_SCORE', 'mean'),
        Avg_Loan_Amount=('LOAN_AMOUNT', 'mean'),
        Default_Rate=('DEFAULT_FLAG', 'mean')
    ).round(3)
    risk_profile['Default_Rate_%'] = (risk_profile['Default_Rate'] * 100).round(2)
    risk_profile = risk_profile.drop(columns='Default_Rate')
    results['region_risk_profile'] = risk_profile
    print("\n📌 Region Risk Profile:")
    print(risk_profile.to_string())

    print("\n✅ Task 13 complete")
    return results
