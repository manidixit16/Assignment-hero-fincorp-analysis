# ─────────────────────────────────────────────────────────
# Hero FinCorp Credit Analytics — Configuration
# ─────────────────────────────────────────────────────────
PROJECT_NAME   = "Hero FinCorp Credit Portfolio Analysis"
AUTHOR         = "Mani Dixit"
VERSION        = "1.0.0"

# Directory paths
DATA_PATH      = "data/raw/"
CLEANED_PATH   = "data/cleaned/"
PROCESSED_PATH = "data/processed/"
REPORT_PATH    = "reports/"
FIGURE_PATH    = "reports/figures/"

# Dataset filenames
RAW_FILES = {
    "customers":    "customers.csv",
    "loans":        "loans.csv",
    "applications": "applications.csv",
    "transactions": "transactions.csv",
    "defaults":     "defaults.csv",
    "branches":     "branches.csv",
}

# Outlier capping targets
OUTLIER_COLS = ["LOAN_AMOUNT", "INTEREST_RATE", "DEFAULT_AMOUNT"]

# Segmentation thresholds
INCOME_BINS   = [0, 300_000, 700_000, float("inf")]
INCOME_LABELS = ["Low", "Medium", "High"]

CREDIT_BINS   = [0, 580, 720, float("inf")]
CREDIT_LABELS = ["Low", "Medium", "High"]

EMI_QUANTILES = 5
