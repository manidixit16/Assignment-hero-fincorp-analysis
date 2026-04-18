"""
Configuration
=============
Central settings for the Hero FinCorp Credit Analytics project.
All path constants and project-level parameters are defined here.
"""

# ─── Project Identity ────────────────────────────────────────────────────────
PROJECT_NAME    = "Hero FinCorp Credit Analytics"
PROJECT_VERSION = "1.0.0"
AUTHOR          = "Mani Dixit"

# ─── Data Paths ──────────────────────────────────────────────────────────────
DATA_PATH         = "data/raw/"
CLEANED_DATA_PATH = "data/cleaned/"
PROCESSED_PATH    = "data/processed/"

# ─── Output Paths ────────────────────────────────────────────────────────────
REPORT_PATH = "reports/"
FIGURE_PATH = "reports/figures/"

# ─── Analysis Parameters ─────────────────────────────────────────────────────
EMI_QUANTILE_BINS    = 5       # Number of EMI bands for risk segmentation
INCOME_BINS          = [0, 300_000, 700_000, float('inf')]
INCOME_LABELS        = ['Low', 'Medium', 'High']
CREDIT_SCORE_BINS    = [0, 580, 720, float('inf')]
CREDIT_SCORE_LABELS  = ['Low', 'Medium', 'High']
OUTLIER_IQR_FACTOR   = 1.5     # Multiplier for IQR-based outlier capping
