"""
TASK 20: Transaction Pattern Analysis
- Identify customers with irregular repayment patterns
- Analyse penalty payments as a proportion of total transactions
- Compare transaction amounts for overdue vs non-overdue loans
"""

import pandas as pd


def transaction_pattern(df, transactions=None):
    """
    Detect irregular repayment behaviour and analyse the structure
    of penalty vs regular EMI transactions.

    Returns
    -------
    dict with keys: penalty_summary, irregular_customers,
                    overdue_vs_nonoverdue, payment_mode_analysis,
                    monthly_penalty_pct, transaction_amount_stats
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 20 — Transaction Pattern Analysis")
    print("="*55)

    if transactions is None:
        print("  ⚠️  Transactions dataset not provided — skipping Task 20")
        return results

    tx = transactions.copy()

    # Detect column names
    type_col = next((c for c in ['PAYMENT_TYPE', 'TRANSACTION_TYPE'] if c in tx.columns), None)
    amt_col  = next((c for c in ['AMOUNT', 'TRANSACTION_AMOUNT'] if c in tx.columns), None)

    if type_col is None or amt_col is None:
        print("  ⚠️  Required columns not found in transactions dataset")
        return results

    # ── 1. Penalty summary ────────────────────────────────────────────────────
    tx_type_counts = tx[type_col].value_counts()
    penalty_count  = tx[type_col].str.upper().eq('PENALTY').sum()
    emi_count      = tx[type_col].str.upper().eq('EMI').sum()
    total_count    = len(tx)

    penalty_pct = penalty_count / total_count * 100 if total_count else 0
    penalty_amt = tx[tx[type_col].str.upper() == 'PENALTY'][amt_col].sum()
    total_amt   = tx[amt_col].sum()

    results['penalty_summary'] = {
        'Penalty_Count':      int(penalty_count),
        'EMI_Count':          int(emi_count),
        'Total_Transactions': int(total_count),
        'Penalty_Pct_%':      round(penalty_pct, 2),
        'Penalty_Amount':     round(penalty_amt, 2),
        'Penalty_Amt_Pct_%':  round(penalty_amt / total_amt * 100, 2) if total_amt else 0,
    }
    print(f"\n📌 Penalty Transaction Summary:")
    for k, v in results['penalty_summary'].items():
        print(f"   {k}: {v:,}" if isinstance(v, (int, float)) else f"   {k}: {v}")

    # ── 2. Irregular customers ────────────────────────────────────────────────
    # Customers with penalty transactions count > median penalty count
    if 'CUSTOMER_ID' in tx.columns:
        penalty_tx = tx[tx[type_col].str.upper() == 'PENALTY']
        cust_penalty_cnt = penalty_tx.groupby('CUSTOMER_ID').size().rename('Penalty_Count')
        median_penalty = cust_penalty_cnt.median()
        irregular = cust_penalty_cnt[cust_penalty_cnt > median_penalty].sort_values(ascending=False)
        results['irregular_customers'] = irregular
        print(f"\n📌 Irregular Customers (penalty count > median {median_penalty:.0f}): {len(irregular):,}")
        print(f"   Top 10 by penalty count:")
        print(irregular.head(10).to_string())

    # ── 3. Overdue vs non-overdue transaction amounts ─────────────────────────
    if 'LOAN_ID' in tx.columns and 'OVERDUE_AMOUNT' in df.columns:
        overdue_ids     = set(df[df['OVERDUE_AMOUNT'] > 0]['LOAN_ID'].dropna())
        tx['IS_OVERDUE'] = tx['LOAN_ID'].isin(overdue_ids).map(
            {True: 'Overdue', False: 'Non-Overdue'}
        )
        overdue_comp = tx.groupby('IS_OVERDUE')[amt_col].agg(
            Mean='mean', Median='median', Total='sum', Count='count'
        ).round(2)
        results['overdue_vs_nonoverdue'] = overdue_comp
        print("\n📌 Transaction Amounts — Overdue vs Non-Overdue Loans:")
        print(overdue_comp.to_string())

    # ── 4. Payment mode analysis ──────────────────────────────────────────────
    if 'MODE_OF_PAYMENT' in tx.columns:
        mode_analysis = tx.groupby('MODE_OF_PAYMENT').agg(
            Count=('CUSTOMER_ID', 'count') if 'CUSTOMER_ID' in tx.columns else (amt_col, 'count'),
            Total_Amount=(amt_col, 'sum'),
            Avg_Amount=(amt_col, 'mean')
        ).round(2).sort_values('Count', ascending=False)
        results['payment_mode_analysis'] = mode_analysis
        print("\n📌 Payment Mode Analysis:")
        print(mode_analysis.to_string())

    # ── 5. Monthly penalty percentage trend ──────────────────────────────────
    if 'TRANSACTION_DATE' in tx.columns:
        tx['TRANSACTION_DATE'] = pd.to_datetime(tx['TRANSACTION_DATE'], errors='coerce')
        monthly = tx.groupby([tx['TRANSACTION_DATE'].dt.to_period('M'), type_col])[amt_col] \
                    .sum().unstack(fill_value=0)
        if 'Penalty' in monthly.columns and 'EMI' in monthly.columns:
            monthly['Penalty_Pct_%'] = (
                monthly['Penalty'] / (monthly['EMI'] + monthly['Penalty']) * 100
            ).round(2)
            results['monthly_penalty_pct'] = monthly[['Penalty_Pct_%']]
            print(f"\n📌 Monthly Penalty % Trend (last 6 periods):")
            print(monthly[['Penalty_Pct_%']].tail(6).to_string())

    # ── 6. Transaction amount statistics ─────────────────────────────────────
    tx_stats = tx.groupby(type_col)[amt_col].describe().round(2)
    results['transaction_amount_stats'] = tx_stats
    print("\n📌 Transaction Amount Statistics by Type:")
    print(tx_stats.to_string())

    print("\n✅ Task 20 complete")
    return results
