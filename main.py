"""
Hero FinCorp: Comprehensive Data-Driven Analysis
================================================
Entry point — runs all 20 analysis tasks end-to-end.

Usage
-----
    python main.py

Output
------
    reports/figures/   → PNG charts for every task
    reports/hero_fincorp_analysis.docx  → full Word report
"""

import os
import warnings
warnings.filterwarnings('ignore')

# ── Data pipeline ──────────────────────────────────────────────────────────
from src.pgds.assignment.dataprocessor.data_loader       import load_data
from src.pgds.assignment.dataprocessor.data_cleaning     import clean_data
from src.pgds.assignment.dataprocessor.feature_engineering import create_features
from src.pgds.assignment.dataprocessor.merge_data        import merge_all

# ── Analysers (Tasks 2–20) ─────────────────────────────────────────────────
from src.pgds.assignment.analyser.descriptive_analysis   import descriptive_analysis
from src.pgds.assignment.analyser.default_analysis       import default_risk_analysis
from src.pgds.assignment.analyser.branch_analysis        import branch_performance
from src.pgds.assignment.analyser.customer_analysis      import customer_segmentation
from src.pgds.assignment.analyser.statistical_analysis   import advanced_statistical_analysis
from src.pgds.assignment.analyser.transaction_analysis   import transaction_and_recovery_analysis
from src.pgds.assignment.analyser.emi_analysis           import emi_analysis
from src.pgds.assignment.analyser.application_analysis   import application_analysis
from src.pgds.assignment.analyser.recovery_analysis      import recovery_effectiveness
from src.pgds.assignment.analyser.disbursement_analysis  import disbursement_efficiency
from src.pgds.assignment.analyser.profitability_analysis import profitability
from src.pgds.assignment.analyser.geospatial_analysis    import geo_analysis
from src.pgds.assignment.analyser.default_trends         import default_trends
from src.pgds.assignment.analyser.branch_efficiency      import branch_efficiency
from src.pgds.assignment.analyser.time_series_analysis   import time_series
from src.pgds.assignment.analyser.customer_behavior      import customer_behavior
from src.pgds.assignment.analyser.risk_analysis          import risk_matrix
from src.pgds.assignment.analyser.time_to_default        import time_to_default
from src.pgds.assignment.analyser.transaction_pattern    import transaction_pattern

# ── Visualiser ─────────────────────────────────────────────────────────────
from src.pgds.assignment.visualizer.plots import (
    plot_all,
    plot_descriptive,
    plot_default_risk,
    plot_statistical_analysis,
    plot_branch_performance,
    plot_customer_segments,
    plot_transaction_recovery,
    plot_emi_analysis,
    plot_application_analysis,
    plot_profitability,
    plot_default_trends,
    plot_time_series,
    plot_time_to_default,
    plot_transaction_patterns,
)

# ── Report generator ───────────────────────────────────────────────────────
from src.pgds.assignment.reporting.report_generator import generate_full_report


