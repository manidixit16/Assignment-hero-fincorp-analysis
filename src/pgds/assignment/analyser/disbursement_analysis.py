"""
TASK 11: Loan Disbursement Efficiency
- Analyse time from application to loan disbursement; identify bottlenecks
- Compare average processing times across branches
- Evaluate disbursement trends by loan purpose and region
"""

import pandas as pd


def processing_time(df, applications=None):
    """Alias — calls disbursement_efficiency."""
    return disbursement_efficiency(df, applications=applications)


def disbursement_efficiency(df, applications=None):
    """
    Measure and benchmark loan disbursement speed and identify
    processing bottlenecks.

    Returns
    -------
    dict with keys: overall_avg_days, processing_by_region,
                    processing_by_purpose, bottleneck_branches,
                    monthly_disbursement_trend, disbursement_by_purpose,
                    disbursement_by_region
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 11 — Loan Disbursement Efficiency")
    print("="*55)

    # ── 1. Overall processing time ────────────────────────────────────────────
    source = applications if applications is not None else df
    source = source.copy()

    if 'PROCESSING_DAYS' not in source.columns:
        if 'APPLICATION_DATE' in source.columns and 'APPROVAL_DATE' in source.columns:
            source['APPLICATION_DATE'] = pd.to_datetime(source['APPLICATION_DATE'], errors='coerce')
            source['APPROVAL_DATE']    = pd.to_datetime(source['APPROVAL_DATE'],    errors='coerce')
            source['PROCESSING_DAYS']  = (source['APPROVAL_DATE'] - source['APPLICATION_DATE']).dt.days

    if 'PROCESSING_DAYS' in source.columns:
        valid_days = source[source['PROCESSING_DAYS'] > 0]['PROCESSING_DAYS']
        overall_avg = valid_days.mean()
        results['overall_avg_days'] = round(overall_avg, 1)
        print(f"\n📌 Overall Avg Processing Time : {overall_avg:.1f} days")
        print(f"   Median                       : {valid_days.median():.1f} days")
        print(f"   Min / Max                    : {valid_days.min():.0f} / {valid_days.max():.0f} days")

        # Processing time distribution
        results['processing_distribution'] = valid_days.describe().round(1)

    # ── 2. Processing time by region ──────────────────────────────────────────
    if 'PROCESSING_DAYS' in source.columns:
        # Join region from master df if not present in source
        if 'REGION' not in source.columns and 'LOAN_ID' in source.columns and 'REGION' in df.columns:
            source = source.merge(
                df[['LOAN_ID', 'REGION']].drop_duplicates(),
                on='LOAN_ID', how='left'
            )

        if 'REGION' in source.columns:
            region_proc = source[source['PROCESSING_DAYS'] > 0].groupby('REGION')['PROCESSING_DAYS'].agg(
                Avg_Days='mean', Median_Days='median', Count='count'
            ).round(1).sort_values('Avg_Days')
            results['processing_by_region'] = region_proc
            print("\n📌 Processing Time by Region (days):")
            print(region_proc.to_string())

        # Processing time by channel
        if 'SOURCE_CHANNEL' in source.columns:
            ch_proc = source[source['PROCESSING_DAYS'] > 0].groupby('SOURCE_CHANNEL')['PROCESSING_DAYS'].agg(
                Avg_Days='mean', Count='count'
            ).round(1).sort_values('Avg_Days')
            results['processing_by_channel'] = ch_proc
            print("\n📌 Processing Time by Source Channel:")
            print(ch_proc.to_string())

    # ── 3. Processing time by loan purpose ────────────────────────────────────
    if 'PROCESSING_DAYS' in source.columns and 'LOAN_PURPOSE' in source.columns:
        purp_proc = source[source['PROCESSING_DAYS'] > 0].groupby('LOAN_PURPOSE')['PROCESSING_DAYS'].agg(
            Avg_Days='mean', Count='count'
        ).round(1).sort_values('Avg_Days')
        results['processing_by_purpose'] = purp_proc
        print("\n📌 Processing Time by Loan Purpose:")
        print(purp_proc.to_string())

    # ── 4. Bottleneck branches (slowest) ──────────────────────────────────────
    if 'PROCESSING_DAYS' in source.columns and 'BRANCH_ID' in source.columns:
        branch_proc = source[source['PROCESSING_DAYS'] > 0].groupby('BRANCH_ID')['PROCESSING_DAYS'].agg(
            Avg_Days='mean', Count='count'
        ).round(1).sort_values('Avg_Days', ascending=False)
        results['bottleneck_branches'] = branch_proc.head(10)
        print("\n📌 Slowest 10 Branches (bottlenecks):")
        print(branch_proc.head(10).to_string())

    # ── 5. Monthly disbursement trend ─────────────────────────────────────────
    if 'DISBURSAL_DATE' in df.columns:
        df_copy = df.copy()
        df_copy['DISBURSAL_DATE'] = pd.to_datetime(df_copy['DISBURSAL_DATE'], errors='coerce')
        monthly_disb = df_copy.groupby(
            df_copy['DISBURSAL_DATE'].dt.to_period('M')
        )['LOAN_AMOUNT'].agg(Total_Disbursed='sum', Loan_Count='count')
        results['monthly_disbursement_trend'] = monthly_disb
        print(f"\n📌 Monthly Disbursement Trend (last 5 periods):")
        print(monthly_disb.tail(5).to_string())

    # ── 6. Disbursement by loan purpose ──────────────────────────────────────
    if 'LOAN_PURPOSE' in df.columns:
        disb_purpose = df.groupby('LOAN_PURPOSE')['LOAN_AMOUNT'].agg(
            Total='sum', Avg='mean', Count='count'
        ).round(0).sort_values('Total', ascending=False)
        results['disbursement_by_purpose'] = disb_purpose
        print("\n📌 Disbursement by Loan Purpose:")
        print(disb_purpose.to_string())

    # ── 7. Disbursement by region ─────────────────────────────────────────────
    if 'REGION' in df.columns:
        disb_region = df.groupby('REGION')['LOAN_AMOUNT'].agg(
            Total='sum', Avg='mean', Count='count'
        ).round(0).sort_values('Total', ascending=False)
        results['disbursement_by_region'] = disb_region
        print("\n📌 Disbursement by Region:")
        print(disb_region.to_string())

    print("\n✅ Task 11 complete")
    return results
