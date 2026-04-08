import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_all(df):
    df['LOAN_AMOUNT'].hist()
    plt.savefig("reports/figures/loan_dist.png")
    plt.clf()

    df.groupby('REGION')['DEFAULT_FLAG'].mean().plot(kind='bar')
    plt.savefig("reports/figures/default_region.png")
    plt.clf()

    sns.heatmap(df.corr(numeric_only=True))
    plt.savefig("reports/figures/corr.png")
    plt.clf()

def plot_descriptive(df, applications=None):

    # -----------------------------
    # 1. DISTRIBUTIONS
    # -----------------------------
    df['LOAN_AMOUNT'].hist()
    plt.title("Loan Amount Distribution")
    plt.savefig("reports/figures/loan_distribution.png")
    plt.clf()

    if 'EMI_AMOUNT' in df.columns:
        df['EMI_AMOUNT'].hist()
        plt.title("EMI Distribution")
        plt.savefig("reports/figures/emi_distribution.png")
        plt.clf()

    df['CREDIT_SCORE'].hist()
    plt.title("Credit Score Distribution")
    plt.savefig("reports/figures/credit_score_distribution.png")
    plt.clf()

    # -----------------------------
    # 2. REGIONAL TRENDS
    # -----------------------------
    if 'REGION' in df.columns:
        df.groupby('REGION')['LOAN_AMOUNT'].sum().plot(kind='bar')
        plt.title("Loan Disbursement by Region")
        plt.savefig("reports/figures/region_disbursement.png")
        plt.clf()

        df.groupby('REGION')['DEFAULT_FLAG'].mean().plot(kind='bar')
        plt.title("Default Rate by Region")
        plt.savefig("reports/figures/region_default.png")
        plt.clf()

    # -----------------------------
    # 3. MONTHLY TRENDS
    # -----------------------------
    if applications is not None:
        applications['APPLICATION_DATE'] = pd.to_datetime(applications['APPLICATION_DATE'])

        applications.groupby(
            applications['APPLICATION_DATE'].dt.to_period('M')
        ).size().plot()

        plt.title("Monthly Loan Applications")
        plt.savefig("reports/figures/monthly_applications.png")
        plt.clf()

import seaborn as sns
import matplotlib.pyplot as plt

def plot_default_risk(df):

    # -----------------------------------
    # 1. LOAN ATTRIBUTE CORRELATION
    # -----------------------------------
    cols = ['LOAN_AMOUNT', 'INTEREST_RATE', 'CREDIT_SCORE', 'DEFAULT_FLAG']
    cols = [c for c in cols if c in df.columns]

    if len(cols) >= 2:
        sns.heatmap(df[cols].corr(), annot=True)
        plt.title("Loan Attribute Correlation")
        plt.savefig("reports/figures/loan_correlation.png")
        plt.clf()

    # -----------------------------------
    # 2. PAIRWISE HEATMAP
    # -----------------------------------
    pair_cols = ['EMI_AMOUNT', 'OVERDUE_AMOUNT', 'DEFAULT_AMOUNT']
    pair_cols = [c for c in pair_cols if c in df.columns]

    if len(pair_cols) >= 2:
        sns.heatmap(df[pair_cols].corr(), annot=True)
        plt.title("Pairwise Correlation Heatmap")
        plt.savefig("reports/figures/pairwise_heatmap.png")
        plt.clf()

# task 4

def plot_branch_performance(df):

    # -----------------------------
    # 1. DISBURSEMENT BY REGION
    # -----------------------------
    if 'REGION' in df.columns:
        df.groupby('REGION')['LOAN_AMOUNT'].sum().plot(kind='bar')
        plt.title("Loan Disbursement by Region")
        plt.savefig("reports/figures/branch_region_disbursement.png")
        plt.clf()

    # -----------------------------
    # 2. DEFAULT RATE BY REGION
    # -----------------------------
    if 'REGION' in df.columns:
        df.groupby('REGION')['DEFAULT_FLAG'].mean().plot(kind='bar')
        plt.title("Default Rate by Region")
        plt.savefig("reports/figures/branch_region_default.png")
        plt.clf()

# task 5
import matplotlib.pyplot as plt

