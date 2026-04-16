import pandas as pd

def risk_analysis(df):

    print("\n RISK ASSESSMENT")

    results = {}

    # -----------------------------------
    # DETECT INCOME COLUMN
    # -----------------------------------
    income_col = None
    for col in df.columns:
        if 'INCOME' in col.upper():
            income_col = col
            break

    # -----------------------------------
    # 1. RISK MATRIX
    # -----------------------------------
    required_cols = ['DEFAULT_AMOUNT', 'LOAN_TERM', 'INTEREST_RATE']

    if all(col in df.columns for col in required_cols):

        # Normalize (simple scaling)
        df['RISK_SCORE'] = (
            df['DEFAULT_AMOUNT'].fillna(0) +
            df['INTEREST_RATE'].fillna(0) +
            df['LOAN_TERM'].fillna(0)
        )

        print("\n Risk Score Created")

        results['risk_score'] = df['RISK_SCORE']

    else:
        print(" Missing columns for risk score")

    # -----------------------------------
    # 2. LOAN PURPOSE RISK
    # -----------------------------------
    if 'LOAN_PURPOSE' in df.columns and 'RISK_SCORE' in df.columns:

        purpose_risk = df.groupby('LOAN_PURPOSE')['RISK_SCORE'].mean().sort_values(ascending=False)

        print("\n Loan Purpose Risk Ranking:\n", purpose_risk)

        results['purpose_risk'] = purpose_risk

    else:
        print("LOAN_PURPOSE or RISK_SCORE missing")

    # -----------------------------------
    # 3. CUSTOMER RISK SEGMENTS
    # -----------------------------------
    if 'CREDIT_SCORE' in df.columns:

        df['CREDIT_SEGMENT'] = pd.cut(
            df['CREDIT_SCORE'],
            bins=[300, 600, 750, 900],
            labels=['Low', 'Medium', 'High']
        )

        if income_col:

            df['INCOME_SEGMENT'] = pd.qcut(
                df[income_col],
                3,
                labels=['Low', 'Medium', 'High']
            )

            risk_segment = df.groupby(
                ['CREDIT_SEGMENT', 'INCOME_SEGMENT']
            )['DEFAULT_FLAG'].mean()

            print("\n Risk by Customer Segment:\n", risk_segment)

            results['customer_risk'] = risk_segment

    else:
        print(" CREDIT_SCORE missing")

    return results