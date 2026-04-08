
from src.pgds.assignment.dataprocessor.data_loader import load_data
from src.pgds.assignment.dataprocessor.data_cleaning import clean_data
from src.pgds.assignment.dataprocessor.feature_engineering import create_features
from src.pgds.assignment.dataprocessor.merge_data import merge_all

from src.pgds.assignment.analyser.descriptive_analysis import descriptive_analysis

# from src.pgds.assignment.analyser.branch_analysis import branch_analysis
# from src.pgds.assignment.analyser.customer_analysis import customer_segmentation
# from src.pgds.assignment.analyser.statistical_analysis import correlation_analysis
# from src.pgds.assignment.analyser.transaction_analysis import transaction_analysis
# from src.pgds.assignment.analyser.emi_analysis import emi_analysis
# from src.pgds.assignment.analyser.application_analysis import application_analysis
# from src.pgds.assignment.analyser.recovery_analysis import recovery_effectiveness
# from src.pgds.assignment.analyser.disbursement_analysis import processing_time
# from src.pgds.assignment.analyser.profitability_analysis import profitability
# from src.pgds.assignment.analyser.geospatial_analysis import geo_analysis
# from src.pgds.assignment.analyser.default_trends import default_trends
# from src.pgds.assignment.analyser.time_series_analysis import time_series
# from src.pgds.assignment.analyser.customer_behavior import customer_behavior
# from src.pgds.assignment.analyser.risk_analysis import risk_matrix
#
# from src.pgds.assignment.analyser.transaction_pattern import transaction_pattern

from src.pgds.assignment.visualizer.plots import plot_all
from src.pgds.assignment.reporting.report_generator import generate_full_report
from src.pgds.assignment.analyser.default_analysis import default_risk_analysis
from src.pgds.assignment.visualizer.plots import plot_default_risk
from src.pgds.assignment.analyser.branch_analysis import branch_performance
from src.pgds.assignment.visualizer.plots import plot_branch_performance
from src.pgds.assignment.analyser.customer_analysis import customer_segmentation
from src.pgds.assignment.visualizer.plots import plot_customer_segments

from src.pgds.assignment.analyser.statistical_analysis import advanced_statistical_analysis
from src.pgds.assignment.visualizer.plots import plot_statistical_analysis
from src.pgds.assignment.analyser.transaction_analysis import transaction_and_recovery_analysis
from src.pgds.assignment.visualizer.plots import plot_transaction_recovery

from src.pgds.assignment.analyser.emi_analysis import emi_analysis
from src.pgds.assignment.visualizer.plots import plot_emi_analysis
from src.pgds.assignment.analyser.recovery_analysis import recovery_effectiveness
from src.pgds.assignment.visualizer.plots import plot_recovery_analysis

from src.pgds.assignment.analyser.application_analysis import application_insights
from src.pgds.assignment.visualizer.plots import plot_application_insights
from src.pgds.assignment.analyser.disbursement_analysis import disbursement_efficiency
from src.pgds.assignment.visualizer.plots import plot_disbursement_efficiency

from src.pgds.assignment.analyser.profitability_analysis import profitability_analysis
from src.pgds.assignment.visualizer.plots import plot_profitability

from src.pgds.assignment.analyser.geospatial_analysis import geospatial_analysis
from src.pgds.assignment.visualizer.plots import plot_geospatial

from src.pgds.assignment.analyser.default_trends import default_trends_analysis
from src.pgds.assignment.visualizer.plots import plot_default_trends

from src.pgds.assignment.analyser.branch_efficiency import branch_efficiency_analysis
from src.pgds.assignment.visualizer.plots import plot_branch_efficiency

from src.pgds.assignment.analyser.time_series_analysis import time_series_analysis
from src.pgds.assignment.visualizer.plots import plot_time_series

from src.pgds.assignment.analyser.customer_behavior import customer_behavior_analysis
from src.pgds.assignment.visualizer.plots import plot_customer_behavior

from src.pgds.assignment.analyser.risk_analysis import risk_assessment
from src.pgds.assignment.visualizer.plots import plot_risk_analysis

from src.pgds.assignment.analyser.time_to_default import time_to_default_analysis
from src.pgds.assignment.visualizer.plots import plot_time_to_default

from src.pgds.assignment.analyser.transaction_pattern import transaction_pattern_analysis
from src.pgds.assignment.visualizer.plots import plot_transaction_patterns

