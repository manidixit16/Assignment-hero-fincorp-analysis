"""
Hero FinCorp Credit Analytics — Main Pipeline
=============================================
Entry point for the full 20-task analysis pipeline.
Orchestrates data loading, cleaning, feature engineering,
analysis, visualisation, and report generation.

Author : Mani Dixit
Project: Hero FinCorp Credit Portfolio Analysis
"""

# ─────────────────────────────────────────────────────────────────────────────
# DATA PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
from src.pgds.assignment.dataprocessor.dataset_loader  import load_data, load_cleaned_data
from src.pgds.assignment.dataprocessor.data_sanitizer  import clean_data
from src.pgds.assignment.dataprocessor.feature_builder import create_features
from src.pgds.assignment.dataprocessor.data_merger     import merge_all

# ─────────────────────────────────────────────────────────────────────────────
# ANALYSIS MODULES
# ─────────────────────────────────────────────────────────────────────────────
from src.pgds.assignment.analyser.exploratory_summary    import exploratory_summary
from src.pgds.assignment.analyser.loan_default_scorer    import loan_default_scorer
from src.pgds.assignment.analyser.branch_performance     import branch_performance_analysis
from src.pgds.assignment.analyser.borrower_segmentation  import borrower_segmentation
from src.pgds.assignment.analyser.advanced_metrics       import advanced_statistical_analysis
from src.pgds.assignment.analyser.payment_recovery_analysis import payment_recovery_analysis
from src.pgds.assignment.analyser.application_insights   import loan_application_analysis
from src.pgds.assignment.analyser.recovery_effectiveness import recovery_effectiveness
from src.pgds.assignment.analyser.emi_risk_analysis      import emi_risk_analysis
from src.pgds.assignment.analyser.loan_disbursement      import disbursement_efficiency
from src.pgds.assignment.analyser.revenue_analysis       import profitability_analysis
from src.pgds.assignment.analyser.regional_analysis      import geospatial_analysis
from src.pgds.assignment.analyser.default_trend_tracker  import default_trend_analysis
from src.pgds.assignment.analyser.temporal_analysis      import time_series_analysis
from src.pgds.assignment.analyser.repayment_behavior     import customer_behavior_analysis
from src.pgds.assignment.analyser.credit_risk_profiler   import credit_risk_profiler
from src.pgds.assignment.analyser.default_velocity_analysis import default_velocity_analysis
from src.pgds.assignment.analyser.txn_behavior_analysis  import txn_behavior_analysis

# ─────────────────────────────────────────────────────────────────────────────
# CHART ENGINE
# ─────────────────────────────────────────────────────────────────────────────
from src.pgds.assignment.visualizer.chart_engine import (
    plot_descriptive,
    plot_default_risk,
    plot_branch_performance,
    plot_customer_segmentation,
    plot_advanced_analysis,
    plot_transaction_recovery,
    plot_emi_analysis,
    plot_application_analysis,
    plot_recovery,
    plot_disbursement_efficiency,
    plot_profitability,
    plot_geospatial,
    plot_default_trends,
    plot_time_series,
    plot_customer_behavior,
    plot_risk,
    plot_time_to_default,
    plot_transaction_pattern,
)

