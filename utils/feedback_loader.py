"""
feedback_loader.py
------------------
Loads one or more college/campus feedback Excel files for the
Trainer Profile Generator.

IMPORTANT DESIGN RULE:
Each uploaded Excel file remains an independent college/campus dataset.
This module never combines feedback across colleges/campuses.

Expected use:
    from utils.feedback_loader import load_multiple_feedback_files

    campuses = load_multiple_feedback_files(uploaded_files)

    for campus in campuses:
        print(campus.campus_name)
        print(campus.trainers)
"""

from __future__ import annotations

import io
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import pandas as pd


# ============================================================
# CANONICAL FIELD NAMES
# ============================================================

FIELD_ALIASES: Dict[str, List[str]] = {
    "member_id": [
        "member id",
        "student id",
        "roll number",
        "roll no",
        "registration number",
        "registration no",
    ],
    "user_name": [
        "user name",
        "student name",
        "name of student",
    ],
    "login_id": [
        "login id",
        "email",
        "email id",
        "mail id",
    ],
    "submitted_on": [
        "submitted on",
        "submitted date",
        "submission date",
        "date",
        "timestamp",
    ],
    "rating": [
        "rating",
        "overall rating",
        "trainer rating",
        "overall trainer rating",
    ],
    "trainer": [
        "select your trainer",
        "trainer name",
        "name of trainer",
        "trainer",
    ],
    "technical": [
        "technical knowledge and confidence",
        "technical knowledge",
        "subject knowledge",
        "technical confidence",
    ],
    "clarity": [
        "explain concepts clearly",
        "clarity of explanation",
        "concept clarity",
        "clarity",
        "easy to understand",
    ],
    "communication": [
        "communication skills and interaction",
        "communication skills",
        "student interaction",
        "communication",
        "interaction with students",
    ],
    "hands_on": [
        "support during hands-on activities",
        "hands-on support",
        "practical support",
        "practical sessions",
        "hands on activities",
    ],
    "industry_relevance": [
        "relevant to industry requirements",
        "industry relevant",
        "industry relevance",
        "practical applications",
        "examples assignments and tasks",
    ],
    "professionalism": [
        "punctuality regularity and professionalism",
        "punctuality",
        "regularity",
        "professionalism",
    ],
    "comments": [
        "improvements comments or suggestions",
        "comments or suggestions",
        "comments",
        "suggestions",
        "feedback",
        "improvements",
    ],
}


# Exact headings used by the current CodeTantra feedback form.
# Keeping them here makes detection very reliable for your present files.
CURRENT_FORM_HEADINGS: Dict[str, str] = {
    "member_id": "Member ID",
    "user_name": "User Name",
    "login_id": "Login ID",
    "submitted_on": "Submitted On",
    "rating": "Rating",
    "trainer": "Select Your Trainer",
    "technical": (
        "How would you rate the trainer’s technical knowledge and confidence "
        "while teaching technical concepts?"
    ),
    "clarity": (
        "Did the trainer explain concepts clearly, accurately, and in an "
        "easy-to-understand manner?"
    ),
    "communication": (
        "How would you rate the trainer’s communication skills and interaction "
        "with students during sessions?"
    ),
    "hands_on": (
        "Did the trainer provide adequate support during hands-on activities "
        "and practical sessions?"
    ),
    "industry_relevance": (
        "Were the examples, assignments, and tasks relevant to industry "
        "requirements and practical applications?"
    ),
    "professionalism": (
        "How would you rate the trainer’s punctuality, regularity, and "
        "professionalism throughout the training?"
    ),
    "comments": (
        "What improvements, comments, or suggestions would you like to provide "
        "for the trainer?"
    ),
}


# ============================================================
# DATA MODEL
# ============================================================

