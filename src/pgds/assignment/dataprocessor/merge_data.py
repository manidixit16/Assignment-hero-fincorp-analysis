def merge_all(data):

    df = data['loans'].copy()

    # -----------------------------------
    # CUSTOMER (existing logic + REGION added)
    # -----------------------------------
    df = df.merge(
        data['customers'][['CUSTOMER_ID', 'CREDIT_SCORE', 'ANNUAL_INCOME', 'REGION']],
        on='CUSTOMER_ID',
        how='left'
    )

    # -----------------------------------
    # DEFAULT + RECOVERY (extended safely)
    # -----------------------------------
    df = df.merge(
        data['defaults'][[
            'LOAN_ID',
            'DEFAULT_AMOUNT',
            'RECOVERY_AMOUNT',
            'DEFAULT_REASON',
            'LEGAL_ACTION',
            'DEFAULT_DATE'
        ]],
        on='LOAN_ID',
        how='left'
    )

    # -----------------------------------
    # APPLICATION (UPDATED HERE ✅)
    # -----------------------------------
    df = df.merge(
        data['applications'][[
            'LOAN_ID',
            'APPLICATION_DATE',
            'LOAN_PURPOSE'   # ✅ ADDED
        ]],
        on='LOAN_ID',
        how='left'
    )

    # -----------------------------------
    # HANDLE MISSING
    # -----------------------------------
    df['DEFAULT_AMOUNT'] = df['DEFAULT_AMOUNT'].fillna(0)
    df['RECOVERY_AMOUNT'] = df['RECOVERY_AMOUNT'].fillna(0)

    # -----------------------------------
    # RECOVERY RATE (existing logic)
    # -----------------------------------
    df['RECOVERY_RATE'] = df['RECOVERY_AMOUNT'] / df['DEFAULT_AMOUNT'].replace(0, 1)

    # -----------------------------------
    # FIX REGION COLUMN
    # -----------------------------------
    if 'REGION_x' in df.columns:
        df['REGION'] = df['REGION_x']
    elif 'REGION_y' in df.columns:
        df['REGION'] = df['REGION_y']

    df.drop(columns=['REGION_x', 'REGION_y'], errors='ignore', inplace=True)

    return df

# def merge_all(data):
#
#     df = data['loans'].copy()
#
#     # -----------------------------------
#     # CUSTOMER (existing logic + REGION added)
#     # -----------------------------------
#     df = df.merge(
#         data['customers'][['CUSTOMER_ID', 'CREDIT_SCORE', 'ANNUAL_INCOME', 'REGION']],
#         on='CUSTOMER_ID',
#         how='left'
#     )
#
#     # -----------------------------------
#     # DEFAULT + RECOVERY (extended safely)
#     # -----------------------------------
#     df = df.merge(
#         data['defaults'][[
#             'LOAN_ID',
#             'DEFAULT_AMOUNT',
#             'RECOVERY_AMOUNT',
#             'DEFAULT_REASON',   # ✅ added
#             'LEGAL_ACTION'      # ✅ added
#         ]],
#         on='LOAN_ID',
#         how='left'
#     )
#     df = df.merge(
#         data['applications'][['LOAN_ID', 'APPLICATION_DATE']],
#         on='LOAN_ID',
#         how='left'
#     )
#
#
#     # -----------------------------------
#     # HANDLE MISSING
#     # -----------------------------------
#     df['DEFAULT_AMOUNT'] = df['DEFAULT_AMOUNT'].fillna(0)
#     df['RECOVERY_AMOUNT'] = df['RECOVERY_AMOUNT'].fillna(0)
#
#     # -----------------------------------
#     # RECOVERY RATE (existing logic)
#     # -----------------------------------
#     df['RECOVERY_RATE'] = df['RECOVERY_AMOUNT'] / df['DEFAULT_AMOUNT'].replace(0, 1)
#
#     # -----------------------------------
#     # 🔥 FIX REGION COLUMN
#     # -----------------------------------
#     if 'REGION_x' in df.columns:
#         df['REGION'] = df['REGION_x']
#     elif 'REGION_y' in df.columns:
#         df['REGION'] = df['REGION_y']
#
#     df.drop(columns=['REGION_x', 'REGION_y'], errors='ignore', inplace=True)
#     return df
#
#
