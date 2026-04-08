"""
TASK 7: Transaction and Recovery Analysis
- Analyse penalty payments and overdue trends
- Evaluate recovery rates by Default_Reason and Legal_Action
- Compare recovery rates across regions and branches
"""

import pandas as pd


def transaction_analysis(df, transactions=None, defaults=None, branches=None):
    """Alias — calls transaction_and_recovery_analysis."""
    return transaction_and_recovery_analysis(df, transactions, defaults, branches)


def transaction_and_recovery_analysis(df, transactions, defaults, branches):
    """
    Deep-dive into transaction patterns and recovery effectiveness.

    Returns
    -------
    dict with keys: penalty_ratio, overdue_trend, recovery_by_reason,
                    recovery_by_legal, region_recovery, branch_recovery,
                    monthly_penalty_trend, payment_mode_breakdown
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 7 — Transaction & Recovery Analysis")
    print("="*55)

    # ── 1. Penalty payment analysis ───────────────────────────────────────────
    if transactions is not None:
        tx = transactions.copy()

        # Detect column name (TRANSACTION_TYPE or PAYMENT_TYPE)
        type_col = next((c for c in ['TRANSACTION_TYPE', 'PAYMENT_TYPE']
                         if c in tx.columns), None)

        if type_col:
            tx_counts = tx[type_col].value_counts()
            penalty_count = tx[type_col].str.upper().eq('PENALTY').sum()
            total_count   = len(tx)
            penalty_ratio = penalty_count / total_count if total_count else 0

            results['transaction_type_counts'] = tx_counts
            results['penalty_ratio'] = penalty_ratio
            print(f"\n📌 Transaction Type Breakdown:")
            print(tx_counts.to_string())
            print(f"\n  Penalty ratio: {penalty_ratio:.2%} of all transactions")

        # Monthly penalty trend
        amt_col = next((c for c in ['AMOUNT', 'TRANSACTION_AMOUNT'] if c in tx.columns), None)
        if type_col and amt_col and 'TRANSACTION_DATE' in tx.columns:
            tx['TRANSACTION_DATE'] = pd.to_datetime(tx['TRANSACTION_DATE'], errors='coerce')
            monthly = (
                tx.groupby([tx['TRANSACTION_DATE'].dt.to_period('M'), type_col])[amt_col]
                .sum()
                .unstack(fill_value=0)
            )
            results['monthly_transaction_trend'] = monthly
            print(f"\n📌 Monthly Transaction Trend (last 3 periods):")
            print(monthly.tail(3).to_string())

        # Payment mode breakdown
        if 'MODE_OF_PAYMENT' in tx.columns:
            mode_breakdown = tx['MODE_OF_PAYMENT'].value_counts()
            results['payment_mode_breakdown'] = mode_breakdown
            print("\n📌 Payment Mode Breakdown:")
            print(mode_breakdown.to_string())

    # ── 2. Overdue trends ─────────────────────────────────────────────────────
    if 'OVERDUE_AMOUNT' in df.columns:
        overdue = df[df['OVERDUE_AMOUNT'] > 0].copy()
        results['overdue_count'] = len(overdue)
        results['overdue_total_amount'] = overdue['OVERDUE_AMOUNT'].sum()
        print(f"\n📌 Overdue Loans     : {len(overdue):,}")
        print(f"   Total Overdue Amt : ₹{overdue['OVERDUE_AMOUNT'].sum():,.0f}")

        if 'REGION' in overdue.columns:
            overdue_region = overdue.groupby('REGION')['OVERDUE_AMOUNT'].agg(
                Total='sum', Count='count', Avg='mean'
            ).round(0)
            results['overdue_by_region'] = overdue_region
            print("\n📌 Overdue Amount by Region:")
            print(overdue_region.to_string())

    # ── 3. Recovery rate by default reason ────────────────────────────────────
    if defaults is not None:
        defs = defaults.copy()
        if 'RECOVERY_RATE' not in defs.columns:
            defs['RECOVERY_RATE'] = (
                defs['RECOVERY_AMOUNT'] / defs['DEFAULT_AMOUNT'].replace(0, pd.NA)
            ).clip(0, 1)

        if 'DEFAULT_REASON' in defs.columns:
            reason_rec = defs.groupby('DEFAULT_REASON')['RECOVERY_RATE'].agg(
                Avg_Recovery_Rate='mean', Count='count'
            )
            reason_rec['Avg_Recovery_Rate'] = (reason_rec['Avg_Recovery_Rate'] * 100).round(2)
            results['recovery_by_reason'] = reason_rec
            print("\n📌 Recovery Rate by Default Reason:")
            print(reason_rec.to_string())

        # ── 4. Recovery by legal action ───────────────────────────────────────
        if 'LEGAL_ACTION' in defs.columns:
            legal_rec = defs.groupby('LEGAL_ACTION')['RECOVERY_RATE'].agg(
                Avg_Recovery_Rate='mean', Count='count'
            )
            legal_rec['Avg_Recovery_Rate'] = (legal_rec['Avg_Recovery_Rate'] * 100).round(2)
            results['recovery_by_legal'] = legal_rec
            print("\n📌 Recovery Rate by Legal Action:")
            print(legal_rec.to_string())

        # ── 5. Recovery by region ─────────────────────────────────────────────
        if 'REGION' in df.columns:
            merged = (
                df[['LOAN_ID', 'REGION']].drop_duplicates()
                .merge(defs[['LOAN_ID', 'RECOVERY_RATE']], on='LOAN_ID', how='inner')
            )
            if not merged.empty:
                region_rec = merged.groupby('REGION')['RECOVERY_RATE'].agg(
                    Avg_Recovery_Rate='mean', Count='count'
                )
                region_rec['Avg_Recovery_Rate'] = (region_rec['Avg_Recovery_Rate'] * 100).round(2)
                results['region_recovery'] = region_rec
                print("\n📌 Recovery Rate by Region:")
                print(region_rec.to_string())

    print("\n✅ Task 7 complete")
    return results
