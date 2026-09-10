"""
feedback_report_config.py
-------------------------
Central configuration for the Feedback Analytics module
in Trainer Profile Generator.

Save this file inside:
    TrainerProfileGenerator/templates/feedback_report_config.py

Purpose:
- Keep report titles and labels in one place
- Keep output folder names in one place
- Keep score thresholds in one place
- Keep colors and dimensions in one place
- Make future visual changes easier

This file contains configuration only.
No Streamlit UI or report-generation logic is placed here.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List


# ============================================================
# APPLICATION / PAGE LABELS
# ============================================================

PAGE_TITLE = "Trainer Feedback Analytics"
PAGE_SUBTITLE = (
    "Upload campus or college feedback files, analyze trainer-wise "
    "performance, and generate image, PDF, PPT, and ZIP reports."
)

UPLOAD_LABEL = "Upload College / Campus Feedback Files"

REPORT_MAIN_TITLE = "TRAINER FEEDBACK SUMMARY"
PERFORMANCE_SECTION_TITLE = "PERFORMANCE AREAS"
STRENGTHS_SECTION_TITLE = "KEY STRENGTHS"
FOCUS_SECTION_TITLE = "DEVELOPMENT FOCUS"
STUDENT_VOICE_SECTION_TITLE = "STUDENT VOICE"
OVERALL_PERFORMANCE_LABEL = "Overall Performance"


# ============================================================
# CAMPUS ACTION LABELS
# ============================================================

CAMPUS_ACTION_GENERATE_IMAGES = "Generate Image Reports For All"
CAMPUS_ACTION_GENERATE_PDFS = "Generate All PDF Reports"
CAMPUS_ACTION_GENERATE_CAMPUS_PDF = "Generate Campus PDF"
CAMPUS_ACTION_GENERATE_CAMPUS_PPT = "Generate Campus PPT"
CAMPUS_ACTION_DOWNLOAD_ZIP = "Download Campus ZIP"


# ============================================================
# INDIVIDUAL TRAINER ACTION LABELS
# ============================================================

TRAINER_ACTION_VIEW = "View Report"
TRAINER_ACTION_IMAGE = "Generate Image"
TRAINER_ACTION_PDF = "Generate PDF"


# ============================================================
# PARAMETER CONFIGURATION
# ============================================================

PARAMETER_ORDER: List[str] = [
    "clarity",
    "communication",
    "technical",
    "hands_on",
    "industry_relevance",
    "professionalism",
]

PARAMETER_LABELS: Dict[str, str] = {
    "clarity": "Clarity of Explanation",
    "communication": "Communication & Interaction",
    "technical": "Technical Knowledge & Confidence",
    "hands_on": "Hands-on Support",
    "industry_relevance": "Industry-Relevant Examples",
    "professionalism": "Punctuality & Professionalism",
}


# ============================================================
# SCORE SETTINGS
# ============================================================

OVERALL_RATING_MIN = 1.0
OVERALL_RATING_MAX = 5.0

DETAIL_SCORE_MIN = -2.0
DETAIL_SCORE_MAX = 2.0

POSITIVE_STAR_THRESHOLD = 4.0
POSITIVE_DETAIL_THRESHOLD = 1.0

DEFAULT_MAX_STRENGTHS = 3
DEFAULT_MAX_FOCUS_AREAS = 2
DEFAULT_MAX_STUDENT_COMMENTS = 3


# ============================================================
# PERFORMANCE CLASSIFICATION
# ============================================================

PERFORMANCE_THRESHOLDS = {
    "excellent": 4.75,
    "very_good": 4.25,
    "good": 3.75,
    "needs_improvement": 3.00,
}

PERFORMANCE_LABELS = {
    "excellent": "Excellent",
    "very_good": "Very Good",
    "good": "Good",
    "needs_improvement": "Needs Improvement",
    "significant_improvement": "Significant Improvement Required",
    "not_available": "Not Available",
}


# ============================================================
# IMAGE REPORT SETTINGS
# ============================================================

IMAGE_WIDTH = 1600
IMAGE_HEIGHT = 2200

IMAGE_FORMAT = "PNG"
IMAGE_EXTENSION = ".png"

IMAGE_BACKGROUND = "#F6F8FC"
IMAGE_CARD_BACKGROUND = "#FFFFFF"

IMAGE_HEADER_BACKGROUND = "#173A63"
IMAGE_HEADER_ACCENT = "#FF8A34"

IMAGE_TEXT_PRIMARY = "#1F2937"
IMAGE_TEXT_SECONDARY = "#667085"
IMAGE_TEXT_LIGHT = "#FFFFFF"

IMAGE_BORDER = "#D9E0EA"

IMAGE_BAR_BACKGROUND = "#E8EDF4"
IMAGE_BAR_FILL = "#2E67A3"

IMAGE_STRENGTH_BACKGROUND = "#EEF7F2"
IMAGE_STRENGTH_TEXT = "#235B3A"

IMAGE_FOCUS_BACKGROUND = "#FFF5EB"
IMAGE_FOCUS_TEXT = "#8B4A12"

IMAGE_STUDENT_VOICE_BACKGROUND = "#F7F3FF"
IMAGE_STUDENT_VOICE_TEXT = "#513779"


# ============================================================
# PDF SETTINGS
# ============================================================

PDF_RESOLUTION = 150.0
PDF_EXTENSION = ".pdf"

CAMPUS_PDF_SUFFIX = "Campus_Feedback_Report.pdf"
TRAINER_PDF_SUFFIX = "Feedback_Report.pdf"


# ============================================================
# POWERPOINT SETTINGS
# ============================================================

PPT_EXTENSION = ".pptx"

# Widescreen 16:9
PPT_SLIDE_WIDTH_INCHES = 13.333333
PPT_SLIDE_HEIGHT_INCHES = 7.5

CAMPUS_PPT_SUFFIX = "Campus_Feedback_Report.pptx"


# ============================================================
# ZIP SETTINGS
# ============================================================

ZIP_EXTENSION = ".zip"
CAMPUS_ZIP_SUFFIX = "Feedback_Reports.zip"


# ============================================================
# OUTPUT DIRECTORY SETTINGS
# ============================================================

OUTPUT_ROOT = Path("output") / "feedback_reports"

IMAGES_FOLDER_NAME = "images"
PDFS_FOLDER_NAME = "pdfs"


def campus_output_folder(campus_name: str) -> Path:
    """
    Return standard campus output folder.

    Example:
        output/feedback_reports/SVPCET
    """
    return OUTPUT_ROOT / campus_name


def campus_images_folder(campus_name: str) -> Path:
    """
    Return standard trainer image folder for a campus.
    """
    return campus_output_folder(campus_name) / IMAGES_FOLDER_NAME


def campus_pdfs_folder(campus_name: str) -> Path:
    """
    Return standard individual trainer PDF folder for a campus.
    """
    return campus_output_folder(campus_name) / PDFS_FOLDER_NAME


# ============================================================
# DISPLAY SETTINGS
# ============================================================

CAMPUS_EXPANDER_DEFAULT = True
TRAINER_EXPANDER_DEFAULT = False

SHOW_RESPONSE_COUNT = True
SHOW_OVERALL_RATING = True
SHOW_POSITIVE_PERCENT = True
SHOW_PERFORMANCE_LABEL = True
SHOW_STUDENT_VOICE = True
SHOW_MANAGEMENT_SUMMARY = True

DEFAULT_TABLE_COLUMNS = [
    "Trainer Name",
    "Responses",
    "Rating",
    "Positive %",
    "Performance",
]


# ============================================================
# FILE UPLOAD SETTINGS
# ============================================================

SUPPORTED_FEEDBACK_FILE_TYPES = [
    "xlsx",
    "xls",
]

ALLOW_MULTIPLE_FEEDBACK_FILES = True


# ============================================================
# DEFAULT SHEET PREFERENCES
# ============================================================

PREFERRED_SHEET_NAMES = [
    "Submissions",
    "Responses",
    "Form Responses 1",
    "Feedback",
    "Feedback Responses",
]


# ============================================================
# LOW-VALUE COMMENT SETTINGS
# ============================================================

LOW_VALUE_COMMENT_WORDS = [
    "good",
    "very good",
    "excellent",
    "nice",
    "ok",
    "okay",
    "fine",
    "nothing",
    "nil",
    "nill",
    "na",
    "n/a",
    "none",
    "no comments",
    "no comment",
    "no suggestions",
    "no suggestion",
    "all good",
    "everything is good",
    "everything is fine",
]


# ============================================================
# CAMPUS REPORT NAMING
# ============================================================

def build_campus_pdf_filename(campus_slug: str) -> str:
    return f"{campus_slug}_{CAMPUS_PDF_SUFFIX}"


def build_campus_ppt_filename(campus_slug: str) -> str:
    return f"{campus_slug}_{CAMPUS_PPT_SUFFIX}"


def build_campus_zip_filename(campus_slug: str) -> str:
    return f"{campus_slug}_{CAMPUS_ZIP_SUFFIX}"


def build_trainer_image_filename(trainer_slug: str) -> str:
    return f"{trainer_slug}_Feedback_Report.png"


def build_trainer_pdf_filename(trainer_slug: str) -> str:
    return f"{trainer_slug}_Feedback_Report.pdf"
