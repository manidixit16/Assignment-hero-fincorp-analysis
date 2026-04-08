"""
TASK 10: Recovery Effectiveness
- Calculate ratio of Recovery_Amount to Default_Amount
- Compare recovery rates for defaults with and without legal actions
- Analyse branch-wise recovery performance
"""

import pandas as pd


def recovery_effectiveness(df, defaults=None, branches=None):
    """
    Measure and compare recovery effectiveness across legal action
    status, branches, and recovery status categories.

    Returns
    -------
    dict with keys: overall_recovery_rate, legal_comparison,
                    branch_recovery, recovery_status_summary,
                    total_default_amount, total_recovery_amount
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 10 — Recovery Effectiveness")
    print("="*55)

    # Use raw defaults table if available, else try from master df
    source = defaults.copy() if defaults is not None else df.copy()

    if 'DEFAULT_AMOUNT' not in source.columns or 'RECOVERY_AMOUNT' not in source.columns:
        print("  ⚠️  DEFAULT_AMOUNT / RECOVERY_AMOUNT not found — skipping Task 10")
        return results

    # ── 1. Overall recovery rate ──────────────────────────────────────────────
    total_default  = source['DEFAULT_AMOUNT'].sum()
    total_recovery = source['RECOVERY_AMOUNT'].sum()
    overall_rate   = total_recovery / total_default * 100 if total_default else 0

    results['total_default_amount']  = round(total_default, 2)
    results['total_recovery_amount'] = round(total_recovery, 2)
    results['overall_recovery_rate'] = round(overall_rate, 2)

    print(f"\n📌 Total Default Amount   : ₹{total_default:,.0f}")
    print(f"   Total Recovery Amount  : ₹{total_recovery:,.0f}")
    print(f"   Overall Recovery Rate  : {overall_rate:.2f}%")

    # Compute per-loan recovery rate
    source = source.copy()
    source['RECOVERY_RATE'] = (
        source['RECOVERY_AMOUNT'] / source['DEFAULT_AMOUNT'].replace(0, pd.NA)
    ).clip(0, 1)

    # ── 2. Legal action comparison ────────────────────────────────────────────
    if 'LEGAL_ACTION' in source.columns:
        legal_comp = source.groupby('LEGAL_ACTION').agg(
            Avg_Recovery_Rate=('RECOVERY_RATE', 'mean'),
            Total_Defaulted=('DEFAULT_AMOUNT', 'sum'),
            Total_Recovered=('RECOVERY_AMOUNT', 'sum'),
            Count=('DEFAULT_AMOUNT', 'count')
        )
        legal_comp['Avg_Recovery_Rate'] = (legal_comp['Avg_Recovery_Rate'] * 100).round(2)
        legal_comp['Portfolio_Recovery_%'] = (
            legal_comp['Total_Recovered'] / legal_comp['Total_Defaulted'] * 100
        ).round(2)
        results['legal_comparison'] = legal_comp
        print("\n📌 Recovery Rate — Legal Action vs None:")
        print(legal_comp.to_string())

    # ── 3. Recovery by recovery status ───────────────────────────────────────
    if 'RECOVERY_STATUS' in source.columns:
        status_summary = source.groupby('RECOVERY_STATUS').agg(
            Count=('DEFAULT_AMOUNT', 'count'),
            Total_Default=('DEFAULT_AMOUNT', 'sum'),
            Total_Recovery=('RECOVERY_AMOUNT', 'sum')
        )
        status_summary['Recovery_Rate_%'] = (
            status_summary['Total_Recovery'] / status_summary['Total_Default'] * 100
        ).round(2)
        results['recovery_status_summary'] = status_summary
        print("\n📌 Recovery by Recovery Status:")
        print(status_summary.to_string())

    # ── 4. Region-wise recovery performance ──────────────────────────────────
    if 'REGION' in df.columns:
        merged = (
            df[['LOAN_ID', 'REGION']].drop_duplicates()
            .merge(source[['LOAN_ID', 'RECOVERY_RATE', 'DEFAULT_AMOUNT', 'RECOVERY_AMOUNT']],
                   on='LOAN_ID', how='inner')
        )
        region_rec = merged.groupby('REGION').agg(
            Avg_Recovery_Rate=('RECOVERY_RATE', 'mean'),
            Total_Defaulted=('DEFAULT_AMOUNT', 'sum'),
            Total_Recovered=('RECOVERY_AMOUNT', 'sum'),
            Default_Count=('DEFAULT_AMOUNT', 'count')
        )
        region_rec['Avg_Recovery_Rate'] = (region_rec['Avg_Recovery_Rate'] * 100).round(2)
        region_rec = region_rec.sort_values('Avg_Recovery_Rate', ascending=False)
        results['branch_recovery'] = region_rec
        print("\n📌 Recovery Performance by Region:")
        print(region_rec.to_string())

    # ── 5. Default reason vs recovery ────────────────────────────────────────
    if 'DEFAULT_REASON' in source.columns:
        reason_rec = source.groupby('DEFAULT_REASON').agg(
            Avg_Recovery_Rate=('RECOVERY_RATE', 'mean'),
            Count=('DEFAULT_AMOUNT', 'count')
        )
        reason_rec['Avg_Recovery_Rate'] = (reason_rec['Avg_Recovery_Rate'] * 100).round(2)
        results['recovery_by_reason'] = reason_rec
        print("\n📌 Recovery Rate by Default Reason:")
        print(reason_rec.to_string())

    print("\n✅ Task 10 complete")
    return results
