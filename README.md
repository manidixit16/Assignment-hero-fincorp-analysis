# Hero FinCorp Credit Analytics

End-to-end Python analysis pipeline for Hero FinCorp's loan portfolio data.
The project covers 20 analytical tasks spanning data quality, risk scoring,
customer segmentation, EMI analysis, recovery effectiveness, and time-series
trend detection.

---

## Repository

**GitHub:** https://github.com/manidixit16/Assignment-hero-fincorp-analysis

---

## Project Structure

```
Assignment-hero-fincorp-analysis/
├── main.py                          # Pipeline entry point
├── config.py                        # Paths and project constants
├── requirements.txt
├── data/
│   ├── raw/                         # 6 source CSV files
│   │   ├── customers.csv
│   │   ├── loans.csv
│   │   ├── applications.csv
│   │   ├── transactions.csv
│   │   ├── defaults.csv
│   │   └── branches.csv
│   ├── cleaned/                     # Output of data_sanitizer
│   └── processed/                   # Feature-engineered data
├── src/pgds/assignment/
│   ├── dataprocessor/
│   │   ├── dataset_loader.py        # Raw & cleaned data ingestion
│   │   ├── data_sanitizer.py        # Deduplication, imputation, outlier capping
│   │   ├── feature_builder.py       # Derived columns (DEFAULT_FLAG, RECOVERY_RATE …)
│   │   ├── data_merger.py           # Master DataFrame join
│   │   └── common.py                # Shared utilities
│   ├── analyser/
│   │   ├── exploratory_summary.py   # Task 2  — distributions & monthly trends
│   │   ├── loan_default_scorer.py   # Task 3  — attribute-level default correlation
│   │   ├── branch_performance.py    # Task 4  — branch delinquency & volume
│   │   ├── borrower_segmentation.py # Task 5  — income & credit score tiers
│   │   ├── advanced_metrics.py      # Task 6  — extended statistical correlation
│   │   ├── payment_recovery_analysis.py # Task 7 — transaction types & recovery
│   │   ├── emi_risk_analysis.py     # Task 8  — EMI band default probability
│   │   ├── application_insights.py  # Task 9  — approval rates & rejection reasons
│   │   ├── recovery_effectiveness.py # Task 10 — legal action vs recovery rate
│   │   ├── loan_disbursement.py     # Task 11 — processing time by region/purpose
│   │   ├── revenue_analysis.py      # Task 12 — profitability by region/purpose
│   │   ├── regional_analysis.py     # Task 13 — geospatial loan & default mapping
│   │   ├── default_trend_tracker.py # Task 14 — defaults over time & income tier
│   │   ├── temporal_analysis.py     # Task 16 — time-series disbursement & defaults
│   │   ├── repayment_behavior.py    # Task 17 — age/gender approval & repayment
│   │   ├── credit_risk_profiler.py  # Task 18 — risk by credit tier & loan purpose
│   │   ├── default_velocity_analysis.py # Task 19 — days-to-default by segment
│   │   └── txn_behavior_analysis.py # Task 20 — transaction pattern analysis
│   ├── visualizer/
│   │   └── chart_engine.py          # All matplotlib/seaborn chart functions
│   └── reporting/
│       └── insight_reporter.py      # Word (.docx) report generator
└── reports/
    ├── figures/                     # All saved PNG charts
    └── hero_fincorp_analysis.docx   # Final report
```

---

## Running the Pipeline

```bash
pip install -r requirements.txt
python main.py
```

Charts are saved to `reports/figures/`. The Word report is generated at
`reports/hero_fincorp_analysis.docx`.

---

## Task Coverage

| Task | Module | Description |
|------|--------|-------------|
| 1  | `data_sanitizer` + `feature_builder` | Data quality, cleaning, feature engineering |
| 2  | `exploratory_summary` | Descriptive distributions & monthly trends |
| 3  | `loan_default_scorer` | Default risk correlation across loan attributes |
| 4  | `branch_performance` | Branch delinquency and volume analysis |
| 5  | `borrower_segmentation` | Income & credit score customer tiers |
| 6  | `advanced_metrics` | Extended statistical correlation |
| 7  | `payment_recovery_analysis` | Transaction types & regional recovery |
| 8  | `emi_risk_analysis` | EMI threshold default probability |
| 9  | `application_insights` | Approval rates & rejection drivers |
| 10 | `recovery_effectiveness` | Legal action vs recovery rate |
| 11 | `loan_disbursement` | Disbursement processing efficiency |
| 12 | `revenue_analysis` | Profitability by region & purpose |
| 13 | `regional_analysis` | Geospatial loan & default mapping |
| 14 | `default_trend_tracker` | Default trends over time & income |
| 15 | *(skipped — no BRANCH_ID linkage)* | Branch efficiency not feasible |
| 16 | `temporal_analysis` | Time-series seasonal patterns |
| 17 | `repayment_behavior` | Customer age/gender repayment behaviour |
| 18 | `credit_risk_profiler` | Risk scoring by credit tier & purpose |
| 19 | `default_velocity_analysis` | Days-to-default by segment |
| 20 | `txn_behavior_analysis` | Transaction behaviour patterns |

---

## Key Findings

- **Credit score** is the strongest predictor of default risk.
- **High-EMI borrowers** default at significantly higher rates.
- **Low-income + low-credit-score** segments form the highest-risk cohort.
- **Legal action** modestly improves recovery rates.
- **Regional default rates** vary — Central and South show elevated risk.
- Loan demand has remained **steady over time** with seasonal application spikes.

---

## Recommendations

1. **Tighten credit score thresholds** for high-value loan approvals.
2. **Cap EMI-to-income ratio** to reduce high-EMI default exposure.
3. **Expand legal recovery** in high-default regions.
4. **Add BRANCH_ID** to loan and application datasets to unlock Task 15.
5. **Invest in low-income segment support** (financial literacy, restructuring options).
