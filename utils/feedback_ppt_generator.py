"""
feedback_ppt_generator.py
-------------------------
Creates campus-wise PowerPoint feedback reports for the
Trainer Profile Generator.

Each campus gets its own PPT.
Each trainer gets exactly one slide.

Works with trainer report dictionaries produced by:
    utils.feedback_analysis

Uses the one-page report design from:
    utils.feedback_image_generator

IMPORTANT:
This module never combines trainers from different colleges/campuses.

Main functions:
    generate_campus_ppt(...)
    generate_campus_ppt_bytes(...)
"""

from __future__ import annotations

import re
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from pptx import Presentation
from pptx.util import Inches

from utils.feedback_image_generator import (
    generate_trainer_report_image,
    generate_trainer_report_image_bytes,
)


# ============================================================
# PPT SETTINGS
# ============================================================

# 16:9 widescreen presentation.
SLIDE_WIDTH_INCHES = 13.333333
SLIDE_HEIGHT_INCHES = 7.5


# ============================================================
# HELPERS
# ============================================================

def _sanitize_filename(value: str) -> str:
    """
    Make a safe filename for Windows/Linux.
    """
    value = re.sub(r'[<>:"/\\|?*]+', "_", str(value))
    value = re.sub(r"\s+", "_", value.strip())
    value = re.sub(r"_+", "_", value)

    return value.strip("._") or "Campus"


def _safe_text(
    value: Any,
    fallback: str = "Campus",
) -> str:
    if value is None:
        return fallback

    text = str(value).strip()

    return text if text else fallback


def _set_widescreen(prs: Presentation) -> None:
    """
    Set PowerPoint size to 16:9.
    """
    prs.slide_width = Inches(
        SLIDE_WIDTH_INCHES
    )
    prs.slide_height = Inches(
        SLIDE_HEIGHT_INCHES
    )


def _add_full_slide_image(
    prs: Presentation,
    image_source: str | Path | BytesIO,
) -> None:
    """
    Add one image so that it fills the entire slide.

    The trainer report image is portrait, while the slide is widescreen.
    To preserve the report without cropping, the image is fitted inside
    the slide and centered.
    """
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    slide_width = prs.slide_width
    slide_height = prs.slide_height

    # Add image first using native dimensions so python-pptx
    # can resolve the image size.
    picture = slide.shapes.add_picture(
        image_source,
        0,
        0,
    )

    image_width = picture.width
    image_height = picture.height

    if not image_width or not image_height:
        return

    image_ratio = image_width / image_height
    slide_ratio = slide_width / slide_height

    if image_ratio > slide_ratio:
        # Fit to slide width.
        target_width = slide_width
        target_height = int(
            target_width / image_ratio
        )

        left = 0
        top = int(
            (slide_height - target_height) / 2
        )
    else:
        # Fit to slide height.
        target_height = slide_height
        target_width = int(
            target_height * image_ratio
        )

        top = 0
        left = int(
            (slide_width - target_width) / 2
        )

    picture.left = left
    picture.top = top
    picture.width = target_width
    picture.height = target_height


# ============================================================
# CAMPUS PPT GENERATION
# ============================================================

def generate_campus_ppt(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
    output_path: str | Path,
) -> Path:
    """
    Generate one campus-specific PowerPoint.

    Structure:
        Slide 1 -> Trainer 1
        Slide 2 -> Trainer 2
        Slide 3 -> Trainer 3
        ...

    No cover slide is added because the required format is
    one slide for each trainer.
    """
    if not reports:
        raise ValueError(
            "No trainer reports were provided for PPT generation."
        )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    prs = Presentation()
    _set_widescreen(prs)

    # Remove the default first slide if the template contains one.
    # A new Presentation normally has zero slides, so this is safe.
    while len(prs.slides) > 0:
        slide_id = prs.slides._sldIdLst[0]
        prs.part.drop_rel(slide_id.rId)
        del prs.slides._sldIdLst[0]

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        for index, report in enumerate(
            reports,
            start=1,
        ):
            trainer_name = _safe_text(
                report.get("trainer_name"),
                f"Trainer_{index}",
            )

            report_copy = dict(report)
            report_copy["campus_name"] = (
                campus_name
            )

            image_path = (
                temp_dir_path
                / (
                    f"{index:03d}_"
                    f"{_sanitize_filename(trainer_name)}"
                    "_Feedback_Report.png"
                )
            )

            generate_trainer_report_image(
                report=report_copy,
                output_path=image_path,
            )

            _add_full_slide_image(
                prs,
                image_path,
            )

    prs.save(output_path)

    return output_path


