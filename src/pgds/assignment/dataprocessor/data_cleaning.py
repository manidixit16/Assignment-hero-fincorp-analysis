import pandas as pd
import numpy as np

def clean_data(data):
    cleaned = {}

    for name, df in data.items():

        print(f"\n🔍 Cleaning {name} dataset...")

        # -----------------------------
        # 1. STANDARDIZE COLUMN NAMES
        # -----------------------------
        # df.columns = df.columns.str.strip().str.upper()
        df.columns = df.columns.str.strip()  # remove spaces
        df.columns = df.columns.str.upper()  # 🔥 REQUIRED FIX

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

        # Fill numeric columns with median
        for col in df.select_dtypes(include=np.number).columns:
            df[col] = df[col].fillna(df[col].median())

        # Fill categorical columns with mode
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "UNKNOWN")

        # -----------------------------
        # 4. STANDARDIZE DATE FORMATS
        # -----------------------------
        for col in df.columns:
            if 'DATE' in col:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # -----------------------------
        # 5. REMOVE IRRELEVANT COLUMNS
        # -----------------------------
        irrelevant_cols = [col for col in df.columns if 'NAME' in col]
        df = df.drop(columns=irrelevant_cols, errors='ignore')

        # -----------------------------
        # 6. HANDLE OUTLIERS
        # -----------------------------
        numeric_cols = df.select_dtypes(include=np.number).columns

        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            # Cap outliers
            df[col] = np.where(df[col] < lower, lower, df[col])
            df[col] = np.where(df[col] > upper, upper, df[col])

        # -----------------------------
        # 7. INVALID VALUES CHECK
        # -----------------------------
        if 'LOAN_AMOUNT' in df.columns:
            df = df[df['LOAN_AMOUNT'] > 0]

        if 'INTEREST_RATE' in df.columns:
            df = df[df['INTEREST_RATE'] >= 0]

        cleaned[name] = df

        print(f"✅ {name} cleaned. Shape: {df.shape}")

    return cleaned