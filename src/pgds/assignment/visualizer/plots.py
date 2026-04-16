import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def plot_descriptive(df, applications):

    print("\n GENERATING DESCRIPTIVE PLOTS")

    # -----------------------------------
    # 1. LOAN DISTRIBUTION
    # -----------------------------------
    if 'LOAN_AMOUNT' in df.columns:
        df['LOAN_AMOUNT'].dropna().hist(bins=30)
        plt.title("Loan Amount Distribution")
        plt.savefig("reports/figures/task_2_loan_distribution.png")
        plt.clf()

    # -----------------------------------
    # 2. EMI DISTRIBUTION
    # -----------------------------------
    if 'EMI_AMOUNT' in df.columns:
        df['EMI_AMOUNT'].dropna().hist(bins=30)
        plt.title("EMI Distribution")
        plt.savefig("reports/figures/task_2_emi_distribution.png")
        plt.clf()

    # -----------------------------------
    # 3. CREDIT SCORE
    # -----------------------------------
    if 'CREDIT_SCORE' in df.columns:
        df['CREDIT_SCORE'].dropna().hist(bins=30)
        plt.title("Credit Score Distribution")
        plt.savefig("reports/figures/task_2_credit_score.png")
        plt.clf()

    # -----------------------------------
    # 4. REGION LOAN DISTRIBUTION
    # -----------------------------------
    if 'REGION' in df.columns:
        df.groupby('REGION')['LOAN_AMOUNT'].sum().plot(kind='bar')
        plt.title("Loan Distribution by Region")
        plt.savefig("reports/figures/task_2_region_loan.png")
        plt.clf()

    # -----------------------------------
    # 5. REGION DEFAULT RATE (FIXED)
    # -----------------------------------
    if 'REGION' in df.columns:
        df.groupby('REGION')['DEFAULT_FLAG'].mean().plot(kind='bar')
        plt.title("Default Rate by Region")
        plt.savefig("reports/figures/task_2_region_default.png")
        plt.clf()

    # -----------------------------------
    # 6. MONTHLY APPLICATIONS
    # -----------------------------------
    applications['APPLICATION_DATE'] = pd.to_datetime(
        applications['APPLICATION_DATE'], errors='coerce'
    )

    applications = applications[applications['APPLICATION_DATE'].notna()]

    monthly = applications.groupby(
        applications['APPLICATION_DATE'].dt.to_period('M')
    ).size()

    if len(monthly) > 1:
        monthly = monthly.iloc[:-1]

    monthly.plot()
    plt.title("Monthly Applications")
    plt.savefig("reports/figures/task_2_monthly_applications.png")
    plt.clf()

    # -----------------------------------
    # 7. MONTHLY APPROVED (NEW FIX)
    # -----------------------------------
    approved = applications[
        applications['APPROVAL_STATUS'].str.upper() == 'APPROVED'
    ]

    monthly_approved = approved.groupby(
        approved['APPLICATION_DATE'].dt.to_period('M')
    ).size()

    if len(monthly_approved) > 1:
        monthly_approved = monthly_approved.iloc[:-1]

    monthly_approved.plot()
    plt.title("Monthly Approved Loans")
    plt.savefig("reports/figures/task_2_monthly_approved.png")
    plt.clf()


