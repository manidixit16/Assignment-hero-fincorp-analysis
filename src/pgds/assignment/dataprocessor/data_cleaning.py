import pandas as pd
import numpy as np

def clean_data(data):
    cleaned = {}

    for name, df in data.items():

        print(f"\n🔍 Cleaning {name} dataset...")

        # -----------------------------
        # 1. STANDARDIZE COLUMN NAMES
        # -----------------------------
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.upper()

        # -----------------------------
        # 2. REMOVE DUPLICATES
        # -----------------------------
        duplicates = df.duplicated().sum()
        print(f"Duplicates found: {duplicates}")
        df = df.drop_duplicates()

        # -----------------------------
        # 3. HANDLE MISSING VALUES
        # -----------------------------
        missing = df.isnull().sum()
        print("Missing values:\n", missing[missing > 0])

        # Drop critical missing IDs
        if 'CUSTOMER_ID' in df.columns:
            df = df.dropna(subset=['CUSTOMER_ID'])

        if 'LOAN_ID' in df.columns:
            df = df.dropna(subset=['LOAN_ID'])

        # Fill numeric columns
        for col in df.select_dtypes(include=np.number).columns:
            df[col] = df[col].fillna(df[col].median())

        # Fill categorical columns
        for col in df.select_dtypes(include='object').columns:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])
            else:
                df[col] = df[col].fillna("UNKNOWN")

        # -----------------------------
        # 4. STANDARDIZE DATE FORMATS (CRITICAL FIX)
        # -----------------------------
        # -----------------------------
        # 4. STANDARDIZE DATE FORMATS (IMPROVED)
        # -----------------------------
        date_cols = [col for col in df.columns if 'DATE' in col]

        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')

            # Remove invalid dates (CRITICAL FIX for .dt errors)
            invalid_dates = df[col].isna().sum()
            if invalid_dates > 0:
                print(f"⚠️ {invalid_dates} invalid dates found in {col}, removing...")
                df = df[df[col].notna()]
        # for col in df.columns:
        #     if 'DATE' in col:
        #         df[col] = pd.to_datetime(df[col], errors='coerce')
        #
        # # 🔥 REMOVE INVALID DATES (fix .dt errors globally)
        # for col in df.columns:
        #     if 'DATE' in col:
        #         df = df[df[col].notna()]

        # -----------------------------
        # 5. REMOVE IRRELEVANT COLUMNS
        # -----------------------------
        irrelevant_cols = [col for col in df.columns if 'NAME' in col]
        df = df.drop(columns=irrelevant_cols, errors='ignore')

        # -----------------------------
        # 6. HANDLE OUTLIERS (CAPPING)
        # -----------------------------
        numeric_cols = df.select_dtypes(include=np.number).columns

        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            df[col] = np.where(df[col] < lower, lower, df[col])
            df[col] = np.where(df[col] > upper, upper, df[col])

        # -----------------------------
        # 7. INVALID VALUES CHECK
        # -----------------------------
        if 'LOAN_AMOUNT' in df.columns:
            df = df[df['LOAN_AMOUNT'] > 0]

        if 'INTEREST_RATE' in df.columns:
            df = df[df['INTEREST_RATE'] >= 0]

        # -----------------------------
        # 8. REGION STANDARDIZATION (NEW)
        # -----------------------------
        if 'REGION' in df.columns:
            df['REGION'] = df['REGION'].astype(str).str.upper().str.strip()

        # -----------------------------
        # SAVE CLEANED DATA
        # -----------------------------
        cleaned[name] = df

        print(f"✅ {name} cleaned. Shape: {df.shape}")

    # =========================================
    # 🔥 GLOBAL FEATURE ENGINEERING (IMPORTANT)
    # =========================================

    # 9. CREATE DEFAULT FLAG (LOANS LEVEL)
    if 'loans' in cleaned and 'defaults' in cleaned:
        loans = cleaned['loans']
        defaults = cleaned['defaults']

        loans['DEFAULT_FLAG'] = loans['LOAN_ID'].isin(
            defaults['LOAN_ID']
        ).astype(int)

        cleaned['loans'] = loans

        print("\n✅ DEFAULT_FLAG created in loans dataset")

    # 10. ENSURE REGION IN LOANS (FOR ANALYSIS)
    if 'loans' in cleaned and 'customers' in cleaned:
        loans = cleaned['loans']
        customers = cleaned['customers']

        if 'REGION' in customers.columns:
            loans = loans.merge(
                customers[['CUSTOMER_ID', 'REGION']],
                on='CUSTOMER_ID',
                how='left'
            )

            cleaned['loans'] = loans

            print("✅ REGION added to loans dataset")

    return cleaned