# ============================================================
# STANDARD CAMPUS FOLDER OUTPUT
# ============================================================

def generate_campus_ppt_to_folder(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
    campus_output_dir: str | Path,
) -> Path:
    """
    Generate campus PPT using the standard project folder structure.

    Example:
        output/
            feedback_reports/
                SVPCET/
                    SVPCET_Campus_Feedback_Report.pptx
    """
    campus_output_dir = Path(
        campus_output_dir
    )

    campus_output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = (
        f"{_sanitize_filename(campus_name)}_"
        "Campus_Feedback_Report.pptx"
    )

    return generate_campus_ppt(
        campus_name=campus_name,
        reports=reports,
        output_path=(
            campus_output_dir / filename
        ),
    )


# ============================================================
# STREAMLIT IN-MEMORY PPT
# ============================================================

def generate_campus_ppt_bytes(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
) -> bytes:
    """
    Generate the campus PPT completely in memory.

    Useful in Streamlit:

        ppt_bytes = generate_campus_ppt_bytes(
            campus.campus_name,
            reports
        )

        st.download_button(
            "Download Campus PPT",
            data=ppt_bytes,
            file_name="SVPCET_Campus_Feedback_Report.pptx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "presentationml.presentation"
            ),
        )
    """
    if not reports:
        raise ValueError(
            "No trainer reports were provided."
        )

    prs = Presentation()
    _set_widescreen(prs)

    while len(prs.slides) > 0:
        slide_id = prs.slides._sldIdLst[0]
        prs.part.drop_rel(slide_id.rId)
        del prs.slides._sldIdLst[0]

    # python-pptx requires file-like objects that remain valid
    # while the slide image is being read.
    image_buffers: List[BytesIO] = []

    try:
        for report in reports:
            report_copy = dict(report)
            report_copy["campus_name"] = (
                campus_name
            )

            image_bytes = (
                generate_trainer_report_image_bytes(
                    report_copy
                )
            )

            image_stream = BytesIO(
                image_bytes
            )

            image_buffers.append(
                image_stream
            )

            _add_full_slide_image(
                prs,
                image_stream,
            )

        output = BytesIO()

        prs.save(output)
        output.seek(0)

        return output.getvalue()

    finally:
        for buffer in image_buffers:
            try:
                buffer.close()
            except Exception:
                pass


# ============================================================
# INDIVIDUAL TRAINER PPT
# ============================================================

def generate_single_trainer_ppt(
    report: Dict[str, Any],
    output_path: str | Path,
) -> Path:
    """
    Optional helper:
    Generate a one-slide PowerPoint for a single trainer.

    This may be useful later if you add:
        [Download PPT]
    beside the individual trainer report.
    """
    campus_name = _safe_text(
        report.get("campus_name"),
        "Campus",
    )

    return generate_campus_ppt(
        campus_name=campus_name,
        reports=[report],
        output_path=output_path,
    )


def generate_single_trainer_ppt_bytes(
    report: Dict[str, Any],
) -> bytes:
    """
    Optional in-memory one-slide PPT for one trainer.
    """
    campus_name = _safe_text(
        report.get("campus_name"),
        "Campus",
    )

    return generate_campus_ppt_bytes(
        campus_name=campus_name,
        reports=[report],
    )


# ============================================================
# FILE DOWNLOAD HELPER
# ============================================================

def ppt_file_to_bytes(
    path: str | Path,
) -> bytes:
    """
    Read a generated PPTX as bytes for Streamlit download.
    """
    return Path(path).read_bytes()


# ============================================================
# VALIDATION
# ============================================================

def validate_reports_for_ppt(
    reports: Sequence[Dict[str, Any]],
) -> List[str]:
    """
    Return validation messages before PPT generation.
    """
    messages: List[str] = []

    if not reports:
        messages.append(
            "No trainer reports are available."
        )
        return messages

    missing_trainer_names = sum(
        1
        for report in reports
        if not report.get("trainer_name")
    )

    if missing_trainer_names:
        messages.append(
            f"{missing_trainer_names} report(s) "
            "do not contain a trainer name."
        )

    return messages
