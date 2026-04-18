"""
Application Insights
Analyses loan application approval rates, rejection drivers,
and fee structures across the application pipeline.
"""
import pandas as pd


def loan_application_analysis(applications):
    """
    Break down approval vs rejection rates, processing fee comparison,
    and reasons for rejection.
    """
    print("\n[TASK 9] Loan Application Insights")

    insights = {}

    # --------------------------------------------------
    # 1. APPROVAL vs REJECTION
    # --------------------------------------------------
    if 'APPROVAL_STATUS' in applications.columns:
        status_counts = applications['APPROVAL_STATUS'].value_counts()
        insights['status_counts'] = status_counts
        print("\nApplication Status Counts:\n", status_counts)

    # --------------------------------------------------
    # 2. REJECTION REASONS
    # --------------------------------------------------
    if 'REJECTION_REASON' in applications.columns:
        rejection_breakdown = applications[
            applications['APPROVAL_STATUS'].str.upper() == 'REJECTED'
        ]['REJECTION_REASON'].value_counts()

        insights['rejection_reasons'] = rejection_breakdown
        print("\nRejection Reason Breakdown:\n", rejection_breakdown)

    # --------------------------------------------------
    # 3. PROCESSING FEE BY STATUS
    # --------------------------------------------------
    if 'PROCESSING_FEE' in applications.columns and 'APPROVAL_STATUS' in applications.columns:
        fee_by_status = applications.groupby('APPROVAL_STATUS')['PROCESSING_FEE'].mean()
        insights['fee_by_status'] = fee_by_status
        print("\nAverage Processing Fee by Status:\n", fee_by_status)

    return insights