def main():
    data = load_data()
    data = clean_data(data)
    data = create_features(data)

    df = merge_all(data)

    descriptive_analysis(df)
    default_risk_analysis(df)
    branch_analysis(df)
    customer_segmentation(df)
    correlation_analysis(df)
    profitability(df)

    # DEFAULT RISK
    default_results = default_risk_analysis(df, data['branches'])

    # HEATMAP
    plot_default_risk(df)

#4
    # BRANCH PERFORMANCE
    branch_results = branch_performance(
        df,
        applications=data['applications'],
        defaults=data['defaults']
    )

    # VISUALS
    plot_branch_performance(df)

    # CUSTOMER SEGMENTATION
    customer_results = customer_segmentation(df)

    # VISUALS
    plot_customer_segments(customer_results['df'])

    # ADVANCED STATISTICS
    stats = advanced_statistical_analysis(
        df,
        branches=data['branches'],
        defaults=data['defaults']
    )

    # VISUALS
    plot_statistical_analysis(df, data['defaults'])

    # TRANSACTION & RECOVERY
    trans_results = transaction_and_recovery_analysis(
        df,
        data['transactions'],
        data['defaults'],
        data['branches']
    )

    # VISUALS
    plot_transaction_recovery(
        df,
        data['transactions'],
        data['defaults']
    )
    # EMI ANALYSIS
    emi_results = emi_analysis(df)

    # VISUALS
    plot_emi_analysis(df)

    # APPLICATION INSIGHTS
    app_results = application_insights(data['applications'])

    # VISUALS
    plot_application_insights(data['applications'])

    # RECOVERY ANALYSIS
    recovery_results = recovery_effectiveness(
        df,
        data['defaults'],
        data['branches']
    )

    # VISUALS
    plot_recovery_analysis(
        data['defaults'],
        df,
        data['branches']
    )

    # DISBURSEMENT ANALYSIS
    disbursement_results = disbursement_efficiency(
        data['applications'],
        data['loans'],
        data['branches']
    )

    # VISUALS
    plot_disbursement_efficiency(
        data['applications'],
        data['loans'],
        data['branches']
    )

    # 12 PROFITABILITY ANALYSIS
    profit_results = profitability_analysis(
        df,
        branches=data['branches']
    )

    # VISUALS
    plot_profitability(df, data['branches'])

    # 13 GEOSPATIAL ANALYSIS
    geo_results = geospatial_analysis(
        df,
        data['branches']
    )

    # VISUALS
    plot_geospatial(df, data['branches'])

    # 14 DEFAULT TRENDS
    trend_results = default_trends_analysis(
        df,
        data['defaults']
    )

    # VISUALS
    plot_default_trends(df, data['defaults'])

    # 15 BRANCH EFFICIENCY
    eff_results = branch_efficiency_analysis(
        data['applications'],
        data['loans'],
        data['branches']
    )

    # VISUALS
    plot_branch_efficiency(
        data['applications'],
        data['loans']
    )

    # 16 TIME SERIES ANALYSIS
    ts_results = time_series_analysis(
        df,
        data['loans'],
        data['applications'],
        data['defaults'],
        data['branches']
    )

    # VISUALS
    plot_time_series(
        data['loans'],
        data['applications'],
        data['defaults'],
        df,
        data['branches']
    )

    # 17 CUSTOMER BEHAVIOR
    behavior_results = customer_behavior_analysis(
        df,
        data['applications']
    )

    # VISUALS
    plot_customer_behavior(df)

    # 18 RISK ASSESSMENT
    risk_results = risk_assessment(
        df,
        data['defaults']
    )

    # VISUALS
    plot_risk_analysis(
        df,
        data['defaults']
    )

    # 19 TIME TO DEFAULT
    ttd_results = time_to_default_analysis(
        df,
        data['loans'],
        data['defaults']
    )

    # VISUALS
    plot_time_to_default(
        data['loans'],
        data['defaults']
    )
    # 20 TRANSACTION PATTERN ANALYSIS
    txn_results = transaction_pattern_analysis(
        df,
        data['transactions']
    )

    # VISUALS
    plot_transaction_patterns(
        data['transactions'],
        df
    )
#---
    # plot_all(df)
    # generate_full_report(df)
    #
    # print("ALL TASKS COMPLETED")

if __name__ == "__main__":
    main()
