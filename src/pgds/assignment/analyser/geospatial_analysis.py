def geospatial_analysis(df):

    print("\n GEOSPATIAL ANALYSIS")

    results = {}

    # -----------------------------------
    # 1. ACTIVE LOANS BY REGION (SAFE)
    # -----------------------------------
    if 'LOAN_STATUS' in df.columns:

        status = df['LOAN_STATUS'].astype(str).str.upper().str.strip()

        active_loans = df[
            status.isin(['ACTIVE', 'APPROVED', 'DISBURSED'])
        ]

        # fallback if empty
        if active_loans.empty:
            print("No ACTIVE loans → using non-default loans")
            active_loans = df[df['DEFAULT_FLAG'] == 0]

    else:
        print("LOAN_STATUS missing → using DEFAULT_FLAG")
        active_loans = df[df['DEFAULT_FLAG'] == 0]

    # REGION DISTRIBUTION
    if 'REGION' in active_loans.columns:

        region_dist = active_loans['REGION'].value_counts()

        print("\n Active Loans by Region:\n", region_dist)

        results['region_distribution'] = region_dist

    else:
        print("REGION missing")

    # -----------------------------------
    # 2. DEFAULT RATE BY REGION
    # -----------------------------------
    if 'REGION' in df.columns and 'DEFAULT_FLAG' in df.columns:

        default_rate = df.groupby('REGION')['DEFAULT_FLAG'].mean()

        print("\n Default Rate by Region:\n", default_rate)

        results['default_rate'] = default_rate

    # -----------------------------------
    # 3. RURAL vs URBAN (NOT AVAILABLE)
    # -----------------------------------
    print("\n Rural vs Urban analysis NOT possible")
    print("Reason: AREA_TYPE column not available in dataset")

    return results