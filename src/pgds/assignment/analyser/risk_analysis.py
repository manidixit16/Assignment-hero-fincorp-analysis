import pandas as pd

def risk_assessment(df, defaults):
    print("\n⚠️ RISK ASSESSMENT")

    results = {}

    # -----------------------------------
    # MERGE DEFAULT DATA
    # -----------------------------------
    merged = df.merge(defaults, on='LOAN_ID', how='left')

    # -----------------------------------
    # 1. RISK MATRIX
    # -----------------------------------
    required_cols = ['DEFAULT_AMOUNT', 'LOAN_TERM', 'INTEREST_RATE']

    available_cols = [c for c in required_cols if c in merged.columns]

    if len(available_cols) >= 2:
        risk_matrix = merged[available_cols].corr()

        results['risk_matrix'] = risk_matrix

        print("\nRisk Matrix:\n", risk_matrix)

    # -----------------------------------
    # 2. LOAN TYPE RISK RANKING
    # -----------------------------------
    if 'LOAN_TYPE' in merged.columns:
        loan_risk = merged.groupby('LOAN_TYPE')['DEFAULT_AMOUNT'].mean()

        loan_risk_sorted = loan_risk.sort_values(ascending=False)

        results['loan_risk'] = loan_risk_sorted

        print("\nLoan Type Risk Ranking:\n", loan_risk_sorted)

    # -----------------------------------
    # 3. HIGH-RISK CUSTOMER SEGMENTS
    # -----------------------------------
    if 'CREDIT_SCORE' in df.columns and 'ANNUAL_INCOME' in df.columns:

        df['CREDIT_SEGMENT'] = pd.cut(
            df['CREDIT_SCORE'],
            bins=[0, 500, 650, 750, 900],
            labels=['High Risk', 'Medium', 'Good', 'Excellent']
        )

        df['INCOME_GROUP'] = pd.qcut(
            df['ANNUAL_INCOME'],
            q=3,
            labels=['Low', 'Medium', 'High']
        )

        segment_risk = df.groupby(
            ['CREDIT_SEGMENT', 'INCOME_GROUP']
        )['DEFAULT_FLAG'].mean()

        results['segment_risk'] = segment_risk

        print("\nHigh-Risk Segments:\n", segment_risk)

    return results