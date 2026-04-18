"""
Branch Performance Analysis
Evaluates delinquency rates, loan volumes, and approval patterns
across Hero FinCorp's branch network.
"""
import pandas as pd


def branch_performance_analysis(branches):
    """
    Summarise branch-level performance metrics including delinquency
    rate and total loan count.
    """
    print("\n[TASK 4] Branch Performance Analysis")

    perf = {}

    if 'DELINQUENCY_RATE' in branches.columns:
        delinq = branches[['BRANCH_ID', 'DELINQUENCY_RATE']].sort_values(
            'DELINQUENCY_RATE', ascending=False
        )
        perf['top_delinquent'] = delinq.head(10)
        print("\nTop Delinquent Branches:\n", perf['top_delinquent'])

    if 'TOTAL_LOANS' in branches.columns:
        loan_vol = branches[['BRANCH_ID', 'TOTAL_LOANS']].sort_values(
            'TOTAL_LOANS', ascending=False
        )
        perf['top_volume'] = loan_vol.head(10)
        print("\nTop Branches by Loan Volume:\n", perf['top_volume'])

    return perf