def plot_customer_segments(df):

    # -----------------------------------
    # CREDIT SEGMENT DISTRIBUTION
    # -----------------------------------
    df['CREDIT_SEGMENT'].value_counts().plot(kind='bar')
    plt.title("Customer Distribution by Credit Segment")
    plt.savefig("reports/figures/customer_credit_segment.png")
    plt.clf()

    # -----------------------------------
    # DEFAULT RATE BY SEGMENT
    # -----------------------------------
    df.groupby('CREDIT_SEGMENT')['DEFAULT_FLAG'].mean().plot(kind='bar')
    plt.title("Default Rate by Credit Segment")
    plt.savefig("reports/figures/customer_default_segment.png")
    plt.clf()

# task 6

def plot_statistical_analysis(df, defaults=None):

    # -----------------------------------
    # DEFAULT RISK HEATMAP
    # -----------------------------------
    cols = ['CREDIT_SCORE', 'LOAN_AMOUNT', 'INTEREST_RATE', 'DEFAULT_FLAG']
    cols = [c for c in cols if c in df.columns]

    if len(cols) >= 2:
        sns.heatmap(df[cols].corr(), annot=True)
        plt.title("Default Risk Correlation")
        plt.savefig("reports/figures/default_risk_heatmap.png")
        plt.clf()

    # -----------------------------------
    # ADVANCED PAIRWISE HEATMAP
    # -----------------------------------
    if defaults is not None:
        defaults['RECOVERY_RATE'] = defaults['RECOVERY_AMOUNT'] / defaults['DEFAULT_AMOUNT']
        merged = df.merge(defaults, on='LOAN_ID', how='left')

        pair_cols = ['EMI_AMOUNT', 'RECOVERY_RATE', 'DEFAULT_AMOUNT']
        pair_cols = [c for c in pair_cols if c in merged.columns]

        if len(pair_cols) >= 2:
            sns.heatmap(merged[pair_cols].corr(), annot=True)
            plt.title("Advanced Pairwise Correlation")
            plt.savefig("reports/figures/advanced_heatmap.png")
            plt.clf()

# Task 7

def plot_transaction_recovery(df, transactions, defaults):

    # -----------------------------
    # PENALTY DISTRIBUTION
    # -----------------------------
    if 'TRANSACTION_TYPE' in transactions.columns:
        transactions['TRANSACTION_TYPE'].value_counts().plot(kind='bar')
        plt.title("Transaction Type Distribution")
        plt.savefig("reports/figures/transaction_types.png")
        plt.clf()

    # -----------------------------
    # RECOVERY RATE DISTRIBUTION
    # -----------------------------
    if 'RECOVERY_AMOUNT' in defaults.columns:
        defaults['RECOVERY_RATE'] = defaults['RECOVERY_AMOUNT'] / defaults['DEFAULT_AMOUNT']

        defaults['RECOVERY_RATE'].hist()
        plt.title("Recovery Rate Distribution")
        plt.savefig("reports/figures/recovery_distribution.png")
        plt.clf()

# Task 8

def plot_emi_analysis(df):

    # -----------------------------
    # EMI vs DEFAULT
    # -----------------------------
    if 'EMI_AMOUNT' in df.columns:
        df.groupby('EMI_AMOUNT')['DEFAULT_FLAG'].mean().plot()
        plt.title("EMI vs Default Probability")
        plt.savefig("reports/figures/emi_default.png")
        plt.clf()

    # -----------------------------
    # EMI BUCKET ANALYSIS
    # -----------------------------
    if 'EMI_AMOUNT' in df.columns:
        df['EMI_BUCKET'] = pd.qcut(df['EMI_AMOUNT'], q=5, duplicates='drop')
        df.groupby('EMI_BUCKET')['DEFAULT_FLAG'].mean().plot(kind='bar')
        plt.title("Default Rate by EMI Bucket")
        plt.savefig("reports/figures/emi_bucket.png")
        plt.clf()

    # -----------------------------
    # EMI BY LOAN TYPE
    # -----------------------------
    if 'LOAN_TYPE' in df.columns:
        df.groupby('LOAN_TYPE')['EMI_AMOUNT'].mean().plot(kind='bar')
        plt.title("EMI by Loan Type")
        plt.savefig("reports/figures/emi_loan_type.png")
        plt.clf()

# Task 9

