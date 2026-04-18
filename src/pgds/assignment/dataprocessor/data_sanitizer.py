"""
Data Sanitizer
Handles all data cleaning steps: duplicate removal, missing value
imputation, date standardisation, outlier capping, and saving
cleaned datasets to data/cleaned/.
"""
import os
import numpy as np
import pandas as pd


def clean_data(data):
    """
    Apply a consistent cleaning pipeline to every dataset in `data`.
    Returns a dict of cleaned DataFrames and saves them to disk.
    """
    os.makedirs("data/cleaned", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    cleaned = {}

    # --------------------------------------------------
    # TRACKING COUNTERS
    # --------------------------------------------------
    totals = {
        'missing_removed':       0,
        'duplicates_removed':    0,
        'invalid_dates_removed': 0,
        'negatives_removed':     0,
        'outliers_capped':       0,
    }
    per_dataset_log = []

    # --------------------------------------------------
    # PROCESS EACH DATASET
    # --------------------------------------------------
    for ds_name, frame in data.items():
        print(f"\n[Sanitizer] Cleaning: {ds_name}")
        ds_log = {k: 0 for k in totals}
        ds_log['dataset'] = ds_name

        # 1. STANDARDISE COLUMN NAMES
        frame.columns = frame.columns.str.strip().str.upper()

        # 2. REMOVE DUPLICATES
        n_dupes = frame.duplicated().sum()
        frame = frame.drop_duplicates()
        totals['duplicates_removed'] += n_dupes
        ds_log['duplicates_removed']  = n_dupes

        # 3. DROP ROWS WITH MISSING KEY IDs
        before = len(frame)
        if 'CUSTOMER_ID' in frame.columns:
            frame = frame[frame['CUSTOMER_ID'].notna()]
        if ds_name != 'applications' and 'LOAN_ID' in frame.columns:
            frame = frame[frame['LOAN_ID'].notna()]
        removed = before - len(frame)
        totals['missing_removed'] += removed
        ds_log['missing_removed']  = removed

        # 4. FILL REMAINING MISSING VALUES
        for col in frame.select_dtypes(include=np.number).columns:
            frame[col] = frame[col].fillna(frame[col].median())
        for col in frame.select_dtypes(include='object').columns:
            mode_val = frame[col].mode()
            frame[col] = frame[col].fillna(mode_val[0] if not mode_val.empty else "UNKNOWN")

        # 5. PARSE & VALIDATE DATE COLUMNS
        for col in frame.columns:
            if 'DATE' in col:
                frame[col] = pd.to_datetime(frame[col], errors='coerce')

        critical_dates = {
            'loans':        'DISBURSAL_DATE',
            'applications': 'APPLICATION_DATE',
            'defaults':     'DEFAULT_DATE',
        }
        if ds_name in critical_dates:
            date_col = critical_dates[ds_name]
            if date_col in frame.columns:
                before = len(frame)
                frame = frame[frame[date_col].notna()]
                removed = before - len(frame)
                totals['invalid_dates_removed'] += removed
                ds_log['invalid_dates_removed']  = removed

        # 6. DROP NAME COLUMNS (PII)
        frame = frame.drop(
            columns=[c for c in frame.columns if 'NAME' in c],
            errors='ignore'
        )

        # 7. CAP OUTLIERS ON KEY NUMERIC COLUMNS
        for col in ['LOAN_AMOUNT', 'INTEREST_RATE', 'DEFAULT_AMOUNT']:
            if col in frame.columns:
                original = frame[col].copy()
                q1, q3 = frame[col].quantile([0.25, 0.75])
                iqr = q3 - q1
                frame[col] = np.clip(frame[col], q1 - 1.5 * iqr, q3 + 1.5 * iqr)
                capped = (original != frame[col]).sum()
                totals['outliers_capped'] += capped
                ds_log['outliers_capped']  += capped

        # 8. REMOVE INVALID VALUES
        for col, condition in [
            ('LOAN_AMOUNT',   frame['LOAN_AMOUNT']   > 0  if 'LOAN_AMOUNT'   in frame.columns else None),
            ('INTEREST_RATE', frame['INTEREST_RATE'] >= 0 if 'INTEREST_RATE' in frame.columns else None),
            ('DEFAULT_AMOUNT',frame['DEFAULT_AMOUNT']>= 0 if 'DEFAULT_AMOUNT'in frame.columns else None),
        ]:
            if condition is not None:
                before = len(frame)
                frame = frame[condition]
                removed = before - len(frame)
                totals['negatives_removed'] += removed
                ds_log['negatives_removed']  += removed

        cleaned[ds_name] = frame
        per_dataset_log.append(ds_log)
        print(f"  Done — shape: {frame.shape}")

    # --------------------------------------------------
    # CROSS-DATASET FEATURE: DEFAULT FLAG & REGION
    # --------------------------------------------------
    loans_df     = cleaned['loans']
    defaults_df  = cleaned['defaults']
    customers_df = cleaned['customers']

    loans_df['DEFAULT_FLAG'] = loans_df['LOAN_ID'].isin(defaults_df['LOAN_ID']).astype(int)
    loans_df = loans_df.merge(
        customers_df[['CUSTOMER_ID', 'REGION']],
        on='CUSTOMER_ID', how='left'
    )
    cleaned['loans'] = loans_df

    # --------------------------------------------------
    # SAVE CLEANED FILES
    # --------------------------------------------------
    for ds_name, frame in cleaned.items():
        frame.to_csv(f"data/cleaned/{ds_name}.csv", index=False)
    print("\n[Sanitizer] All cleaned datasets saved to data/cleaned/")

    # SAVE CLEANING REPORT
    summary_df  = pd.DataFrame([totals])
    detail_df   = pd.DataFrame(per_dataset_log)
    with pd.ExcelWriter("reports/data_cleaning_summary.xlsx") as writer:
        summary_df.to_excel(writer, sheet_name="overall",    index=False)
        detail_df.to_excel( writer, sheet_name="by_dataset", index=False)
    detail_df.to_csv("reports/data_cleaning_dataset_breakdown.csv", index=False)
    print("[Sanitizer] Cleaning report saved")

    return cleaned
