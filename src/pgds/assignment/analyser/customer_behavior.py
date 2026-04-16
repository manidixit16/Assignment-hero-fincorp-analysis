import pandas as pd

def customer_behavior_analysis(df, applications, customers):

    print("\n CUSTOMER BEHAVIOR ANALYSIS")

    results = {}

    # -----------------------------------
    # DETECT INCOME COLUMN (IMPORTANT FIX)
    # -----------------------------------
    income_col = None
    for col in customers.columns:
        if 'INCOME' in col.upper():
            income_col = col
            break

    # -----------------------------------
    # 1. REPAYMENT BEHAVIOR SEGMENTATION
    # -----------------------------------
    if 'CUSTOMER_ID' in df.columns and 'DEFAULT_FLAG' in df.columns:

        behavior = df.groupby('CUSTOMER_ID')['DEFAULT_FLAG'].mean()

        def categorize(x):
            if x == 0:
                return 'Always On Time'
            elif x < 0.5:
                return 'Occasional Defaulter'
            else:
                return 'Frequent Defaulter'

        segments = behavior.apply(categorize)

        print("\n Repayment Behavior:\n", segments.value_counts())

        results['behavior'] = segments

    else:
        print(" Missing CUSTOMER_ID or DEFAULT_FLAG")

    # -----------------------------------
    # 2. DEMOGRAPHIC ANALYSIS (FIXED)
    # -----------------------------------
    merged = applications.merge(
        customers,
        on='CUSTOMER_ID',
        how='left'
    )

    # AGE ANALYSIS
    if 'AGE' in merged.columns:

        merged['AGE_GROUP'] = pd.cut(
            merged['AGE'],
            bins=[18, 30, 50, 70],
            labels=['Young', 'Middle', 'Senior']
        )

        age_analysis = merged.groupby(
            ['AGE_GROUP', 'APPROVAL_STATUS']
        ).size()

        print("\n Approval by Age Group:\n", age_analysis)

        results['age'] = age_analysis

    else:
        print("AGE column not available")

    # GENDER ANALYSIS
    if 'GENDER' in merged.columns:

        gender_analysis = merged.groupby(
            ['GENDER', 'APPROVAL_STATUS']
        ).size()

        print("\n Approval by Gender:\n", gender_analysis)

        results['gender'] = gender_analysis

    else:
        print("GENDER column not available")

    # INCOME ANALYSIS (FIXED)
    if income_col and income_col in merged.columns:

        merged['INCOME_SEGMENT'] = pd.qcut(
            merged[income_col],
            3,
            labels=['Low', 'Medium', 'High']
        )

        income_analysis = merged.groupby(
            ['INCOME_SEGMENT', 'APPROVAL_STATUS']
        ).size()

        print("\n Approval by Income Segment:\n", income_analysis)

        results['income'] = income_analysis

    else:
        print(" Income column not available")

    # -----------------------------------
    # 3. HIGH-VALUE CUSTOMERS
    # -----------------------------------
    if income_col and income_col in df.columns:

        high_value = df[
            (df[income_col] > df[income_col].quantile(0.75)) &
            (df['DEFAULT_FLAG'] == 0)
        ]

        print("\n High Value Customers:", len(high_value))

        results['high_value'] = high_value

    else:
        print(" Cannot compute high-value customers (income missing)")

    return results