## Task 3
def plot_default_risk(df, branches):

    print("\nPLOTTING DEFAULT RISK (CLEAR SIMPLE HEATMAP)")

    # -----------------------------------
    # 1. LOAN ATTRIBUTE CORRELATION
    # -----------------------------------
    cols = ['LOAN_AMOUNT', 'INTEREST_RATE', 'CREDIT_SCORE', 'DEFAULT_FLAG']

    if all(col in df.columns for col in cols):

        corr = df[cols].corr()

        plt.figure()
        sns.heatmap(
            corr,
            annot=True,
            cmap="YlGnBu",
            annot_kws={"size": 10}
        )

        plt.title("Loan Attribute Correlation")
        plt.xticks(rotation=30)
        plt.yticks(rotation=0)

        plt.savefig("reports/figures/task_3_correlation_main.png")
        plt.clf()

    # -----------------------------------
    # 2. PAIRWISE CORRELATION
    # -----------------------------------
    pair_cols = ['EMI_AMOUNT', 'OVERDUE_AMOUNT', 'DEFAULT_AMOUNT']

    available_cols = [col for col in pair_cols if col in df.columns]

    if len(available_cols) >= 2:

        corr_pair = df[available_cols].corr()

        plt.figure()
        sns.heatmap(
            corr_pair,
            annot=True,
            cmap="YlGnBu",
            annot_kws={"size": 10}
        )

        plt.title("EMI / Overdue / Default Correlation")
        plt.xticks(rotation=30)
        plt.yticks(rotation=0)

        plt.savefig("reports/figures/task_3_correlation_pairwise.png")
        plt.clf()

    # -----------------------------------
    # 3. BRANCH CORRELATION (BAR — SIMPLE)
    # -----------------------------------
    if 'REGION' in df.columns:

        region_default = df.groupby('REGION')['DEFAULT_FLAG'].mean().reset_index()

        branch_analysis = branches.merge(region_default, on='REGION', how='left')

        branch_corr = {}

        if 'DELINQUENT_LOANS' in branch_analysis.columns:
            branch_corr['DELINQUENT_LOANS'] = branch_analysis['DELINQUENT_LOANS'].corr(
                branch_analysis['DEFAULT_FLAG']
            )

        if 'LOAN_DISBURSEMENT_AMOUNT' in branch_analysis.columns:
            branch_corr['LOAN_DISBURSEMENT_AMOUNT'] = branch_analysis['LOAN_DISBURSEMENT_AMOUNT'].corr(
                branch_analysis['DEFAULT_FLAG']
            )

        plt.bar(branch_corr.keys(), branch_corr.values())
        plt.title("Branch Metrics vs Default")

        plt.savefig("reports/figures/task_3_correlation_branch.png")
        plt.clf()

# Task 4

def plot_branch_performance(branches):

    print("\n PLOTTING BRANCH PERFORMANCE (BRANCH DATA ONLY)")

    # -----------------------------------
    # 1. LOAN DISBURSEMENT
    # -----------------------------------
    branches.sort_values(
        'LOAN_DISBURSEMENT_AMOUNT',
        ascending=False
    ).head(10).plot(
        x='REGION',
        y='LOAN_DISBURSEMENT_AMOUNT',
        kind='bar'
    )

    plt.title("Top Regions by Loan Disbursement")
    plt.savefig("reports/figures/task_4_branch_loan.png")
    plt.clf()

    # -----------------------------------
    # 2. DELINQUENCY
    # -----------------------------------
    branches.sort_values(
        'DELINQUENT_LOANS',
        ascending=False
    ).head(10).plot(
        x='REGION',
        y='DELINQUENT_LOANS',
        kind='bar'
    )

    plt.title("High Delinquency Regions")
    plt.savefig("reports/figures/task_4_branch_delinquency.png")
    plt.clf()

    # -----------------------------------
    # 3. REGION SUMMARY
    # -----------------------------------
    region_perf = branches.groupby('REGION').sum()

    region_perf['LOAN_DISBURSEMENT_AMOUNT'].plot(kind='bar')
    plt.title("Loan Disbursement by Region")
    plt.savefig("reports/figures/task_4_region_loan.png")
    plt.clf()

    region_perf['DELINQUENT_LOANS'].plot(kind='bar')
    plt.title("Delinquent Loans by Region")
    plt.savefig("reports/figures/task_4_region_delinquency.png")
    plt.clf()

    # -----------------------------------
    # LIMITATION MESSAGE
    # -----------------------------------
    print("\n Note:")
    print("Only loan volume and delinquency are plotted.")
    print("Processing time, default rate, and recovery rate are not available in branch dataset.")

# Task 5

