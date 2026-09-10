"""
feedback_analysis.py
--------------------
Trainer-wise feedback analysis for the Trainer Profile Generator.

Works with CampusFeedback objects created by:
    utils.feedback_loader

IMPORTANT:
Each campus/college remains completely independent.
No trainer score is combined across campuses.

Main functions:
    analyze_trainer(...)
    analyze_campus(...)
    build_trainer_summary_table(...)
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from utils.feedback_loader import CampusFeedback, clean_trainer_name


# ============================================================
# CONFIGURATION
# ============================================================

PARAMETER_ORDER = [
    "clarity",
    "communication",
    "technical",
    "hands_on",
    "industry_relevance",
    "professionalism",
]

PARAMETER_LABELS = {
    "clarity": "Clarity of Explanation",
    "communication": "Communication & Interaction",
    "technical": "Technical Knowledge & Confidence",
    "hands_on": "Hands-on Support",
    "industry_relevance": "Industry-Relevant Examples",
    "professionalism": "Punctuality & Professionalism",
}

# Your current detailed feedback scale:
# -2, -1, 0, 1, 2
DETAIL_SCORE_MIN = -2.0
DETAIL_SCORE_MAX = 2.0

# Overall star rating is normally 1 to 5.
STAR_RATING_MIN = 1.0
STAR_RATING_MAX = 5.0

# Consider 4-star and 5-star overall ratings as positive.
POSITIVE_STAR_THRESHOLD = 4.0

# Detailed feedback: +1 / +2 are treated as positive.
POSITIVE_DETAIL_THRESHOLD = 1.0

# Number of comments to show in the one-page report.
DEFAULT_MAX_COMMENTS = 3


# ============================================================
# DATA MODEL
# ============================================================

@dataclass
class ParameterScore:
    key: str
    label: str
    average: Optional[float]
    count: int
    positive_count: int
    positive_percent: Optional[float]
    min_score: Optional[float]
    max_score: Optional[float]


@dataclass
class TrainerAnalysis:
    campus_name: str
    trainer_name: str
    responses: int

    overall_rating: Optional[float]
    positive_rating_count: int
    positive_rating_percent: Optional[float]

    five_star_count: int
    four_star_count: int
    three_star_count: int
    two_star_count: int
    one_star_count: int

    detail_positive_count: int
    detail_total_count: int
    detail_positive_percent: Optional[float]

    parameter_scores: List[ParameterScore]

    strengths: List[str]
    development_focus: List[str]
    student_voice: List[str]

    overall_label: str
    management_summary: str

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data


# ============================================================
# NUMERIC CLEANING
# ============================================================

def _parse_numeric_value(value: Any) -> float:
    """
    Extract a numeric score from feedback values.

    Supports both plain numbers and the text formats used by the
    current feedback Excel files, for example:

        5 / 5
        4 / 5
        +2 – Excellent
        +1 – Very Good
        0 – Good
        -1 – Average
        -2 – Poor

    Returns NaN when no valid number is found.
    """
    if value is None or pd.isna(value):
        return np.nan

    if isinstance(value, (int, float, np.integer, np.floating)):
        try:
            return float(value)
        except Exception:
            return np.nan

    text = str(value).strip()

    if not text:
        return np.nan

    # Capture the first signed integer/decimal in the cell.
    match = re.search(r"[+-]?\d+(?:\.\d+)?", text)

    if not match:
        return np.nan

    try:
        return float(match.group(0))
    except Exception:
        return np.nan


def _to_numeric_series(series: pd.Series) -> pd.Series:
    """
    Convert ratings/scores safely to numeric values.

    Handles both numeric cells and descriptive text cells such as
    '5 / 5' and '+2 – Excellent'.
    """
    if series is None:
        return pd.Series(dtype="float64")

    return series.apply(_parse_numeric_value).astype("float64")


def _round_or_none(value: Any, digits: int = 2) -> Optional[float]:
    try:
        if value is None or pd.isna(value):
            return None
        return round(float(value), digits)
    except Exception:
        return None


def _percent(part: int, total: int) -> Optional[float]:
    if not total:
        return None
    return round((part / total) * 100, 1)


# ============================================================
# COMMENT CLEANING
# ============================================================

LOW_VALUE_COMMENTS = {
    "",
    "good",
    "very good",
    "excellent",
    "nice",
    "ok",
    "okay",
    "fine",
    "nothing",
    "nothing to say",
    "nothing to improve",
    "nothing to improve sir",
    "no",
    "no comments",
    "no comment",
    "no suggestions",
    "no suggestion",
    "no improvements",
    "nil",
    "nill",
    "na",
    "n/a",
    "none",
    "-",
    ".",
    "everything is good",
    "everything is fine",
    "all good",
    "good teaching",
    "very good teaching",
}


def _normalize_comment(text: Any) -> str:
    if text is None or pd.isna(text):
        return ""

    value = str(text).strip()
    value = re.sub(r"\s+", " ", value)

    return value


def _comment_key(text: str) -> str:
    value = text.casefold()
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _is_meaningful_comment(text: str) -> bool:
    """
    Remove blank, ultra-short, and generic feedback.
    """
    if not text:
        return False

    key = _comment_key(text)

    if key in LOW_VALUE_COMMENTS:
        return False

    # Ignore very short generic text.
    if len(key) < 8:
        return False

    # Keep comments that communicate some actual observation.
    word_count = len(key.split())
    if word_count < 3:
        return False

    return True


def extract_meaningful_comments(
    df: pd.DataFrame,
    comments_column: Optional[str],
    max_comments: int = DEFAULT_MAX_COMMENTS,
) -> List[str]:
    """
    Pick up to max_comments useful, non-duplicate student comments.

    Preference:
    - meaningful comments
    - slightly longer comments
    - unique wording
    """
    if (
        not comments_column
        or comments_column not in df.columns
        or df.empty
    ):
        return []

    comments: List[str] = []
    seen = set()

    for raw in df[comments_column].tolist():
        text = _normalize_comment(raw)

        if not _is_meaningful_comment(text):
            continue

        key = _comment_key(text)

        if key in seen:
            continue

        seen.add(key)
        comments.append(text)

    # Prefer comments with useful detail but avoid extremely long text.
    comments.sort(
        key=lambda x: (
            abs(len(x.split()) - 12),
            len(x)
        )
    )

    return comments[:max_comments]


# ============================================================
# OVERALL RATING ANALYSIS
# ============================================================

def calculate_rating_distribution(
    df: pd.DataFrame,
    rating_column: Optional[str],
) -> Dict[str, Any]:
    """
    Analyze overall 1-5 star ratings.
    """
    result = {
        "average": None,
        "valid_count": 0,
        "positive_count": 0,
        "positive_percent": None,
        "5": 0,
        "4": 0,
        "3": 0,
        "2": 0,
        "1": 0,
    }

    if (
        not rating_column
        or rating_column not in df.columns
        or df.empty
    ):
        return result

    ratings = _to_numeric_series(df[rating_column]).dropna()

    # Keep only plausible 1-5 ratings.
    ratings = ratings[
        (ratings >= STAR_RATING_MIN)
        & (ratings <= STAR_RATING_MAX)
    ]

    if ratings.empty:
        return result

    result["average"] = round(float(ratings.mean()), 2)
    result["valid_count"] = int(len(ratings))

    positive_count = int(
        (ratings >= POSITIVE_STAR_THRESHOLD).sum()
    )

    result["positive_count"] = positive_count
    result["positive_percent"] = _percent(
        positive_count,
        len(ratings),
    )

    # Count each star after nearest-integer rounding.
    rounded = ratings.round().astype(int)

    for star in [5, 4, 3, 2, 1]:
        result[str(star)] = int((rounded == star).sum())

    return result


# ============================================================
# DETAILED PARAMETER ANALYSIS
# ============================================================

def calculate_parameter_score(
    df: pd.DataFrame,
    column_name: Optional[str],
    parameter_key: str,
) -> ParameterScore:
    """
    Calculate average and positive percentage for one detailed parameter.
    """
    label = PARAMETER_LABELS[parameter_key]

    if (
        not column_name
        or column_name not in df.columns
        or df.empty
    ):
        return ParameterScore(
            key=parameter_key,
            label=label,
            average=None,
            count=0,
            positive_count=0,
            positive_percent=None,
            min_score=None,
            max_score=None,
        )

    values = _to_numeric_series(df[column_name]).dropna()

    # Keep only scores within the intended -2 to +2 scale.
    values = values[
        (values >= DETAIL_SCORE_MIN)
        & (values <= DETAIL_SCORE_MAX)
    ]

    if values.empty:
        return ParameterScore(
            key=parameter_key,
            label=label,
            average=None,
            count=0,
            positive_count=0,
            positive_percent=None,
            min_score=None,
            max_score=None,
        )

    positive_count = int(
        (values >= POSITIVE_DETAIL_THRESHOLD).sum()
    )

    return ParameterScore(
        key=parameter_key,
        label=label,
        average=round(float(values.mean()), 2),
        count=int(len(values)),
        positive_count=positive_count,
        positive_percent=_percent(
            positive_count,
            len(values),
        ),
        min_score=round(float(values.min()), 2),
        max_score=round(float(values.max()), 2),
    )


def calculate_all_parameter_scores(
    df: pd.DataFrame,
    column_map: Dict[str, Optional[str]],
) -> List[ParameterScore]:
    scores: List[ParameterScore] = []

    for key in PARAMETER_ORDER:
        scores.append(
            calculate_parameter_score(
                df=df,
                column_name=column_map.get(key),
                parameter_key=key,
            )
        )

    return scores


def calculate_detail_positive_summary(
    parameter_scores: Sequence[ParameterScore],
) -> Tuple[int, int, Optional[float]]:
    """
    Calculate overall detailed positive percentage across all parameters.
    """
    positive = sum(p.positive_count for p in parameter_scores)
    total = sum(p.count for p in parameter_scores)

    return positive, total, _percent(positive, total)


# ============================================================
# STRENGTH / DEVELOPMENT LOGIC
# ============================================================

def _available_parameter_scores(
    parameter_scores: Sequence[ParameterScore],
) -> List[ParameterScore]:
    return [
        p for p in parameter_scores
        if p.average is not None
    ]


def identify_strengths(
    parameter_scores: Sequence[ParameterScore],
    max_items: int = 3,
) -> List[str]:
    """
    Highest scoring parameters become strengths.
    """
    available = _available_parameter_scores(parameter_scores)

    if not available:
        return []

    ranked = sorted(
        available,
        key=lambda p: (
            p.average if p.average is not None else -999
        ),
        reverse=True,
    )

    return [p.label for p in ranked[:max_items]]


def identify_development_focus(
    parameter_scores: Sequence[ParameterScore],
    max_items: int = 2,
) -> List[str]:
    """
    Lowest scoring parameters become development focus areas.

    This does NOT label them as weaknesses. A trainer may still have
    good scores across all parameters.
    """
    available = _available_parameter_scores(parameter_scores)

    if not available:
        return []

    ranked = sorted(
        available,
        key=lambda p: (
            p.average if p.average is not None else 999
        ),
    )

    return [p.label for p in ranked[:max_items]]


# ============================================================
# OVERALL LABEL / MANAGEMENT SUMMARY
# ============================================================

def classify_overall_performance(
    overall_rating: Optional[float],
    parameter_scores: Sequence[ParameterScore],
) -> str:
    """
    Human-readable overall label.

    Primary source:
        1-5 overall rating

    Fallback:
        average detailed parameter score (-2 to +2)
    """
    if overall_rating is not None:
        if overall_rating >= 4.75:
            return "Excellent"
        if overall_rating >= 4.25:
            return "Very Good"
        if overall_rating >= 3.75:
            return "Good"
        if overall_rating >= 3.00:
            return "Needs Improvement"
        return "Significant Improvement Required"

    available = [
        p.average
        for p in parameter_scores
        if p.average is not None
    ]

    if not available:
        return "Not Available"

    avg_detail = float(np.mean(available))

    if avg_detail >= 1.50:
        return "Excellent"
    if avg_detail >= 1.00:
        return "Very Good"
    if avg_detail >= 0.50:
        return "Good"
    if avg_detail >= 0.00:
        return "Needs Improvement"
    return "Significant Improvement Required"


def build_management_summary(
    trainer_name: str,
    overall_label: str,
    strengths: Sequence[str],
    development_focus: Sequence[str],
    positive_rating_percent: Optional[float],
) -> str:
    """
    Generate a concise management-style statement for the report.
    """
    parts: List[str] = []

    if positive_rating_percent is not None:
        parts.append(
            f"{positive_rating_percent:.1f}% of valid overall ratings "
            "were 4-star or 5-star."
        )

    if strengths:
        if len(strengths) == 1:
            strength_text = strengths[0]
        else:
            strength_text = ", ".join(strengths[:-1]) + \
                f" and {strengths[-1]}"

        parts.append(
            f"Key strengths are {strength_text}."
        )

    if development_focus:
        if len(development_focus) == 1:
            focus_text = development_focus[0]
        else:
            focus_text = ", ".join(development_focus[:-1]) + \
                f" and {development_focus[-1]}"

        parts.append(
            f"Development focus can be placed on {focus_text}."
        )

    if not parts:
        return (
            f"{trainer_name} is classified as {overall_label}; "
            "additional valid feedback is required for detailed analysis."
        )

    return " ".join(parts)


# ============================================================
# TRAINER ANALYSIS
# ============================================================

def analyze_trainer(
    campus: CampusFeedback,
    trainer_name: str,
    max_comments: int = DEFAULT_MAX_COMMENTS,
) -> TrainerAnalysis:
    """
    Analyze one trainer inside one campus.

    No data from any other campus is used.
    """
    trainer_df = campus.trainer_dataframe(trainer_name)

    rating = calculate_rating_distribution(
        trainer_df,
        campus.column_map.get("rating"),
    )

    parameter_scores = calculate_all_parameter_scores(
        trainer_df,
        campus.column_map,
    )

    detail_positive_count, detail_total_count, detail_positive_percent = (
        calculate_detail_positive_summary(parameter_scores)
    )

    strengths = identify_strengths(parameter_scores)
    development_focus = identify_development_focus(parameter_scores)

    comments = extract_meaningful_comments(
        trainer_df,
        campus.column_map.get("comments"),
        max_comments=max_comments,
    )

    overall_label = classify_overall_performance(
        rating["average"],
        parameter_scores,
    )

    summary = build_management_summary(
        trainer_name=trainer_name,
        overall_label=overall_label,
        strengths=strengths,
        development_focus=development_focus,
        positive_rating_percent=rating["positive_percent"],
    )

    return TrainerAnalysis(
        campus_name=campus.campus_name,
        trainer_name=trainer_name,
        responses=int(len(trainer_df)),

        overall_rating=rating["average"],
        positive_rating_count=rating["positive_count"],
        positive_rating_percent=rating["positive_percent"],

        five_star_count=rating["5"],
        four_star_count=rating["4"],
        three_star_count=rating["3"],
        two_star_count=rating["2"],
        one_star_count=rating["1"],

        detail_positive_count=detail_positive_count,
        detail_total_count=detail_total_count,
        detail_positive_percent=detail_positive_percent,

        parameter_scores=parameter_scores,

        strengths=strengths,
        development_focus=development_focus,
        student_voice=comments,

        overall_label=overall_label,
        management_summary=summary,
    )


# ============================================================
# CAMPUS ANALYSIS
# ============================================================

def analyze_campus(
    campus: CampusFeedback,
    max_comments: int = DEFAULT_MAX_COMMENTS,
) -> List[TrainerAnalysis]:
    """
    Analyze every trainer in one campus.

    Trainer order follows the order found in the uploaded Excel file.
    """
    analyses: List[TrainerAnalysis] = []

    for trainer_name in campus.trainers:
        analyses.append(
            analyze_trainer(
                campus=campus,
                trainer_name=trainer_name,
                max_comments=max_comments,
            )
        )

    return analyses


def build_trainer_summary_table(
    campus: CampusFeedback,
) -> pd.DataFrame:
    """
    Build the compact table shown directly under each campus section.

    Suggested Page 15 display:
        Trainer Name | Responses | Rating | Positive % | Performance
    """
    analyses = analyze_campus(campus)

    rows: List[Dict[str, Any]] = []

    for item in analyses:
        rows.append({
            "Trainer Name": item.trainer_name,
            "Responses": item.responses,
            "Rating": item.overall_rating,
            "Positive %": item.positive_rating_percent,
            "Performance": item.overall_label,
        })

    if not rows:
        return pd.DataFrame(
            columns=[
                "Trainer Name",
                "Responses",
                "Rating",
                "Positive %",
                "Performance",
            ]
        )

    return pd.DataFrame(rows)


# ============================================================
# REPORT-FRIENDLY DICTIONARIES
# ============================================================

def trainer_analysis_to_report_dict(
    analysis: TrainerAnalysis,
) -> Dict[str, Any]:
    """
    Convert TrainerAnalysis to a simple dictionary for the image/PDF/PPT
    generator files.

    This keeps report-generation code independent from pandas.
    """
    parameter_dicts = []

    for p in analysis.parameter_scores:
        parameter_dicts.append({
            "key": p.key,
            "label": p.label,
            "average": p.average,
            "count": p.count,
            "positive_count": p.positive_count,
            "positive_percent": p.positive_percent,
        })

    return {
        "campus_name": analysis.campus_name,
        "trainer_name": analysis.trainer_name,
        "responses": analysis.responses,

        "overall_rating": analysis.overall_rating,
        "positive_rating_percent": analysis.positive_rating_percent,
        "detail_positive_percent": analysis.detail_positive_percent,

        "rating_distribution": {
            "5": analysis.five_star_count,
            "4": analysis.four_star_count,
            "3": analysis.three_star_count,
            "2": analysis.two_star_count,
            "1": analysis.one_star_count,
        },

        "parameters": parameter_dicts,
        "strengths": analysis.strengths,
        "development_focus": analysis.development_focus,
        "student_voice": analysis.student_voice,

        "overall_label": analysis.overall_label,
        "management_summary": analysis.management_summary,
    }


def campus_report_data(
    campus: CampusFeedback,
) -> List[Dict[str, Any]]:
    """
    Return report-ready dictionaries for all trainers in one campus.
    """
    return [
        trainer_analysis_to_report_dict(item)
        for item in analyze_campus(campus)
    ]


# ============================================================
# OPTIONAL CAMPUS STATISTICS
# ============================================================

def campus_basic_statistics(
    campus: CampusFeedback,
) -> Dict[str, Any]:
    """
    Campus-level statistics for the campus heading only.

    IMPORTANT:
    This summarizes trainers within ONE campus.
    It does not compare or combine multiple campuses.
    """
    analyses = analyze_campus(campus)

    valid_ratings = [
        a.overall_rating
        for a in analyses
        if a.overall_rating is not None
    ]

    best_trainer = None
    best_rating = None

    if valid_ratings:
        valid_analyses = [
            a for a in analyses
            if a.overall_rating is not None
        ]

        best = max(
            valid_analyses,
            key=lambda x: x.overall_rating,
        )

        best_trainer = best.trainer_name
        best_rating = best.overall_rating

    return {
        "campus_name": campus.campus_name,
        "total_trainers": campus.total_trainers,
        "total_responses": campus.total_responses,
        "average_trainer_rating": (
            round(float(np.mean(valid_ratings)), 2)
            if valid_ratings else None
        ),
        "highest_rated_trainer": best_trainer,
        "highest_rating": best_rating,
    }


# ============================================================
# VALIDATION
# ============================================================

def validate_feedback_for_analysis(
    campus: CampusFeedback,
) -> List[str]:
    """
    Return analysis-related validation messages.

    The UI can show these before enabling report generation.
    """
    messages: List[str] = []

    if campus.dataframe.empty:
        messages.append(
            "No feedback rows are available in the selected sheet."
        )

    if not campus.column_map.get("trainer"):
        messages.append(
            "Trainer Name column must be mapped before analysis."
        )

    if campus.total_trainers == 0:
        messages.append(
            "No trainer names were found in the mapped Trainer column."
        )

    if not campus.column_map.get("rating"):
        messages.append(
            "Overall Rating column is not mapped. "
            "Reports can still use detailed parameter scores."
        )

    detected_parameters = [
        key
        for key in PARAMETER_ORDER
        if campus.column_map.get(key)
    ]

    if not detected_parameters:
        messages.append(
            "No detailed feedback parameter columns are mapped."
        )

    return messages
