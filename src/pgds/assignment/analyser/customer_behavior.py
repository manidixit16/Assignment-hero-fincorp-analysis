import pandas as pd

def customer_behavior_analysis(df, applications):
    print("\n🧠 CUSTOMER BEHAVIOR ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. REPAYMENT BEHAVIOR SEGMENTATION
    # -----------------------------------
    customer_default = df.groupby('CUSTOMER_ID')['DEFAULT_FLAG'].sum()

    def categorize(x):
        if x == 0:
            return "Always On Time"
        elif x <= 2:
            return "Occasional Defaulter"
        else:
            return "Frequent Defaulter"

    behavior = customer_default.apply(categorize)
    results['behavior'] = behavior

    print("\nCustomer Behavior Distribution:\n", behavior.value_counts())

    # -----------------------------------
    # 2. DEMOGRAPHIC PATTERNS
    # -----------------------------------
    if 'ANNUAL_INCOME' in df.columns:
        df['INCOME_GROUP'] = pd.qcut(
            df['ANNUAL_INCOME'],
            q=3,
            labels=['Low', 'Medium', 'High']
        )

        income_pattern = df.groupby('INCOME_GROUP')['DEFAULT_FLAG'].mean()
        results['income_pattern'] = income_pattern

        print("\nDefault Rate by Income Group:\n", income_pattern)

    if 'REGION' in df.columns:
        region_pattern = df.groupby('REGION')['DEFAULT_FLAG'].mean()
        results['region_pattern'] = region_pattern

        print("\nDefault Rate by Region:\n", region_pattern)

    # -----------------------------------
    # 3. APPROVAL/REJECTION BY SEGMENT
    # -----------------------------------
    if 'CUSTOMER_ID' in applications.columns and 'APPROVAL_STATUS' in applications.columns:
        merged = df[['CUSTOMER_ID']].merge(applications, on='CUSTOMER_ID', how='left')

        approval_pattern = merged.groupby('APPROVAL_STATUS').size()
        results['approval_pattern'] = approval_pattern

        print("\nApproval Pattern:\n", approval_pattern)

    # -----------------------------------
    # 4. HIGH-VALUE CUSTOMERS
    # -----------------------------------
    if 'LOAN_AMOUNT' in df.columns:
        high_value = df[
            (df['DEFAULT_FLAG'] == 0) &
            (df['LOAN_AMOUNT'] > df['LOAN_AMOUNT'].quantile(0.75))
        ]

        results['high_value'] = high_value

        print("\nHigh Value Customers:", len(high_value))

    return results