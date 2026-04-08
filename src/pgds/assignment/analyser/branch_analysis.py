"""
TASK 4: Branch and Regional Performance
- Rank branches by loan disbursement volume
- Rank branches by processing time efficiency
- Rank branches by default rate and recovery rate
- Compare branch performance across regions
"""

import pandas as pd


def branch_analysis(df, applications=None, defaults=None, branches=None):
    """Alias that calls branch_performance for backward compatibility."""
    return branch_performance(df, applications=applications,
                              defaults=defaults, branches=branches)


def branch_performance(df, applications=None, defaults=None, branches=None):
    """
    Comprehensive branch and regional performance analysis.

    Returns
    -------
    dict with keys: disbursement_rank, processing_rank, default_rank,
                    recovery_rank, region_performance, delinquency_stats
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 4 — Branch & Regional Performance")
    print("="*55)

    # ── 1. Disbursement volume ranking ────────────────────────────────────────
    if branches is not None:
        disb_rank = branches.sort_values('LOAN_DISBURSEMENT_AMOUNT', ascending=False).copy()
        disb_rank['RANK'] = range(1, len(disb_rank) + 1)
        results['disbursement_rank'] = disb_rank[['RANK', 'BRANCH_NAME', 'REGION',
                                                    'LOAN_DISBURSEMENT_AMOUNT']].head(10)
        print("\n📌 Top 10 Branches by Disbursement Volume:")
        print(results['disbursement_rank'].to_string(index=False))

    # ── 2. Processing time efficiency ─────────────────────────────────────────
    if applications is not None and 'PROCESSING_DAYS' in applications.columns:
        if 'REGION' in applications.columns:
            proc_rank = (
                applications.groupby('REGION')['PROCESSING_DAYS']
                .mean().round(1).sort_values()
                .reset_index()
            )
            proc_rank.columns = ['REGION', 'AVG_PROCESSING_DAYS']
            results['processing_rank'] = proc_rank
            print("\n📌 Processing Time by Region (fastest first):")
            print(proc_rank.to_string(index=False))

        # Processing time by region (from master df)
        if 'REGION' in df.columns and 'LOAN_ID' in applications.columns:
            reg_proc = (
                applications.merge(df[['LOAN_ID', 'REGION']].drop_duplicates(),
                                   on='LOAN_ID', how='left')
                .groupby('REGION')['PROCESSING_DAYS'].mean().round(1)
                .sort_values()
            )
            results['processing_by_region'] = reg_proc
            print("\n📌 Avg Processing Time by Region (days):")
            print(reg_proc.to_string())

    # ── 3. Default rate ranking by region ────────────────────────────────────
    if 'DEFAULT_FLAG' in df.columns and 'REGION' in df.columns:
        def_rank = (
            df.groupby('REGION')['DEFAULT_FLAG']
            .mean()
            .mul(100).round(2)
            .sort_values(ascending=False)
            .reset_index()
        )
        def_rank.columns = ['REGION', 'DEFAULT_RATE_%']
        def_rank['RANK'] = range(1, len(def_rank) + 1)
        results['default_rank'] = def_rank
        print("\n📌 Default Rate by Region (ranked):")
        print(def_rank.to_string(index=False))

    # ── 4. Recovery rate ranking ──────────────────────────────────────────────
    if defaults is not None and 'REGION' in df.columns:
        if 'RECOVERY_RATE' in defaults.columns:
            rec_merged = (
                df[['LOAN_ID', 'REGION']].drop_duplicates()
                .merge(defaults[['LOAN_ID', 'RECOVERY_RATE']], on='LOAN_ID', how='left')
            )
            rec_rank = (
                rec_merged.groupby('REGION')['RECOVERY_RATE']
                .mean().mul(100).round(2)
                .sort_values(ascending=False)
                .reset_index()
            )
            rec_rank.columns = ['REGION', 'RECOVERY_RATE_%']
            results['recovery_rank'] = rec_rank
            print("\n📌 Recovery Rate by Region:")
            print(rec_rank.to_string(index=False))

    # ── 5. Region comparison ──────────────────────────────────────────────────
    if 'REGION' in df.columns:
        region_perf = df.groupby('REGION').agg(
            Total_Disbursement=('LOAN_AMOUNT', 'sum'),
            Loan_Count=('LOAN_ID', 'count'),
            Default_Rate=('DEFAULT_FLAG', 'mean'),
            Avg_Loan_Amount=('LOAN_AMOUNT', 'mean'),
            Avg_Interest_Rate=('INTEREST_RATE', 'mean')
        )
        region_perf['Default_Rate'] = (region_perf['Default_Rate'] * 100).round(2)
        region_perf['Avg_Loan_Amount'] = region_perf['Avg_Loan_Amount'].round(0)
        region_perf['Avg_Interest_Rate'] = region_perf['Avg_Interest_Rate'].round(2)
        results['region_performance'] = region_perf
        print("\n📌 Regional Performance Summary:")
        print(region_perf.to_string())

    # ── 6. Delinquency statistics ─────────────────────────────────────────────
    if branches is not None and 'DELINQUENT_LOANS' in branches.columns:
        branches = branches.copy()
        branches['DELINQUENCY_RATE_%'] = (
            branches['DELINQUENT_LOANS'] / branches['TOTAL_ACTIVE_LOANS'] * 100
        ).round(2)
        delinq_stats = branches.groupby('REGION')['DELINQUENCY_RATE_%'].agg(
            Mean='mean', Max='max', Min='min'
        ).round(2)
        results['delinquency_stats'] = delinq_stats
        print("\n📌 Delinquency Rate by Region (%):")
        print(delinq_stats.to_string())

    print("\n✅ Task 4 complete")
    return results
