"""
TASK 9: Loan Application Insights
- Calculate approval and rejection rates
- Identify the most common reasons for loan rejection
- Compare application processing fees between approved and rejected applications
"""

import pandas as pd


def application_analysis(df, applications=None):
    """
    Analyse Hero FinCorp loan application patterns, approval rates,
    rejection drivers, and processing fees.

    Parameters
    ----------
    df           : pd.DataFrame  — master merged dataset
    applications : pd.DataFrame  — raw applications table (preferred)

    Returns
    -------
    dict with keys: approval_rate, rejection_rate, status_counts,
                    rejection_reasons, fee_comparison, monthly_approval_trend,
                    approval_by_channel, approval_by_purpose
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 9 — Loan Application Insights")
    print("="*55)

    # Use raw applications table when available, else fall back to master df
    source = applications if applications is not None else df
    source = source.copy()

    # Detect column names
    status_col  = next((c for c in ['APPROVAL_STATUS'] if c in source.columns), None)
    reason_col  = next((c for c in ['REJECTION_REASON'] if c in source.columns), None)
    fee_col     = next((c for c in ['PROCESSING_FEE'] if c in source.columns), None)
    channel_col = next((c for c in ['SOURCE_CHANNEL'] if c in source.columns), None)
    purpose_col = next((c for c in ['LOAN_PURPOSE'] if c in source.columns), None)

    if status_col is None:
        print("  ⚠️  APPROVAL_STATUS column not found — skipping Task 9")
        return results

    # ── 1. Approval / rejection rates ─────────────────────────────────────────
    status_counts = source[status_col].value_counts()
    total         = len(source)
    approval_rate  = status_counts.get('Approved', 0) / total * 100
    rejection_rate = status_counts.get('Rejected', 0) / total * 100

    results['status_counts']  = status_counts
    results['approval_rate']  = round(approval_rate, 2)
    results['rejection_rate'] = round(rejection_rate, 2)

    print(f"\n📌 Application Status Breakdown:")
    print(status_counts.to_string())
    print(f"\n  Approval Rate  : {approval_rate:.2f}%")
    print(f"  Rejection Rate : {rejection_rate:.2f}%")

    # ── 2. Rejection reasons ──────────────────────────────────────────────────
    if reason_col:
        rejected = source[source[status_col] == 'Rejected']
        rej_reasons = (
            rejected[reason_col]
            .value_counts()
            .rename_axis('Reason')
            .reset_index(name='Count')
        )
        rej_reasons['Pct_of_Rejections'] = (
            rej_reasons['Count'] / len(rejected) * 100
        ).round(2)
        results['rejection_reasons'] = rej_reasons
        print("\n📌 Top Rejection Reasons:")
        print(rej_reasons.to_string(index=False))

    # ── 3. Processing fee comparison ──────────────────────────────────────────
    if fee_col:
        fee_comp = source.groupby(status_col)[fee_col].agg(
            Mean='mean', Median='median', Count='count'
        ).round(2)
        results['fee_comparison'] = fee_comp
        print("\n📌 Processing Fee — Approved vs Rejected:")
        print(fee_comp.to_string())

    # ── 4. Monthly approval trend ─────────────────────────────────────────────
    if 'APPLICATION_DATE' in source.columns:
        source['APPLICATION_DATE'] = pd.to_datetime(source['APPLICATION_DATE'], errors='coerce')
        monthly = source.groupby(
            [source['APPLICATION_DATE'].dt.to_period('M'), status_col]
        ).size().unstack(fill_value=0)
        results['monthly_approval_trend'] = monthly
        print(f"\n📌 Monthly Approval Trend (last 3 periods):")
        print(monthly.tail(3).to_string())

    # ── 5. Approval rate by source channel ────────────────────────────────────
    if channel_col:
        ch_approval = source.groupby(channel_col)[status_col].apply(
            lambda x: (x == 'Approved').mean() * 100
        ).round(2).rename('Approval_Rate_%')
        results['approval_by_channel'] = ch_approval
        print("\n📌 Approval Rate by Source Channel:")
        print(ch_approval.to_string())

    # ── 6. Approval rate by loan purpose ─────────────────────────────────────
    if purpose_col:
        purp_approval = source.groupby(purpose_col)[status_col].apply(
            lambda x: (x == 'Approved').mean() * 100
        ).round(2).rename('Approval_Rate_%')
        results['approval_by_purpose'] = purp_approval
        print("\n📌 Approval Rate by Loan Purpose:")
        print(purp_approval.to_string())

    print("\n✅ Task 9 complete")
    return results