def plot_customer_segmentation(df):

    print("\n PLOTTING CUSTOMER SEGMENTS")

    # -----------------------------------
    # INCOME SEGMENT
    # -----------------------------------
    if 'INCOME_SEGMENT' in df.columns:
        df['INCOME_SEGMENT'].value_counts().plot(kind='bar')
        plt.title("Customer Distribution by Income")
        plt.savefig("reports/figures/task_5_income_segment.png")
        plt.clf()

    # -----------------------------------
    # CREDIT SEGMENT
    # -----------------------------------
    if 'CREDIT_SEGMENT' in df.columns:
        df['CREDIT_SEGMENT'].value_counts().plot(kind='bar')
        plt.title("Customer Distribution by Credit Score")
        plt.savefig("reports/figures/task_5_credit_segment.png")
        plt.clf()

    # -----------------------------------
    # LOAN STATUS
    # -----------------------------------
    if 'LOAN_STATUS' in df.columns:
        df['LOAN_STATUS'].value_counts().plot(kind='bar')
        plt.title("Loan Status Distribution")
        plt.savefig("reports/figures/task_5_loan_status.png")
        plt.clf()

#         Task 6
def plot_advanced_analysis(df, branches):

    print("\n PLOTTING ADVANCED ANALYSIS")

    # -----------------------------------
    # 1. DEFAULT CORRELATION
    # -----------------------------------
    cols = [
        'CREDIT_SCORE',
        'LOAN_AMOUNT',
        'INTEREST_RATE',
        'OVERDUE_AMOUNT',
        'DEFAULT_FLAG'
    ]

    available = [col for col in cols if col in df.columns]

    if len(available) >= 2:

        corr = df[available].corr()

        plt.figure()
        sns.heatmap(corr, annot=True, cmap="YlGnBu")

        plt.title("Default Risk Correlation")
        plt.savefig("reports/figures/task_6_adv_default_corr.png")
        plt.clf()

    # -----------------------------------
    # 2. PAIRWISE HEATMAP
    # -----------------------------------
    pair_cols = ['EMI_AMOUNT', 'RECOVERY_RATE', 'DEFAULT_AMOUNT']

    available_pair = [col for col in pair_cols if col in df.columns]

    if len(available_pair) >= 2:

        corr_pair = df[available_pair].corr()

        plt.figure()
        sns.heatmap(corr_pair, annot=True, cmap="YlGnBu")

        plt.title("Pairwise Correlation")
        plt.savefig("reports/figures/task_6_adv_pairwise_corr.png")
        plt.clf()

    # -----------------------------------
    # 3. BRANCH (LIMITED)
    # -----------------------------------
    print("\n Branch heatmap limited (no linkage to loans)")

    corr_branch = branches[['DELINQUENT_LOANS', 'LOAN_DISBURSEMENT_AMOUNT']].corr()

    plt.figure()
    sns.heatmap(corr_branch, annot=True, cmap="YlGnBu")

    plt.title("Branch Internal Correlation")
    plt.savefig("reports/figures/task_6_adv_branch_corr.png")
    plt.clf()

#  Task 7
def plot_transaction_recovery(df, transactions):

    print("\n PLOTTING TRANSACTION & RECOVERY")

    # -----------------------------------
    # PENALTY DISTRIBUTION
    # -----------------------------------
    if 'PAYMENT_TYPE' in transactions.columns:

        transactions['PAYMENT_TYPE'].value_counts().plot(kind='bar')
        plt.title("Transaction Type Distribution")
        plt.savefig("reports/figures/task_7_txn_type.png")
        plt.clf()

    # -----------------------------------
    # RECOVERY BY REASON
    # -----------------------------------
    if 'DEFAULT_REASON' in df.columns:

        df.groupby('DEFAULT_REASON')['RECOVERY_RATE'].mean().plot(kind='bar')
        plt.title("Recovery by Default Reason")
        plt.savefig("reports/figures/task_7_recovery_reason.png")
        plt.clf()

    # -----------------------------------
    # RECOVERY BY REGION
    # -----------------------------------
    if 'REGION' in df.columns:

        df.groupby('REGION')['RECOVERY_RATE'].mean().plot(kind='bar')
        plt.title("Recovery by Region")
        plt.savefig("reports/figures/task_7_recovery_region.png")
        plt.clf()

    # -----------------------------------
    #  LIMITATION MESSAGE
    # -----------------------------------
    print("\n Branch plots not generated (no linkage)")

