"""
Default Velocity Analysis
Measures how quickly loans default after disbursement, segmented
by credit score tier and loan purpose.
"""
import pandas as pd


def default_velocity_analysis(df):
    """
    Compute 'days to default' distributions by credit score tier
    and loan purpose to identify fast-defaulting segments.
    """
    print("\n[TASK 19] Default Velocity Analysis")

    velocity = {}

    # --------------------------------------------------
    # 1. COMPUTE DAYS TO DEFAULT
    # --------------------------------------------------
    if 'DISBURSAL_DATE' in df.columns and 'DEFAULT_DATE' in df.columns:
        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')
        df['DEFAULT_DATE']   = pd.to_datetime(df['DEFAULT_DATE'],   errors='coerce')

        defaulted = df[df['DEFAULT_DATE'].notna()].copy()
        defaulted['DAYS_TO_DEFAULT'] = (
            defaulted['DEFAULT_DATE'] - defaulted['DISBURSAL_DATE']
        ).dt.days

        velocity['days_to_default_stats'] = defaulted['DAYS_TO_DEFAULT'].describe()
        print("\nDays-to-Default Summary:\n", velocity['days_to_default_stats'])

        # --------------------------------------------------
        # 2. BY CREDIT SCORE TIER
        # --------------------------------------------------
        if 'CREDIT_SCORE' in defaulted.columns:
            score_bins   = [0, 580, 720, float('inf')]
            score_labels = ['Low', 'Medium', 'High']
            defaulted['SCORE_TIER'] = pd.cut(
                defaulted['CREDIT_SCORE'], bins=score_bins, labels=score_labels
            )
            velocity_by_tier = defaulted.groupby('SCORE_TIER')['DAYS_TO_DEFAULT'].mean()
            velocity['velocity_by_tier'] = velocity_by_tier
            print("\nAvg Days to Default by Credit Tier:\n", velocity_by_tier)

        # --------------------------------------------------
        # 3. BY LOAN PURPOSE
        # --------------------------------------------------
        if 'LOAN_PURPOSE' in defaulted.columns:
            velocity_by_purpose = defaulted.groupby('LOAN_PURPOSE')['DAYS_TO_DEFAULT'].mean()
            velocity['velocity_by_purpose'] = velocity_by_purpose
            print("\nAvg Days to Default by Loan Purpose:\n", velocity_by_purpose)
    else:
        print(" DISBURSAL_DATE or DEFAULT_DATE not available — skipping velocity calc")

    return velocity