def main():
    print("\n" + "="*60)
    print("  HERO FINCORP — COMPREHENSIVE DATA-DRIVEN ANALYSIS")
    print("="*60)

    # ──────────────────────────────────────────────────────────────
    # STEP 1 — Load raw data
    # ──────────────────────────────────────────────────────────────
    print("\n[STEP 1] Loading datasets...")
    data = load_data()

    # ──────────────────────────────────────────────────────────────
    # TASK 1 — Data Quality & Preparation
    # ──────────────────────────────────────────────────────────────
    print("\n[TASK 1] Data Quality & Preparation")
    data = clean_data(data)

    # ──────────────────────────────────────────────────────────────
    # Feature Engineering
    # ──────────────────────────────────────────────────────────────
    data = create_features(data)

    # ──────────────────────────────────────────────────────────────
    # Master merge
    # ──────────────────────────────────────────────────────────────
    df = merge_all(data)

    # Shortcuts to raw tables
    applications = data['applications']
    transactions = data['transactions']
    defaults     = data['defaults']
    branches     = data['branches']

    # ──────────────────────────────────────────────────────────────
    # TASK 2 — Descriptive Analysis
    # ──────────────────────────────────────────────────────────────
    t2 = descriptive_analysis(df, applications=applications)
    plot_descriptive(df, applications=applications)

    # ──────────────────────────────────────────────────────────────
    # TASK 3 — Default Risk Analysis
    # ──────────────────────────────────────────────────────────────
    t3 = default_risk_analysis(df, branches=branches)
    plot_default_risk(df)

    # ──────────────────────────────────────────────────────────────
    # TASK 4 — Branch & Regional Performance
    # ──────────────────────────────────────────────────────────────
    t4 = branch_performance(df, applications=applications,
                            defaults=defaults, branches=branches)
    plot_branch_performance(df, branches=branches)

    # ──────────────────────────────────────────────────────────────
    # TASK 5 — Customer Segmentation
    # ──────────────────────────────────────────────────────────────
    t5 = customer_segmentation(df)
    plot_customer_segments(t5['df'])

    # ──────────────────────────────────────────────────────────────
    # TASK 6 — Advanced Statistical Analysis
    # ──────────────────────────────────────────────────────────────
    t6 = advanced_statistical_analysis(df, branches=branches, defaults=defaults)
    plot_statistical_analysis(df, defaults=defaults)

    # ──────────────────────────────────────────────────────────────
    # TASK 7 — Transaction & Recovery Analysis
    # ──────────────────────────────────────────────────────────────
    t7 = transaction_and_recovery_analysis(df, transactions, defaults, branches)
    plot_transaction_recovery(df, transactions, defaults)

    # ──────────────────────────────────────────────────────────────
    # TASK 8 — EMI Analysis
    # ──────────────────────────────────────────────────────────────
    t8 = emi_analysis(df)
    plot_emi_analysis(df)

    # ──────────────────────────────────────────────────────────────
    # TASK 9 — Loan Application Insights
    # ──────────────────────────────────────────────────────────────
    t9 = application_analysis(df, applications=applications)
    plot_application_analysis(df, applications=applications)

    # ──────────────────────────────────────────────────────────────
    # TASK 10 — Recovery Effectiveness
    # ──────────────────────────────────────────────────────────────
    t10 = recovery_effectiveness(df, defaults=defaults, branches=branches)

    # ──────────────────────────────────────────────────────────────
    # TASK 11 — Loan Disbursement Efficiency
    # ──────────────────────────────────────────────────────────────
    t11 = disbursement_efficiency(df, applications=applications)

    # ──────────────────────────────────────────────────────────────
    # TASK 12 — Profitability Analysis
    # ──────────────────────────────────────────────────────────────
    t12 = profitability(df, branches=branches)
    plot_profitability(df)

    # ──────────────────────────────────────────────────────────────
    # TASK 13 — Geospatial Analysis
    # ──────────────────────────────────────────────────────────────
    t13 = geo_analysis(df, branches=branches)

    # ──────────────────────────────────────────────────────────────
    # TASK 14 — Default Trends
    # ──────────────────────────────────────────────────────────────
    t14 = default_trends(df, defaults=defaults)
    plot_default_trends(df, defaults=defaults)

    # ──────────────────────────────────────────────────────────────
    # TASK 15 — Branch Efficiency
    # ──────────────────────────────────────────────────────────────
    t15 = branch_efficiency(df, applications=applications, branches=branches)

    # ──────────────────────────────────────────────────────────────
    # TASK 16 — Time-Series Analysis
    # ──────────────────────────────────────────────────────────────
    t16 = time_series(df, applications=applications, defaults=defaults)
    plot_time_series(df, applications=applications)

    # ──────────────────────────────────────────────────────────────
    # TASK 17 — Customer Behavior Analysis
    # ──────────────────────────────────────────────────────────────
    t17 = customer_behavior(df, applications=applications, transactions=transactions)

    # ──────────────────────────────────────────────────────────────
    # TASK 18 — Risk Assessment
    # ──────────────────────────────────────────────────────────────
    t18 = risk_matrix(df, defaults=defaults)

    # ──────────────────────────────────────────────────────────────
    # TASK 19 — Time to Default Analysis
    # ──────────────────────────────────────────────────────────────
    t19 = time_to_default(df, defaults=defaults)
    plot_time_to_default(df, defaults=defaults)

    # ──────────────────────────────────────────────────────────────
    # TASK 20 — Transaction Pattern Analysis
    # ──────────────────────────────────────────────────────────────
    t20 = transaction_pattern(df, transactions=transactions)
    plot_transaction_patterns(df, transactions)

    # ──────────────────────────────────────────────────────────────
    # Generate Word Report
    # ──────────────────────────────────────────────────────────────
    generate_full_report(df)

    print("\n" + "="*60)
    print("  ✅  ALL 20 TASKS COMPLETED SUCCESSFULLY")
    print("  📊  Charts  → reports/figures/")
    print("  📄  Report  → reports/hero_fincorp_analysis.docx")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