#     TASK 8

def plot_emi_analysis(df):
    print("\n PLOTTING EMI ANALYSIS")

    # -----------------------------------
    # EMI vs DEFAULT
    # -----------------------------------
    if 'EMI_AMOUNT' in df.columns and 'DEFAULT_FLAG' in df.columns:
        emi_default = df.groupby(pd.qcut(df['EMI_AMOUNT'], 5))['DEFAULT_FLAG'].mean()

        emi_default.plot(kind='bar')
        plt.title("Default Probability by EMI Segment")

        plt.savefig("reports/figures/task_8_emi_default.png")
        plt.clf()

    # -----------------------------------
    # EMI THRESHOLD
    # -----------------------------------
    if 'EMI_BIN' in df.columns:
        threshold = df.groupby('EMI_BIN')['DEFAULT_FLAG'].mean()

        threshold.plot(kind='bar')
        plt.title("EMI Threshold Analysis")

        plt.savefig("reports/figures/task_8_emi_threshold.png")
        plt.clf()

    # -----------------------------------
    # LIMITATION MESSAGE
    # -----------------------------------
    print("\n Loan type comparison not plotted (column missing)")

#   TASK 9

def plot_application_analysis(applications):

    print("\n PLOTTING APPLICATION INSIGHTS")

    applications.columns = [col.upper() for col in applications.columns]

    # -----------------------------------
    # APPROVAL STATUS
    # -----------------------------------
    if 'APPROVAL_STATUS' in applications.columns:

        applications['APPROVAL_STATUS'].value_counts().plot(kind='bar')
        plt.title("Approval vs Rejection")

        plt.savefig("reports/figures/task_9_application_status.png")
        plt.clf()

    # -----------------------------------
    # REJECTION REASONS
    # -----------------------------------
    reason_col = None

    for col in applications.columns:
        if 'REASON' in col:
            reason_col = col
            break

    if reason_col:

        rejected = applications[
            applications['APPROVAL_STATUS'].str.upper() == 'REJECTED'
        ]

        rejected[reason_col].value_counts().plot(kind='bar')
        plt.title("Rejection Reasons")

        plt.savefig("reports/figures/task_9_rejection_reason.png")
        plt.clf()

    # -----------------------------------
    # PROCESSING FEE
    # -----------------------------------
    fee_col = None

    for col in applications.columns:
        if 'FEE' in col:
            fee_col = col
            break

    if fee_col:

        applications.groupby('APPROVAL_STATUS')[fee_col].mean().plot(kind='bar')
        plt.title("Processing Fee Comparison")

        plt.savefig("reports/figures/task_9_processing_fee.png")
        plt.clf()

    print("\n Some plots may be skipped if columns not present")

#     TASK 11
def plot_disbursement_efficiency(df):

    print("\n PLOTTING DISBURSEMENT EFFICIENCY")

    # -----------------------------------
    # REGION
    # -----------------------------------
    if 'REGION' in df.columns:

        df.groupby('REGION')['PROCESSING_DAYS'].mean().plot(kind='bar')
        plt.title("Processing Time by Region")

        plt.savefig("reports/figures/task_11_disbursement_region.png")
        plt.clf()

    # -----------------------------------
    # LOAN PURPOSE
    # -----------------------------------
    if 'LOAN_PURPOSE' in df.columns:

        purpose_data = df.groupby('LOAN_PURPOSE')['PROCESSING_DAYS'].mean()

        if not purpose_data.empty:

            purpose_data.plot(kind='bar')
            plt.title("Processing Time by Loan Purpose")

            plt.savefig("reports/figures/task_11_disbursement_purpose.png")
            plt.clf()

        else:
            print(" Loan purpose data is empty")

    else:
        print(" LOAN_PURPOSE not available")

# Task 12