def plot_application_insights(applications):

    # -----------------------------
    # APPROVAL RATE
    # -----------------------------
    if 'APPROVAL_STATUS' in applications.columns:
        applications['APPROVAL_STATUS'].value_counts().plot(kind='bar')
        plt.title("Approval vs Rejection")
        plt.savefig("reports/figures/application_status.png")
        plt.clf()

    # -----------------------------
    # REJECTION REASONS
    # -----------------------------
    if 'REJECTION_REASON' in applications.columns:
        applications['REJECTION_REASON'].value_counts().head(5).plot(kind='bar')
        plt.title("Top Rejection Reasons")
        plt.savefig("reports/figures/rejection_reasons.png")
        plt.clf()


# Task 10

def plot_recovery_analysis(defaults, df, branches):

    # -----------------------------
    # RECOVERY RATE DISTRIBUTION
    # -----------------------------
    defaults['RECOVERY_RATE'] = defaults['RECOVERY_AMOUNT'] / defaults['DEFAULT_AMOUNT']

    defaults['RECOVERY_RATE'].hist()
    plt.title("Recovery Rate Distribution")
    plt.savefig("reports/figures/recovery_distribution.png")
    plt.clf()

    # -----------------------------
    # LEGAL ACTION COMPARISON
    # -----------------------------
    if 'LEGAL_ACTION' in defaults.columns:
        defaults.groupby('LEGAL_ACTION')['RECOVERY_RATE'].mean().plot(kind='bar')
        plt.title("Recovery Rate by Legal Action")
        plt.savefig("reports/figures/recovery_legal.png")
        plt.clf()

# Task 11
import pandas as pd
import matplotlib.pyplot as plt

def plot_disbursement_efficiency(applications, loans, branches):

    # Convert to datetime safely
    applications['APPLICATION_DATE'] = pd.to_datetime(
        applications['APPLICATION_DATE'], errors='coerce'
    )
    loans['DISBURSEMENT_DATE'] = pd.to_datetime(
        loans['DISBURSEMENT_DATE'], errors='coerce'
    )

    # Merge safely
    if 'APPLICATION_ID' in applications.columns and 'APPLICATION_ID' in loans.columns:
        merged = applications.merge(loans, on='APPLICATION_ID', how='left')
    else:
        print("⚠️ APPLICATION_ID missing → cannot merge")
        return

    # Processing time
    merged['PROCESSING_DAYS'] = (
        merged['DISBURSEMENT_DATE'] - merged['APPLICATION_DATE']
    ).dt.days

    # -----------------------------
    # PLOT 1: DISTRIBUTION
    # -----------------------------
    merged['PROCESSING_DAYS'].dropna().hist()
    plt.title("Processing Time Distribution")
    plt.savefig("reports/figures/processing_time.png")
    plt.clf()

    # -----------------------------
    # PLOT 2: BRANCH COMPARISON
    # -----------------------------
    if 'BRANCH_ID' in merged.columns:
        merged.groupby('BRANCH_ID')['PROCESSING_DAYS'].mean().plot(kind='bar')
        plt.title("Processing Time by Branch")
        plt.savefig("reports/figures/processing_branch.png")
        plt.clf()

# Task 12

def plot_profitability(df, branches):

    # -----------------------------
    # PROFIT BY LOAN PURPOSE
    # -----------------------------
    if 'LOAN_PURPOSE' in df.columns:
        df.groupby('LOAN_PURPOSE')['INTEREST_INCOME'].sum().plot(kind='bar')
        plt.title("Profit by Loan Purpose")
        plt.savefig("reports/figures/profit_purpose.png")
        plt.clf()

    # -----------------------------
    # REGION PROFITABILITY
    # -----------------------------
    merged = df.merge(branches, on='BRANCH_ID', how='left')

    if 'REGION' in merged.columns:
        merged.groupby('REGION')['INTEREST_INCOME'].sum().plot(kind='bar')
        plt.title("Profit by Region")
        plt.savefig("reports/figures/profit_region.png")
        plt.clf()

# Task 13
import matplotlib.pyplot as plt

