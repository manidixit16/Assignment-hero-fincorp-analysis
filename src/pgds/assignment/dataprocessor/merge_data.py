
# def merge_all(data):
#     df = data['applications'].copy()
#
#     df = df.merge(data['loans'], on='LOAN_ID', how='left')
#
#     df = df.merge(data['customers'], on='CUSTOMER_ID', how='left')
#
#     df = df.merge(data['branches'], on='BRANCH_ID', how='left')
#
#     return df
    # df = data['loans'].merge(data['customers'], on='CUSTOMER_ID', how='left')
    # if 'BRANCH_ID' in data['loans'].columns:
    #     df = df.merge(data['branches'], on='BRANCH_ID', how='left')
    # return df
def merge_all(data):

    applications = data['applications']
    loans = data['loans']
    customers = data['customers']
    defaults = data['defaults']
    transactions = data['transactions']


    # -----------------------------------
    # BASE: APPLICATIONS
    # -----------------------------------
    df = applications.copy()

    # -----------------------------------
    # MERGE LOANS
    # -----------------------------------
    df = df.merge(loans, on=['LOAN_ID', 'CUSTOMER_ID'], how='left')

    # -----------------------------------
    # MERGE CUSTOMERS
    # -----------------------------------
    df = df.merge(customers, on='CUSTOMER_ID', how='left')

    # -----------------------------------
    # MERGE DEFAULTS
    # -----------------------------------
    df = df.merge(defaults, on=['LOAN_ID', 'CUSTOMER_ID'], how='left')
    # -----------------------------------
    # MERGE TRANSACTIONS (AGGREGATED)
    # -----------------------------------
    # txn_agg = transactions.groupby('LOAN_ID').agg({
    #     'TRANSACTION_AMOUNT': 'sum',
    #     'PENALTY_AMOUNT': 'sum'
    # }).reset_index()

    # txn_agg.columns = ['LOAN_ID', 'TOTAL_TRANSACTION_AMOUNT', 'TOTAL_PENALTY']
    txn_agg = transactions.groupby('LOAN_ID').size().reset_index(name='TOTAL_TRANSACTIONS')

    df = df.merge(txn_agg, on='LOAN_ID', how='left')

    # df = df.merge(txn_agg, on='LOAN_ID', how='left')

    # -----------------------------------
    # CREATE DERIVED FEATURES
    # -----------------------------------
    if 'LOAN_AMOUNT' in df.columns and 'INTEREST_RATE' in df.columns:
        df['INTEREST_INCOME'] = (
            df['LOAN_AMOUNT'] *
            (df['INTEREST_RATE'] / 100) *
            (df['LOAN_TERM'] / 12)
        )

    return df