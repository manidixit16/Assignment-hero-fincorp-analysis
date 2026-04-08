"""
featureEngineering.py
Legacy camelCase module retained for compatibility with reference repo.
Full implementation is in dataprocessor/feature_engineering.py
"""


def createFeatures(data):
    """
    Create derived features on the loans dataset.

    Features added
    --------------
    DEFAULT_FLAG     : 1 if loan appears in defaults table, else 0
    INTEREST_INCOME  : LOAN_AMOUNT * (INTEREST_RATE/100) * (LOAN_TERM/12)
    """
    loans    = data['loans']
    defaults = data['defaults']

    # Default flag
    loans['DEFAULT_FLAG'] = loans['LOAN_ID'].isin(defaults['LOAN_ID']).astype(int)

    # Interest income
    if 'INTEREST_RATE' in loans.columns and 'LOAN_TERM' in loans.columns:
        loans['INTEREST_INCOME'] = (
            loans['LOAN_AMOUNT'] * (loans['INTEREST_RATE'] / 100) * (loans['LOAN_TERM'] / 12)
        )
    else:
        # Fallback used in original reference repo (simple multiply)
        loans['INTEREST_INCOME'] = loans['LOAN_AMOUNT'] * loans['INTEREST_RATE']

    data['loans'] = loans
    print("✅ createFeatures complete")
    return data
