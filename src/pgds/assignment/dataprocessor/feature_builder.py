"""
Feature Builder
Creates derived columns used across all 20 analysis tasks,
including default flags, interest income, processing days,
and recovery rates.
"""
import pandas as pd


def create_features(data):
    """
    Enrich the cleaned datasets with calculated columns.

    Derived features
    ----------------
    loans:
        DEFAULT_FLAG     — 1 if loan appears in defaults table, else 0
        INTEREST_INCOME  — estimated interest revenue per loan
    applications:
        PROCESSING_DAYS  — calendar days between application and approval
    defaults:
        RECOVERY_RATE    — fraction of default amount recovered (0–1)
    """
    loans_df        = data['loans'].copy()
    applications_df = data['applications'].copy()
    defaults_df     = data['defaults'].copy()

    # --------------------------------------------------
    # LOANS: DEFAULT FLAG
    # --------------------------------------------------
    loans_df['DEFAULT_FLAG'] = (
        loans_df['LOAN_ID'].isin(defaults_df['LOAN_ID']).astype(int)
    )

    # --------------------------------------------------
    # LOANS: INTEREST INCOME ESTIMATE
    # --------------------------------------------------
    if {'LOAN_AMOUNT', 'INTEREST_RATE', 'LOAN_TERM'}.issubset(loans_df.columns):
        loans_df['INTEREST_INCOME'] = (
            loans_df['LOAN_AMOUNT']
            * (loans_df['INTEREST_RATE'] / 100)
            * (loans_df['LOAN_TERM'] / 12)
        )

    # --------------------------------------------------
    # APPLICATIONS: PROCESSING DAYS
    # --------------------------------------------------
    if {'APPLICATION_DATE', 'APPROVAL_DATE'}.issubset(applications_df.columns):
        applications_df['APPLICATION_DATE'] = pd.to_datetime(
            applications_df['APPLICATION_DATE'], errors='coerce'
        )
        applications_df['APPROVAL_DATE'] = pd.to_datetime(
            applications_df['APPROVAL_DATE'], errors='coerce'
        )
        applications_df['PROCESSING_DAYS'] = (
            applications_df['APPROVAL_DATE'] - applications_df['APPLICATION_DATE']
        ).dt.days

    # --------------------------------------------------
    # DEFAULTS: RECOVERY RATE
    # --------------------------------------------------
    if {'RECOVERY_AMOUNT', 'DEFAULT_AMOUNT'}.issubset(defaults_df.columns):
        defaults_df['RECOVERY_RATE'] = (
            defaults_df['RECOVERY_AMOUNT']
            / defaults_df['DEFAULT_AMOUNT'].replace(0, pd.NA)
        ).clip(0, 1)

    data['loans']        = loans_df
    data['applications'] = applications_df
    data['defaults']     = defaults_df

    print("[FeatureBuilder] Derived columns created successfully")
    return data