@dataclass
class CampusFeedback:
    """
    One uploaded Excel file = one independent campus/college.
    """

    campus_name: str
    file_name: str
    sheet_name: str
    dataframe: pd.DataFrame
    column_map: Dict[str, Optional[str]]
    trainers: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def total_responses(self) -> int:
        return int(len(self.dataframe))

    @property
    def total_trainers(self) -> int:
        return int(len(self.trainers))

    @property
    def trainer_column(self) -> Optional[str]:
        return self.column_map.get("trainer")

    @property
    def rating_column(self) -> Optional[str]:
        return self.column_map.get("rating")

    def trainer_dataframe(self, trainer_name: str) -> pd.DataFrame:
        """
        Return only the rows for one trainer within this campus.
        """
        trainer_col = self.trainer_column

        if not trainer_col or trainer_col not in self.dataframe.columns:
            return pd.DataFrame()

        values = (
            self.dataframe[trainer_col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        return self.dataframe.loc[
            values.str.casefold() == str(trainer_name).strip().casefold()
        ].copy()


# ============================================================
# BASIC CLEANING HELPERS
# ============================================================

def _normalize_text(value: Any) -> str:
    """
    Convert text to a comparison-friendly form.
    """
    if value is None:
        return ""

    text = str(value).strip().lower()

    replacements = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "_": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove completely empty rows/columns and clean column labels.
    """
    df = df.copy()

    df = df.dropna(axis=0, how="all")
    df = df.dropna(axis=1, how="all")

    cleaned_columns = []
    for col in df.columns:
        name = str(col).strip()
        name = re.sub(r"\s+", " ", name)
        cleaned_columns.append(name)

    df.columns = cleaned_columns
    df.reset_index(drop=True, inplace=True)

    return df


def campus_name_from_filename(file_name: str) -> str:
    """
    Create a readable campus/college name suggestion from the filename.

    Example:
        SVPCET_Feedback_Submissions_573.xlsx
        -> SVPCET

        KITS_Guntur_Feedback.xlsx
        -> KITS Guntur
    """
    stem = Path(str(file_name)).stem

    # Remove common report/export words.
    remove_patterns = [
        r"\bfeedback\b",
        r"\bsubmissions?\b",
        r"\bresponses?\b",
        r"\breport\b",
        r"\bdata\b",
        r"\bexport\b",
        r"\bform\b",
        r"\bresults?\b",
    ]

    name = stem.replace("_", " ").replace("-", " ")

    for pattern in remove_patterns:
        name = re.sub(pattern, " ", name, flags=re.IGNORECASE)

    # Remove standalone trailing row-count-like numbers.
    name = re.sub(r"\b\d{2,6}\b\s*$", " ", name)

    name = re.sub(r"\s+", " ", name).strip(" _-")

    return name if name else stem


def clean_trainer_name(value: Any) -> str:
    """
    Standardize trainer display names without changing the actual identity.
    """
    if pd.isna(value):
        return ""

    name = str(value).strip()
    name = re.sub(r"\s+", " ", name)

    # Remove values that are clearly blank placeholders.
    if name.casefold() in {"", "nan", "none", "null", "na", "n/a", "-"}:
        return ""

    return name


# ============================================================
# COLUMN DETECTION
# ============================================================

def _column_matches_alias(column_name: str, alias: str) -> bool:
    col = _normalize_text(column_name)
    ali = _normalize_text(alias)

    if not col or not ali:
        return False

    if col == ali:
        return True

    # Allow meaningful aliases to occur inside long question headings.
    if len(ali) >= 7 and ali in col:
        return True

    return False


def detect_columns(df: pd.DataFrame) -> Dict[str, Optional[str]]:
    """
    Detect the important feedback columns.

    Returns:
        {
            "trainer": "Select Your Trainer",
            "rating": "Rating",
            "technical": "...",
            ...
        }

    If a field cannot be detected, its value is None.
    """
    columns = list(df.columns)
    mapping: Dict[str, Optional[str]] = {
        field_name: None for field_name in FIELD_ALIASES
    }

    # --------------------------------------------------------
    # Pass 1: exact current CodeTantra feedback-form headings
    # --------------------------------------------------------
    normalized_columns = {
        _normalize_text(col): col for col in columns
    }

    for field_name, expected_heading in CURRENT_FORM_HEADINGS.items():
        expected_normalized = _normalize_text(expected_heading)

        if expected_normalized in normalized_columns:
            mapping[field_name] = normalized_columns[expected_normalized]

    # --------------------------------------------------------
    # Pass 2: alias matching for future college formats
    # --------------------------------------------------------
    for field_name, aliases in FIELD_ALIASES.items():
        if mapping[field_name] is not None:
            continue

        # Prefer exact normalized matches.
        for col in columns:
            normalized_col = _normalize_text(col)

            if any(
                normalized_col == _normalize_text(alias)
                for alias in aliases
            ):
                mapping[field_name] = col
                break

        if mapping[field_name] is not None:
            continue

        # Then allow aliases within longer question text.
        for alias in aliases:
            for col in columns:
                if _column_matches_alias(col, alias):
                    mapping[field_name] = col
                    break

            if mapping[field_name] is not None:
                break

    return mapping


def apply_manual_column_mapping(
    campus: CampusFeedback,
    manual_mapping: Dict[str, Optional[str]],
) -> CampusFeedback:
    """
    Replace auto-detected columns with mappings chosen by the user.

    This will be useful later in 15_Feedback_Analytics.py when a college
    uses different question headings.
    """
    valid_columns = set(campus.dataframe.columns)

    for field_name, column_name in manual_mapping.items():
        if field_name not in campus.column_map:
            continue

        if column_name in (None, "", "-- Not Available --"):
            campus.column_map[field_name] = None
        elif column_name in valid_columns:
            campus.column_map[field_name] = column_name

    campus.trainers = extract_trainers(
        campus.dataframe,
        campus.column_map.get("trainer"),
    )

    campus.warnings = _build_warnings(
        campus.dataframe,
        campus.column_map,
    )

    return campus


# ============================================================
# TRAINER EXTRACTION
# ============================================================

def extract_trainers(
    df: pd.DataFrame,
    trainer_column: Optional[str],
) -> List[str]:
    """
    Return unique trainer names in their first-occurrence order.
    """
    if (
        not trainer_column
        or trainer_column not in df.columns
        or df.empty
    ):
        return []

    trainers: List[str] = []
    seen = set()

    for value in df[trainer_column].tolist():
        name = clean_trainer_name(value)

        if not name:
            continue

        key = name.casefold()

        if key not in seen:
            seen.add(key)
            trainers.append(name)

    return trainers


def get_trainer_response_counts(
    campus: CampusFeedback,
) -> pd.DataFrame:
    """
    Simple trainer list for the Page 15 campus section.

    Returns columns:
        Trainer Name | Responses

    Ratings/analysis will be added by feedback_analysis.py.
    """
    trainer_col = campus.trainer_column

    if not trainer_col or trainer_col not in campus.dataframe.columns:
        return pd.DataFrame(
            columns=["Trainer Name", "Responses"]
        )

    cleaned_names = campus.dataframe[trainer_col].apply(clean_trainer_name)
    cleaned_names = cleaned_names[cleaned_names != ""]

    counts = (
        cleaned_names.value_counts(sort=False)
        .rename_axis("Trainer Name")
        .reset_index(name="Responses")
    )

    # Preserve campus trainer order rather than alphabetical order.
    order = {
        name.casefold(): index
        for index, name in enumerate(campus.trainers)
    }

    counts["_order"] = (
        counts["Trainer Name"]
        .str.casefold()
        .map(order)
        .fillna(999999)
    )

    counts = (
        counts.sort_values("_order")
        .drop(columns="_order")
        .reset_index(drop=True)
    )

    return counts


# ============================================================
# EXCEL READING
# ============================================================

def _source_to_bytes_and_name(
    source: Any,
    fallback_name: str = "Feedback.xlsx",
) -> Tuple[bytes, str]:
    """
    Accept:
        - Streamlit UploadedFile
        - file path
        - bytes / bytearray
        - file-like object
    """
    # Path/string
    if isinstance(source, (str, Path)):
        path = Path(source)
        return path.read_bytes(), path.name

    # Streamlit UploadedFile usually provides getvalue() and name.
    if hasattr(source, "getvalue"):
        data = source.getvalue()
        name = getattr(source, "name", fallback_name)
        return bytes(data), str(name)

    # Raw bytes
    if isinstance(source, (bytes, bytearray)):
        return bytes(source), fallback_name

    # Generic file-like object
    if hasattr(source, "read"):
        try:
            if hasattr(source, "seek"):
                source.seek(0)

            data = source.read()

            if hasattr(source, "seek"):
                source.seek(0)

            name = getattr(source, "name", fallback_name)
            return bytes(data), str(name)

        except Exception as exc:
            raise ValueError(
                f"Unable to read uploaded feedback file: {exc}"
            ) from exc

    raise TypeError(
        "Unsupported feedback source. Use a Streamlit UploadedFile, "
        "Excel file path, bytes, or a file-like object."
    )


def get_excel_sheet_names(source: Any) -> List[str]:
    """
    Return available Excel sheet names.
    """
    file_bytes, _ = _source_to_bytes_and_name(source)

    with pd.ExcelFile(io.BytesIO(file_bytes)) as workbook:
        return list(workbook.sheet_names)


def _choose_sheet_name(
    file_bytes: bytes,
    preferred_sheet: Optional[str] = None,
) -> str:
    """
    Select the most likely feedback sheet.

    Priority:
        1. User-supplied preferred sheet
        2. 'Submissions'
        3. 'Responses'
        4. 'Form Responses 1'
        5. First non-empty sheet
        6. First sheet
    """
    with pd.ExcelFile(io.BytesIO(file_bytes)) as workbook:
        sheet_names = list(workbook.sheet_names)

    if not sheet_names:
        raise ValueError("The Excel workbook contains no sheets.")

    if preferred_sheet and preferred_sheet in sheet_names:
        return preferred_sheet

    preferred_names = [
        "submissions",
        "responses",
        "form responses 1",
        "feedback",
        "feedback responses",
    ]

    normalized_lookup = {
        _normalize_text(sheet): sheet
        for sheet in sheet_names
    }

    for preferred in preferred_names:
        key = _normalize_text(preferred)

        if key in normalized_lookup:
            return normalized_lookup[key]

    # Find first non-empty sheet.
    for sheet in sheet_names:
        try:
            test_df = pd.read_excel(
                io.BytesIO(file_bytes),
                sheet_name=sheet,
                nrows=5,
            )

            if not test_df.empty and len(test_df.columns) > 0:
                return sheet

        except Exception:
            continue

    return sheet_names[0]


def _build_warnings(
    df: pd.DataFrame,
    column_map: Dict[str, Optional[str]],
) -> List[str]:
    warnings: List[str] = []

    if df.empty:
        warnings.append("The selected sheet contains no feedback rows.")

    if not column_map.get("trainer"):
        warnings.append(
            "Trainer-name column was not detected. "
            "Manual column mapping will be required."
        )

    if not column_map.get("rating"):
        warnings.append(
            "Overall rating column was not detected. "
            "The trainer list can still be displayed, but overall-rating "
            "analysis will require manual mapping."
        )

    parameter_fields = [
        "technical",
        "clarity",
        "communication",
        "hands_on",
        "industry_relevance",
        "professionalism",
    ]

    detected_parameters = sum(
        bool(column_map.get(field))
        for field in parameter_fields
    )

    if detected_parameters == 0:
        warnings.append(
            "Detailed feedback parameters were not detected. "
            "Map the required feedback question columns manually."
        )
    elif detected_parameters < len(parameter_fields):
        warnings.append(
            f"Only {detected_parameters} of "
            f"{len(parameter_fields)} standard feedback parameters "
            "were detected."
        )

    if not column_map.get("comments"):
        warnings.append(
            "Comments/suggestions column was not detected."
        )

    return warnings


def load_feedback_file(
    source: Any,
    campus_name: Optional[str] = None,
    sheet_name: Optional[str] = None,
) -> CampusFeedback:
    """
    Load ONE college/campus feedback Excel file.

    The returned dataset belongs only to this campus and is never merged
    with another uploaded file.
    """
    file_bytes, file_name = _source_to_bytes_and_name(source)

    selected_sheet = _choose_sheet_name(
        file_bytes,
        preferred_sheet=sheet_name,
    )

    try:
        df = pd.read_excel(
            io.BytesIO(file_bytes),
            sheet_name=selected_sheet,
        )
    except Exception as exc:
        raise ValueError(
            f"Unable to read '{file_name}' "
            f"(sheet: '{selected_sheet}'): {exc}"
        ) from exc

    df = _clean_dataframe(df)

    column_map = detect_columns(df)
    trainers = extract_trainers(
        df,
        column_map.get("trainer"),
    )
    warnings = _build_warnings(df, column_map)

    resolved_campus_name = (
        str(campus_name).strip()
        if campus_name and str(campus_name).strip()
        else campus_name_from_filename(file_name)
    )

    return CampusFeedback(
        campus_name=resolved_campus_name,
        file_name=file_name,
        sheet_name=selected_sheet,
        dataframe=df,
        column_map=column_map,
        trainers=trainers,
        warnings=warnings,
    )


def load_multiple_feedback_files(
    uploaded_files: Sequence[Any],
    campus_names: Optional[Dict[str, str]] = None,
    sheet_names: Optional[Dict[str, str]] = None,
) -> List[CampusFeedback]:
    """
    Load multiple college/campus feedback files.

    IMPORTANT:
    Every file remains a separate CampusFeedback object.

    Example:
        campuses = load_multiple_feedback_files(files)

        campuses[0] -> SVPCET only
        campuses[1] -> KITS Guntur only
        campuses[2] -> VEMU only

    No cross-campus consolidation is performed.
    """
    if not uploaded_files:
        return []

    campus_names = campus_names or {}
    sheet_names = sheet_names or {}

    campuses: List[CampusFeedback] = []

    for source in uploaded_files:
        file_name = str(
            getattr(source, "name", "Feedback.xlsx")
        )

        campus = load_feedback_file(
            source=source,
            campus_name=campus_names.get(file_name),
            sheet_name=sheet_names.get(file_name),
        )

        campuses.append(campus)

    return campuses


# ============================================================
# CAMPUS DISPLAY HELPERS
# ============================================================

def rename_campus(
    campus: CampusFeedback,
    new_name: str,
) -> CampusFeedback:
    """
    Update only the display/report campus name.
    Feedback rows are unchanged.
    """
    cleaned = re.sub(r"\s+", " ", str(new_name)).strip()

    if cleaned:
        campus.campus_name = cleaned

    return campus


def campus_overview(campus: CampusFeedback) -> Dict[str, Any]:
    """
    Small summary used by the Streamlit page header.
    """
    return {
        "campus_name": campus.campus_name,
        "file_name": campus.file_name,
        "sheet_name": campus.sheet_name,
        "total_trainers": campus.total_trainers,
        "total_responses": campus.total_responses,
        "trainers": campus.trainers,
        "warnings": campus.warnings,
    }
