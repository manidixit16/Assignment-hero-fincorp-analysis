import pandas as pd

def loadAllData():
        return {
            "applications": pd.read_csv("data/raw/applications.csv", low_memory=False),
            "customers": pd.read_csv("data/raw/customers.csv"),
            "loans": pd.read_csv("data/raw/loans.csv"),
            "defaults": pd.read_csv("data/raw/defaults.csv"),
            "transactions": pd.read_csv("data/raw/transactions.csv"),
            "branches": pd.read_csv("data/raw/branches.csv"),
        }


    # def merge(self, data):
    #     df = data["applications"]
    #     df = df.merge(data["customers"], on="Customer_ID", how="left")
    #     df = df.merge(data["loans"], on="Loan_ID", how="left")
    #     df = df.merge(data["defaults"], on="Loan_ID", how="left")
    #     return df

def mergeAll(data):
    loans = data['loans']
    customers = data['customers']

    df = loans.merge(customers, on='CUSTOMER_ID', how='left')

    # if 'Branch_ID' in loans.columns and 'Branch_ID' in data['branches'].columns:
    #     df = df.merge(data['branches'], on='Branch_ID', how='left')

    if 'BRANCH_ID' in loans.columns and 'BRANCH_ID' in data['branches'].columns:
         df = df.merge(data['branches'], on='BRANCH_ID', how='left')

    return df
# def mergeAll(data):
#     df = data['loans'] \
#         .merge(data['customers'], on='Customer_ID', how='left') \
#         .merge(data['branches'], on='Region', how='left') \
#         .merge(data['defaults'], on='Loan_ID', how='left')
#
#     return df

