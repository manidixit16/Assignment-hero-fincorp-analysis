import pandas as pd
import numpy as np
import os

def clean_data(data):

    # -----------------------------------
    # CREATE FOLDERS
    # -----------------------------------
    os.makedirs("data/cleaned", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    cleaned = {}

    # -----------------------------------
    # OVERALL SUMMARY
    # -----------------------------------
    summary = {
        'missing_removed': 0,
        'duplicates_removed': 0,
        'invalid_dates_removed': 0,
        'negative_values_removed': 0,
        'outliers_capped': 0
    }

    dataset_summary = []

    # -----------------------------------
    # LOOP THROUGH DATASETS
    # -----------------------------------
    for name, df in data.items():

        print(f"\nCleaning {name} dataset...")

        ds_summary = {
            'dataset': name,
            'missing_removed': 0,
            'duplicates_removed': 0,
            'invalid_dates_removed': 0,
            'negative_values_removed': 0,
            'outliers_capped': 0
        }

        # -----------------------------------
        # 1. STANDARDIZE COLUMN NAMES
        # -----------------------------------
        df.columns = df.columns.str.strip().str.upper()

        # -----------------------------------
        # 2. REMOVE DUPLICATES
        # -----------------------------------
        duplicates = df.duplicated().sum()

        summary['duplicates_removed'] += duplicates
        ds_summary['duplicates_removed'] += duplicates

        df = df.drop_duplicates()

        # -----------------------------------
        # 3. HANDLE MISSING VALUES (CRITICAL FIX)
        # -----------------------------------
        before = df.shape[0]

        # Drop CUSTOMER_ID if missing (safe)
        if 'CUSTOMER_ID' in df.columns:
            df = df[df['CUSTOMER_ID'].notna()]

        # IMPORTANT FIX: DO NOT DROP LOAN_ID FOR APPLICATIONS
        if name != 'applications':
            if 'LOAN_ID' in df.columns:
                df = df[df['LOAN_ID'].notna()]

        removed = before - df.shape[0]

        summary['missing_removed'] += removed
        ds_summary['missing_removed'] += removed

        # Fill numeric
        for col in df.select_dtypes(include=np.number).columns:
            df[col] = df[col].fillna(df[col].median())

        # Fill categorical
        for col in df.select_dtypes(include='object').columns:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])
            else:
                df[col] = df[col].fillna("UNKNOWN")

        # -----------------------------------
        # 4. DATE STANDARDIZATION
        # -----------------------------------
        for col in df.columns:
            if 'DATE' in col:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # Drop invalid critical dates
        if name == 'loans' and 'DISBURSAL_DATE' in df.columns:
            before = df.shape[0]
            df = df[df['DISBURSAL_DATE'].notna()]
            removed = before - df.shape[0]

            summary['invalid_dates_removed'] += removed
            ds_summary['invalid_dates_removed'] += removed

        if name == 'applications' and 'APPLICATION_DATE' in df.columns:
            before = df.shape[0]
            df = df[df['APPLICATION_DATE'].notna()]
            removed = before - df.shape[0]

            summary['invalid_dates_removed'] += removed
            ds_summary['invalid_dates_removed'] += removed

        if name == 'defaults' and 'DEFAULT_DATE' in df.columns:
            before = df.shape[0]
            df = df[df['DEFAULT_DATE'].notna()]
            removed = before - df.shape[0]

            summary['invalid_dates_removed'] += removed
            ds_summary['invalid_dates_removed'] += removed

        # if 'INCOME' in df.columns:
        #     df.rename(columns={'INCOME': 'ANNUAL_INCOME'}, inplace=True)
        # -----------------------------------
        # 5. REMOVE IRRELEVANT COLUMNS
        # -----------------------------------
        df = df.drop(columns=[col for col in df.columns if 'NAME' in col], errors='ignore')

        # -----------------------------------
        # 6. OUTLIER HANDLING (IMPORTANT COLS ONLY)
        # -----------------------------------
        for col in ['LOAN_AMOUNT', 'INTEREST_RATE', 'DEFAULT_AMOUNT']:
            if col in df.columns:

                before_vals = df[col].copy()

                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1

                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR

                df[col] = np.clip(df[col], lower, upper)

                count = (before_vals != df[col]).sum()

                summary['outliers_capped'] += count
                ds_summary['outliers_capped'] += count

        # -----------------------------------
        # 7. INVALID VALUE REMOVAL
        # -----------------------------------
        if 'LOAN_AMOUNT' in df.columns:
            before = df.shape[0]
            df = df[df['LOAN_AMOUNT'] > 0]
            removed = before - df.shape[0]

            summary['negative_values_removed'] += removed
            ds_summary['negative_values_removed'] += removed

        if 'INTEREST_RATE' in df.columns:
            before = df.shape[0]
            df = df[df['INTEREST_RATE'] >= 0]
            removed = before - df.shape[0]

            summary['negative_values_removed'] += removed
            ds_summary['negative_values_removed'] += removed

        if 'DEFAULT_AMOUNT' in df.columns:
            before = df.shape[0]
            df = df[df['DEFAULT_AMOUNT'] >= 0]
            removed = before - df.shape[0]

            summary['negative_values_removed'] += removed
            ds_summary['negative_values_removed'] += removed

        # Save cleaned dataset
        cleaned[name] = df
        dataset_summary.append(ds_summary)

        print(f"{name} cleaned. Shape: {df.shape}")

    # -----------------------------------
    # GLOBAL FEATURE ENGINEERING
    # -----------------------------------

    loans = cleaned['loans']
    defaults = cleaned['defaults']
    customers = cleaned['customers']

    # DEFAULT FLAG
    loans['DEFAULT_FLAG'] = loans['LOAN_ID'].isin(defaults['LOAN_ID']).astype(int)

    # REGION
    loans = loans.merge(
        customers[['CUSTOMER_ID', 'REGION']],
        on='CUSTOMER_ID',
        how='left'
    )

    cleaned['loans'] = loans

    # -----------------------------------
    # SAVE CLEANED DATASETS
    # -----------------------------------
    for name, df in cleaned.items():
        df.to_csv(f"data/cleaned/{name}.csv", index=False)

    print("\nCleaned datasets saved")

    # -----------------------------------
    # SAVE SUMMARY
    # -----------------------------------
    overall_df = pd.DataFrame([summary])
    dataset_df = pd.DataFrame(dataset_summary)

    with pd.ExcelWriter("reports/data_cleaning_summary.xlsx") as writer:
        overall_df.to_excel(writer, sheet_name="overall", index=False)
        dataset_df.to_excel(writer, sheet_name="dataset_breakdown", index=False)

    dataset_df.to_csv("reports/data_cleaning_dataset_breakdown.csv", index=False)

    print("\nSummary saved")

    return cleaned