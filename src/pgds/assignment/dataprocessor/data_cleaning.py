"""
TASK 1: Data Quality and Preparation
- Validate and clean all six datasets
- Check for missing values, duplicates, and inconsistent data
- Standardize date formats and remove irrelevant columns
- Handle outliers in numeric columns (IQR capping)
"""

import pandas as pd
import numpy as np


def clean_data(data):
    """
    Clean all Hero FinCorp datasets.

    Steps per dataset:
      1. Standardize column names (strip + uppercase)
      2. Remove duplicate rows
      3. Handle missing values (median for numeric, mode for categorical)
      4. Drop rows with null primary keys (CUSTOMER_ID / LOAN_ID)
      5. Parse all *DATE columns to datetime
      6. Cap outliers via IQR (Q1 - 1.5*IQR, Q3 + 1.5*IQR)
      7. Enforce domain rules (LOAN_AMOUNT > 0, INTEREST_RATE >= 0)

    Returns
    -------
    dict : cleaned DataFrames keyed by dataset name
    """
    cleaned = {}

    for name, df in data.items():

        print(f"\n{'='*55}")
        print(f" TASK 1 — Cleaning: {name.upper()}")
        print(f"{'='*55}")
        print(f"  Original shape : {df.shape}")

        # ── 1. Standardize column names ───────────────────────────────────────
        df.columns = df.columns.str.strip().str.upper()

        # ── 2. Remove duplicates ──────────────────────────────────────────────
        n_dup = df.duplicated().sum()
        print(f"  Duplicates     : {n_dup}")
        df = df.drop_duplicates()

        # ── 3. Missing values ─────────────────────────────────────────────────
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            print(f"  Missing values :\n{missing.to_string()}")
        else:
            print("  Missing values : None")

        # Drop rows missing primary key
        for key in ['CUSTOMER_ID', 'LOAN_ID']:
            if key in df.columns:
                before = len(df)
                df = df.dropna(subset=[key])
                dropped = before - len(df)
                if dropped:
                    print(f"  Dropped {dropped} rows with null {key}")

        # Fill numeric nulls with median
        for col in df.select_dtypes(include=np.number).columns:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].median())

        # Fill categorical nulls with mode
        for col in df.select_dtypes(include='object').columns:
            if df[col].isnull().any():
                mode_val = df[col].mode()
                df[col] = df[col].fillna(mode_val[0] if not mode_val.empty else "UNKNOWN")

        # ── 4. Parse date columns ─────────────────────────────────────────────
        for col in df.columns:
            if 'DATE' in col:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # ── 5. Outlier capping via IQR ────────────────────────────────────────
        priority_cols = ['LOAN_AMOUNT', 'INTEREST_RATE', 'DEFAULT_AMOUNT',
                         'EMI_AMOUNT', 'ANNUAL_INCOME', 'CREDIT_SCORE']
        numeric_cols = [c for c in df.select_dtypes(include=np.number).columns
                        if c in priority_cols]

        for col in numeric_cols:
            Q1    = df[col].quantile(0.25)
            Q3    = df[col].quantile(0.75)
            IQR   = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            n_out = ((df[col] < lower) | (df[col] > upper)).sum()
            if n_out:
                df[col] = df[col].clip(lower=lower, upper=upper)
                print(f"  Outliers capped in {col}: {n_out} values")

        # ── 6. Domain rules ───────────────────────────────────────────────────
        if 'LOAN_AMOUNT' in df.columns:
            before = len(df)
            df = df[df['LOAN_AMOUNT'] > 0]
            if len(df) < before:
                print(f"  Removed {before - len(df)} rows with LOAN_AMOUNT <= 0")

        if 'INTEREST_RATE' in df.columns:
            before = len(df)
            df = df[df['INTEREST_RATE'] >= 0]
            if len(df) < before:
                print(f"  Removed {before - len(df)} rows with negative INTEREST_RATE")

        cleaned[name] = df
        print(f"  Cleaned shape  : {df.shape}")
        print(f"  ✅ {name} cleaned successfully")

    return cleaned
