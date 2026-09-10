
"""
16_Feedback_Analytics.py
------------------------
Campus/college-wise Trainer Feedback Analytics and Report Generator.

Save at:
    TrainerProfileGenerator/pages/16_Feedback_Analytics.py

Design:
- Upload multiple campus/college Excel feedback files together.
- Each uploaded file remains completely independent.
- Display Campus 1 -> trainers -> trainer actions -> campus actions.
- Then Campus 2 -> trainers -> trainer actions -> campus actions.
- Never combine trainers across different campuses/colleges.
- Campus Consolidated Summary is also campus-specific only.

Required helper files:
    utils/feedback_loader.py
    utils/feedback_analysis.py
    utils/feedback_image_generator.py
    utils/feedback_pdf_generator.py
    utils/feedback_ppt_generator.py
    utils/feedback_zip_generator.py
    templates/feedback_report_config.py
"""

from __future__ import annotations

import hashlib
import io
import os
import re
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

from login import require_login

from utils.feedback_loader import (
    CampusFeedback,
    apply_manual_column_mapping,
    load_multiple_feedback_files,
    rename_campus,
)
from utils.feedback_analysis import (
    TrainerAnalysis,
    analyze_campus,
    campus_basic_statistics,
    trainer_analysis_to_report_dict,
    validate_feedback_for_analysis,
)
from utils.feedback_image_generator import (
    generate_trainer_report_image_bytes,
)
from utils.feedback_pdf_generator import (
    generate_campus_pdf_bytes,
    generate_trainer_pdf_bytes,
)
from utils.feedback_ppt_generator import (
    generate_campus_ppt_bytes,
)
from utils.feedback_html_generator import (
    generate_campus_html_bytes,
)
from utils.feedback_zip_generator import (
    generate_campus_zip_bytes,
)
from templates.feedback_report_config import (
    PAGE_TITLE,
    PAGE_SUBTITLE,
    UPLOAD_LABEL,
    SUPPORTED_FEEDBACK_FILE_TYPES,
    CAMPUS_ACTION_GENERATE_IMAGES,
    CAMPUS_ACTION_GENERATE_PDFS,
    CAMPUS_ACTION_GENERATE_CAMPUS_PDF,
    CAMPUS_ACTION_GENERATE_CAMPUS_PPT,
    CAMPUS_ACTION_DOWNLOAD_ZIP,
    TRAINER_ACTION_VIEW,
    TRAINER_ACTION_IMAGE,
    TRAINER_ACTION_PDF,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

require_login()


# ============================================================
# PAGE STYLING
# ============================================================

st.markdown(
    """
    <style>
        .feedback-title {
            color: #173A63;
            font-size: 2.15rem;
            font-weight: 800;
            margin-bottom: 0.15rem;
        }

        .feedback-subtitle {
            color: #667085;
            font-size: 1rem;
            margin-bottom: 1rem;
        }

        .campus-banner {
            background: linear-gradient(90deg, #173A63, #2E67A3);
            color: #FFFFFF;
            padding: 13px 18px;
            border-radius: 10px;
            font-size: 1.25rem;
            font-weight: 750;
            margin: 4px 0 8px 0;
        }

        .campus-note {
            color: #667085;
            font-size: 0.92rem;
            margin-bottom: 10px;
        }

        .trainer-table-head {
            background: #EEF3F8;
            color: #344054;
            padding: 8px 10px;
            border-radius: 7px;
            font-weight: 700;
            text-align: left;
        }

        .trainer-name-cell {
            color: #173A63;
            font-weight: 700;
            padding-top: 0.55rem;
        }

        .trainer-data-cell {
            color: #344054;
            padding-top: 0.55rem;
        }

        .section-heading {
            color: #173A63;
            font-size: 1.05rem;
            font-weight: 750;
            margin-top: 12px;
            margin-bottom: 6px;
        }

        .small-note {
            background: #F8FAFC;
            border-left: 4px solid #FF8A34;
            color: #475467;
            padding: 9px 12px;
            border-radius: 6px;
            margin: 8px 0 12px 0;
        }

        .mapping-ok {
            background: #EEF7F2;
            border: 1px solid #CDE8D6;
            color: #235B3A;
            padding: 8px 12px;
            border-radius: 7px;
            margin-bottom: 8px;
        }

        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #D9E0EA;
            border-radius: 9px;
            padding: 10px 12px;
        }

        div[data-testid="stFileUploader"] {
            background: #FFFFFF;
            border: 1px solid #D9E0EA;
            border-radius: 10px;
            padding: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONSTANTS
# ============================================================

CONSOLIDATED_ACTION = "Generate Consolidated Summary"

MAPPING_FIELDS = [
    ("trainer", "Trainer Name"),
    ("rating", "Overall Rating"),
    ("clarity", "Clarity of Explanation"),
    ("communication", "Communication & Interaction"),
    ("technical", "Technical Knowledge & Confidence"),
    ("hands_on", "Hands-on Support"),
    ("industry_relevance", "Industry-Relevant Examples"),
    ("professionalism", "Punctuality & Professionalism"),
    ("comments", "Student Comments / Suggestions"),
]


# ============================================================
# GENERAL HELPERS
# ============================================================

def _safe_slug(value: Any) -> str:
    text = str(value or "").strip()
    text = re.sub(r'[<>:"/\\|?*]+', "_", text)
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("._") or "item"


def _file_signature(uploaded_file: Any) -> str:
    try:
        raw = uploaded_file.getvalue()
    except Exception:
        raw = bytes(str(getattr(uploaded_file, "name", "")), "utf-8")

    digest = hashlib.md5(raw).hexdigest()[:10]
    name = _safe_slug(getattr(uploaded_file, "name", "feedback"))
    return f"{name}_{digest}"


def _rating_text(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return f"{value:.2f}"


def _percent_text(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return f"{value:.1f}%"


def _get_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = []

    if bold:
        candidates.extend(
            [
                r"C:\Windows\Fonts\arialbd.ttf",
                r"C:\Windows\Fonts\calibrib.ttf",
                r"C:\Windows\Fonts\segoeuib.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            ]
        )
    else:
        candidates.extend(
            [
                r"C:\Windows\Fonts\arial.ttf",
                r"C:\Windows\Fonts\calibri.ttf",
                r"C:\Windows\Fonts\segoeui.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
                "/System/Library/Fonts/Supplemental/Arial.ttf",
            ]
        )

    for font_path in candidates:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size=size)
            except Exception:
                pass

    return ImageFont.load_default()


def _fit_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    start_size: int,
    min_size: int = 18,
    bold: bool = False,
) -> ImageFont.ImageFont:
    size = start_size

    while size >= min_size:
        font = _get_font(size, bold=bold)
        bbox = draw.textbbox((0, 0), text, font=font)

        if (bbox[2] - bbox[0]) <= max_width:
            return font

        size -= 2

    return _get_font(min_size, bold=bold)


# ============================================================
# CAMPUS CONSOLIDATED SUMMARY
# ============================================================

def _ranked_trainer_rows(
    analyses: Sequence[TrainerAnalysis],
) -> List[Dict[str, Any]]:
    """
    Campus-only ranking.

    Per trainer, the consolidated report intentionally shows:
        Rank
        Trainer Name
        Average Rating

    This matches the requirement for averages + ranking only.
    """
    valid = list(analyses)

    valid.sort(
        key=lambda item: (
            item.overall_rating is not None,
            item.overall_rating if item.overall_rating is not None else -999,
            item.responses,
        ),
        reverse=True,
    )

    rows: List[Dict[str, Any]] = []

    for rank, item in enumerate(valid, start=1):
        rows.append(
            {
                "Rank": rank,
                "Trainer Name": item.trainer_name,
                "Average Rating": item.overall_rating,
            }
        )

    return rows


def _campus_average_rating(
    analyses: Sequence[TrainerAnalysis],
) -> Optional[float]:
    valid = [
        item.overall_rating
        for item in analyses
        if item.overall_rating is not None
    ]

    if not valid:
        return None

    return round(sum(valid) / len(valid), 2)


def generate_consolidated_summary_image_bytes(
    campus_name: str,
    analyses: Sequence[TrainerAnalysis],
) -> bytes:
    """
    Generate ONE campus-specific image containing all trainer averages
    and ranking.

    No trainers from any other campus are included.
    """
    rows = _ranked_trainer_rows(analyses)

    width = 1600
    row_height = 72
    header_height = 330
    footer_height = 120

    # Keep it as one image/page. Height expands if the campus has
    # many trainers.
    height = max(
        1100,
        header_height + (max(len(rows), 1) * row_height) + footer_height,
    )

    image = Image.new(
        "RGB",
        (width, height),
        "#F6F8FC",
    )
    draw = ImageDraw.Draw(image)

    # Header
    draw.rectangle(
        (0, 0, width, 230),
        fill="#173A63",
    )
    draw.rectangle(
        (0, 0, 18, 230),
        fill="#FF8A34",
    )

    draw.text(
        (70, 48),
        "CAMPUS TRAINER FEEDBACK SUMMARY",
        font=_get_font(48, bold=True),
        fill="#FFFFFF",
    )

    campus_font = _fit_text(
        draw,
        campus_name,
        max_width=width - 140,
        start_size=40,
        min_size=24,
        bold=True,
    )

    draw.text(
        (70, 126),
        campus_name,
        font=campus_font,
        fill="#DCE8F4",
    )

    campus_avg = _campus_average_rating(analyses)

    # Summary cards
    card_y = 265
    card_h = 125
    gap = 24
    card_w = (width - 140 - gap * 2) // 3
    card_x = 70

    summary_cards = [
        ("TOTAL TRAINERS", str(len(rows))),
        (
            "CAMPUS AVG RATING",
            f"{campus_avg:.2f} / 5" if campus_avg is not None else "N/A",
        ),
        (
            "HIGHEST RATING",
            (
                f"{rows[0]['Average Rating']:.2f} / 5"
                if rows and rows[0]["Average Rating"] is not None
                else "N/A"
            ),
        ),
    ]

    for idx, (label, value) in enumerate(summary_cards):
        left = card_x + idx * (card_w + gap)
        right = left + card_w

        draw.rounded_rectangle(
            (left, card_y, right, card_y + card_h),
            radius=20,
            fill="#FFFFFF",
            outline="#D9E0EA",
            width=2,
        )

        draw.text(
            (left + 24, card_y + 20),
            label,
            font=_get_font(20, bold=True),
            fill="#667085",
        )

        draw.text(
            (left + 24, card_y + 57),
            value,
            font=_get_font(34, bold=True),
            fill="#1F2937",
        )

    # Table
    table_x = 70
    table_y = 435
    table_w = width - 140

    rank_w = 160
    rating_w = 290
    name_w = table_w - rank_w - rating_w

    draw.rounded_rectangle(
        (
            table_x,
            table_y,
            table_x + table_w,
            table_y + 62,
        ),
        radius=12,
        fill="#E8EEF5",
    )

    draw.text(
        (table_x + 28, table_y + 17),
        "RANK",
        font=_get_font(23, bold=True),
        fill="#344054",
    )

    draw.text(
        (table_x + rank_w + 20, table_y + 17),
        "TRAINER NAME",
        font=_get_font(23, bold=True),
        fill="#344054",
    )

    draw.text(
        (
            table_x + rank_w + name_w + 20,
            table_y + 17,
        ),
        "AVERAGE RATING",
        font=_get_font(23, bold=True),
        fill="#344054",
    )

    y = table_y + 72

    if not rows:
        draw.text(
            (table_x + 30, y + 12),
            "No trainer feedback data available.",
            font=_get_font(25),
            fill="#667085",
        )
    else:
        for index, row in enumerate(rows):
            fill = "#FFFFFF" if index % 2 == 0 else "#F9FBFD"

            draw.rounded_rectangle(
                (
                    table_x,
                    y,
                    table_x + table_w,
                    y + 60,
                ),
                radius=8,
                fill=fill,
                outline="#E4E9F0",
                width=1,
            )

            rank_text = str(row["Rank"])
            trainer_name = str(row["Trainer Name"])

            avg = row["Average Rating"]
            rating_text = (
                f"{avg:.2f} / 5"
                if avg is not None
                else "N/A"
            )

            draw.text(
                (table_x + 47, y + 15),
                rank_text,
                font=_get_font(24, bold=True),
                fill="#173A63",
            )

            trainer_font = _fit_text(
                draw,
                trainer_name,
                max_width=name_w - 55,
                start_size=25,
                min_size=18,
                bold=True,
            )

            draw.text(
                (
                    table_x + rank_w + 20,
                    y + 15,
                ),
                trainer_name,
                font=trainer_font,
                fill="#1F2937",
            )

            draw.text(
                (
                    table_x + rank_w + name_w + 20,
                    y + 15,
                ),
                rating_text,
                font=_get_font(24, bold=True),
                fill="#173A63",
            )

            y += row_height

    draw.text(
        (70, height - 70),
        "Ranking is based on the average overall trainer rating within this campus only.",
        font=_get_font(20),
        fill="#667085",
    )

    output = io.BytesIO()

    image.save(
        output,
        format="PNG",
        optimize=True,
    )
    output.seek(0)

    return output.getvalue()


def consolidated_summary_pdf_bytes(
    campus_name: str,
    analyses: Sequence[TrainerAnalysis],
) -> bytes:
    """
    Convert the campus consolidated summary image into a one-page PDF.
    """
    image_bytes = generate_consolidated_summary_image_bytes(
        campus_name,
        analyses,
    )

    image_stream = io.BytesIO(image_bytes)
    pdf_stream = io.BytesIO()

    with Image.open(image_stream) as image:
        if image.mode != "RGB":
            image = image.convert("RGB")

        image.save(
            pdf_stream,
            format="PDF",
            resolution=150.0,
            save_all=False,
        )

    pdf_stream.seek(0)
    return pdf_stream.getvalue()


# ============================================================
# BULK ZIP HELPERS
# ============================================================

def generate_images_zip_bytes(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
) -> bytes:
    output = io.BytesIO()

    with zipfile.ZipFile(
        output,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zf:
        for report in reports:
            current = dict(report)
            current["campus_name"] = campus_name

            trainer_name = current.get(
                "trainer_name",
                "Trainer",
            )

            image_bytes = generate_trainer_report_image_bytes(
                current
            )

            zf.writestr(
                (
                    f"{_safe_slug(trainer_name)}_"
                    "Feedback_Report.png"
                ),
                image_bytes,
            )

    output.seek(0)
    return output.getvalue()


def generate_individual_pdfs_zip_bytes(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
) -> bytes:
    output = io.BytesIO()

    with zipfile.ZipFile(
        output,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zf:
        for report in reports:
            current = dict(report)
            current["campus_name"] = campus_name

            trainer_name = current.get(
                "trainer_name",
                "Trainer",
            )

            pdf_bytes = generate_trainer_pdf_bytes(
                current
            )

            zf.writestr(
                (
                    f"{_safe_slug(trainer_name)}_"
                    "Feedback_Report.pdf"
                ),
                pdf_bytes,
            )

    output.seek(0)
    return output.getvalue()


# ============================================================
# COLUMN MAPPING UI
# ============================================================

def render_column_mapping(
    campus: CampusFeedback,
    campus_key: str,
) -> CampusFeedback:
    """
    Allow the user to review or correct automatic column detection.
    """
    all_columns = list(campus.dataframe.columns)
    options = ["-- Not Available --"] + all_columns

    manual_mapping: Dict[str, Optional[str]] = {}

    with st.expander(
        "Column Mapping",
        expanded=False,
    ):
        st.caption(
            "The app automatically detects the standard feedback columns. "
            "Change a mapping only when a campus uses different headings."
        )

        col1, col2 = st.columns(2)

        for index, (field_name, display_name) in enumerate(
            MAPPING_FIELDS
        ):
            detected = campus.column_map.get(field_name)

            try:
                default_index = (
                    options.index(detected)
                    if detected in options
                    else 0
                )
            except Exception:
                default_index = 0

            target_col = col1 if index % 2 == 0 else col2

            selected = target_col.selectbox(
                display_name,
                options=options,
                index=default_index,
                key=f"map_{campus_key}_{field_name}",
            )

            manual_mapping[field_name] = (
                None
                if selected == "-- Not Available --"
                else selected
            )

        campus = apply_manual_column_mapping(
            campus,
            manual_mapping,
        )

    return campus


# ============================================================
# TRAINER REPORT DISPLAY
# ============================================================

def render_trainer_report_preview(
    analysis: TrainerAnalysis,
    report: Dict[str, Any],
    trainer_key: str,
) -> None:
    """
    Show the selected trainer report below the trainer row.
    """
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Overall Rating",
        (
            f"{analysis.overall_rating:.2f} / 5"
            if analysis.overall_rating is not None
            else "N/A"
        ),
    )
    c2.metric(
        "Responses",
        analysis.responses,
    )
    c3.metric(
        "Positive Feedback",
        _percent_text(
            analysis.positive_rating_percent
        ),
    )
    c4.metric(
        "Performance",
        analysis.overall_label,
    )

    image_bytes = generate_trainer_report_image_bytes(
        report
    )

    st.image(
        image_bytes,
        use_container_width=True,
    )

    d1, d2 = st.columns(2)

    d1.download_button(
        "Download Image",
        data=image_bytes,
        file_name=(
            f"{_safe_slug(analysis.trainer_name)}_"
            "Feedback_Report.png"
        ),
        mime="image/png",
        key=f"download_preview_img_{trainer_key}",
        use_container_width=True,
    )

    pdf_bytes = generate_trainer_pdf_bytes(
        report
    )

    d2.download_button(
        "Download PDF",
        data=pdf_bytes,
        file_name=(
            f"{_safe_slug(analysis.trainer_name)}_"
            "Feedback_Report.pdf"
        ),
        mime="application/pdf",
        key=f"download_preview_pdf_{trainer_key}",
        use_container_width=True,
    )


def render_trainer_rows(
    campus: CampusFeedback,
    analyses: Sequence[TrainerAnalysis],
    campus_key: str,
) -> None:
    """
    Display trainer list and individual trainer actions.
    """
    st.markdown(
        '<div class="section-heading">Trainer Reports</div>',
        unsafe_allow_html=True,
    )

    h1, h2, h3, h4, h5, h6 = st.columns(
        [3.5, 1.1, 1.15, 1.2, 1.25, 1.25]
    )

    h1.markdown(
        '<div class="trainer-table-head">Trainer Name</div>',
        unsafe_allow_html=True,
    )
    h2.markdown(
        '<div class="trainer-table-head">Responses</div>',
        unsafe_allow_html=True,
    )
    h3.markdown(
        '<div class="trainer-table-head">Rating</div>',
        unsafe_allow_html=True,
    )
    h4.markdown(
        '<div class="trainer-table-head">Report</div>',
        unsafe_allow_html=True,
    )
    h5.markdown(
        '<div class="trainer-table-head">Image</div>',
        unsafe_allow_html=True,
    )
    h6.markdown(
        '<div class="trainer-table-head">PDF</div>',
        unsafe_allow_html=True,
    )

    for index, analysis in enumerate(
        analyses,
        start=1,
    ):
        trainer_slug = _safe_slug(
            analysis.trainer_name
        )
        trainer_key = (
            f"{campus_key}_{index}_{trainer_slug}"
        )

        report = trainer_analysis_to_report_dict(
            analysis
        )

        r1, r2, r3, r4, r5, r6 = st.columns(
            [3.5, 1.1, 1.15, 1.2, 1.25, 1.25]
        )

        r1.markdown(
            (
                f'<div class="trainer-name-cell">'
                f'{analysis.trainer_name}'
                f'</div>'
            ),
            unsafe_allow_html=True,
        )

        r2.markdown(
            (
                f'<div class="trainer-data-cell">'
                f'{analysis.responses}'
                f'</div>'
            ),
            unsafe_allow_html=True,
        )

        r3.markdown(
            (
                f'<div class="trainer-data-cell">'
                f'{_rating_text(analysis.overall_rating)}'
                f'</div>'
            ),
            unsafe_allow_html=True,
        )

        view_key = f"view_state_{trainer_key}"

        if view_key not in st.session_state:
            st.session_state[view_key] = False

        if r4.button(
            TRAINER_ACTION_VIEW,
            key=f"view_btn_{trainer_key}",
            use_container_width=True,
        ):
            st.session_state[view_key] = (
                not st.session_state[view_key]
            )

        image_state_key = (
            f"trainer_image_{trainer_key}"
        )

        if r5.button(
            TRAINER_ACTION_IMAGE,
            key=f"image_btn_{trainer_key}",
            use_container_width=True,
        ):
            with st.spinner(
                f"Generating image for {analysis.trainer_name}..."
            ):
                st.session_state[
                    image_state_key
                ] = generate_trainer_report_image_bytes(
                    report
                )

        pdf_state_key = (
            f"trainer_pdf_{trainer_key}"
        )

        if r6.button(
            TRAINER_ACTION_PDF,
            key=f"pdf_btn_{trainer_key}",
            use_container_width=True,
        ):
            with st.spinner(
                f"Generating PDF for {analysis.trainer_name}..."
            ):
                st.session_state[
                    pdf_state_key
                ] = generate_trainer_pdf_bytes(
                    report
                )

        # Generated individual image download
        if image_state_key in st.session_state:
            r5.download_button(
                "Download",
                data=st.session_state[
                    image_state_key
                ],
                file_name=(
                    f"{trainer_slug}_"
                    "Feedback_Report.png"
                ),
                mime="image/png",
                key=f"image_download_{trainer_key}",
                use_container_width=True,
            )

        # Generated individual PDF download
        if pdf_state_key in st.session_state:
            r6.download_button(
                "Download",
                data=st.session_state[
                    pdf_state_key
                ],
                file_name=(
                    f"{trainer_slug}_"
                    "Feedback_Report.pdf"
                ),
                mime="application/pdf",
                key=f"pdf_download_{trainer_key}",
                use_container_width=True,
            )

        if st.session_state[view_key]:
            with st.container(border=True):
                render_trainer_report_preview(
                    analysis,
                    report,
                    trainer_key,
                )


# ============================================================
# CAMPUS ACTIONS
# ============================================================

def render_campus_actions(
    campus: CampusFeedback,
    analyses: Sequence[TrainerAnalysis],
    campus_key: str,
) -> None:
    """
    Campus-specific report actions.

    Every generated file contains trainers from this campus only.
    """
    reports = [
        trainer_analysis_to_report_dict(
            analysis
        )
        for analysis in analyses
    ]

    campus_slug = _safe_slug(
        campus.campus_name
    )

    st.markdown(
        '<div class="section-heading">Campus Actions</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # ROW 1
    # Consolidated + Images + PDFs
    # --------------------------------------------------------
    a1, a2, a3 = st.columns(3)

    consolidated_state = (
        f"consolidated_{campus_key}"
    )
    images_state = (
        f"all_images_{campus_key}"
    )
    pdfs_state = (
        f"all_pdfs_{campus_key}"
    )

    if a1.button(
        CONSOLIDATED_ACTION,
        key=f"btn_consolidated_{campus_key}",
        use_container_width=True,
    ):
        with st.spinner(
            f"Generating {campus.campus_name} consolidated summary..."
        ):
            st.session_state[
                consolidated_state
            ] = {
                "image": generate_consolidated_summary_image_bytes(
                    campus.campus_name,
                    analyses,
                ),
                "pdf": consolidated_summary_pdf_bytes(
                    campus.campus_name,
                    analyses,
                ),
            }

    if a2.button(
        CAMPUS_ACTION_GENERATE_IMAGES,
        key=f"btn_all_images_{campus_key}",
        use_container_width=True,
    ):
        with st.spinner(
            f"Generating all trainer images for {campus.campus_name}..."
        ):
            st.session_state[
                images_state
            ] = generate_images_zip_bytes(
                campus.campus_name,
                reports,
            )

    if a3.button(
        CAMPUS_ACTION_GENERATE_PDFS,
        key=f"btn_all_pdfs_{campus_key}",
        use_container_width=True,
    ):
        with st.spinner(
            f"Generating all trainer PDFs for {campus.campus_name}..."
        ):
            st.session_state[
                pdfs_state
            ] = generate_individual_pdfs_zip_bytes(
                campus.campus_name,
                reports,
            )

    # --------------------------------------------------------
    # ROW 2
    # Campus PDF + Campus PPT + Campus HTML + Full ZIP
    # --------------------------------------------------------
    b1, b2, b3, b4 = st.columns(4)

    campus_pdf_state = (
        f"campus_pdf_{campus_key}"
    )
    campus_ppt_state = (
        f"campus_ppt_{campus_key}"
    )
    campus_html_state = (
        f"campus_html_{campus_key}"
    )
    campus_zip_state = (
        f"campus_zip_{campus_key}"
    )

    if b1.button(
        CAMPUS_ACTION_GENERATE_CAMPUS_PDF,
        key=f"btn_campus_pdf_{campus_key}",
        use_container_width=True,
    ):
        with st.spinner(
            f"Generating campus PDF for {campus.campus_name}..."
        ):
            st.session_state[
                campus_pdf_state
            ] = generate_campus_pdf_bytes(
                campus.campus_name,
                reports,
            )

    if b2.button(
        CAMPUS_ACTION_GENERATE_CAMPUS_PPT,
        key=f"btn_campus_ppt_{campus_key}",
        use_container_width=True,
    ):
        with st.spinner(
            f"Generating campus PPT for {campus.campus_name}..."
        ):
            st.session_state[
                campus_ppt_state
            ] = generate_campus_ppt_bytes(
                campus.campus_name,
                reports,
            )

    if b3.button(
        "Generate Campus HTML",
        key=f"btn_campus_html_{campus_key}",
        use_container_width=True,
    ):
        with st.spinner(
            f"Generating campus HTML for {campus.campus_name}..."
        ):
            st.session_state[
                campus_html_state
            ] = generate_campus_html_bytes(
                campus_name=campus.campus_name,
                reports=reports,
            )

    if b4.button(
        CAMPUS_ACTION_DOWNLOAD_ZIP,
        key=f"btn_campus_zip_{campus_key}",
        use_container_width=True,
    ):
        with st.spinner(
            f"Preparing complete ZIP for {campus.campus_name}..."
        ):
            st.session_state[
                campus_zip_state
            ] = generate_campus_zip_bytes(
                campus.campus_name,
                reports,
                include_images=True,
                include_individual_pdfs=True,
                include_campus_pdf=True,
                include_campus_ppt=True,
            )

    # --------------------------------------------------------
    # GENERATED DOWNLOADS
    # --------------------------------------------------------

    if consolidated_state in st.session_state:
        consolidated = st.session_state[
            consolidated_state
        ]

        st.markdown(
            "#### Campus Consolidated Summary"
        )

        st.image(
            consolidated["image"],
            use_container_width=True,
        )

        c1, c2 = st.columns(2)

        c1.download_button(
            "Download Consolidated Summary Image",
            data=consolidated["image"],
            file_name=(
                f"{campus_slug}_"
                "Consolidated_Feedback_Summary.png"
            ),
            mime="image/png",
            key=f"download_consolidated_img_{campus_key}",
            use_container_width=True,
        )

        c2.download_button(
            "Download Consolidated Summary PDF",
            data=consolidated["pdf"],
            file_name=(
                f"{campus_slug}_"
                "Consolidated_Feedback_Summary.pdf"
            ),
            mime="application/pdf",
            key=f"download_consolidated_pdf_{campus_key}",
            use_container_width=True,
        )

    download_row_1 = st.columns(3)

    if images_state in st.session_state:
        download_row_1[0].download_button(
            "Download All Images",
            data=st.session_state[
                images_state
            ],
            file_name=(
                f"{campus_slug}_"
                "Trainer_Images.zip"
            ),
            mime="application/zip",
            key=f"download_all_images_{campus_key}",
            use_container_width=True,
        )

    if pdfs_state in st.session_state:
        download_row_1[1].download_button(
            "Download All PDFs",
            data=st.session_state[
                pdfs_state
            ],
            file_name=(
                f"{campus_slug}_"
                "Trainer_PDFs.zip"
            ),
            mime="application/zip",
            key=f"download_all_pdfs_{campus_key}",
            use_container_width=True,
        )

    if campus_pdf_state in st.session_state:
        download_row_1[2].download_button(
            "Download Campus PDF",
            data=st.session_state[
                campus_pdf_state
            ],
            file_name=(
                f"{campus_slug}_"
                "Campus_Feedback_Report.pdf"
            ),
            mime="application/pdf",
            key=f"download_campus_pdf_{campus_key}",
            use_container_width=True,
        )

    download_row_2 = st.columns(3)

    if campus_ppt_state in st.session_state:
        download_row_2[0].download_button(
            "Download Campus PPT",
            data=st.session_state[
                campus_ppt_state
            ],
            file_name=(
                f"{campus_slug}_"
                "Campus_Feedback_Report.pptx"
            ),
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "presentationml.presentation"
            ),
            key=f"download_campus_ppt_{campus_key}",
            use_container_width=True,
        )

    if campus_html_state in st.session_state:
        download_row_2[1].download_button(
            "Download Campus HTML",
            data=st.session_state[
                campus_html_state
            ],
            file_name=(
                f"{campus_slug}_"
                "Feedback_Report.html"
            ),
            mime="text/html",
            key=f"download_campus_html_{campus_key}",
            use_container_width=True,
        )

    if campus_zip_state in st.session_state:
        download_row_2[2].download_button(
            "Download Campus ZIP",
            data=st.session_state[
                campus_zip_state
            ],
            file_name=(
                f"{campus_slug}_"
                "Feedback_Reports.zip"
            ),
            mime="application/zip",
            key=f"download_campus_zip_{campus_key}",
            use_container_width=True,
        )


# ============================================================
# CAMPUS SECTION
# ============================================================

def render_campus_section(
    campus: CampusFeedback,
    campus_number: int,
    source_key: str,
) -> None:
    """
    Render one campus, its trainer list and its report actions.
    """
    campus_name_state = (
        f"campus_name_{source_key}"
    )

    if campus_name_state not in st.session_state:
        st.session_state[
            campus_name_state
        ] = campus.campus_name

    editable_name = st.text_input(
        f"College / Campus Name - File {campus_number}",
        key=campus_name_state,
        help=(
            "This name will appear on trainer images, PDFs, "
            "the campus PDF, PPT, consolidated summary and ZIP."
        ),
    )

    rename_campus(
        campus,
        editable_name,
    )

    campus_key = (
        f"{source_key}_{_safe_slug(campus.campus_name)}"
    )

    st.markdown(
        (
            f'<div class="campus-banner">'
            f'Campus {campus_number}: {campus.campus_name}'
            f'</div>'
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        (
            f'<div class="campus-note">'
            f'Source file: {campus.file_name} &nbsp; | &nbsp; '
            f'Sheet: {campus.sheet_name}'
            f'</div>'
        ),
        unsafe_allow_html=True,
    )

    campus = render_column_mapping(
        campus,
        campus_key,
    )

    validation = validate_feedback_for_analysis(
        campus
    )

    critical_messages = [
        message
        for message in validation
        if (
            "Trainer Name column must be mapped" in message
            or "No trainer names were found" in message
            or "No feedback rows" in message
        )
    ]

    for warning in campus.warnings:
        st.warning(warning)

    if critical_messages:
        for message in critical_messages:
            st.error(message)

        st.info(
            "Correct the Column Mapping above before generating reports."
        )
        return

    analyses = analyze_campus(
        campus
    )

    if not analyses:
        st.warning(
            "No trainer-wise feedback could be analyzed for this campus."
        )
        return

    stats = campus_basic_statistics(
        campus
    )

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Total Trainers",
        stats["total_trainers"],
    )
    m2.metric(
        "Total Responses",
        stats["total_responses"],
    )
    m3.metric(
        "Average Trainer Rating",
        (
            f"{stats['average_trainer_rating']:.2f} / 5"
            if stats["average_trainer_rating"] is not None
            else "N/A"
        ),
    )
    m4.metric(
        "Highest Rated Trainer",
        (
            stats["highest_rated_trainer"]
            if stats["highest_rated_trainer"]
            else "N/A"
        ),
    )

    render_trainer_rows(
        campus,
        analyses,
        campus_key,
    )

    st.markdown("---")

    render_campus_actions(
        campus,
        analyses,
        campus_key,
    )


# ============================================================
# MAIN PAGE
# ============================================================

st.markdown(
    f'<div class="feedback-title">{PAGE_TITLE}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="feedback-subtitle">{PAGE_SUBTITLE}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="small-note">
        Upload multiple feedback Excel files together. Each file is treated as
        a separate college/campus. Trainer analysis and all generated reports
        remain strictly campus-wise.
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_files = st.file_uploader(
    UPLOAD_LABEL,
    type=SUPPORTED_FEEDBACK_FILE_TYPES,
    accept_multiple_files=True,
    key="feedback_multiple_file_uploader",
)

if not uploaded_files:
    st.info(
        "Upload one or more college/campus feedback Excel files to begin."
    )
    st.stop()


# ============================================================
# LOAD ALL FILES AS SEPARATE CAMPUSES
# ============================================================

try:
    campuses = load_multiple_feedback_files(
        uploaded_files
    )
except Exception as exc:
    st.error(
        f"Unable to read the uploaded feedback file(s): {exc}"
    )
    st.stop()

if not campuses:
    st.warning(
        "No campus feedback data was loaded."
    )
    st.stop()


# ============================================================
# UPLOAD SUMMARY
# ============================================================

st.success(
    f"{len(campuses)} college/campus feedback file(s) loaded."
)

summary_rows = []

for index, campus in enumerate(
    campuses,
    start=1,
):
    summary_rows.append(
        {
            "Campus": campus.campus_name,
            "Uploaded File": campus.file_name,
            "Trainers Detected": campus.total_trainers,
            "Responses": campus.total_responses,
        }
    )

with st.expander(
    "Uploaded Campus Files",
    expanded=False,
):
    st.dataframe(
        pd.DataFrame(summary_rows),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# DISPLAY CAMPUS 1, CAMPUS 2, CAMPUS 3...
# ============================================================

for campus_number, (campus, uploaded_file) in enumerate(
    zip(campuses, uploaded_files),
    start=1,
):
    source_key = (
        f"campus_{campus_number}_"
        f"{_file_signature(uploaded_file)}"
    )

    with st.container(border=True):
        try:
            render_campus_section(
                campus=campus,
                campus_number=campus_number,
                source_key=source_key,
            )
        except Exception as exc:
            st.error(
                (
                    f"Error while processing Campus {campus_number} "
                    f"({campus.file_name}): {exc}"
                )
            )

    if campus_number < len(campuses):
        st.markdown("<br>", unsafe_allow_html=True)