def plot_profitability(df):

    print("\n PLOTTING PROFITABILITY")

    # -----------------------------------
    # LOAN PURPOSE
    # -----------------------------------
    if 'LOAN_PURPOSE' in df.columns:

        df.groupby('LOAN_PURPOSE')['INTEREST_INCOME'].sum().plot(kind='bar')
        plt.title("Profit by Loan Purpose")

        plt.savefig("reports/figures/task_12_profit_purpose.png")
        plt.clf()

    # -----------------------------------
    # REGION
    # -----------------------------------
    if 'REGION' in df.columns:

        df.groupby('REGION')['INTEREST_INCOME'].sum().plot(kind='bar')
        plt.title("Profit by Region")

        plt.savefig("reports/figures/task_12_profit_region.png")
        plt.clf()

    print("\n Branch plot not generated (no linkage)")

# Task 13

def plot_geospatial(df):

    print("\n PLOTTING GEOSPATIAL ANALYSIS")

    # -----------------------------------
    # SAFE ACTIVE LOANS FILTER
    # -----------------------------------
    if 'LOAN_STATUS' in df.columns:

        status = df['LOAN_STATUS'].astype(str).str.upper().str.strip()

        active_loans = df[
            status.isin(['ACTIVE', 'APPROVED', 'DISBURSED'])
        ]

        if active_loans.empty:
            print(" No ACTIVE loans → fallback to non-default")
            active_loans = df[df['DEFAULT_FLAG'] == 0]

    else:
        print(" LOAN_STATUS missing → fallback used")
        active_loans = df[df['DEFAULT_FLAG'] == 0]

    # -----------------------------------
    # 1. REGION DISTRIBUTION (SAFE)
    # -----------------------------------
    if 'REGION' in active_loans.columns:

        region_counts = active_loans['REGION'].value_counts()

        if not region_counts.empty:

            region_counts.plot(kind='bar')
            plt.title("Active Loans by Region")

            plt.savefig("reports/figures/task_13_geo_distribution.png")
            plt.clf()

        else:
            print(" No data for region distribution")

    else:
        print(" REGION column missing")

    # -----------------------------------
    # 2. DEFAULT RATE BY REGION
    # -----------------------------------
    if 'REGION' in df.columns and 'DEFAULT_FLAG' in df.columns:

        default_rate = df.groupby('REGION')['DEFAULT_FLAG'].mean()

        if not default_rate.empty:

            default_rate.plot(kind='bar')
            plt.title("Default Rate by Region")

            plt.savefig("reports/figures/task_13_geo_default.png")
            plt.clf()

        else:
            print(" Default rate data empty")

    else:
        print("Missing REGION or DEFAULT_FLAG")

    # -----------------------------------
    # LIMITATION
    # -----------------------------------
    print("\n Rural vs Urban plot not generated (no AREA_TYPE)")

 #  Task 14

def plot_default_trends(df):
    print("\n PLOTTING DEFAULT TRENDS")

    # -----------------------------------
    # DATE COLUMN
    # -----------------------------------
    date_col = None

    if 'DEFAULT_DATE' in df.columns:
        date_col = 'DEFAULT_DATE'
    elif 'DISBURSAL_DATE' in df.columns:
        date_col = 'DISBURSAL_DATE'

    # -----------------------------------
    # 1. TIME TREND
    # -----------------------------------
    if date_col:

        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        trend = df.groupby(
            df[date_col].dt.to_period('M')
        )['DEFAULT_FLAG'].sum()

        if not trend.empty:

            trend.plot(kind='line')
            plt.title("Default Trend Over Time")

            plt.savefig("reports/figures/task_14_default_trend.png")
            plt.clf()

        else:
            print(" Trend data empty")

    # -----------------------------------
    # 2. PURPOSE DEFAULT
    # -----------------------------------
    if 'LOAN_PURPOSE' in df.columns:

        purpose = df.groupby('LOAN_PURPOSE')['DEFAULT_AMOUNT'].mean()

        if not purpose.empty:
            purpose.plot(kind='bar')
            plt.title("Default Amount by Loan Purpose")

            plt.savefig("reports/figures/task_14_default_purpose.png")
            plt.clf()

    # -----------------------------------
    # 3. INCOME SEGMENT
    # -----------------------------------

    if 'ANNUAL_INCOME' in df.columns:

        df['INCOME_SEGMENT'] = pd.qcut(
            df['ANNUAL_INCOME'],
            3,
            labels=['Low', 'Medium', 'High']
        )

        income = df.groupby('INCOME_SEGMENT')['DEFAULT_FLAG'].mean()

        if not income.empty:
            income.plot(kind='bar')
            plt.title("Default Rate by Income Segment")

            plt.savefig("reports/figures/task_14_default_income.png")
            plt.clf()

            print(" default_income.png saved")

        else:
            print(" Income segment data empty")

    else:
        print(" ANNUAL_INCOME missing")

