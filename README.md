# Hero FinCorp Credit Portfolio Analysis

**Author:** Mani Dixit  
**GitHub:** [manidixit16/Assignment-hero-fincorp-analysis](https://github.com/manidixit16/Assignment-hero-fincorp-analysis)

---

## Overview

A complete 20-task data analysis of Hero FinCorp's credit portfolio, covering ~70,000 customers, 90,000 loans, 82,600 applications, 9,000 defaults, 495,000 transactions, and 50 branches.

---

## Project Structure

```
Assignment-hero-fincorp-analysis/
├── main.py                          # Pipeline entry point
├── config.py                        # Path and parameter config
├── requirements.txt
├── data/
│   ├── raw/                         # 6 source CSV files
│   ├── cleaned/                     # Post-sanitisation datasets
│   └── processed/                   # Feature-engineered datasets
├── src/pgds/assignment/
│   ├── dataprocessor/
│   │   ├── dataset_loader.py        # CSV ingestion
│   │   ├── data_sanitizer.py        # Cleaning & validation
│   │   ├── feature_builder.py       # Derived column creation
│   │   └── data_merger.py           # Master frame assembly
│   ├── analyser/
│   │   ├── exploratory_summary.py   # Task 2
│   │   ├── loan_default_scorer.py   # Task 3
│   │   ├── branch_performance.py    # Task 4
│   │   ├── borrower_segmentation.py # Task 5
│   │   ├── advanced_metrics.py      # Task 6
│   │   ├── payment_recovery_analysis.py # Task 7
│   │   ├── emi_risk_analysis.py     # Task 8
│   │   ├── application_insights.py  # Task 9
│   │   ├── recovery_effectiveness.py # Task 10
│   │   ├── loan_disbursement.py     # Task 11
│   │   ├── revenue_analysis.py      # Task 12
│   │   ├── regional_analysis.py     # Task 13
│   │   ├── default_trend_tracker.py # Task 14
│   │   ├── temporal_analysis.py     # Task 16
│   │   ├── repayment_behavior.py    # Task 17
│   │   ├── credit_risk_profiler.py  # Task 18
│   │   ├── default_velocity_analysis.py # Task 19
│   │   └── txn_behavior_analysis.py # Task 20
│   ├── visualizer/
│   │   └── chart_engine.py          # All chart generation
│   └── reporting/
│       └── insight_reporter.py      # Word report generator
└── reports/
    ├── figures/                     # All generated charts (.png)
    └── mani_hero_fincorp_report.docx
```

---

## Setup & Run

```bash
pip install -r requirements.txt
python main.py
```

Output goes to `reports/figures/` (charts) and `reports/mani_hero_fincorp_report.docx` (full report).

---

## Task Summary

| Task | Module | Description |
|------|--------|-------------|
| 1 | `data_sanitizer.py` | Data quality & preparation |
| 2 | `exploratory_summary.py` | Distribution & trend overview |
| 3 | `loan_default_scorer.py` | Default risk correlation |
| 4 | `branch_performance.py` | Branch & regional performance |
| 5 | `borrower_segmentation.py` | Customer segmentation |
| 6 | `advanced_metrics.py` | Advanced statistical analysis |
| 7 | `payment_recovery_analysis.py` | Transaction & recovery |
| 8 | `emi_risk_analysis.py` | EMI risk analysis |
| 9 | `application_insights.py` | Loan application insights |
| 10 | `recovery_effectiveness.py` | Recovery effectiveness |
| 11 | `loan_disbursement.py` | Disbursement efficiency |
| 12 | `revenue_analysis.py` | Profitability analysis |
| 13 | `regional_analysis.py` | Regional distribution |
| 14 | `default_trend_tracker.py` | Default trend analysis |
| 15 | N/A | Branch efficiency (BRANCH_ID linkage absent) |
| 16 | `temporal_analysis.py` | Time-series analysis |
| 17 | `repayment_behavior.py` | Customer behaviour |
| 18 | `credit_risk_profiler.py` | Risk assessment |
| 19 | `default_velocity_analysis.py` | Time to default |
| 20 | `txn_behavior_analysis.py` | Transaction patterns |

---

## Key Findings

- **Default rate** is concentrated in low-income, low-credit-score borrowers
- **EMI-to-income ratio** above 40% is a strong default predictor  
- **Recovery rates** are low across the board; legal action provides marginal uplift
- **Processing time** varies significantly by region — a key operational bottleneck
- **Penalty transactions** make up a large share of total transaction volume
- **BRANCH_ID** linkage between branches and loans/applications is absent — a critical data gap

---

## Recommendations

1. Enforce minimum credit score thresholds for unsecured products
2. Implement early-warning monitoring at 3, 6, and 12 months post-disbursement
3. Deploy tiered collections model; refer NPAs >360 days to ARCs
4. Digitise document submission to reduce processing time to ≤30 days
5. Add `BRANCH_ID` to `loans.csv` and `applications.csv` for branch-level analytics
