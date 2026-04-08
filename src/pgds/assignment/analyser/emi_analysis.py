"""
TASK 8: EMI Analysis
- Analyse the relationship between EMI amounts and default probabilities
- Identify thresholds for EMI amounts where defaults are most likely
- Compare EMI trends across loan types / purposes
"""

import pandas as pd


def emi_analysis(df):
    """
    Examine how EMI burden relates to default risk and identify
    high-risk EMI thresholds.

    Returns
    -------
    dict with keys: emi_stats, emi_vs_default, emi_threshold,
                    emi_by_purpose, emi_by_term, high_risk_emi_range
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 8 — EMI Analysis")
    print("="*55)

    if 'EMI_AMOUNT' not in df.columns:
        print("  ⚠️  EMI_AMOUNT column not found — skipping Task 8")
        return results

    # ── 1. EMI descriptive stats ──────────────────────────────────────────────
    emi_stats = df['EMI_AMOUNT'].describe()
    results['emi_stats'] = emi_stats
    print("\n📌 EMI Amount Statistics:")
    print(emi_stats.to_string())

    # ── 2. EMI vs default probability (binned) ────────────────────────────────
    df = df.copy()
    df['EMI_BUCKET'] = pd.qcut(df['EMI_AMOUNT'], q=5, duplicates='drop')
    emi_default = df.groupby('EMI_BUCKET', observed=True)['DEFAULT_FLAG'].agg(
        Default_Rate='mean', Count='count'
    )
    emi_default['Default_Rate'] = (emi_default['Default_Rate'] * 100).round(2)
    results['emi_vs_default'] = emi_default
    print("\n📌 Default Rate by EMI Bucket:")
    print(emi_default.to_string())

    # ── 3. Threshold — highest default bucket ────────────────────────────────
    peak_bucket = emi_default['Default_Rate'].idxmax()
    results['high_risk_emi_range'] = str(peak_bucket)
    print(f"\n📌 Highest Default Rate EMI Range: {peak_bucket}")

    # ── 4. EMI to income ratio ────────────────────────────────────────────────
    if 'ANNUAL_INCOME' in df.columns:
        df['MONTHLY_INCOME'] = df['ANNUAL_INCOME'] / 12
        df['EMI_TO_INCOME_RATIO'] = df['EMI_AMOUNT'] / df['MONTHLY_INCOME'].replace(0, pd.NA)
        emi_income_def = df.groupby(
            pd.cut(df['EMI_TO_INCOME_RATIO'].clip(0, 1), bins=5)
        )['DEFAULT_FLAG'].agg(Default_Rate='mean', Count='count')
        emi_income_def['Default_Rate'] = (emi_income_def['Default_Rate'] * 100).round(2)
        results['emi_income_ratio'] = emi_income_def
        print("\n📌 Default Rate by EMI-to-Income Ratio:")
        print(emi_income_def.to_string())

    # ── 5. EMI trends by loan purpose ─────────────────────────────────────────
    if 'LOAN_PURPOSE' in df.columns:
        emi_by_purpose = df.groupby('LOAN_PURPOSE')['EMI_AMOUNT'].agg(
            Mean='mean', Median='median', Count='count'
        ).round(0)
        results['emi_by_purpose'] = emi_by_purpose
        print("\n📌 EMI Amount by Loan Purpose:")
        print(emi_by_purpose.to_string())

    # ── 6. EMI trends by loan term ────────────────────────────────────────────
    if 'LOAN_TERM' in df.columns:
        emi_by_term = df.groupby('LOAN_TERM')['EMI_AMOUNT'].mean().round(0)
        results['emi_by_term'] = emi_by_term
        print("\n📌 Avg EMI by Loan Term (months) — sample:")
        print(emi_by_term.head(10).to_string())

    print("\n✅ Task 8 complete")
    return results
