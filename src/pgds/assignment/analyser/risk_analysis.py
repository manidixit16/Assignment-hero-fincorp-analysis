"""
TASK 18: Risk Assessment
- Develop a risk matrix for loan products based on Default_Amount,
  Loan_Term, and Interest_Rate
- Rank loan types by risk level and suggest mitigation strategies
- Analyse high-risk customer segments by credit score and income
"""

import pandas as pd


def risk_matrix(df, defaults=None):
    """
    Build a risk matrix across loan products and customer segments,
    and provide actionable mitigation strategies.

    Returns
    -------
    dict with keys: loan_risk_matrix, risk_ranked_purposes,
                    high_risk_segments, mitigation_strategies,
                    risk_by_term, risk_by_interest_band
    """
    results = {}
    print("\n" + "="*55)
    print(" TASK 18 — Risk Assessment")
    print("="*55)

    df = df.copy()

    # ── 1. Risk matrix by loan purpose ───────────────────────────────────────
    if 'LOAN_PURPOSE' in df.columns:
        risk_cols = {
            'Default_Rate':       ('DEFAULT_FLAG', 'mean'),
            'Avg_Default_Amount': ('DEFAULT_AMOUNT', 'mean') if 'DEFAULT_AMOUNT' in df.columns else ('LOAN_AMOUNT', 'mean'),
            'Avg_Loan_Term':      ('LOAN_TERM', 'mean'),
            'Avg_Interest_Rate':  ('INTEREST_RATE', 'mean'),
            'Count':              ('LOAN_ID', 'count'),
        }

        agg_dict = {v[0]: v[1] for v in risk_cols.values() if v[0] in df.columns}
        risk_matrix_df = df.groupby('LOAN_PURPOSE').agg(**{
            k: pd.NamedAgg(column=v[0], aggfunc=v[1])
            for k, v in risk_cols.items() if v[0] in df.columns
        }).round(4)

        if 'Default_Rate' in risk_matrix_df.columns:
            risk_matrix_df['Default_Rate_%'] = (risk_matrix_df['Default_Rate'] * 100).round(2)
            risk_matrix_df = risk_matrix_df.drop(columns='Default_Rate')

        # Composite risk score (normalised sum of default rate + interest rate)
        if 'Default_Rate_%' in risk_matrix_df.columns and 'Avg_Interest_Rate' in risk_matrix_df.columns:
            norm_def  = risk_matrix_df['Default_Rate_%'] / risk_matrix_df['Default_Rate_%'].max()
            norm_int  = risk_matrix_df['Avg_Interest_Rate'] / risk_matrix_df['Avg_Interest_Rate'].max()
            risk_matrix_df['Risk_Score'] = ((norm_def + norm_int) / 2).round(4)
            risk_matrix_df['Risk_Level']  = pd.cut(
                risk_matrix_df['Risk_Score'],
                bins=[0, 0.4, 0.65, 1.0],
                labels=['Low', 'Medium', 'High']
            )

        risk_matrix_df = risk_matrix_df.sort_values('Risk_Score', ascending=False)
        results['loan_risk_matrix'] = risk_matrix_df
        print("\n📌 Loan Product Risk Matrix:")
        print(risk_matrix_df.to_string())

    # ── 2. Risk ranking with mitigation strategies ────────────────────────────
    MITIGATION = {
        'Personal':       'Tighten income-to-EMI ratio (max 35%); require 2 references',
        'Education':      'Link disbursement to institution verification; add moratorium',
        'Vehicle':        'Require vehicle registration as collateral; GPS tracking',
        'Business':       'Mandate GST returns for 2 years; cap at 60% of turnover',
        'Home Renovation': 'Stage-wise disbursement tied to construction progress',
    }

    if 'loan_risk_matrix' in results:
        ranked = results['loan_risk_matrix'].reset_index()[['LOAN_PURPOSE', 'Risk_Score', 'Risk_Level']].copy() \
            if 'Risk_Level' in results['loan_risk_matrix'].columns else results['loan_risk_matrix'].reset_index()
        ranked['Mitigation'] = ranked['LOAN_PURPOSE'].map(MITIGATION).fillna('Standard credit policy applies')
        results['risk_ranked_purposes'] = ranked
        print("\n📌 Loan Types Ranked by Risk:")
        print(ranked.to_string(index=False))

    # ── 3. High-risk customer segments ───────────────────────────────────────
    if 'CREDIT_SCORE' in df.columns and 'ANNUAL_INCOME' in df.columns:
        income_33 = df['ANNUAL_INCOME'].quantile(0.33)

        df['RISK_SEGMENT'] = 'Standard'
        df.loc[
            (df['CREDIT_SCORE'] < 580) | (df['ANNUAL_INCOME'] < income_33),
            'RISK_SEGMENT'
        ] = 'High Risk'
        df.loc[
            (df['CREDIT_SCORE'] < 400) & (df['ANNUAL_INCOME'] < income_33),
            'RISK_SEGMENT'
        ] = 'Very High Risk'

        risk_seg = df.groupby('RISK_SEGMENT')['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Count='count'
        )
        risk_seg['Default_Rate_%'] = (risk_seg['Default_Rate'] * 100).round(2)
        results['high_risk_segments'] = risk_seg
        print("\n📌 High-Risk Customer Segments:")
        print(risk_seg[['Count', 'Default_Rate_%']].to_string())

    # ── 4. Risk by loan term ──────────────────────────────────────────────────
    if 'LOAN_TERM' in df.columns:
        risk_term = df.groupby('LOAN_TERM')['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Count='count'
        )
        risk_term['Default_Rate_%'] = (risk_term['Default_Rate'] * 100).round(2)
        results['risk_by_term'] = risk_term
        print("\n📌 Default Rate by Loan Term (months) — sample:")
        print(risk_term.head(10).to_string())

    # ── 5. Risk by interest rate band ────────────────────────────────────────
    if 'INTEREST_RATE' in df.columns:
        df['INTEREST_BAND'] = pd.cut(
            df['INTEREST_RATE'],
            bins=[0, 8, 11, 14, 20],
            labels=['Low (≤8%)', 'Medium (8-11%)', 'High (11-14%)', 'Very High (>14%)']
        )
        risk_int = df.groupby('INTEREST_BAND', observed=True)['DEFAULT_FLAG'].agg(
            Default_Rate='mean', Count='count'
        )
        risk_int['Default_Rate_%'] = (risk_int['Default_Rate'] * 100).round(2)
        results['risk_by_interest_band'] = risk_int
        print("\n📌 Default Rate by Interest Rate Band:")
        print(risk_int[['Count', 'Default_Rate_%']].to_string())

    print("\n✅ Task 18 complete")
    return results
