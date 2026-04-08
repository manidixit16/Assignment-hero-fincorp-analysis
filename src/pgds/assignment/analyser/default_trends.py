"""
TASK 14: Default Trends
- Analyse the number of defaults over time to identify patterns
- Calculate the average default amount for different loan purposes
- Compare default rates across customer income categories
"""

import pandas as pd


def default_trends(df, defaults=None):
    """
    Analyse temporal and categorical patterns in loan defaults.

    Returns
    -------
    dict with keys: monthly_defaults, yearly_defaults,
                    default_by_purpose, default_by_income_category,
                    default_amount_stats, default_seasonality
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 14 — Default Trends")
    print("="*55)

    source = defaults.copy() if defaults is not None else df[df['DEFAULT_FLAG'] == 1].copy()

    # ── 1. Defaults over time ─────────────────────────────────────────────────
    date_col = next((c for c in ['DEFAULT_DATE'] if c in source.columns), None)

    if date_col:
        source[date_col] = pd.to_datetime(source[date_col], errors='coerce')
        source = source.dropna(subset=[date_col])

        # Monthly defaults
        monthly = source.groupby(source[date_col].dt.to_period('M')).agg(
            Default_Count=('DEFAULT_AMOUNT', 'count'),
            Total_Default_Amount=('DEFAULT_AMOUNT', 'sum')
        )
        results['monthly_defaults'] = monthly
        print(f"\n📌 Monthly Defaults — sample (last 5 periods):")
        print(monthly.tail(5).to_string())

        # Yearly defaults
        yearly = source.groupby(source[date_col].dt.year).agg(
            Default_Count=('DEFAULT_AMOUNT', 'count'),
            Total_Default_Amount=('DEFAULT_AMOUNT', 'sum'),
            Avg_Default_Amount=('DEFAULT_AMOUNT', 'mean')
        ).round(2)
        results['yearly_defaults'] = yearly
        print("\n📌 Yearly Default Summary:")
        print(yearly.to_string())

        # Seasonal pattern (month of year)
        monthly_pattern = source.groupby(source[date_col].dt.month).agg(
            Default_Count=('DEFAULT_AMOUNT', 'count')
        )
        monthly_pattern.index.name = 'Month'
        results['default_seasonality'] = monthly_pattern
        print("\n📌 Default Seasonality (by calendar month):")
        print(monthly_pattern.to_string())

    # ── 2. Avg default amount by loan purpose ─────────────────────────────────
    if 'LOAN_PURPOSE' in df.columns:
        purpose_df = df[df['DEFAULT_FLAG'] == 1].copy()
        if 'DEFAULT_AMOUNT' in purpose_df.columns:
            def_purpose = purpose_df.groupby('LOAN_PURPOSE').agg(
                Default_Count=('DEFAULT_AMOUNT', 'count'),
                Avg_Default_Amount=('DEFAULT_AMOUNT', 'mean'),
                Total_Default_Amount=('DEFAULT_AMOUNT', 'sum'),
                Default_Rate=('DEFAULT_FLAG', 'mean')
            ).round(2)
        else:
            def_purpose = purpose_df.groupby('LOAN_PURPOSE').agg(
                Default_Count=('LOAN_ID', 'count'),
                Default_Rate=('DEFAULT_FLAG', 'mean')
            ).round(4)
        results['default_by_purpose'] = def_purpose.sort_values('Default_Count', ascending=False)
        print("\n📌 Default Stats by Loan Purpose:")
        print(results['default_by_purpose'].to_string())

    # ── 3. Default rate by income category ───────────────────────────────────
    if 'ANNUAL_INCOME' in df.columns:
        df = df.copy()
        df['INCOME_CATEGORY'] = pd.cut(
            df['ANNUAL_INCOME'],
            bins=[0, 300000, 600000, 1000000, float('inf')],
            labels=['Low (<3L)', 'Lower-Mid (3-6L)', 'Upper-Mid (6-10L)', 'High (>10L)']
        )
        inc_def = df.groupby('INCOME_CATEGORY', observed=True)['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Count='count'
        )
        inc_def['Default_Rate_%'] = (inc_def['Default_Rate'] * 100).round(2)
        inc_def = inc_def.drop(columns='Default_Rate')
        results['default_by_income_category'] = inc_def
        print("\n📌 Default Rate by Income Category:")
        print(inc_def.to_string())

    # ── 4. Default amount statistics ──────────────────────────────────────────
    if 'DEFAULT_AMOUNT' in source.columns:
        def_stats = source['DEFAULT_AMOUNT'].describe().round(2)
        results['default_amount_stats'] = def_stats
        print("\n📌 Default Amount Statistics:")
        print(def_stats.to_string())

    # ── 5. Default trend by region ────────────────────────────────────────────
    if 'REGION' in df.columns:
        region_trend = df.groupby('REGION')['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Default_Count='sum', Total='count'
        )
        region_trend['Default_Rate_%'] = (region_trend['Default_Rate'] * 100).round(2)
        region_trend = region_trend.sort_values('Default_Rate_%', ascending=False)
        results['default_by_region'] = region_trend
        print("\n📌 Default Rate by Region:")
        print(region_trend[['Default_Count', 'Total', 'Default_Rate_%']].to_string())

    print("\n✅ Task 14 complete")
    return results