def plot_geospatial(df, branches):

    merged = df.merge(branches, on='BRANCH_ID', how='left')

    # -----------------------------
    # REGION DISTRIBUTION
    # -----------------------------
    if 'REGION' in merged.columns:
        merged['REGION'].value_counts().plot(kind='bar')
        plt.title("Loan Distribution by Region")
        plt.savefig("reports/figures/geo_distribution.png")
        plt.clf()

    # -----------------------------
    # DEFAULT RATE BY REGION
    # -----------------------------
    if 'REGION' in merged.columns:
        merged.groupby('REGION')['DEFAULT_FLAG'].mean().plot(kind='bar')
        plt.title("Default Rate by Region")
        plt.savefig("reports/figures/geo_default.png")
        plt.clf()

    # -----------------------------
    # RURAL vs URBAN
    # -----------------------------
    if 'AREA_TYPE' in merged.columns:
        merged.groupby('AREA_TYPE')['LOAN_AMOUNT'].sum().plot(kind='bar')
        plt.title("Loan Disbursement: Rural vs Urban")
        plt.savefig("reports/figures/geo_rural_urban.png")
        plt.clf()

# Task 14

def plot_default_trends(df, defaults):

    # -----------------------------------
    # DEFAULT TREND OVER TIME
    # -----------------------------------
    if 'DEFAULT_DATE' in defaults.columns:
        defaults['DEFAULT_DATE'] = pd.to_datetime(defaults['DEFAULT_DATE'])

        defaults.groupby(
            defaults['DEFAULT_DATE'].dt.to_period('M')
        ).size().plot()

        plt.title("Default Trends Over Time")
        plt.savefig("reports/figures/default_trend.png")
        plt.clf()

    # -----------------------------------
    # DEFAULT BY INCOME GROUP
    # -----------------------------------
    if 'ANNUAL_INCOME' in df.columns:
        df['INCOME_GROUP'] = pd.qcut(df['ANNUAL_INCOME'], q=3, labels=['Low','Medium','High'])

        df.groupby('INCOME_GROUP')['DEFAULT_FLAG'].mean().plot(kind='bar')
        plt.title("Default Rate by Income Group")
        plt.savefig("reports/figures/default_income.png")
        plt.clf()

#Task 15
def plot_branch_efficiency(applications, loans):

    applications['APPLICATION_DATE'] = pd.to_datetime(applications['APPLICATION_DATE'])
    loans['DISBURSEMENT_DATE'] = pd.to_datetime(loans['DISBURSEMENT_DATE'])

    merged = applications.merge(loans, on='APPLICATION_ID', how='left')

    merged['PROCESSING_DAYS'] = (
        merged['DISBURSEMENT_DATE'] - merged['APPLICATION_DATE']
    ).dt.days

    # -----------------------------
    # PROCESSING TIME
    # -----------------------------
    if 'BRANCH_ID' in merged.columns:
        merged.groupby('BRANCH_ID')['PROCESSING_DAYS'].mean().plot(kind='bar')
        plt.title("Branch Processing Time")
        plt.savefig("reports/figures/branch_efficiency_time.png")
        plt.clf()

    # -----------------------------
    # REJECTED APPLICATIONS
    # -----------------------------
    if 'APPROVAL_STATUS' in applications.columns:
        applications[applications['APPROVAL_STATUS'] == 'REJECTED'] \
            .groupby('BRANCH_ID').size().plot(kind='bar')

        plt.title("Rejected Applications by Branch")
        plt.savefig("reports/figures/branch_rejections.png")
        plt.clf()

# Task 16

def plot_time_series(loans, applications, defaults, df, branches):

    # -----------------------------
    # DISBURSEMENT TREND
    # -----------------------------
    loans['DISBURSEMENT_DATE'] = pd.to_datetime(loans['DISBURSEMENT_DATE'])

    loans.groupby(
        loans['DISBURSEMENT_DATE'].dt.to_period('M')
    ).size().plot()

    plt.title("Monthly Loan Disbursement")
    plt.savefig("reports/figures/time_disbursement.png")
    plt.clf()

    # -----------------------------
    # SEASONAL PATTERN
    # -----------------------------
    applications['APPLICATION_DATE'] = pd.to_datetime(applications['APPLICATION_DATE'])

    applications.groupby(
        applications['APPLICATION_DATE'].dt.month
    ).size().plot(kind='bar')

    plt.title("Seasonal Loan Applications")
    plt.savefig("reports/figures/time_seasonal.png")
    plt.clf()

    # -----------------------------
    # DEFAULT RATE BY REGION
    # -----------------------------
    defaults['DEFAULT_DATE'] = pd.to_datetime(defaults['DEFAULT_DATE'])

    merged = df.merge(branches, on='BRANCH_ID', how='left') \
               .merge(defaults, on='LOAN_ID', how='left')

    merged['MONTH'] = merged['DEFAULT_DATE'].dt.to_period('M')

    merged.groupby('MONTH')['DEFAULT_FLAG'].mean().plot()

    plt.title("Monthly Default Rate")
    plt.savefig("reports/figures/time_default.png")
    plt.clf()

