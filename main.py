# -----------------------------------
# CORE PIPELINE
# -----------------------------------
from src.pgds.assignment.dataprocessor.data_loader import load_data
from src.pgds.assignment.dataprocessor.data_loader import load_cleaned_data
from src.pgds.assignment.dataprocessor.data_cleaning import clean_data
from src.pgds.assignment.dataprocessor.feature_engineering import create_features
from src.pgds.assignment.dataprocessor.merge_data import merge_all

# -----------------------------------
# ANALYSIS MODULES
# -----------------------------------
from src.pgds.assignment.analyser.descriptive_analysis import descriptive_analysis
from src.pgds.assignment.analyser.default_risk_analysis import default_risk_analysis
from src.pgds.assignment.analyser.branch_analysis import branch_performance_analysis
from src.pgds.assignment.analyser.customer_analysis import customer_segmentation
from src.pgds.assignment.analyser.statistical_analysis import advanced_statistical_analysis
from src.pgds.assignment.analyser.transaction_analysis import transaction_recovery_analysis
from src.pgds.assignment.analyser.loan_application_analysis import loan_application_analysis

from src.pgds.assignment.analyser.emi_analysis import emi_analysis
from src.pgds.assignment.analyser.disbursement_analysis import disbursement_efficiency
from src.pgds.assignment.analyser.profitability_analysis import profitability_analysis
from src.pgds.assignment.analyser.geospatial_analysis import geospatial_analysis
from src.pgds.assignment.analyser.default_trend_analysis import default_trend_analysis
from src.pgds.assignment.analyser.time_series_analysis import time_series_analysis
from src.pgds.assignment.analyser.customer_behavior import customer_behavior_analysis
from src.pgds.assignment.analyser.risk_analysis import risk_analysis
from src.pgds.assignment.analyser.time_to_default_analysis import time_to_default_analysis
from src.pgds.assignment.analyser.transaction_pattern_analysis import transaction_pattern_analysis

# -----------------------------------
# VISUALIZATION MODULES
# -----------------------------------
from src.pgds.assignment.visualizer.plots import (
    plot_descriptive,
    plot_branch_performance,
    plot_customer_segmentation,
    plot_advanced_analysis,
    plot_transaction_recovery,
    plot_emi_analysis,
    plot_application_analysis,
    plot_disbursement_efficiency,
    plot_profitability,
    plot_geospatial,
    plot_default_trends,
    plot_time_series,
    plot_customer_behavior,
    plot_risk,
    plot_time_to_default,
    plot_transaction_pattern,
     plot_default_risk

)

# -----------------------------------
# REPORT
# -----------------------------------
from src.pgds.assignment.reporting.report_generator import generate_full_report


