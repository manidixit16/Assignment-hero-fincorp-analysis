"""Feature Engineering — derived columns used across all analysis tasks."""

import pandas as pd


def create_features(data):
    """
    Create derived features on the cleaned datasets.

    Features added
    --------------
    loans:
        DEFAULT_FLAG      : 1 if loan is in defaults table, else 0
        INTEREST_INCOME   : LOAN_AMOUNT * (INTEREST_RATE/100) * (LOAN_TERM/12)

    applications:
        PROCESSING_DAYS   : APPROVAL_DATE - APPLICATION_DATE in days

    defaults:
        RECOVERY_RATE     : RECOVERY_AMOUNT / DEFAULT_AMOUNT (capped 0–1)
    """
    loans        = data['loans'].copy()
    applications = data['applications'].copy()
    defaults     = data['defaults'].copy()

    # ── Loans ─────────────────────────────────────────────────────────────────
    loans['DEFAULT_FLAG'] = loans['LOAN_ID'].isin(defaults['LOAN_ID']).astype(int)

    if 'INTEREST_RATE' in loans.columns and 'LOAN_TERM' in loans.columns:
        loans['INTEREST_INCOME'] = (
            loans['LOAN_AMOUNT'] * (loans['INTEREST_RATE'] / 100) * (loans['LOAN_TERM'] / 12)
        )

    # ── Applications ──────────────────────────────────────────────────────────
    if 'APPROVAL_DATE' in applications.columns and 'APPLICATION_DATE' in applications.columns:
        applications['APPLICATION_DATE'] = pd.to_datetime(applications['APPLICATION_DATE'], errors='coerce')
        applications['APPROVAL_DATE']    = pd.to_datetime(applications['APPROVAL_DATE'],    errors='coerce')
        applications['PROCESSING_DAYS']  = (
            applications['APPROVAL_DATE'] - applications['APPLICATION_DATE']
        ).dt.days

    # ── Defaults ──────────────────────────────────────────────────────────────
    if 'RECOVERY_AMOUNT' in defaults.columns and 'DEFAULT_AMOUNT' in defaults.columns:
        defaults['RECOVERY_RATE'] = (
            defaults['RECOVERY_AMOUNT'] / defaults['DEFAULT_AMOUNT'].replace(0, pd.NA)
        ).clip(0, 1)

    data['loans']        = loans
    data['applications'] = applications
    data['defaults']     = defaults

    print("\n✅ Feature engineering complete")
    return data
