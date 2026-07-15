# Configuration
"""
=========================================================
Trainer Profile Generator
Configuration File
=========================================================
"""

from pathlib import Path

# -------------------------------------------------------
# Project Root
# -------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

# -------------------------------------------------------
# Input Files
# -------------------------------------------------------

DATA_FOLDER = PROJECT_ROOT / "data"

EXCEL_FILE = DATA_FOLDER / "Trainers.xlsx"

TEMPLATE_FILE = DATA_FOLDER / "Trainer_Profile_Template.docx"

IMAGE_FOLDER = DATA_FOLDER / "CTImages"

# -------------------------------------------------------
# Output
# -------------------------------------------------------

OUTPUT_FOLDER = PROJECT_ROOT / "output"

DOCX_OUTPUT = OUTPUT_FOLDER / "docx"

PDF_OUTPUT = OUTPUT_FOLDER / "pdf"

# -------------------------------------------------------
# Logs
# -------------------------------------------------------

LOG_FOLDER = PROJECT_ROOT / "logs"

LOG_FILE = LOG_FOLDER / "generation.log"

MISSING_IMAGE_LOG = LOG_FOLDER / "missing_images.txt"

# -------------------------------------------------------
# Assets
# -------------------------------------------------------

ASSETS_FOLDER = PROJECT_ROOT / "assets"

ICON_FOLDER = ASSETS_FOLDER / "icons"

# -------------------------------------------------------
# Image Settings
# -------------------------------------------------------

PHOTO_WIDTH = 1.50      # inches

PHOTO_HEIGHT = 1.85     # inches

# -------------------------------------------------------
# Rating
# -------------------------------------------------------

MAX_RATING = 5

STAR = "⭐"

# -------------------------------------------------------
# Company Details
# -------------------------------------------------------

COMPANY_NAME = "CodeTantra Tech Solutions Pvt. Ltd."

PROFILE_TITLE = "Technical Trainer"

# -------------------------------------------------------
# Experience Format
# -------------------------------------------------------

DATE_FORMAT = "%d-%m-%Y"

# -------------------------------------------------------
# Supported Image Types
# -------------------------------------------------------

IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png"
]

# -------------------------------------------------------
# Create Required Folders Automatically
# -------------------------------------------------------

DOCX_OUTPUT.mkdir(parents=True, exist_ok=True)
PDF_OUTPUT.mkdir(parents=True, exist_ok=True)
LOG_FOLDER.mkdir(parents=True, exist_ok=True)

print("Configuration Loaded Successfully.")