# def branch_performance(df):
#     branch = df.groupby('Branch_ID').agg({
#         'Loan_Amount': 'sum',
#         'Default_Flag': 'mean'
#     }).rename(columns={'Default_Flag': 'Default_Rate'})
#
#     return branch.sort_values(by='Loan_Amount', ascending=False)