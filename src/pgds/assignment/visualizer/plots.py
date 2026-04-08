"""
Visualizer — plots.py
Generates and saves charts for all 20 analysis tasks.
All figures are saved to reports/figures/.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np
from config import FIGURE_PATH

os.makedirs(FIGURE_PATH, exist_ok=True)

# ── Shared style ──────────────────────────────────────────────────────────────
RED    = '#E31E24'
BLUE   = '#2E86AB'
GREEN  = '#27AE60'
DARK   = '#1A1A2E'
ORANGE = '#F39C12'
PURPLE = '#8E44AD'
BG     = '#F8F9FC'
GRAY   = '#95A5A6'
PALETTE = [RED, BLUE, GREEN, ORANGE, PURPLE, '#16A085', '#D35400', '#2C3E50']

sns.set_theme(style='whitegrid', font_scale=1.0)
plt.rcParams.update({
    'figure.facecolor': BG,
    'axes.facecolor': 'white',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
})


def _save(name):
    path = os.path.join(FIGURE_PATH, name)
    plt.savefig(path, dpi=130, bbox_inches='tight')
    plt.close()
    print(f"  📊 Saved: {name}")


# ─────────────────────────────────────────────────────────────────────────────
# TASK 2: Descriptive Analysis
# ─────────────────────────────────────────────────────────────────────────────

def plot_descriptive(df, applications=None):
    """Loan amount, EMI, credit score distributions + regional + monthly trend."""

    # Loan Amount distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df['LOAN_AMOUNT'].dropna(), bins=60, color=RED, alpha=0.85, edgecolor='white')
    ax.axvline(df['LOAN_AMOUNT'].median(), color=DARK, lw=2, linestyle='--',
               label=f'Median ₹{df["LOAN_AMOUNT"].median()/1e5:.1f}L')
    ax.set_title('Loan Amount Distribution')
    ax.set_xlabel('Loan Amount (₹)')
    ax.set_ylabel('Count')
    ax.legend()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x/1e5:.0f}L'))
    _save('task02_loan_distribution.png')

    # EMI distribution
    if 'EMI_AMOUNT' in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(df['EMI_AMOUNT'].dropna(), bins=60, color=BLUE, alpha=0.85, edgecolor='white')
        ax.axvline(df['EMI_AMOUNT'].median(), color=DARK, lw=2, linestyle='--',
                   label=f'Median ₹{df["EMI_AMOUNT"].median():,.0f}')
        ax.set_title('EMI Amount Distribution')
        ax.set_xlabel('EMI Amount (₹)')
        ax.set_ylabel('Count')
        ax.legend()
        _save('task02_emi_distribution.png')

    # Credit Score distribution
    if 'CREDIT_SCORE' in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(df['CREDIT_SCORE'].dropna(), bins=50, color=GREEN, alpha=0.85, edgecolor='white')
        ax.axvline(df['CREDIT_SCORE'].mean(), color=DARK, lw=2, linestyle='--',
                   label=f'Mean {df["CREDIT_SCORE"].mean():.0f}')
        for thr, c in [(580, ORANGE), (670, GREEN), (740, BLUE)]:
            ax.axvline(thr, color=c, lw=1, linestyle=':', alpha=0.7)
        ax.set_title('Credit Score Distribution')
        ax.set_xlabel('Credit Score')
        ax.set_ylabel('Count')
        ax.legend(fontsize=9)
        _save('task02_credit_score_distribution.png')

    # Regional disbursement
    if 'REGION' in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        reg = df.groupby('REGION')['LOAN_AMOUNT'].sum().sort_values()
        bars = ax.barh(reg.index, reg.values / 1e9, color=PALETTE[:len(reg)], edgecolor='white')
        for bar, val in zip(bars, reg.values):
            ax.text(val/1e9 + 0.05, bar.get_y() + bar.get_height()/2,
                    f'₹{val/1e9:.1f}B', va='center', fontsize=9)
        ax.set_title('Loan Disbursement by Region')
        ax.set_xlabel('Total Disbursement (₹ Billions)')
        _save('task02_region_disbursement.png')

        # Regional default rate
        fig, ax = plt.subplots(figsize=(8, 5))
        reg_def = df.groupby('REGION')['DEFAULT_FLAG'].mean().mul(100).sort_values(ascending=False)
        avg = reg_def.mean()
        colors = [RED if v > avg else BLUE for v in reg_def.values]
        ax.bar(reg_def.index, reg_def.values, color=colors, edgecolor='white')
        ax.axhline(avg, color=DARK, lw=1.5, linestyle='--', label=f'Avg {avg:.1f}%')
        ax.set_title('Default Rate by Region (%)')
        ax.set_ylabel('Default Rate (%)')
        ax.legend()
        _save('task02_region_default.png')

    # Monthly application trend
    if applications is not None and 'APPLICATION_DATE' in applications.columns:
        apps = applications.copy()
        apps['APPLICATION_DATE'] = pd.to_datetime(apps['APPLICATION_DATE'], errors='coerce')
        monthly = apps.groupby(apps['APPLICATION_DATE'].dt.to_period('M')).size()
        monthly.index = monthly.index.to_timestamp()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(monthly.index, monthly.values, color=RED, lw=2)
        ax.fill_between(monthly.index, monthly.values, alpha=0.15, color=RED)
        ax.set_title('Monthly Loan Applications Trend')
        ax.set_xlabel('Month')
        ax.set_ylabel('Applications')
        ax.tick_params(axis='x', rotation=30)
        _save('task02_monthly_applications.png')


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3 & 6: Default Risk + Correlation Heatmaps
# ─────────────────────────────────────────────────────────────────────────────

def plot_default_risk(df):
    """Correlation heatmap for default risk variables + credit score bucket chart."""

    # Loan attribute correlation heatmap
    cols = ['LOAN_AMOUNT', 'INTEREST_RATE', 'CREDIT_SCORE',
            'OVERDUE_AMOUNT', 'DEFAULT_FLAG']
    cols = [c for c in cols if c in df.columns]
    if len(cols) >= 2:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(df[cols].corr(), annot=True, fmt='.2f', cmap='RdYlGn',
                    center=0, ax=ax, linewidths=0.5, cbar_kws={'shrink': 0.8})
        ax.set_title('Loan Attribute Correlation Heatmap')
        ax.tick_params(axis='x', rotation=45)
        _save('task03_loan_correlation_heatmap.png')

    # Pairwise: EMI / Overdue / Default Amount
    pair_cols = ['EMI_AMOUNT', 'OVERDUE_AMOUNT', 'DEFAULT_AMOUNT']
    pair_cols = [c for c in pair_cols if c in df.columns]
    if len(pair_cols) >= 2:
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(df[pair_cols].corr(), annot=True, fmt='.2f', cmap='coolwarm',
                    center=0, ax=ax, linewidths=0.5)
        ax.set_title('Pairwise Correlation: EMI / Overdue / Default Amount')
        _save('task03_pairwise_heatmap.png')

    # Default rate by credit score bucket
    if 'CREDIT_SCORE' in df.columns:
        df = df.copy()
        df['CREDIT_BUCKET'] = pd.cut(
            df['CREDIT_SCORE'],
            bins=[0, 300, 580, 670, 740, 900],
            labels=['Very Poor\n(<300)', 'Poor\n(300-580)',
                    'Fair\n(580-670)', 'Good\n(670-740)', 'Excellent\n(>740)']
        )
        cs_def = df.groupby('CREDIT_BUCKET', observed=True)['DEFAULT_FLAG'].mean().mul(100)
        fig, ax = plt.subplots(figsize=(9, 5))
        bar_colors = ['#c0392b', '#e67e22', '#f1c40f', '#27ae60', '#2980b9']
        bars = ax.bar(cs_def.index, cs_def.values, color=bar_colors, edgecolor='white', width=0.6)
        for bar, val in zip(bars, cs_def.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{val:.1f}%', ha='center', fontweight='bold')
        ax.set_title('Default Rate by Credit Score Bucket')
        ax.set_ylabel('Default Rate (%)')
        _save('task03_default_by_credit_bucket.png')


def plot_statistical_analysis(df, defaults=None):
    """Advanced statistical analysis plots — Task 6."""

    # Full correlation heatmap
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    key_cols = ['CREDIT_SCORE', 'LOAN_AMOUNT', 'INTEREST_RATE',
                'EMI_AMOUNT', 'OVERDUE_AMOUNT', 'DEFAULT_FLAG']
    key_cols = [c for c in key_cols if c in num_cols]
    if len(key_cols) >= 2:
        fig, ax = plt.subplots(figsize=(9, 7))
        sns.heatmap(df[key_cols].corr(), annot=True, fmt='.2f', cmap='RdYlGn',
                    center=0, ax=ax, linewidths=0.5, cbar_kws={'shrink': 0.8})
        ax.set_title('Default Risk Correlation Heatmap (Task 6)')
        ax.tick_params(axis='x', rotation=45)
        _save('task06_default_risk_heatmap.png')

    # Advanced pairwise with recovery rate
    if defaults is not None:
        defs = defaults.copy()
        if 'RECOVERY_RATE' not in defs.columns:
            defs['RECOVERY_RATE'] = (
                defs['RECOVERY_AMOUNT'] / defs['DEFAULT_AMOUNT'].replace(0, pd.NA)
            ).clip(0, 1)
        merged = df.merge(defs[['LOAN_ID', 'RECOVERY_RATE', 'DEFAULT_AMOUNT']],
                          on='LOAN_ID', how='left', suffixes=('', '_D'))
        pair_cols = ['EMI_AMOUNT', 'RECOVERY_RATE', 'DEFAULT_AMOUNT']
        pair_cols = [c for c in pair_cols if c in merged.columns]
        if len(pair_cols) >= 2:
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.heatmap(merged[pair_cols].corr(), annot=True, fmt='.2f',
                        cmap='coolwarm', center=0, ax=ax)
            ax.set_title('Advanced Pairwise Correlation (EMI / Recovery / Default Amt)')
            _save('task06_advanced_pairwise_heatmap.png')


# ─────────────────────────────────────────────────────────────────────────────
# TASK 4: Branch Performance
# ─────────────────────────────────────────────────────────────────────────────

def plot_branch_performance(df, branches=None):
    """Branch disbursement, delinquency, and region comparison charts."""

    if branches is not None:
        # Top 15 branches by disbursement
        top_b = branches.nlargest(15, 'LOAN_DISBURSEMENT_AMOUNT')
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.barh(top_b['BRANCH_NAME'].str[:28], top_b['LOAN_DISBURSEMENT_AMOUNT'] / 1e7,
                color=RED, alpha=0.85, edgecolor='white')
        ax.set_title('Top 15 Branches — Loan Disbursement (₹ Crores)')
        ax.set_xlabel('Disbursement (₹ Crores)')
        _save('task04_top_branches_disbursement.png')

        # Delinquency rate
        if 'DELINQUENT_LOANS' in branches.columns and 'TOTAL_ACTIVE_LOANS' in branches.columns:
            branches = branches.copy()
            branches['DELINQUENCY_RATE'] = (
                branches['DELINQUENT_LOANS'] / branches['TOTAL_ACTIVE_LOANS'] * 100
            )
            top_del = branches.nlargest(15, 'DELINQUENCY_RATE')
            avg_del = branches['DELINQUENCY_RATE'].mean()
            colors = [RED if v > avg_del else BLUE for v in top_del['DELINQUENCY_RATE']]
            fig, ax = plt.subplots(figsize=(10, 7))
            ax.barh(top_del['BRANCH_NAME'].str[:28], top_del['DELINQUENCY_RATE'],
                    color=colors, edgecolor='white')
            ax.axvline(avg_del, color=DARK, lw=1.5, linestyle='--', label=f'Avg {avg_del:.1f}%')
            ax.set_title('Top 15 Branches — Delinquency Rate (%)')
            ax.set_xlabel('Delinquency Rate (%)')
            ax.legend()
            _save('task04_branch_delinquency.png')

    # Region disbursement
    if 'REGION' in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        df.groupby('REGION')['LOAN_AMOUNT'].sum().sort_values().div(1e9).plot(
            kind='barh', color=BLUE, ax=ax, edgecolor='white'
        )
        ax.set_title('Loan Disbursement by Region (₹ Billions)')
        ax.set_xlabel('₹ Billions')
        _save('task04_region_disbursement.png')

        # Default rate by region
        fig, ax = plt.subplots(figsize=(8, 5))
        df.groupby('REGION')['DEFAULT_FLAG'].mean().mul(100).sort_values(ascending=False).plot(
            kind='bar', color=[RED, ORANGE, BLUE, GREEN, PURPLE, GRAY][:len(df['REGION'].unique())],
            ax=ax, edgecolor='white'
        )
        ax.set_title('Default Rate by Region (%)')
        ax.set_ylabel('Default Rate (%)')
        ax.tick_params(axis='x', rotation=30)
        _save('task04_region_default_rate.png')


# ─────────────────────────────────────────────────────────────────────────────
# TASK 5: Customer Segmentation
# ─────────────────────────────────────────────────────────────────────────────

def plot_customer_segments(df):
    """Customer credit segment distribution and default rates."""

    seg_colors = {'High Risk': RED, 'Medium': ORANGE, 'Good': BLUE, 'Excellent': GREEN}

    if 'CREDIT_SEGMENT' in df.columns:
        # Segment distribution
        fig, ax = plt.subplots(figsize=(8, 5))
        counts = df['CREDIT_SEGMENT'].value_counts()
        colors = [seg_colors.get(k, GRAY) for k in counts.index]
        bars = ax.bar(counts.index, counts.values, color=colors, edgecolor='white', width=0.5)
        for bar, val in zip(bars, counts.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                    f'{val:,}', ha='center', fontsize=10)
        ax.set_title('Customer Distribution by Credit Segment')
        ax.set_ylabel('Count')
        _save('task05_customer_credit_segment.png')

        # Default rate by credit segment
        fig, ax = plt.subplots(figsize=(8, 5))
        seg_def = df.groupby('CREDIT_SEGMENT', observed=True)['DEFAULT_FLAG'].mean().mul(100)
        colors2 = [seg_colors.get(k, GRAY) for k in seg_def.index]
        bars = ax.bar(seg_def.index, seg_def.values, color=colors2, edgecolor='white', width=0.5)
        for bar, val in zip(bars, seg_def.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{val:.1f}%', ha='center', fontweight='bold')
        ax.set_title('Default Rate by Credit Segment')
        ax.set_ylabel('Default Rate (%)')
        _save('task05_default_by_credit_segment.png')

    if 'INCOME_SEGMENT' in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        inc_def = df.groupby('INCOME_SEGMENT', observed=True)['DEFAULT_FLAG'].mean().mul(100)
        bars = ax.bar(inc_def.index, inc_def.values,
                      color=[RED, ORANGE, GREEN], edgecolor='white', width=0.5)
        for bar, val in zip(bars, inc_def.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{val:.1f}%', ha='center', fontweight='bold')
        ax.set_title('Default Rate by Income Segment')
        ax.set_ylabel('Default Rate (%)')
        _save('task05_default_by_income_segment.png')


# ─────────────────────────────────────────────────────────────────────────────
# TASK 7: Transaction & Recovery
# ─────────────────────────────────────────────────────────────────────────────

def plot_transaction_recovery(df, transactions, defaults):
    """Transaction types, recovery rates, and overdue trends."""

    type_col = next((c for c in ['PAYMENT_TYPE', 'TRANSACTION_TYPE']
                     if c in transactions.columns), None)

    if type_col:
        fig, ax = plt.subplots(figsize=(7, 5))
        tx_counts = transactions[type_col].value_counts()
        colors = [RED, BLUE, GREEN, ORANGE][:len(tx_counts)]
        bars = ax.bar(tx_counts.index, tx_counts.values / 1000, color=colors, edgecolor='white')
        for bar, val in zip(bars, tx_counts.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{val/1000:.0f}K', ha='center', fontweight='bold')
        ax.set_title('Transaction Type Distribution')
        ax.set_ylabel('Count (Thousands)')
        _save('task07_transaction_types.png')

    if 'RECOVERY_AMOUNT' in defaults.columns and 'DEFAULT_AMOUNT' in defaults.columns:
        defs = defaults.copy()
        defs['RECOVERY_RATE'] = (defs['RECOVERY_AMOUNT'] / defs['DEFAULT_AMOUNT'].replace(0, pd.NA)).clip(0, 1)

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.hist(defs['RECOVERY_RATE'].dropna() * 100, bins=40,
                color=BLUE, alpha=0.85, edgecolor='white')
        ax.axvline(defs['RECOVERY_RATE'].mean() * 100, color=RED, lw=2,
                   linestyle='--', label=f'Mean {defs["RECOVERY_RATE"].mean()*100:.1f}%')
        ax.set_title('Recovery Rate Distribution')
        ax.set_xlabel('Recovery Rate (%)')
        ax.set_ylabel('Count')
        ax.legend()
        _save('task07_recovery_distribution.png')

        if 'LEGAL_ACTION' in defs.columns:
            fig, ax = plt.subplots(figsize=(6, 5))
            legal_rec = defs.groupby('LEGAL_ACTION')['RECOVERY_RATE'].mean().mul(100)
            colors_l = [GREEN if v >= 50 else RED for v in legal_rec.values]
            bars = ax.bar(legal_rec.index, legal_rec.values, color=colors_l, edgecolor='white', width=0.4)
            for bar, val in zip(bars, legal_rec.values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                        f'{val:.1f}%', ha='center', fontweight='bold')
            ax.set_title('Recovery Rate: Legal Action vs None')
            ax.set_ylabel('Avg Recovery Rate (%)')
            _save('task07_recovery_by_legal_action.png')

        if 'DEFAULT_REASON' in defs.columns:
            fig, ax = plt.subplots(figsize=(8, 5))
            reason_rec = defs.groupby('DEFAULT_REASON')['RECOVERY_RATE'].mean().mul(100).sort_values()
            bars = ax.barh(reason_rec.index, reason_rec.values, color=BLUE, alpha=0.85, edgecolor='white')
            ax.axvline(50, color=RED, lw=1.5, linestyle='--', label='50% mark')
            for bar, val in zip(bars, reason_rec.values):
                ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                        f'{val:.1f}%', va='center', fontsize=9)
            ax.set_title('Recovery Rate by Default Reason')
            ax.set_xlabel('Avg Recovery Rate (%)')
            ax.legend()
            _save('task07_recovery_by_reason.png')


# ─────────────────────────────────────────────────────────────────────────────
# TASK 8: EMI Analysis
# ─────────────────────────────────────────────────────────────────────────────

def plot_emi_analysis(df):
    """EMI bucket default rates and EMI by loan purpose."""

    if 'EMI_AMOUNT' not in df.columns:
        return

    df = df.copy()
    df['EMI_BUCKET'] = pd.qcut(df['EMI_AMOUNT'], q=5, duplicates='drop')

    fig, ax = plt.subplots(figsize=(10, 5))
    emi_def = df.groupby('EMI_BUCKET', observed=True)['DEFAULT_FLAG'].mean().mul(100)
    ax.bar(range(len(emi_def)), emi_def.values, color=RED, alpha=0.85, edgecolor='white')
    ax.set_xticks(range(len(emi_def)))
    ax.set_xticklabels([str(b) for b in emi_def.index], rotation=40, ha='right', fontsize=8)
    ax.set_title('Default Rate by EMI Amount Bucket (Task 8)')
    ax.set_ylabel('Default Rate (%)')
    _save('task08_emi_default.png')

    if 'LOAN_PURPOSE' in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        emi_purpose = df.groupby('LOAN_PURPOSE')['EMI_AMOUNT'].mean().sort_values()
        bars = ax.barh(emi_purpose.index, emi_purpose.values,
                       color=PALETTE[:len(emi_purpose)], edgecolor='white')
        for bar, val in zip(bars, emi_purpose.values):
            ax.text(val + 50, bar.get_y() + bar.get_height()/2,
                    f'₹{val:,.0f}', va='center', fontsize=9)
        ax.set_title('Avg EMI Amount by Loan Purpose')
        ax.set_xlabel('Avg EMI Amount (₹)')
        _save('task08_emi_by_purpose.png')


# ─────────────────────────────────────────────────────────────────────────────
# TASK 9: Application Insights
# ─────────────────────────────────────────────────────────────────────────────

def plot_application_analysis(df, applications=None):
    """Approval/rejection rates, rejection reasons, processing fee comparison."""

    src = applications if applications is not None else df
    src = src.copy()

    if 'APPROVAL_STATUS' not in src.columns:
        return

    # Approval pie
    fig, ax = plt.subplots(figsize=(6, 6))
    counts = src['APPROVAL_STATUS'].value_counts()
    ax.pie(counts.values, labels=counts.index,
           colors=[GREEN, RED, ORANGE][:len(counts)],
           autopct='%1.1f%%', startangle=90,
           wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    ax.set_title('Loan Application Approval Rate (Task 9)')
    _save('task09_approval_rate_pie.png')

    # Rejection reasons
    if 'REJECTION_REASON' in src.columns:
        rej = src[src['APPROVAL_STATUS'] == 'Rejected']['REJECTION_REASON'].value_counts().head(8)
        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.barh(rej.index, rej.values, color=BLUE, alpha=0.85, edgecolor='white')
        for bar, val in zip(bars, rej.values):
            ax.text(val + 10, bar.get_y() + bar.get_height()/2, f'{val:,}', va='center', fontsize=9)
        ax.set_title('Top Loan Rejection Reasons')
        ax.set_xlabel('Count')
        _save('task09_rejection_reasons.png')

    # Processing fee comparison
    if 'PROCESSING_FEE' in src.columns:
        fig, ax = plt.subplots(figsize=(6, 5))
        fee = src.groupby('APPROVAL_STATUS')['PROCESSING_FEE'].mean()
        colors = [GREEN if s == 'Approved' else RED for s in fee.index]
        bars = ax.bar(fee.index, fee.values, color=colors, edgecolor='white', width=0.4)
        for bar, val in zip(bars, fee.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                    f'₹{val:,.0f}', ha='center', fontweight='bold')
        ax.set_title('Avg Processing Fee: Approved vs Rejected')
        ax.set_ylabel('Avg Processing Fee (₹)')
        _save('task09_processing_fee_comparison.png')


# ─────────────────────────────────────────────────────────────────────────────
# TASK 12: Profitability
# ─────────────────────────────────────────────────────────────────────────────

def plot_profitability(df):
    """Interest income by purpose, region, and monthly disbursement trend."""

    if 'INTEREST_INCOME' not in df.columns:
        if 'INTEREST_RATE' in df.columns and 'LOAN_TERM' in df.columns:
            df = df.copy()
            df['INTEREST_INCOME'] = df['LOAN_AMOUNT'] * (df['INTEREST_RATE']/100) * (df['LOAN_TERM']/12)

    if 'INTEREST_INCOME' not in df.columns:
        return

    if 'LOAN_PURPOSE' in df.columns:
        fig, ax = plt.subplots(figsize=(9, 5))
        purp = df.groupby('LOAN_PURPOSE')['INTEREST_INCOME'].sum().sort_values()
        bars = ax.barh(purp.index, purp.values / 1e7, color=RED, alpha=0.85, edgecolor='white')
        for bar, val in zip(bars, purp.values):
            ax.text(val/1e7 + 2, bar.get_y() + bar.get_height()/2,
                    f'₹{val/1e7:.0f}Cr', va='center', fontsize=9)
        ax.set_title('Estimated Interest Income by Loan Purpose (Task 12)')
        ax.set_xlabel('Interest Income (₹ Crores)')
        _save('task12_interest_income_by_purpose.png')

    if 'REGION' in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        reg_inc = df.groupby('REGION')['INTEREST_INCOME'].sum().sort_values(ascending=False)
        bars = ax.bar(reg_inc.index, reg_inc.values / 1e9,
                      color=PALETTE[:len(reg_inc)], edgecolor='white')
        for bar, val in zip(bars, reg_inc.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f'₹{val/1e9:.1f}B', ha='center', fontsize=9, fontweight='bold')
        ax.set_title('Estimated Interest Income by Region')
        ax.set_xlabel('Region')
        ax.set_ylabel('Interest Income (₹ Billions)')
        _save('task12_interest_income_by_region.png')

    # Monthly disbursement trend
    if 'DISBURSAL_DATE' in df.columns:
        df2 = df.copy()
        df2['DISBURSAL_DATE'] = pd.to_datetime(df2['DISBURSAL_DATE'], errors='coerce')
        monthly = df2.groupby(df2['DISBURSAL_DATE'].dt.to_period('M'))['LOAN_AMOUNT'].sum()
        monthly.index = monthly.index.to_timestamp()
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(monthly.index, monthly.values / 1e9, color=RED, lw=2)
        ax.fill_between(monthly.index, monthly.values / 1e9, alpha=0.12, color=RED)
        ax.set_title('Monthly Loan Disbursement Trend')
        ax.set_xlabel('Month')
        ax.set_ylabel('Disbursement (₹ Billions)')
        ax.tick_params(axis='x', rotation=30)
        _save('task12_monthly_disbursement_trend.png')


# ─────────────────────────────────────────────────────────────────────────────
# TASK 14: Default Trends
# ─────────────────────────────────────────────────────────────────────────────

def plot_default_trends(df, defaults=None):
    """Monthly default count trend and default by purpose."""

    src = defaults if defaults is not None else df[df['DEFAULT_FLAG'] == 1]

    if 'DEFAULT_DATE' in src.columns:
        src = src.copy()
        src['DEFAULT_DATE'] = pd.to_datetime(src['DEFAULT_DATE'], errors='coerce')
        monthly_def = src.groupby(src['DEFAULT_DATE'].dt.to_period('M')).size()
        monthly_def.index = monthly_def.index.to_timestamp()
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(monthly_def.index, monthly_def.values, color=RED, lw=2, marker='o', markersize=3)
        ax.fill_between(monthly_def.index, monthly_def.values, alpha=0.15, color=RED)
        ax.set_title('Monthly Default Count Trend (Task 14)')
        ax.set_ylabel('# Defaults')
        ax.tick_params(axis='x', rotation=30)
        _save('task14_monthly_default_trend.png')

    if 'LOAN_PURPOSE' in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        purp_def = df.groupby('LOAN_PURPOSE')['DEFAULT_FLAG'].mean().mul(100).sort_values(ascending=False)
        avg = purp_def.mean()
        colors = [RED if v > avg else BLUE for v in purp_def.values]
        bars = ax.bar(purp_def.index, purp_def.values, color=colors, edgecolor='white')
        ax.axhline(avg, color=DARK, lw=1.5, linestyle='--', label=f'Avg {avg:.1f}%')
        ax.set_title('Default Rate by Loan Purpose')
        ax.set_ylabel('Default Rate (%)')
        ax.legend()
        ax.tick_params(axis='x', rotation=20)
        _save('task14_default_by_purpose.png')


# ─────────────────────────────────────────────────────────────────────────────
# TASK 16: Time-Series Analysis
# ─────────────────────────────────────────────────────────────────────────────

def plot_time_series(df, applications=None):
    """Seasonal pattern and yearly disbursement trend."""

    # Seasonal: applications by month of year
    src = applications if applications is not None else df
    src = src.copy()
    if 'APPLICATION_DATE' in src.columns:
        src['APPLICATION_DATE'] = pd.to_datetime(src['APPLICATION_DATE'], errors='coerce')
        seasonal = src.groupby(src['APPLICATION_DATE'].dt.month).size()
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(range(1, 13), seasonal.values, color=BLUE, alpha=0.85, edgecolor='white')
        ax.plot(range(1, 13), seasonal.values, color=RED, lw=2, marker='o')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(month_names)
        ax.set_title('Seasonal Pattern — Loan Applications by Month (Task 16)')
        ax.set_ylabel('Total Applications')
        _save('task16_seasonal_applications.png')

    # Yearly disbursement
    if 'DISBURSAL_DATE' in df.columns:
        df2 = df.copy()
        df2['DISBURSAL_DATE'] = pd.to_datetime(df2['DISBURSAL_DATE'], errors='coerce')
        yearly = df2.groupby(df2['DISBURSAL_DATE'].dt.year)['LOAN_AMOUNT'].sum()
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(yearly.index.astype(str), yearly.values / 1e9,
                      color=PALETTE[:len(yearly)], edgecolor='white')
        for bar, val in zip(bars, yearly.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'₹{val/1e9:.1f}B', ha='center', fontsize=9, fontweight='bold')
        ax.set_title('Yearly Loan Disbursement')
        ax.set_ylabel('₹ Billions')
        _save('task16_yearly_disbursement.png')


# ─────────────────────────────────────────────────────────────────────────────
# TASK 19: Time to Default
# ─────────────────────────────────────────────────────────────────────────────

def plot_time_to_default(df, defaults=None):
    """Distribution of time from disbursement to default."""

    if defaults is not None and 'DEFAULT_DATE' in defaults.columns:
        defs_plot = defaults[['LOAN_ID', 'DEFAULT_DATE']].copy().rename(
            columns={'DEFAULT_DATE': 'TTD_DEFAULT_DATE'}
        )
        merged = df.merge(defs_plot, on='LOAN_ID', how='inner').copy()
        merged['_DD'] = pd.to_datetime(merged['TTD_DEFAULT_DATE'], errors='coerce')
    elif 'DEFAULT_DATE' in df.columns:
        merged = df[df['DEFAULT_FLAG'] == 1].copy()
        merged['_DD'] = pd.to_datetime(merged['DEFAULT_DATE'], errors='coerce')
    else:
        return

    merged = merged.copy()
    merged['_DISB'] = pd.to_datetime(merged.get('DISBURSAL_DATE', merged.get('REPAYMENT_START_DATE')), errors='coerce')
    merged['TTD'] = (merged['_DD'] - merged['_DISB']).dt.days
    valid = merged[merged['TTD'] > 0]['TTD']

    if valid.empty:
        return

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(valid, bins=50, color=RED, alpha=0.85, edgecolor='white')
    ax.axvline(valid.median(), color=DARK, lw=2, linestyle='--',
               label=f'Median {valid.median():.0f} days')
    ax.axvline(valid.mean(), color=BLUE, lw=2, linestyle='-.',
               label=f'Mean {valid.mean():.0f} days')
    ax.set_title('Time from Disbursement to Default (Task 19)')
    ax.set_xlabel('Days')
    ax.set_ylabel('Count')
    ax.legend()
    _save('task19_time_to_default.png')


# ─────────────────────────────────────────────────────────────────────────────
# TASK 20: Transaction Patterns
# ─────────────────────────────────────────────────────────────────────────────

def plot_transaction_patterns(df, transactions):
    """Penalty % trend and overdue vs non-overdue transaction comparison."""

    tx = transactions.copy()
    type_col = next((c for c in ['PAYMENT_TYPE', 'TRANSACTION_TYPE'] if c in tx.columns), None)
    amt_col  = next((c for c in ['AMOUNT', 'TRANSACTION_AMOUNT'] if c in tx.columns), None)

    if type_col and amt_col and 'TRANSACTION_DATE' in tx.columns:
        tx['TRANSACTION_DATE'] = pd.to_datetime(tx['TRANSACTION_DATE'], errors='coerce')
        monthly = tx.groupby([tx['TRANSACTION_DATE'].dt.to_period('M'), type_col])[amt_col] \
                    .sum().unstack(fill_value=0)
        monthly.index = monthly.index.to_timestamp()
        if 'Penalty' in monthly.columns and 'EMI' in monthly.columns:
            monthly['Penalty_Pct'] = monthly['Penalty'] / (monthly['EMI'] + monthly['Penalty']) * 100
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(monthly.index, monthly['Penalty_Pct'], color=RED, lw=2)
            ax.fill_between(monthly.index, monthly['Penalty_Pct'], alpha=0.15, color=RED)
            ax.set_title('Penalty Payments as % of Total Transactions (Task 20)')
            ax.set_xlabel('Month')
            ax.set_ylabel('Penalty %')
            ax.tick_params(axis='x', rotation=30)
            _save('task20_monthly_penalty_pct.png')

    # Overdue vs non-overdue
    if amt_col and 'LOAN_ID' in tx.columns and 'OVERDUE_AMOUNT' in df.columns:
        overdue_ids = set(df[df['OVERDUE_AMOUNT'] > 0]['LOAN_ID'].dropna())
        tx['IS_OVERDUE'] = tx['LOAN_ID'].isin(overdue_ids).map(
            {True: 'Overdue', False: 'Non-Overdue'}
        )
        fig, ax = plt.subplots(figsize=(7, 5))
        overdue_comp = tx.groupby('IS_OVERDUE')[amt_col].mean()
        colors = [RED, BLUE]
        bars = ax.bar(overdue_comp.index, overdue_comp.values,
                      color=colors, edgecolor='white', width=0.4)
        for bar, val in zip(bars, overdue_comp.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                    f'₹{val:,.0f}', ha='center', fontweight='bold')
        ax.set_title('Avg Transaction Amount: Overdue vs Non-Overdue Loans')
        ax.set_ylabel('Avg Amount (₹)')
        _save('task20_overdue_vs_nonoverdue_transactions.png')


# ─────────────────────────────────────────────────────────────────────────────
# Master plot_all — called once from main.py
# ─────────────────────────────────────────────────────────────────────────────

def plot_all(df, data=None):
    """
    Generate all plots for all 20 tasks.

    Parameters
    ----------
    df   : master merged DataFrame
    data : raw data dict (for transactions, applications, defaults, branches)
    """
    print("\n" + "="*55)
    print(" Generating all visualizations...")
    print("="*55)

    applications = data.get('applications') if data else None
    transactions = data.get('transactions') if data else None
    defaults     = data.get('defaults')     if data else None
    branches     = data.get('branches')     if data else None

    plot_descriptive(df, applications=applications)
    plot_default_risk(df)
    plot_statistical_analysis(df, defaults=defaults)
    plot_branch_performance(df, branches=branches)
    plot_customer_segments(df)
    plot_transaction_recovery(df, transactions, defaults)
    plot_emi_analysis(df)
    plot_application_analysis(df, applications=applications)
    plot_profitability(df)
    plot_default_trends(df, defaults=defaults)
    plot_time_series(df, applications=applications)
    plot_time_to_default(df, defaults=defaults)
    if transactions is not None:
        plot_transaction_patterns(df, transactions)

    print(f"\n✅ All plots saved to: {FIGURE_PATH}")