# ─────────────────────────────────────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────────────────────────────────────
from src.pgds.assignment.reporting.insight_reporter import generate_full_report


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  HERO FINCORP CREDIT ANALYTICS PIPELINE — STARTING")
    print("=" * 60)

    # ── TASK 1: Load, Clean & Engineer ────────────────────────────────────────
    print("\n[Task 1] Data Quality & Preparation")
    raw_data = load_data()
    raw_data = clean_data(raw_data)
    data     = load_cleaned_data()
    data     = create_features(data)
    master   = merge_all(data)

    # ── TASK 2: Exploratory Summary ───────────────────────────────────────────
    print("\n[Task 2] Exploratory Summary")
    exploratory_summary(master, data['applications'])
    plot_descriptive(master, data['applications'])

    # ── TASK 3: Loan Default Scoring ──────────────────────────────────────────
    print("\n[Task 3] Loan Default Scoring")
    loan_default_scorer(master, data['branches'])
    plot_default_risk(master, data['branches'])

    # ── TASK 4: Branch Performance ────────────────────────────────────────────
    print("\n[Task 4] Branch & Regional Performance")
    branch_performance_analysis(data['branches'])
    plot_branch_performance(data['branches'])

    # ── TASK 5: Borrower Segmentation ─────────────────────────────────────────
    print("\n[Task 5] Borrower Segmentation")
    borrower_segmentation(master)
    plot_customer_segmentation(master)

    # ── TASK 6: Advanced Statistical Metrics ──────────────────────────────────
    print("\n[Task 6] Advanced Statistical Metrics")
    advanced_statistical_analysis(master, data['branches'])
    plot_advanced_analysis(master, data['branches'])

    # ── TASK 7: Payment & Recovery Analysis ───────────────────────────────────
    print("\n[Task 7] Payment & Recovery Analysis")
    payment_recovery_analysis(master, data['transactions'])
    plot_transaction_recovery(master, data['transactions'])

    # ── TASK 8: EMI Risk Analysis ─────────────────────────────────────────────
    print("\n[Task 8] EMI Risk Analysis")
    emi_risk_analysis(master)
    plot_emi_analysis(master)

    # ── TASK 9: Application Insights ─────────────────────────────────────────
    print("\n[Task 9] Application Insights")
    loan_application_analysis(data['applications'])
    plot_application_analysis(data['applications'])

    # ── TASK 10: Recovery Effectiveness ──────────────────────────────────────
    print("\n[Task 10] Recovery Effectiveness")
    recovery_effectiveness(master)
    plot_recovery(master)

    # ── TASK 11: Loan Disbursement Efficiency ─────────────────────────────────
    print("\n[Task 11] Loan Disbursement Efficiency")
    disbursement_efficiency(master)
    plot_disbursement_efficiency(master)

    # ── TASK 12: Revenue Analysis ────────────────────────────────────────────
    print("\n[Task 12] Revenue & Profitability")
    profitability_analysis(master)
    plot_profitability(master)

    # ── TASK 13: Regional Analysis ───────────────────────────────────────────
    print("\n[Task 13] Regional (Geospatial) Analysis")
    geospatial_analysis(master)
    plot_geospatial(master)

    # ── TASK 14: Default Trend Tracker ───────────────────────────────────────
    print("\n[Task 14] Default Trend Analysis")
    default_trend_analysis(master)
    plot_default_trends(master)

    # ── TASK 15: Branch Efficiency (feasibility note) ─────────────────────────
    print("\n[Task 15] Branch Efficiency — BRANCH_ID linkage unavailable in loans/applications")
    print("         Metrics requiring BRANCH_ID cannot be computed.")
    print("         Recommendation: add BRANCH_ID to source datasets.")

    # ── TASK 16: Temporal Analysis ───────────────────────────────────────────
    print("\n[Task 16] Temporal Analysis")
    time_series_analysis(master)
    plot_time_series(master)

    # ── TASK 17: Repayment Behaviour ─────────────────────────────────────────
    print("\n[Task 17] Repayment Behaviour Analysis")
    customer_behavior_analysis(master, data['applications'], data['customers'])
    plot_customer_behavior(master, data['applications'], data['customers'])

    # ── TASK 18: Credit Risk Profiling ───────────────────────────────────────
    print("\n[Task 18] Credit Risk Profiling")
    credit_risk_profiler(master)
    plot_risk(master)

    # ── TASK 19: Default Velocity ────────────────────────────────────────────
    print("\n[Task 19] Default Velocity Analysis")
    default_velocity_analysis(master)
    plot_time_to_default(master)

    # ── TASK 20: Transaction Behaviour ───────────────────────────────────────
    print("\n[Task 20] Transaction Behaviour Analysis")
    txn_behavior_analysis(master, data['transactions'])
    plot_transaction_pattern(data['transactions'], master)

    # ── FINAL REPORT ─────────────────────────────────────────────────────────
    generate_full_report(master)

    print("\n" + "=" * 60)
    print("  ALL 20 TASKS COMPLETED")
    print("  Charts  → reports/figures/")
    print("  Report  → reports/mani_hero_fincorp_report.docx")
    print("=" * 60)
    print("\nMaster frame columns:")
    print(master.columns.tolist())


if __name__ == "__main__":
    main()