# Task 16
def plot_time_series(df):

    print("\n PLOTTING TIME SERIES")

    # -----------------------------------
    # DISBURSEMENT TREND
    # -----------------------------------
    if 'DISBURSAL_DATE' in df.columns:

        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')

        trend = df.groupby(
            df['DISBURSAL_DATE'].dt.to_period('M')
        ).size()

        if not trend.empty:

            trend.plot(kind='line')
            plt.title("Monthly Loan Disbursement")

            plt.savefig("reports/figures/task_16_time_disbursement.png")
            plt.clf()

    # -----------------------------------
    # SEASONAL APPLICATION
    # -----------------------------------
    if 'APPLICATION_DATE' in df.columns:

        df['APPLICATION_DATE'] = pd.to_datetime(df['APPLICATION_DATE'], errors='coerce')

        seasonal = df.groupby(
            df['APPLICATION_DATE'].dt.month
        ).size()

        if not seasonal.empty:

            seasonal.plot(kind='bar')
            plt.title("Seasonal Applications")

            plt.savefig("reports/figures/task_16_time_seasonal_app.png")
            plt.clf()

    # -----------------------------------
    # SEASONAL DISBURSEMENT
    # -----------------------------------
    if 'DISBURSAL_DATE' in df.columns:

        seasonal = df.groupby(
            df['DISBURSAL_DATE'].dt.month
        ).size()

        if not seasonal.empty:

            seasonal.plot(kind='bar')
            plt.title("Seasonal Disbursement")

            plt.savefig("reports/figures/task_16_time_seasonal_disb.png")
            plt.clf()

        # -----------------------------------
        # 3. DEFAULT RATE BY REGION (FIXED)
        # -----------------------------------
    if 'DISBURSAL_DATE' in df.columns and 'REGION' in df.columns:

        df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], errors='coerce')

        df_valid = df[df['DISBURSAL_DATE'].notna()].copy()

        if not df_valid.empty:

            df_valid['MONTH'] = df_valid['DISBURSAL_DATE'].dt.to_period('M')

            region_default = df_valid.groupby(
                ['MONTH', 'REGION']
            )['DEFAULT_FLAG'].mean().unstack()

            if not region_default.empty:
                region_default.plot()
                plt.title("Monthly Default Rate by Region")

                plt.savefig("reports/figures/task_16_time_default_region.png")
                plt.clf()

                print(" time_default_region.png saved")

            else:
                print(" No data for region default plot")
        else:
            print(" DISBURSAL_DATE invalid")

    else:
        print(" Required columns missing")

# Task 17


def plot_customer_behavior(df, applications, customers):

    print("\n PLOTTING CUSTOMER BEHAVIOR")

    # -----------------------------------
    # 1. REPAYMENT BEHAVIOR
    # -----------------------------------
    if 'CUSTOMER_ID' in df.columns and 'DEFAULT_FLAG' in df.columns:

        behavior = df.groupby('CUSTOMER_ID')['DEFAULT_FLAG'].mean()

        def categorize(x):
            if x == 0:
                return 'On Time'
            elif x < 0.5:
                return 'Occasional'
            else:
                return 'Frequent'

        segments = behavior.apply(categorize).value_counts()

        if not segments.empty:
            segments.plot(kind='bar')
            plt.title("Customer Repayment Behavior")
            plt.savefig("reports/figures/task_17_customer_behavior.png")
            plt.clf()

    # -----------------------------------
    # MERGE FOR DEMOGRAPHICS
    # -----------------------------------
    merged = applications.merge(customers, on='CUSTOMER_ID', how='left')

    # -----------------------------------
    # 2. AGE ANALYSIS
    # -----------------------------------
    if 'AGE' in merged.columns:

        merged['AGE_GROUP'] = pd.cut(
            merged['AGE'],
            bins=[18, 30, 50, 70],
            labels=['Young', 'Middle', 'Senior']
        )

        age_plot = merged.groupby(
            ['AGE_GROUP', 'APPROVAL_STATUS']
        ).size().unstack()

        if not age_plot.empty:
            age_plot.plot(kind='bar')
            plt.title("Approval by Age Group")
            plt.savefig("reports/figures/task_17_customer_age.png")
            plt.clf()

    # -----------------------------------
    # 3. GENDER ANALYSIS
    # -----------------------------------
    if 'GENDER' in merged.columns:

        gender_plot = merged.groupby(
            ['GENDER', 'APPROVAL_STATUS']
        ).size().unstack()

        if not gender_plot.empty:
            gender_plot.plot(kind='bar')
            plt.title("Approval by Gender")
            plt.savefig("reports/figures/task_17_customer_gender.png")
            plt.clf()

