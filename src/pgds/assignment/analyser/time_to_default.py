"""
TASK 19: Time to Default Analysis
- Calculate the average time from loan disbursement to default
- Identify loan purposes with the shortest time to default
- Compare time to default across customer demographics
"""

import pandas as pd


def time_to_default(df, defaults=None):
    """
    Measure how quickly loans default after disbursement and
    identify the highest-risk early-default profiles.

    Returns
    -------
    dict with keys: avg_days, median_days, ttd_stats,
                    ttd_by_purpose, ttd_by_employment,
                    ttd_by_age_group, ttd_distribution
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 19 — Time to Default Analysis")
    print("="*55)

    if defaults is not None and 'DEFAULT_DATE' in defaults.columns:
        defs_ttd = defaults[['LOAN_ID', 'DEFAULT_DATE']].copy().rename(
            columns={'DEFAULT_DATE': 'TTD_DEFAULT_DATE'}
        )
        merged = df.merge(defs_ttd, on='LOAN_ID', how='inner').copy()
        merged['DEFAULT_DATE_COL'] = pd.to_datetime(merged['TTD_DEFAULT_DATE'], errors='coerce')
    elif 'DEFAULT_DATE' in df.columns and 'DEFAULT_FLAG' in df.columns:
        merged = df[df['DEFAULT_FLAG'] == 1].copy()
        merged['DEFAULT_DATE_COL'] = pd.to_datetime(merged.get('DEFAULT_DATE'), errors='coerce')
    else:
        print("  ⚠️  DEFAULT_DATE not available — skipping Task 19")
        return results

    merged['DISBURSAL_DATE_COL'] = pd.to_datetime(
        merged.get('DISBURSAL_DATE', merged.get('REPAYMENT_START_DATE', pd.Series())),
        errors='coerce'
    )
    merged['TIME_TO_DEFAULT'] = (merged['DEFAULT_DATE_COL'] - merged['DISBURSAL_DATE_COL']).dt.days
    merged = merged[merged['TIME_TO_DEFAULT'] > 0].dropna(subset=['TIME_TO_DEFAULT'])

    if merged.empty:
        print("  ⚠️  No valid TIME_TO_DEFAULT values computed — check date columns")
        return results

    # ── 1. Overall statistics ─────────────────────────────────────────────────
    ttd_stats = merged['TIME_TO_DEFAULT'].describe().round(1)
    results['avg_days']    = round(merged['TIME_TO_DEFAULT'].mean(), 1)
    results['median_days'] = round(merged['TIME_TO_DEFAULT'].median(), 1)
    results['ttd_stats']   = ttd_stats

    print(f"\n📌 Time to Default Statistics (days):")
    print(ttd_stats.to_string())
    print(f"\n  Average : {results['avg_days']} days  (~{results['avg_days']/30:.1f} months)")
    print(f"  Median  : {results['median_days']} days  (~{results['median_days']/30:.1f} months)")

    # ── 2. By loan purpose ────────────────────────────────────────────────────
    if 'LOAN_PURPOSE' in merged.columns:
        ttd_purpose = merged.groupby('LOAN_PURPOSE')['TIME_TO_DEFAULT'].agg(
            Avg_Days='mean', Median_Days='median', Count='count'
        ).round(1).sort_values('Avg_Days')
        results['ttd_by_purpose'] = ttd_purpose
        print("\n📌 Avg Time to Default by Loan Purpose (shortest first):")
        print(ttd_purpose.to_string())

    # ── 3. By employment status ───────────────────────────────────────────────
    if 'EMPLOYMENT_STATUS' in merged.columns:
        ttd_emp = merged.groupby('EMPLOYMENT_STATUS')['TIME_TO_DEFAULT'].agg(
            Avg_Days='mean', Median_Days='median', Count='count'
        ).round(1).sort_values('Avg_Days')
        results['ttd_by_employment'] = ttd_emp
        print("\n📌 Avg Time to Default by Employment Status:")
        print(ttd_emp.to_string())

    # ── 4. By age group ───────────────────────────────────────────────────────
    if 'AGE' in merged.columns:
        merged['AGE_GROUP'] = pd.cut(
            merged['AGE'],
            bins=[18, 25, 35, 45, 55, 100],
            labels=['18-25', '26-35', '36-45', '46-55', '55+']
        )
        ttd_age = merged.groupby('AGE_GROUP', observed=True)['TIME_TO_DEFAULT'].agg(
            Avg_Days='mean', Median_Days='median', Count='count'
        ).round(1)
        results['ttd_by_age_group'] = ttd_age
        print("\n📌 Avg Time to Default by Age Group:")
        print(ttd_age.to_string())

    # ── 5. By region ──────────────────────────────────────────────────────────
    if 'REGION' in merged.columns:
        ttd_region = merged.groupby('REGION')['TIME_TO_DEFAULT'].agg(
            Avg_Days='mean', Median_Days='median', Count='count'
        ).round(1).sort_values('Avg_Days')
        results['ttd_by_region'] = ttd_region
        print("\n📌 Avg Time to Default by Region:")
        print(ttd_region.to_string())

    # ── 6. Distribution buckets ───────────────────────────────────────────────
    ttd_dist = pd.cut(
        merged['TIME_TO_DEFAULT'],
        bins=[0, 90, 180, 365, 730, 9999],
        labels=['0-3 months', '3-6 months', '6-12 months', '1-2 years', '>2 years']
    ).value_counts().sort_index()
    results['ttd_distribution'] = ttd_dist
    print("\n📌 Time-to-Default Distribution Buckets:")
    print(ttd_dist.to_string())

    print("\n✅ Task 19 complete")
    return results
