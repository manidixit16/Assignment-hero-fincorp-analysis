"""
TASK 5: Customer Segmentation
- Segment customers by income, credit score, and loan status
- Identify high-risk and high-value customer groups
- Analyse repayment behaviour across segments
"""

import pandas as pd


def customer_segmentation(df):
    """
    Segment Hero FinCorp customers into meaningful groups.

    Returns
    -------
    dict with keys: df (enriched), high_risk, high_value,
                    behavior, segment_summary, income_segment_default
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 5 — Customer Segmentation")
    print("="*55)

    df = df.copy()

    # ── 1. Credit score segment ───────────────────────────────────────────────
    if 'CREDIT_SCORE' in df.columns:
        df['CREDIT_SEGMENT'] = pd.cut(
            df['CREDIT_SCORE'],
            bins=[0, 500, 650, 750, 900],
            labels=['High Risk', 'Medium', 'Good', 'Excellent']
        )

    # ── 2. Income segment ─────────────────────────────────────────────────────
    if 'ANNUAL_INCOME' in df.columns:
        df['INCOME_SEGMENT'] = pd.qcut(
            df['ANNUAL_INCOME'], q=3,
            labels=['Low Income', 'Mid Income', 'High Income'],
            duplicates='drop'
        )

    # ── 3. Loan status label ──────────────────────────────────────────────────
    df['LOAN_STATUS_LABEL'] = df['DEFAULT_FLAG'].map({0: 'Non-Defaulter', 1: 'Defaulter'})

    # ── 4. High-risk customers ────────────────────────────────────────────────
    high_risk_mask = (
        (df.get('CREDIT_SEGMENT') == 'High Risk') |
        (df['DEFAULT_FLAG'] == 1)
    )
    high_risk = df[high_risk_mask]
    results['high_risk'] = high_risk
    print(f"\n📌 High-Risk Customers : {len(high_risk):,}")

    # ── 5. High-value customers ───────────────────────────────────────────────
    high_value_mask = (
        (df.get('CREDIT_SEGMENT', pd.Series()).isin(['Good', 'Excellent'])) &
        (df.get('INCOME_SEGMENT', pd.Series()) == 'High Income') &
        (df['DEFAULT_FLAG'] == 0)
    )
    high_value = df[high_value_mask]
    results['high_value'] = high_value
    print(f"📌 High-Value Customers : {len(high_value):,}")

    # ── 6. Repayment behaviour by credit segment ──────────────────────────────
    if 'CREDIT_SEGMENT' in df.columns:
        behavior = df.groupby('CREDIT_SEGMENT', observed=True)['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Count='count'
        )
        behavior['Default_Rate'] = (behavior['Default_Rate'] * 100).round(2)
        results['behavior'] = behavior
        print("\n📌 Repayment Behaviour by Credit Segment:")
        print(behavior.to_string())

    # ── 7. Segment summary ────────────────────────────────────────────────────
    if 'CREDIT_SEGMENT' in df.columns and 'INCOME_SEGMENT' in df.columns:
        seg_summary = df.groupby(['CREDIT_SEGMENT', 'INCOME_SEGMENT'],
                                  observed=True).agg(
            Count=('LOAN_ID', 'count'),
            Avg_Loan=('LOAN_AMOUNT', 'mean'),
            Default_Rate=('DEFAULT_FLAG', 'mean')
        ).round(2)
        seg_summary['Default_Rate'] = (seg_summary['Default_Rate'] * 100).round(2)
        results['segment_summary'] = seg_summary
        print("\n📌 Segment Summary (Credit × Income):")
        print(seg_summary.to_string())

    # ── 8. Default rate by income segment ────────────────────────────────────
    if 'INCOME_SEGMENT' in df.columns:
        inc_def = df.groupby('INCOME_SEGMENT', observed=True)['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Count='count'
        )
        inc_def['Default_Rate'] = (inc_def['Default_Rate'] * 100).round(2)
        results['income_segment_default'] = inc_def
        print("\n📌 Default Rate by Income Segment:")
        print(inc_def.to_string())

    results['df'] = df
    print("\n✅ Task 5 complete")
    return results
