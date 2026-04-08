"""
defaultAnalyzer.py
Legacy camelCase module retained for compatibility with reference repo.
Full Task 3 implementation is in analyser/default_analysis.py
"""


def defaultMetrics(df):
    """
    Compute key default metrics: overall rate and risk by credit score.

    Returns
    -------
    dict with default_rate and credit_risk summary
    """
    default_rate = df['DEFAULT_FLAG'].mean()

    by_credit = df.groupby('CREDIT_SCORE')['DEFAULT_FLAG'].mean() \
        if 'CREDIT_SCORE' in df.columns else None

    print(f"\n📌 Overall Default Rate: {default_rate:.2%}")
    if by_credit is not None:
        print("\n📌 Default Rate by Credit Score (stats):")
        print(by_credit.describe().round(4).to_string())

    return {
        "default_rate":  round(default_rate, 4),
        "credit_risk":   by_credit.describe() if by_credit is not None else None
    }


def defaultByRegion(df):
    """Default rate broken down by region."""
    if 'REGION' not in df.columns:
        return None
    region_def = df.groupby('REGION')['DEFAULT_FLAG'].agg(
        Default_Rate='mean', Count='count'
    )
    region_def['Default_Rate_%'] = (region_def['Default_Rate'] * 100).round(2)
    print("\n📌 Default Rate by Region:")
    print(region_def[['Count', 'Default_Rate_%']].to_string())
    return region_def


def defaultByPurpose(df):
    """Default rate broken down by loan purpose."""
    if 'LOAN_PURPOSE' not in df.columns:
        return None
    purpose_def = df.groupby('LOAN_PURPOSE')['DEFAULT_FLAG'].agg(
        Default_Rate='mean', Count='count'
    )
    purpose_def['Default_Rate_%'] = (purpose_def['Default_Rate'] * 100).round(2)
    print("\n📌 Default Rate by Loan Purpose:")
    print(purpose_def[['Count', 'Default_Rate_%']].to_string())
    return purpose_def
