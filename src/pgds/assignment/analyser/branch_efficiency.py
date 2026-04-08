"""
TASK 15: Branch Efficiency
- Calculate the average loan disbursement time for each branch
- Identify branches with the highest number of rejected applications
- Compare branch efficiency based on disbursement volume and delinquency
"""

import pandas as pd


def branch_efficiency(df, applications=None, branches=None):
    """
    Measure and rank branch-level operational efficiency.

    Returns
    -------
    dict with keys: disbursement_time_by_branch, rejection_by_branch,
                    efficiency_scorecard, top_efficient, bottom_efficient
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 15 — Branch Efficiency")
    print("="*55)

    # ── 1. Avg disbursement time per branch ───────────────────────────────────
    src = applications if applications is not None else df
    src = src.copy()

    if 'PROCESSING_DAYS' not in src.columns:
        if 'APPLICATION_DATE' in src.columns and 'APPROVAL_DATE' in src.columns:
            src['APPLICATION_DATE'] = pd.to_datetime(src['APPLICATION_DATE'], errors='coerce')
            src['APPROVAL_DATE']    = pd.to_datetime(src['APPROVAL_DATE'],    errors='coerce')
            src['PROCESSING_DAYS']  = (src['APPROVAL_DATE'] - src['APPLICATION_DATE']).dt.days

    # Add REGION from master df if missing
    if 'REGION' not in src.columns and 'LOAN_ID' in src.columns and 'REGION' in df.columns:
        src = src.merge(df[['LOAN_ID', 'REGION']].drop_duplicates(), on='LOAN_ID', how='left')

    if 'PROCESSING_DAYS' in src.columns and 'REGION' in src.columns:
        disburse_time = (
            src[src['PROCESSING_DAYS'] > 0]
            .groupby('REGION')['PROCESSING_DAYS']
            .agg(Avg_Days='mean', Median_Days='median', Count='count')
            .round(1)
            .sort_values('Avg_Days')
        )
        results['disbursement_time_by_branch'] = disburse_time
        print("\n📌 Avg Disbursement Time by Region (fastest first):")
        print(disburse_time.to_string())
    elif 'PROCESSING_DAYS' in src.columns:
        avg_days = src[src['PROCESSING_DAYS'] > 0]['PROCESSING_DAYS'].mean()
        results['disbursement_time_by_branch'] = {'overall_avg_days': round(avg_days, 1)}
        print(f"\n📌 Overall Avg Processing Days: {avg_days:.1f}")

    # ── 2. Rejected applications by region ───────────────────────────────────
    if applications is not None and 'APPROVAL_STATUS' in applications.columns:
        apps = applications.copy()

        # Get region from master df via LOAN_ID
        if 'REGION' not in apps.columns and 'LOAN_ID' in apps.columns and 'REGION' in df.columns:
            apps = apps.merge(
                df[['LOAN_ID', 'REGION']].drop_duplicates(),
                on='LOAN_ID', how='left'
            )

        if 'REGION' in apps.columns:
            rej_by_region = (
                apps[apps['APPROVAL_STATUS'] == 'Rejected']
                .groupby('REGION').size()
                .sort_values(ascending=False)
                .rename('Rejection_Count')
                .reset_index()
            )
            total_by_region = apps.groupby('REGION').size().rename('Total_Applications').reset_index()
            rej_by_region = rej_by_region.merge(total_by_region, on='REGION', how='left')
            rej_by_region['Rejection_Rate_%'] = (
                rej_by_region['Rejection_Count'] / rej_by_region['Total_Applications'] * 100
            ).round(2)
            results['rejection_by_branch'] = rej_by_region
            print("\n📌 Rejection Count by Region:")
            print(rej_by_region.to_string(index=False))

    # ── 3. Efficiency scorecard (from branches table) ─────────────────────────
    if branches is not None:
        br = branches.copy()
        if 'DELINQUENT_LOANS' in br.columns and 'TOTAL_ACTIVE_LOANS' in br.columns:
            br['DELINQUENCY_RATE_%'] = (
                br['DELINQUENT_LOANS'] / br['TOTAL_ACTIVE_LOANS'] * 100
            ).round(2)

        score_cols = ['BRANCH_ID', 'BRANCH_NAME', 'REGION',
                      'LOAN_DISBURSEMENT_AMOUNT', 'DELINQUENCY_RATE_%',
                      'AVG_PROCESSING_TIME', 'TOTAL_ACTIVE_LOANS']
        score_cols = [c for c in score_cols if c in br.columns]
        scorecard = br[score_cols].sort_values('LOAN_DISBURSEMENT_AMOUNT', ascending=False)
        results['efficiency_scorecard'] = scorecard
        print("\n📌 Branch Efficiency Scorecard (top 10 by disbursement):")
        print(scorecard.head(10).to_string(index=False))

        # Best vs worst
        if 'DELINQUENCY_RATE_%' in scorecard.columns:
            results['top_efficient']    = scorecard.nsmallest(5, 'DELINQUENCY_RATE_%')
            results['bottom_efficient'] = scorecard.nlargest(5, 'DELINQUENCY_RATE_%')
            print("\n📌 5 Most Efficient Branches (lowest delinquency):")
            print(results['top_efficient'][['BRANCH_NAME', 'REGION', 'DELINQUENCY_RATE_%']].to_string(index=False))
            print("\n📌 5 Least Efficient Branches (highest delinquency):")
            print(results['bottom_efficient'][['BRANCH_NAME', 'REGION', 'DELINQUENCY_RATE_%']].to_string(index=False))

    print("\n✅ Task 15 complete")
    return results
