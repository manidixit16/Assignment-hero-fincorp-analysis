"""
Chart Engine
Central module for generating all visualisation outputs across
the 20 analysis tasks. Charts are saved to reports/figures/.
"""
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

os.makedirs("reports/figures", exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# TASK 2 — Exploratory Summary
# ─────────────────────────────────────────────────────────────────────────────
def plot_descriptive(df, applications):
    print("\n[Chart] Task 2 — Exploratory Summary Plots")

    if 'LOAN_AMOUNT' in df.columns:
        df['LOAN_AMOUNT'].dropna().hist(bins=30, color='steelblue', edgecolor='white')
        plt.title("Loan Amount Distribution")
        plt.xlabel("Loan Amount")
        plt.tight_layout()
        plt.savefig("reports/figures/task_2_loan_distribution.png")
        plt.clf()

    if 'EMI_AMOUNT' in df.columns:
        df['EMI_AMOUNT'].dropna().hist(bins=30, color='steelblue', edgecolor='white')
        plt.title("EMI Distribution")
        plt.xlabel("EMI Amount")
        plt.tight_layout()
        plt.savefig("reports/figures/task_2_emi_distribution.png")
        plt.clf()

    if 'CREDIT_SCORE' in df.columns:
        df['CREDIT_SCORE'].dropna().hist(bins=30, color='teal', edgecolor='white')
        plt.title("Credit Score Distribution")
        plt.xlabel("Credit Score")
        plt.tight_layout()
        plt.savefig("reports/figures/task_2_credit_score.png")
        plt.clf()

    if 'REGION' in df.columns and 'LOAN_AMOUNT' in df.columns:
        df.groupby('REGION')['LOAN_AMOUNT'].sum().plot(kind='bar', color='steelblue')
        plt.title("Total Loan Amount by Region")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("reports/figures/task_2_region_loan.png")
        plt.clf()

    if 'REGION' in df.columns and 'DEFAULT_FLAG' in df.columns:
        df.groupby('REGION')['DEFAULT_FLAG'].mean().plot(kind='bar', color='coral')
        plt.title("Default Rate by Region")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("reports/figures/task_2_region_default.png")
        plt.clf()

    applications['APPLICATION_DATE'] = pd.to_datetime(
        applications['APPLICATION_DATE'], errors='coerce'
    )
    applications = applications[applications['APPLICATION_DATE'].notna()]
    app_trend = applications.groupby(
        applications['APPLICATION_DATE'].dt.to_period('M')
    ).size()
    if len(app_trend) > 1:
        app_trend = app_trend.iloc[:-1]
    app_trend.plot(color='steelblue')
    plt.title("Monthly Applications")
    plt.tight_layout()
    plt.savefig("reports/figures/task_2_monthly_applications.png")
    plt.clf()

    if 'APPROVAL_STATUS' in applications.columns:
        approved = applications[applications['APPROVAL_STATUS'].str.upper() == 'APPROVED']
        approval_trend = approved.groupby(
            approved['APPLICATION_DATE'].dt.to_period('M')
        ).size()
        if len(approval_trend) > 1:
            approval_trend = approval_trend.iloc[:-1]
        approval_trend.plot(color='green')
        plt.title("Monthly Approved Loans")
        plt.tight_layout()
        plt.savefig("reports/figures/task_2_monthly_approved.png")
        plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3 — Loan Default Scoring
# ─────────────────────────────────────────────────────────────────────────────
def plot_default_risk(df, branches):
    print("\n[Chart] Task 3 — Default Risk Correlation Plots")

    loan_cols = ['LOAN_AMOUNT', 'INTEREST_RATE', 'CREDIT_SCORE', 'DEFAULT_FLAG']
    avail = [c for c in loan_cols if c in df.columns]
    if avail:
        plt.figure()
        sns.heatmap(df[avail].corr(), annot=True, cmap="YlGnBu", annot_kws={"size": 10})
        plt.title("Loan Attribute Correlation")
        plt.xticks(rotation=30); plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig("reports/figures/task_3_correlation_main.png")
        plt.clf()

    pair_cols = [c for c in ['EMI_AMOUNT', 'OVERDUE_AMOUNT', 'DEFAULT_AMOUNT'] if c in df.columns]
    if len(pair_cols) >= 2:
        plt.figure()
        sns.heatmap(df[pair_cols].corr(), annot=True, cmap="YlGnBu", annot_kws={"size": 10})
        plt.title("EMI / Overdue / Default Correlation")
        plt.tight_layout()
        plt.savefig("reports/figures/task_3_correlation_pairwise.png")
        plt.clf()

    if 'REGION' in df.columns:
        region_def = df.groupby('REGION')['DEFAULT_FLAG'].mean().reset_index()
        branch_merged = branches.merge(region_def, on='REGION', how='left')
        branch_corr = {}
        for col in ['DELINQUENT_LOANS', 'LOAN_DISBURSEMENT_AMOUNT']:
            if col in branch_merged.columns:
                branch_corr[col] = branch_merged[col].corr(branch_merged['DEFAULT_FLAG'])
        if branch_corr:
            plt.bar(branch_corr.keys(), branch_corr.values(), color='steelblue')
            plt.title("Branch Metrics vs Default Rate")
            plt.tight_layout()
            plt.savefig("reports/figures/task_3_correlation_branch.png")
            plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 4 — Branch Performance
# ─────────────────────────────────────────────────────────────────────────────
def plot_branch_performance(branches):
    print("\n[Chart] Task 4 — Branch Performance Plots")

    if 'LOAN_DISBURSEMENT_AMOUNT' in branches.columns:
        branches.sort_values('LOAN_DISBURSEMENT_AMOUNT', ascending=False).head(10).plot(
            x='REGION', y='LOAN_DISBURSEMENT_AMOUNT', kind='bar', color='steelblue', legend=False
        )
        plt.title("Top Regions by Loan Disbursement")
        plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_4_branch_loan.png"); plt.clf()

    if 'DELINQUENT_LOANS' in branches.columns:
        branches.sort_values('DELINQUENT_LOANS', ascending=False).head(10).plot(
            x='REGION', y='DELINQUENT_LOANS', kind='bar', color='coral', legend=False
        )
        plt.title("High Delinquency Regions")
        plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_4_branch_delinquency.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 5 — Borrower Segmentation
# ─────────────────────────────────────────────────────────────────────────────
def plot_customer_segmentation(df):
    print("\n[Chart] Task 5 — Borrower Segmentation Plots")

    for col, fname, title in [
        ('INCOME_SEGMENT', 'task_5_income_segment.png',  'Borrower Distribution by Income'),
        ('CREDIT_SEGMENT', 'task_5_credit_segment.png',  'Borrower Distribution by Credit Score'),
        ('LOAN_STATUS',    'task_5_loan_status.png',     'Loan Status Distribution'),
    ]:
        if col in df.columns:
            df[col].value_counts().plot(kind='bar', color='steelblue')
            plt.title(title); plt.xticks(rotation=45); plt.tight_layout()
            plt.savefig(f"reports/figures/{fname}"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 6 — Advanced Metrics
# ─────────────────────────────────────────────────────────────────────────────
def plot_advanced_analysis(df, branches):
    print("\n[Chart] Task 6 — Advanced Statistical Plots")

    risk_cols = [c for c in ['CREDIT_SCORE', 'LOAN_AMOUNT', 'INTEREST_RATE', 'OVERDUE_AMOUNT', 'DEFAULT_FLAG']
                 if c in df.columns]
    if len(risk_cols) >= 2:
        plt.figure()
        sns.heatmap(df[risk_cols].corr(), annot=True, cmap="YlGnBu")
        plt.title("Default Risk Correlation"); plt.tight_layout()
        plt.savefig("reports/figures/task_6_adv_default_corr.png"); plt.clf()

    pair_cols = [c for c in ['EMI_AMOUNT', 'RECOVERY_RATE', 'DEFAULT_AMOUNT'] if c in df.columns]
    if len(pair_cols) >= 2:
        plt.figure()
        sns.heatmap(df[pair_cols].corr(), annot=True, cmap="YlGnBu")
        plt.title("Pairwise Correlation"); plt.tight_layout()
        plt.savefig("reports/figures/task_6_adv_pairwise_corr.png"); plt.clf()

    branch_num = [c for c in ['DELINQUENT_LOANS', 'LOAN_DISBURSEMENT_AMOUNT'] if c in branches.columns]
    if len(branch_num) >= 2:
        plt.figure()
        sns.heatmap(branches[branch_num].corr(), annot=True, cmap="YlGnBu")
        plt.title("Branch Internal Correlation"); plt.tight_layout()
        plt.savefig("reports/figures/task_6_adv_branch_corr.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 7 — Payment & Recovery
# ─────────────────────────────────────────────────────────────────────────────
def plot_transaction_recovery(df, transactions):
    print("\n[Chart] Task 7 — Payment & Recovery Plots")

    if 'PAYMENT_TYPE' in transactions.columns:
        transactions['PAYMENT_TYPE'].value_counts().plot(kind='bar', color='steelblue')
        plt.title("Transaction Type Distribution"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_7_txn_type.png"); plt.clf()

    if 'DEFAULT_REASON' in df.columns and 'RECOVERY_RATE' in df.columns:
        df.groupby('DEFAULT_REASON')['RECOVERY_RATE'].mean().plot(kind='bar', color='teal')
        plt.title("Recovery Rate by Default Reason"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_7_recovery_reason.png"); plt.clf()

    if 'REGION' in df.columns and 'RECOVERY_RATE' in df.columns:
        df.groupby('REGION')['RECOVERY_RATE'].mean().plot(kind='bar', color='steelblue')
        plt.title("Recovery Rate by Region"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_7_recovery_region.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 8 — EMI Risk
# ─────────────────────────────────────────────────────────────────────────────
def plot_emi_analysis(df):
    print("\n[Chart] Task 8 — EMI Risk Plots")

    if 'EMI_AMOUNT' in df.columns and 'DEFAULT_FLAG' in df.columns:
        bands = pd.qcut(df['EMI_AMOUNT'], 5, duplicates='drop')
        df.groupby(bands)['DEFAULT_FLAG'].mean().plot(kind='bar', color='coral')
        plt.title("Default Probability by EMI Band"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_8_emi_default.png"); plt.clf()

    if 'EMI_BIN' in df.columns and 'DEFAULT_FLAG' in df.columns:
        df.groupby('EMI_BIN')['DEFAULT_FLAG'].mean().plot(kind='bar', color='steelblue')
        plt.title("EMI Threshold Risk Profile"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_8_emi_threshold.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 9 — Application Insights
# ─────────────────────────────────────────────────────────────────────────────
def plot_application_analysis(applications):
    print("\n[Chart] Task 9 — Application Insight Plots")
    applications.columns = [c.upper() for c in applications.columns]

    if 'APPROVAL_STATUS' in applications.columns:
        applications['APPROVAL_STATUS'].value_counts().plot(kind='bar', color='steelblue')
        plt.title("Approval vs Rejection"); plt.tight_layout()
        plt.savefig("reports/figures/task_9_application_status.png"); plt.clf()

    reason_col = next((c for c in applications.columns if 'REASON' in c), None)
    if reason_col:
        rejected = applications[applications['APPROVAL_STATUS'].str.upper() == 'REJECTED']
        rejected[reason_col].value_counts().plot(kind='bar', color='coral')
        plt.title("Rejection Reasons"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_9_rejection_reason.png"); plt.clf()

    fee_col = next((c for c in applications.columns if 'FEE' in c), None)
    if fee_col and 'APPROVAL_STATUS' in applications.columns:
        applications.groupby('APPROVAL_STATUS')[fee_col].mean().plot(kind='bar', color='teal')
        plt.title("Avg Processing Fee by Status"); plt.tight_layout()
        plt.savefig("reports/figures/task_9_processing_fee.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 10 — Recovery Effectiveness
# ─────────────────────────────────────────────────────────────────────────────
def plot_recovery(df):
    print("\n[Chart] Task 10 — Recovery Effectiveness Plots")

    if 'RECOVERY_RATE' in df.columns:
        df['RECOVERY_RATE'].dropna().hist(bins=20, color='teal', edgecolor='white')
        plt.title("Recovery Rate Distribution"); plt.tight_layout()
        plt.savefig("reports/figures/task_10_recovery_rate.png"); plt.clf()

    if 'LEGAL_ACTION' in df.columns and 'RECOVERY_RATE' in df.columns:
        df.groupby('LEGAL_ACTION')['RECOVERY_RATE'].mean().plot(kind='bar', color='steelblue')
        plt.title("Recovery Rate by Legal Action"); plt.tight_layout()
        plt.savefig("reports/figures/task_10_recovery_legal.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 11 — Loan Disbursement Efficiency
# ─────────────────────────────────────────────────────────────────────────────
def plot_disbursement_efficiency(df):
    print("\n[Chart] Task 11 — Disbursement Efficiency Plots")

    if 'REGION' in df.columns and 'PROCESSING_DAYS' in df.columns:
        df.groupby('REGION')['PROCESSING_DAYS'].mean().plot(kind='bar', color='steelblue')
        plt.title("Avg Processing Days by Region"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_11_disbursement_region.png"); plt.clf()

    if 'LOAN_PURPOSE' in df.columns and 'PROCESSING_DAYS' in df.columns:
        df.groupby('LOAN_PURPOSE')['PROCESSING_DAYS'].mean().plot(kind='bar', color='teal')
        plt.title("Avg Processing Days by Loan Purpose"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_11_disbursement_purpose.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 12 — Revenue Analysis
# ─────────────────────────────────────────────────────────────────────────────
def plot_profitability(df):
    print("\n[Chart] Task 12 — Revenue Analysis Plots")

    if 'LOAN_PURPOSE' in df.columns and 'INTEREST_INCOME' in df.columns:
        df.groupby('LOAN_PURPOSE')['INTEREST_INCOME'].sum().plot(kind='bar', color='steelblue')
        plt.title("Revenue by Loan Purpose"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_12_profit_purpose.png"); plt.clf()

    if 'REGION' in df.columns and 'INTEREST_INCOME' in df.columns:
        df.groupby('REGION')['INTEREST_INCOME'].sum().plot(kind='bar', color='teal')
        plt.title("Revenue by Region"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_12_profit_region.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 13 — Regional Analysis
# ─────────────────────────────────────────────────────────────────────────────
def plot_geospatial(df):
    print("\n[Chart] Task 13 — Regional Distribution Plots")

    if 'LOAN_STATUS' in df.columns:
        status_upper = df['LOAN_STATUS'].astype(str).str.upper().str.strip()
        active = df[status_upper.isin(['ACTIVE', 'APPROVED', 'DISBURSED'])]
        if active.empty:
            active = df[df['DEFAULT_FLAG'] == 0]
    else:
        active = df[df['DEFAULT_FLAG'] == 0] if 'DEFAULT_FLAG' in df.columns else df

    if 'REGION' in active.columns:
        active['REGION'].value_counts().plot(kind='bar', color='steelblue')
        plt.title("Active Loans by Region"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_13_geo_distribution.png"); plt.clf()

    if 'REGION' in df.columns and 'DEFAULT_FLAG' in df.columns:
        df.groupby('REGION')['DEFAULT_FLAG'].mean().plot(kind='bar', color='coral')
        plt.title("Default Rate by Region"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_13_geo_default.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 14 — Default Trend Tracker
# ─────────────────────────────────────────────────────────────────────────────
def plot_default_trends(df):
    print("\n[Chart] Task 14 — Default Trend Plots")

    date_col = 'DEFAULT_DATE' if 'DEFAULT_DATE' in df.columns else (
        'DISBURSAL_DATE' if 'DISBURSAL_DATE' in df.columns else None
    )
    if date_col and 'DEFAULT_FLAG' in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df.groupby(df[date_col].dt.to_period('M'))['DEFAULT_FLAG'].sum().plot(kind='line', color='coral')
        plt.title("Default Count Over Time"); plt.tight_layout()
        plt.savefig("reports/figures/task_14_default_trend.png"); plt.clf()

    if 'LOAN_PURPOSE' in df.columns and 'DEFAULT_AMOUNT' in df.columns:
        df.groupby('LOAN_PURPOSE')['DEFAULT_AMOUNT'].mean().plot(kind='bar', color='steelblue')
        plt.title("Avg Default Amount by Loan Purpose"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_14_default_purpose.png"); plt.clf()

    if 'ANNUAL_INCOME' in df.columns and 'DEFAULT_FLAG' in df.columns:
        df['INCOME_TIER'] = pd.qcut(df['ANNUAL_INCOME'], 3, labels=['Low', 'Medium', 'High'])
        df.groupby('INCOME_TIER')['DEFAULT_FLAG'].mean().plot(kind='bar', color='teal')
        plt.title("Default Rate by Income Tier"); plt.tight_layout()
        plt.savefig("reports/figures/task_14_default_income.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 16 — Temporal Analysis
# ─────────────────────────────────────────────────────────────────────────────
def plot_time_series(df):
    print("\n[Chart] Task 16 — Temporal Analysis Plots")

    if 'DISBURSAL_DATE' in df.columns:
        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')
        df.groupby(df['DISBURSAL_DATE'].dt.to_period('M')).size().plot(kind='line', color='steelblue')
        plt.title("Monthly Loan Disbursement"); plt.tight_layout()
        plt.savefig("reports/figures/task_16_time_disbursement.png"); plt.clf()

        df.groupby(df['DISBURSAL_DATE'].dt.month).size().plot(kind='bar', color='teal')
        plt.title("Seasonal Disbursement Pattern"); plt.tight_layout()
        plt.savefig("reports/figures/task_16_time_seasonal_disb.png"); plt.clf()

    if 'APPLICATION_DATE' in df.columns:
        df['APPLICATION_DATE'] = pd.to_datetime(df['APPLICATION_DATE'], errors='coerce')
        df.groupby(df['APPLICATION_DATE'].dt.month).size().plot(kind='bar', color='steelblue')
        plt.title("Seasonal Application Pattern"); plt.tight_layout()
        plt.savefig("reports/figures/task_16_time_seasonal_app.png"); plt.clf()

    if all(c in df.columns for c in ['DISBURSAL_DATE', 'REGION', 'DEFAULT_FLAG']):
        valid = df[df['DISBURSAL_DATE'].notna()].copy()
        valid['MONTH'] = valid['DISBURSAL_DATE'].dt.to_period('M')
        region_ts = valid.groupby(['MONTH', 'REGION'])['DEFAULT_FLAG'].mean().unstack()
        if not region_ts.empty:
            region_ts.plot()
            plt.title("Monthly Default Rate by Region"); plt.tight_layout()
            plt.savefig("reports/figures/task_16_time_default_region.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 17 — Repayment Behaviour
# ─────────────────────────────────────────────────────────────────────────────
def plot_customer_behavior(df, applications, customers):
    print("\n[Chart] Task 17 — Repayment Behaviour Plots")

    if 'CUSTOMER_ID' in df.columns and 'DEFAULT_FLAG' in df.columns:
        def categorise(x):
            if x == 0:      return 'On Time'
            elif x < 0.5:   return 'Occasional'
            else:            return 'Frequent'

        df.groupby('CUSTOMER_ID')['DEFAULT_FLAG'].mean().apply(categorise).value_counts().plot(
            kind='bar', color='steelblue'
        )
        plt.title("Customer Repayment Behaviour"); plt.tight_layout()
        plt.savefig("reports/figures/task_17_customer_behavior.png"); plt.clf()

    merged = applications.merge(customers, on='CUSTOMER_ID', how='left')

    if 'AGE' in merged.columns and 'APPROVAL_STATUS' in merged.columns:
        merged['AGE_GROUP'] = pd.cut(merged['AGE'], bins=[18, 30, 50, 70], labels=['Young', 'Middle', 'Senior'])
        merged.groupby(['AGE_GROUP', 'APPROVAL_STATUS']).size().unstack().plot(kind='bar')
        plt.title("Approval Rate by Age Group"); plt.tight_layout()
        plt.savefig("reports/figures/task_17_customer_age.png"); plt.clf()

    if 'GENDER' in merged.columns and 'APPROVAL_STATUS' in merged.columns:
        merged.groupby(['GENDER', 'APPROVAL_STATUS']).size().unstack().plot(kind='bar')
        plt.title("Approval Rate by Gender"); plt.tight_layout()
        plt.savefig("reports/figures/task_17_customer_gender.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 18 — Credit Risk Profiler
# ─────────────────────────────────────────────────────────────────────────────
def plot_risk(df):
    print("\n[Chart] Task 18 — Credit Risk Plots")

    if 'LOAN_PURPOSE' in df.columns and 'DEFAULT_FLAG' in df.columns:
        df.groupby('LOAN_PURPOSE')['DEFAULT_FLAG'].sum().plot(kind='bar', color='coral')
        plt.title("Default Count by Loan Purpose"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_18_risk_purpose.png"); plt.clf()

    if 'CREDIT_SCORE' in df.columns and 'DEFAULT_FLAG' in df.columns:
        score_bins   = [0, 580, 720, float('inf')]
        score_labels = ['Low', 'Medium', 'High']
        df['SCORE_TIER'] = pd.cut(df['CREDIT_SCORE'], bins=score_bins, labels=score_labels)
        df.groupby('SCORE_TIER')['DEFAULT_FLAG'].mean().plot(kind='bar', color='steelblue')
        plt.title("Default Rate by Credit Score Tier"); plt.tight_layout()
        plt.savefig("reports/figures/task_18_risk_credit.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 19 — Default Velocity
# ─────────────────────────────────────────────────────────────────────────────
def plot_time_to_default(df):
    print("\n[Chart] Task 19 — Default Velocity Plots")

    if 'TIME_TO_DEFAULT' not in df.columns:
        print("  TIME_TO_DEFAULT column absent — skipping")
        return

    if 'LOAN_PURPOSE' in df.columns:
        df.groupby('LOAN_PURPOSE')['TIME_TO_DEFAULT'].mean().plot(kind='bar', color='teal')
        plt.title("Avg Days to Default by Loan Purpose"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_19_time_to_default_purpose.png"); plt.clf()

    if 'CREDIT_SEGMENT' in df.columns:
        df.groupby('CREDIT_SEGMENT')['TIME_TO_DEFAULT'].mean().plot(kind='bar', color='steelblue')
        plt.title("Avg Days to Default by Credit Tier"); plt.tight_layout()
        plt.savefig("reports/figures/task_19_time_to_default_credit.png"); plt.clf()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 20 — Transaction Behaviour
# ─────────────────────────────────────────────────────────────────────────────
def plot_transaction_pattern(transactions, df):
    print("\n[Chart] Task 20 — Transaction Behaviour Plots")
    transactions.columns = [c.upper() for c in transactions.columns]

    if 'PAYMENT_TYPE' in transactions.columns:
        transactions['PAYMENT_TYPE'].value_counts().plot(kind='bar', color='steelblue')
        plt.title("Payment Type Distribution"); plt.xticks(rotation=45); plt.tight_layout()
        plt.savefig("reports/figures/task_20_txn_type_dist.png"); plt.clf()
