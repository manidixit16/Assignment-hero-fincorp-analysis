"""
Hero FinCorp Credit Analytics — Main Pipeline
=============================================
Orchestrates the full 20-task data analysis pipeline:
  data loading → sanitisation → feature engineering → analysis → charts → report
"""

# ─────────────────────────────────────────────────────────────────────────────
# CORE PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
from src.pgds.assignment.dataprocessor.dataset_loader  import load_data, load_cleaned_data
from src.pgds.assignment.dataprocessor.data_sanitizer  import clean_data
from src.pgds.assignment.dataprocessor.feature_builder import create_features
from src.pgds.assignment.dataprocessor.data_merger     import merge_all

# ─────────────────────────────────────────────────────────────────────────────
# ANALYSIS MODULES
# ─────────────────────────────────────────────────────────────────────────────
from src.pgds.assignment.analyser.exploratory_summary     import exploratory_summary
from src.pgds.assignment.analyser.loan_default_scorer     import loan_default_scorer
from src.pgds.assignment.analyser.branch_performance      import branch_performance_analysis
from src.pgds.assignment.analyser.borrower_segmentation   import borrower_segmentation
from src.pgds.assignment.analyser.advanced_metrics        import advanced_statistical_analysis
from src.pgds.assignment.analyser.payment_recovery_analysis import payment_recovery_analysis
from src.pgds.assignment.analyser.application_insights    import loan_application_analysis
from src.pgds.assignment.analyser.recovery_effectiveness  import recovery_effectiveness
from src.pgds.assignment.analyser.emi_risk_analysis       import emi_risk_analysis
from src.pgds.assignment.analyser.loan_disbursement       import disbursement_efficiency
from src.pgds.assignment.analyser.revenue_analysis        import profitability_analysis
from src.pgds.assignment.analyser.regional_analysis       import geospatial_analysis
from src.pgds.assignment.analyser.default_trend_tracker   import default_trend_analysis
from src.pgds.assignment.analyser.temporal_analysis       import time_series_analysis
from src.pgds.assignment.analyser.repayment_behavior      import customer_behavior_analysis
from src.pgds.assignment.analyser.credit_risk_profiler    import credit_risk_profiler
from src.pgds.assignment.analyser.default_velocity_analysis import default_velocity_analysis
from src.pgds.assignment.analyser.txn_behavior_analysis   import txn_behavior_analysis

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
# REPORT GENERATOR
# ─────────────────────────────────────────────────────────────────────────────
from src.pgds.assignment.reporting.insight_reporter import generate_full_report


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  HERO FINCORP CREDIT ANALYTICS — FULL PIPELINE")
    print("=" * 60)

    # ── TASK 1: Data Ingestion & Sanitisation ─────────────────────
    print("\n[TASK 1] Data Loading & Sanitisation")
    raw_data = load_data()
    raw_data = clean_data(raw_data)

    # Load the freshly cleaned CSVs and build derived features
    data = load_cleaned_data()
    data = create_features(data)

    # Build master analysis frame
    master_df = merge_all(data)

    # ── TASK 2: Exploratory Summary ───────────────────────────────
    print("\n[TASK 2] Exploratory Summary")
    exploratory_summary(master_df, data['applications'])
    plot_descriptive(master_df, data['applications'])

    # ── TASK 3: Loan Default Scoring ──────────────────────────────
    print("\n[TASK 3] Loan Default Scoring")
    loan_default_scorer(master_df, data['branches'])
    plot_default_risk(master_df, data['branches'])

    # ── TASK 4: Branch Performance ────────────────────────────────
    print("\n[TASK 4] Branch Performance")
    branch_performance_analysis(data['branches'])
    plot_branch_performance(data['branches'])

    # ── TASK 5: Borrower Segmentation ────────────────────────────
    print("\n[TASK 5] Borrower Segmentation")
    borrower_segmentation(master_df)
    plot_customer_segmentation(master_df)

    # ── TASK 6: Advanced Statistical Metrics ─────────────────────
    print("\n[TASK 6] Advanced Statistical Metrics")
    advanced_statistical_analysis(master_df, data['branches'])
    plot_advanced_analysis(master_df, data['branches'])

    # ── TASK 7: Payment & Recovery Analysis ──────────────────────
    print("\n[TASK 7] Payment & Recovery Analysis")
    payment_recovery_analysis(master_df, data['transactions'])
    plot_transaction_recovery(master_df, data['transactions'])

    # ── TASK 8: EMI Risk Analysis ─────────────────────────────────
    print("\n[TASK 8] EMI Risk Analysis")
    emi_risk_analysis(master_df)
    plot_emi_analysis(master_df)

    # ── TASK 9: Application Insights ─────────────────────────────
    print("\n[TASK 9] Application Insights")
    loan_application_analysis(data['applications'])
    plot_application_analysis(data['applications'])

    # ── TASK 10: Recovery Effectiveness ──────────────────────────
    print("\n[TASK 10] Recovery Effectiveness")
    recovery_effectiveness(master_df)
    plot_recovery(master_df)

    # ── TASK 11: Loan Disbursement Efficiency ─────────────────────
    print("\n[TASK 11] Loan Disbursement Efficiency")
    disbursement_efficiency(master_df)
    plot_disbursement_efficiency(master_df)

    # ── TASK 12: Revenue & Profitability ─────────────────────────
    print("\n[TASK 12] Revenue & Profitability")
    profitability_analysis(master_df)
    plot_profitability(master_df)

    # ── TASK 13: Regional Analysis ────────────────────────────────
    print("\n[TASK 13] Regional Analysis")
    geospatial_analysis(master_df)
    plot_geospatial(master_df)

    # ── TASK 14: Default Trend Tracker ────────────────────────────
    print("\n[TASK 14] Default Trend Tracker")
    default_trend_analysis(master_df)
    plot_default_trends(master_df)

    # ── TASK 15: Branch Linkage (NOT FEASIBLE) ────────────────────
    print("\n[TASK 15] Branch-Level Efficiency — SKIPPED")
    print("""
  Reason: No BRANCH_ID in loans.csv or applications.csv.
  The following sub-tasks cannot be completed without this linkage:
    • Avg disbursement time per branch  (needs BRANCH_ID + DISBURSAL_DATE)
    • Rejected applications per branch  (needs BRANCH_ID + APPROVAL_STATUS)
    • Customer satisfaction per branch  (needs BRANCH_ID + satisfaction column)
  Recommendation: Add BRANCH_ID to loan and application datasets.
    """)

    # ── TASK 16: Temporal Analysis ────────────────────────────────
    print("\n[TASK 16] Temporal (Time-Series) Analysis")
    time_series_analysis(master_df)
    plot_time_series(master_df)

    # ── TASK 17: Repayment Behaviour ─────────────────────────────
    print("\n[TASK 17] Repayment Behaviour Analysis")
    customer_behavior_analysis(master_df, data['applications'], data['customers'])
    plot_customer_behavior(master_df, data['applications'], data['customers'])

    # ── TASK 18: Credit Risk Profiler ────────────────────────────
    print("\n[TASK 18] Credit Risk Profiler")
    credit_risk_profiler(master_df)
    plot_risk(master_df)

    # ── TASK 19: Default Velocity Analysis ───────────────────────
    print("\n[TASK 19] Default Velocity Analysis")
    default_velocity_analysis(master_df)
    plot_time_to_default(master_df)

    # ── TASK 20: Transaction Behaviour Analysis ───────────────────
    print("\n[TASK 20] Transaction Behaviour Analysis")
    txn_behavior_analysis(master_df, data['transactions'])
    plot_transaction_pattern(data['transactions'], master_df)

    # ── FINAL REPORT ─────────────────────────────────────────────
    # generate_full_report(master_df)   # uncomment to build .docx

    print("\n" + "=" * 60)
    print("  ALL TASKS COMPLETED SUCCESSFULLY")
    print("  Charts  →  reports/figures/")
    print("  Report  →  reports/hero_fincorp_analysis.docx")
    print("=" * 60)
    print("\nMaster DataFrame columns:\n", list(master_df.columns))


if __name__ == "__main__":
    main()