# Task 18
def plot_risk(df):

    print("\ PLOTTING RISK ANALYSIS")

    # -----------------------------------
    # LOAN PURPOSE RISK
    # -----------------------------------
    if 'LOAN_PURPOSE' in df.columns and 'RISK_SCORE' in df.columns:

        purpose_risk = df.groupby('LOAN_PURPOSE')['RISK_SCORE'].mean()

        if not purpose_risk.empty:

            purpose_risk.plot(kind='bar')
            plt.title("Risk by Loan Purpose")

            plt.savefig("reports/figures/task_18_risk_purpose.png")
            plt.clf()

    # -----------------------------------
    # CREDIT SEGMENT RISK
    # -----------------------------------
    if 'CREDIT_SEGMENT' in df.columns:

        credit_risk = df.groupby('CREDIT_SEGMENT')['DEFAULT_FLAG'].mean()

        if not credit_risk.empty:

            credit_risk.plot(kind='bar')
            plt.title("Risk by Credit Segment")

            plt.savefig("reports/figures/task_18_risk_credit.png")
            plt.clf()

# Task 19
def plot_time_to_default(df):

    print("\n PLOTTING TIME TO DEFAULT")

    if 'TIME_TO_DEFAULT' not in df.columns:
        print(" TIME_TO_DEFAULT not found")
        return

    # -----------------------------------
    # PURPOSE PLOT
    # -----------------------------------
    if 'LOAN_PURPOSE' in df.columns:

        purpose = df.groupby('LOAN_PURPOSE')['TIME_TO_DEFAULT'].mean()

        if not purpose.empty:

            purpose.plot(kind='bar')
            plt.title("Time to Default by Loan Purpose")

            plt.savefig("reports/figures/task_19_time_to_default_purpose.png")
            plt.clf()

    # -----------------------------------
    # CREDIT SEGMENT
    # -----------------------------------
    if 'CREDIT_SEGMENT' in df.columns:

        credit = df.groupby('CREDIT_SEGMENT')['TIME_TO_DEFAULT'].mean()

        if not credit.empty:

            credit.plot(kind='bar')
            plt.title("Time to Default by Credit Segment")

            plt.savefig("reports/figures/task_19_time_to_default_credit.png")
            plt.clf()

# Task 20


def plot_transaction_pattern(transactions, df):

    print("\n PLOTTING TRANSACTION PATTERN")

    transactions.columns = [col.upper() for col in transactions.columns]

    # Ensure folder exists
    # os.makedirs("reports/figures", exist_ok=True)

    # -----------------------------------
    # PAYMENT TYPE DISTRIBUTION
    # -----------------------------------
    if 'PAYMENT_TYPE' in transactions.columns:

        counts = transactions['PAYMENT_TYPE'].value_counts()

        if not counts.empty:
            counts.plot(kind='bar')
            plt.title("Payment Type Distribution")

            plt.savefig("reports/figures/task_20_txn_type_dist.png")
            plt.clf()

            print(" txn_type.png saved")
        else:
            print(" No data to plot")

    else:
        print(" PAYMENT_TYPE missing")