# Task 17

def plot_customer_behavior(df):

    # -----------------------------
    # DEFAULT RATE BY INCOME
    # -----------------------------
    if 'ANNUAL_INCOME' in df.columns:
        df['INCOME_GROUP'] = pd.qcut(df['ANNUAL_INCOME'], q=3, labels=['Low','Medium','High'])

        df.groupby('INCOME_GROUP')['DEFAULT_FLAG'].mean().plot(kind='bar')
        plt.title("Default Rate by Income Group")
        plt.savefig("reports/figures/behavior_income.png")
        plt.clf()

    # -----------------------------
    # DEFAULT RATE BY REGION
    # -----------------------------
    if 'REGION' in df.columns:
        df.groupby('REGION')['DEFAULT_FLAG'].mean().plot(kind='bar')
        plt.title("Default Rate by Region")
        plt.savefig("reports/figures/behavior_region.png")
        plt.clf()

# Task 18

def plot_risk_analysis(df, defaults):

    merged = df.merge(defaults, on='LOAN_ID', how='left')

    # -----------------------------
    # RISK MATRIX HEATMAP
    # -----------------------------
    cols = ['DEFAULT_AMOUNT', 'LOAN_TERM', 'INTEREST_RATE']
    cols = [c for c in cols if c in merged.columns]

    if len(cols) >= 2:
        sns.heatmap(merged[cols].corr(), annot=True)
        plt.title("Risk Matrix Heatmap")
        plt.savefig("reports/figures/risk_matrix.png")
        plt.clf()

    # -----------------------------
    # LOAN TYPE RISK
    # -----------------------------
    if 'LOAN_TYPE' in merged.columns:
        merged.groupby('LOAN_TYPE')['DEFAULT_AMOUNT'].mean().plot(kind='bar')
        plt.title("Loan Type Risk Ranking")
        plt.savefig("reports/figures/risk_loan_type.png")
        plt.clf()

# Task 19

def plot_time_to_default(loans, defaults):

    loans['DISBURSEMENT_DATE'] = pd.to_datetime(loans['DISBURSEMENT_DATE'])
    defaults['DEFAULT_DATE'] = pd.to_datetime(defaults['DEFAULT_DATE'])

    merged = loans.merge(defaults, on='LOAN_ID', how='inner')

    merged['TIME_TO_DEFAULT'] = (
        merged['DEFAULT_DATE'] - merged['DISBURSEMENT_DATE']
    ).dt.days

    # -----------------------------
    # DISTRIBUTION
    # -----------------------------
    merged['TIME_TO_DEFAULT'].dropna().hist()
    plt.title("Time to Default Distribution")
    plt.savefig("reports/figures/time_to_default_dist.png")
    plt.clf()

# Task 20

def plot_transaction_patterns(transactions, df):

    # -----------------------------
    # TRANSACTION TYPE DISTRIBUTION
    # -----------------------------
    if 'TRANSACTION_TYPE' in transactions.columns:
        transactions['TRANSACTION_TYPE'].value_counts().plot(kind='bar')
        plt.title("Transaction Types")
        plt.savefig("reports/figures/txn_types.png")
        plt.clf()

    # -----------------------------
    # OVERDUE VS NON-OVERDUE
    # -----------------------------
    if 'OVERDUE_AMOUNT' in df.columns:
        overdue = df[df['OVERDUE_AMOUNT'] > 0]['LOAN_AMOUNT']
        non_overdue = df[df['OVERDUE_AMOUNT'] == 0]['LOAN_AMOUNT']

        plt.hist([overdue, non_overdue], label=['Overdue', 'Non-Overdue'])
        plt.legend()
        plt.title("Overdue vs Non-Overdue Loan Amount")
        plt.savefig("reports/figures/overdue_vs_non.png")
        plt.clf()