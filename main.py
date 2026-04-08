# -----------------------------------
# CORE PIPELINE
# -----------------------------------
from src.pgds.assignment.dataprocessor.data_loader import load_data
from src.pgds.assignment.dataprocessor.data_cleaning import clean_data
from src.pgds.assignment.dataprocessor.feature_engineering import create_features
from src.pgds.assignment.dataprocessor.merge_data import merge_all

# -----------------------------------
# ANALYSIS MODULES
# -----------------------------------
from src.pgds.assignment.analyser.descriptive_analysis import descriptive_analysis
from src.pgds.assignment.analyser.default_analysis import default_risk_analysis
from src.pgds.assignment.analyser.branch_analysis import branch_performance
from src.pgds.assignment.analyser.customer_analysis import customer_segmentation
from src.pgds.assignment.analyser.statistical_analysis import advanced_statistical_analysis
from src.pgds.assignment.analyser.transaction_analysis import transaction_and_recovery_analysis
from src.pgds.assignment.analyser.emi_analysis import emi_analysis
from src.pgds.assignment.analyser.application_analysis import application_insights
from src.pgds.assignment.analyser.recovery_analysis import recovery_effectiveness
from src.pgds.assignment.analyser.disbursement_analysis import disbursement_efficiency
from src.pgds.assignment.analyser.profitability_analysis import profitability_analysis
from src.pgds.assignment.analyser.geospatial_analysis import geospatial_analysis
from src.pgds.assignment.analyser.default_trends import default_trends_analysis
from src.pgds.assignment.analyser.time_series_analysis import time_series_analysis
from src.pgds.assignment.analyser.customer_behavior import customer_behavior_analysis
from src.pgds.assignment.analyser.risk_analysis import risk_assessment
from src.pgds.assignment.analyser.time_to_default import time_to_default_analysis
from src.pgds.assignment.analyser.transaction_pattern import transaction_pattern_analysis
from src.pgds.assignment.analyser.branch_efficiency import branch_efficiency_analysis

# -----------------------------------
# VISUALIZATION MODULES
# -----------------------------------
from src.pgds.assignment.visualizer.plots import (
    plot_descriptive,
    plot_default_risk,
    plot_branch_performance,
    plot_customer_segments,
    plot_statistical_analysis,
    plot_transaction_recovery,
    plot_emi_analysis,
    plot_application_insights,
    plot_recovery_analysis,
    plot_disbursement_efficiency,
    plot_profitability,
    plot_geospatial,
    plot_default_trends,
    plot_time_series,
    plot_customer_behavior,
    plot_risk_analysis,
    plot_time_to_default,
    plot_transaction_patterns,
    plot_branch_efficiency
)

# -----------------------------------
# REPORT
# -----------------------------------
from src.pgds.assignment.reporting.report_generator import generate_full_report


def main():

    print("\n🚀 STARTING FULL DATA ANALYSIS PIPELINE\n")

    # -----------------------------------
    # LOAD + CLEAN + FEATURE ENGINEERING
    # -----------------------------------
    data = load_data()
    data = clean_data(data)
    data = create_features(data)

    print("Loans columns:==================", data['loans'].columns)
    print("Applications columns:===============", data['applications'].columns)

    df = merge_all(data)

    # -----------------------------------
    # ANALYSIS
    # -----------------------------------

    descriptive_analysis(df, data['applications'])

    default_risk_analysis(df, data['branches'])

    branch_performance(df, data['applications'], data['defaults'])

    customer_segmentation(df)

    advanced_statistical_analysis(df, data['branches'], data['defaults'])

    transaction_and_recovery_analysis(
        df,
        data['transactions'],
        data['defaults'],
        data['branches']
    )

    emi_analysis(df)

    application_insights(data['applications'])

    recovery_effectiveness(df, data['defaults'], data['branches'])

    disbursement_efficiency(
        data['applications'],
        data['loans'],
        data['branches']
    )

    profitability_analysis(df, data['branches'])

    geospatial_analysis(df, data['branches'])

    default_trends_analysis(df, data['defaults'])

    time_series_analysis(
        df,
        data['loans'],
        data['applications'],
        data['defaults'],
        data['branches']
    )

    customer_behavior_analysis(df, data['applications'])

    risk_assessment(df, data['defaults'])

    time_to_default_analysis(
        df,
        data['loans'],
        data['defaults']
    )

    transaction_pattern_analysis(
        df,
        data['transactions']
    )

    branch_efficiency_analysis(
        data['applications'],
        data['loans'],
        data['branches']
    )

    # -----------------------------------
    # VISUALIZATIONS
    # -----------------------------------

    plot_descriptive(df, data['applications'])
    plot_default_risk(df)
    plot_branch_performance(df)
    plot_customer_segments(df)
    plot_statistical_analysis(df, data['defaults'])
    plot_transaction_recovery(df, data['transactions'], data['defaults'])
    plot_emi_analysis(df)
    plot_application_insights(data['applications'])
    plot_recovery_analysis(data['defaults'], df, data['branches'])
    plot_disbursement_efficiency(
        data['applications'],
        data['loans'],
        data['branches']
    )
    plot_profitability(df, data['branches'])
    plot_geospatial(df, data['branches'])
    plot_default_trends(df, data['defaults'])
    plot_time_series(
        data['loans'],
        data['applications'],
        data['defaults'],
        df,
        data['branches']
    )
    plot_customer_behavior(df)
    plot_risk_analysis(df, data['defaults'])
    plot_time_to_default(data['loans'], data['defaults'])
    plot_transaction_patterns(data['transactions'], df)
    plot_branch_efficiency(data['applications'], data['loans'])

    # -----------------------------------
    # FINAL REPORT
    # -----------------------------------
    generate_full_report(df)

    print("\n✅ ALL TASKS COMPLETED SUCCESSFULLY\n")
    print("📊 Check reports/figures/ for charts")
    print("📄 Check reports/hero_fincorp_analysis.docx for report")


if __name__ == "__main__":
    main()