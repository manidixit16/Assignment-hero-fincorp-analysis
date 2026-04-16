import pandas as pd

def customer_segmentation(df):

    print("\n CUSTOMER SEGMENTATION")

    results = {}

    # -----------------------------------
    # 1. CREATE SEGMENTS
    # -----------------------------------

    # Income Segmentation
    if 'ANNUAL_INCOME' in df.columns:
        df['INCOME_SEGMENT'] = pd.qcut(
            df['ANNUAL_INCOME'],
            3,
            labels=['Low', 'Medium', 'High']
        )

    # Credit Score Segmentation
    if 'CREDIT_SCORE' in df.columns:
        df['CREDIT_SEGMENT'] = pd.cut(
            df['CREDIT_SCORE'],
            bins=[300, 600, 750, 900],
            labels=['Low', 'Medium', 'High']
        )

    # Loan Status
    if 'DEFAULT_FLAG' in df.columns:
        df['LOAN_STATUS'] = df['DEFAULT_FLAG'].map({
            0: 'Non-Default',
            1: 'Default'
        })

    # -----------------------------------
    # 2. HIGH-RISK CUSTOMERS
    # -----------------------------------
    high_risk = df[
        (df['CREDIT_SEGMENT'] == 'Low') &
        (df['DEFAULT_FLAG'] == 1)
    ]

    print("\n High Risk Customers:", len(high_risk))

    results['high_risk'] = high_risk

    # -----------------------------------
    # 3. HIGH-VALUE CUSTOMERS
    # -----------------------------------
    high_value = df[
        (df['INCOME_SEGMENT'] == 'High') &
        (df['DEFAULT_FLAG'] == 0)
    ]

    print("\n High Value Customers:", len(high_value))

    results['high_value'] = high_value

    # -----------------------------------
    # 4. REPAYMENT BEHAVIOR
    # -----------------------------------
    if 'OVERDUE_AMOUNT' in df.columns:

        repayment = df.groupby('INCOME_SEGMENT')['OVERDUE_AMOUNT'].mean()

        print("\n Repayment Behavior by Income:\n", repayment)

        results['repayment'] = repayment

    return results