def main():

    print("STARTING FULL DATA ANALYSIS PIPELINE")

    # -----------------------------------
    # TASK 1.   Data Quality and Preparation (LOAD + CLEAN + FEATURE ENGINEERING)
    # -----------------------------------
    data = load_data() #Load raw data set from the data/raw folder
    data = clean_data(data) # clean the data set
    # Load cleaned data
    data = load_cleaned_data()
    data = create_features(data)

    df = merge_all(data)


    # # -----------------------------------
    # # Task 2 :  Descriptive Analysis
    # # -----------------------------------
    print(" Task 2 :  Descriptive Analysis")
    descriptive_analysis(df, data['applications'])
    plot_descriptive(df, data['applications'])

    # # -----------------------------------
    # # Task 3 :  Default Risk Analysis
    # # -----------------------------------
    default_risk_analysis(df, data['branches'])
    plot_default_risk(df, data['branches'])
    # # -----------------------------------
    # # Task 4 :  Branch and Regional Performance
    # # -----------------------------------
    print(" Task 4 :  Branch and Regional Performance")
    branch_performance_analysis(data['branches'])
    plot_branch_performance(data['branches'])

    # # -----------------------------------
    # # Task 5 :  Customer Segmentation
    # # -----------------------------------
    print(" Task 5 :  Customer Segmentation")
    customer_segmentation(df)
    plot_customer_segmentation(df)

    # # -----------------------------------
    # # Task 6 :   Advanced Statistical Analysis
    # # -----------------------------------
    print("Task 6 :   Advanced Statistical Analysis")
    advanced_statistical_analysis(df, data['branches'])
    plot_advanced_analysis(df, data['branches'])

    # # -----------------------------------
    # # Task 7 :   Transaction and Recovery Analysis
    # # -----------------------------------
    print("Task 7 :   Transaction and Recovery Analysis")
    transaction_recovery_analysis(df, data['transactions'])
    plot_transaction_recovery(df, data['transactions'])

    # # -----------------------------------
    # # Task 8 :    EMI Analysis
    # # -----------------------------------
    print("Task 8 :    EMI Analysis")
    emi_analysis(df)
    plot_emi_analysis(df)
    # print(df.columns)

    # # -----------------------------------
    # # Task 9 :    Loan Application Insights
    # # -----------------------------------
    print("Task 9 :    Loan Application Insights")
    loan_application_analysis(data['applications'])
    plot_application_analysis(data['applications'])

    # # -----------------------------------
    # # Task 10 :    Recovery Effectiveness
    # # -----------------------------------
    print("Task 10 :    Recovery Effectiveness")
    print("TODO")

    # # -----------------------------------
    # # Task 11 :     Loan Disbursement Efficiency
    # # -----------------------------------
    print("Task 11 : Loan Disbursement Efficiency ")

    disbursement_efficiency(df)
    plot_disbursement_efficiency(df)

    # # -----------------------------------
    # # Task 12 :     Profitability Analysis
    # # -----------------------------------
    print("Task 12 :     Profitability Analysis ")
    profitability_analysis(df)
    plot_profitability(df)
    # print(df.columns)

    # # -----------------------------------
    # # Task 13 :     Geospatial Analysis
    # # -----------------------------------
    print("Task 13 :     Geospatial Analysis ")
    geospatial_analysis(df)
    plot_geospatial(df)
    # print(df.columns)

    # # -----------------------------------
    # # Task 14 :      Default Trends
    # # -----------------------------------
    print("Task 14 :      Default Trends  ")
    default_trend_analysis(df)
    plot_default_trends(df)
    # print(df.columns)

    # # -----------------------------------
    # # Task 15 :      Default Trends
    # # -----------------------------------
    print("""Task 15 is NOT DOABLE due to missing linkage between branch and loan/application data
    loans.csv :  no BRANCH_ID
    applications.csv :  no BRANCH_ID
     TASK FEASIBILITY
     1. Avg Disbursement Time per Branch Required: BRANCH_ID APPLICATION_DATE + DISBURSAL_DATE : NOT DOABLE

     2. Rejected Applications per Branch Required:BRANCH_ID ,APPROVAL_STATUS :NOT DOABLE

     3. Customer Satisfaction per Branch Required:BRANCH_ID ,Satisfaction column :NOT DOABLE
    """)


    # # -----------------------------------
    # # Task 16 :       Time-Series Analysis
    # # -----------------------------------
    print("Task 16 :      Time-Series Analysis   ")
    time_series_analysis(df)
    plot_time_series(df)
    # print(df.columns)

    # # -----------------------------------
    # # Task 17 :        Customer Behavior Analysis
    # # -----------------------------------
    print("Task 17 :      Customer Behavior Analysis   ")
    customer_behavior_analysis(
        df,
        data['applications'],
        data['customers']
    )

    plot_customer_behavior(
        df,
        data['applications'],
        data['customers']
    )
    # print(df.columns)

    # # -----------------------------------
    # # Task 18 :         Risk Assessment
    # # -----------------------------------
    print("Task 18 :       Risk Assessment   ")
    risk_analysis(df)
    plot_risk(df)
    # print(df.columns)

    # # -----------------------------------
    # # Task 19 :          Time to Default Analysis
    # # -----------------------------------
    print("Task 19 :        Time to Default Analysis   ")
    time_to_default_analysis(df)
    plot_time_to_default(df)
    # print(df.columns)

    # # -----------------------------------
    # # Task 20 :          Transaction Pattern Analysis
    # # -----------------------------------
    print("Task 20 :          Transaction Pattern Analysis")
    transaction_pattern_analysis(df, data['transactions'])
    plot_transaction_pattern(data['transactions'], df)
    # print(df.columns)
    # -----------------------------------
    # FINAL REPORT
    # -----------------------------------
    # generate_full_report(df)

    print("\n ALL TASKS COMPLETED SUCCESSFULLY\n")
    print(" Check reports/figures/ for charts")
    print(" Check reports/hero_fincorp_analysis.docx for report")
    print("\n All merge column names shown below")
    print(df.columns)

if __name__ == "__main__":
    main()