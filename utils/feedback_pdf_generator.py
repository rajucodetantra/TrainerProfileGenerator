"""
feedback_pdf_generator.py
-------------------------
Creates trainer feedback PDFs for the Trainer Profile Generator.

Works with trainer report dictionaries produced by:
    utils.feedback_analysis

Uses the image report design from:
    utils.feedback_image_generator

IMPORTANT:
Each college/campus remains independent.
This module never combines trainers from different campuses.

Main functions:
    generate_trainer_pdf(...)
    generate_all_trainer_pdfs(...)
    generate_campus_pdf(...)
"""

from __future__ import annotations

import re
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from PIL import Image

from utils.feedback_image_generator import (
    generate_trainer_report_image,
    generate_trainer_report_image_bytes,
)


# ============================================================
# FILE HELPERS
# ============================================================

def _sanitize_filename(value: str) -> str:
    """
    Make a safe filename for Windows/Linux.
    """
    value = re.sub(r'[<>:"/\\|?*]+', "_", str(value))
    value = re.sub(r"\s+", "_", value.strip())
    value = re.sub(r"_+", "_", value)

    return value.strip("._") or "Trainer"


def _safe_text(value: Any, fallback: str = "Trainer") -> str:
    if value is None:
        return fallback

    text = str(value).strip()
    return text if text else fallback


# ============================================================
# IMAGE -> PDF CONVERSION
# ============================================================

def _image_to_pdf(
    image_path: str | Path,
    pdf_path: str | Path,
) -> Path:
    """
    Convert one generated image into a one-page PDF.
    """
    image_path = Path(image_path)
    pdf_path = Path(pdf_path)

    pdf_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with Image.open(image_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")

        img.save(
            pdf_path,
            "PDF",
            resolution=150.0,
            save_all=False,
        )

    return pdf_path


# ============================================================
# INDIVIDUAL TRAINER PDF
# ============================================================

def generate_trainer_pdf(
    report: Dict[str, Any],
    output_path: Optional[str | Path] = None,
    keep_temp_image: bool = False,
) -> Path:
    """
    Generate one PDF for one trainer.

    Parameters
    ----------
    report:
        Report dictionary from feedback_analysis.

    output_path:
        Target PDF filename.

    keep_temp_image:
        If True, the intermediate image is retained beside the PDF.

    Returns
    -------
    pathlib.Path
        Path to generated PDF.
    """
    trainer_name = _safe_text(
        report.get("trainer_name"),
        "Trainer",
    )

    campus_name = _safe_text(
        report.get("campus_name"),
        "Campus",
    )

    if output_path is None:
        output_path = (
            Path.cwd()
            / (
                f"{_sanitize_filename(campus_name)}_"
                f"{_sanitize_filename(trainer_name)}_"
                f"Feedback_Report.pdf"
            )
        )
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if keep_temp_image:
        image_path = output_path.with_suffix(".png")

        generate_trainer_report_image(
            report=report,
            output_path=image_path,
        )

        return _image_to_pdf(
            image_path=image_path,
            pdf_path=output_path,
        )

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_image = (
            Path(temp_dir)
            / (
                f"{_sanitize_filename(trainer_name)}_"
                "Feedback_Report.png"
            )
        )

        generate_trainer_report_image(
            report=report,
            output_path=temp_image,
        )

        return _image_to_pdf(
            image_path=temp_image,
            pdf_path=output_path,
        )


# ============================================================
# GENERATE ALL TRAINER PDFs FOR ONE CAMPUS
# ============================================================

def generate_all_trainer_pdfs(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
    output_dir: str | Path,
    overwrite: bool = True,
) -> List[Path]:
    """
    Generate one PDF per trainer for ONE campus.

    Example:
        output/
            feedback_reports/
                SVPCET/
                    pdfs/
                        Ch_Manohar_Feedback_Report.pdf
                        Trainer_2_Feedback_Report.pdf
    """
    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated: List[Path] = []

    for report in reports:
        trainer_name = _safe_text(
            report.get("trainer_name"),
            "Trainer",
        )

        filename = (
            f"{_sanitize_filename(trainer_name)}_"
            "Feedback_Report.pdf"
        )

        output_path = output_dir / filename

        if output_path.exists() and not overwrite:
            generated.append(output_path)
            continue

        report_copy = dict(report)
        report_copy["campus_name"] = campus_name

        generated_path = generate_trainer_pdf(
            report=report_copy,
            output_path=output_path,
        )

        generated.append(generated_path)

    return generated


# ============================================================
# COMBINED CAMPUS PDF
# ============================================================

def generate_campus_pdf(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
    output_path: str | Path,
) -> Path:
    """
    Generate ONE combined campus PDF.

    Structure:
        Page 1 -> Trainer 1
        Page 2 -> Trainer 2
        Page 3 -> Trainer 3
        ...

    No cover page is added by default because the user requested
    one trainer report per page.
    """
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not reports:
        raise ValueError(
            "No trainer reports were provided for campus PDF generation."
        )

    images: List[Image.Image] = []

    try:
        for report in reports:
            report_copy = dict(report)
            report_copy["campus_name"] = campus_name

            image_bytes = generate_trainer_report_image_bytes(
                report_copy
            )

            from io import BytesIO

            img = Image.open(
                BytesIO(image_bytes)
            )

            if img.mode != "RGB":
                img = img.convert("RGB")

            # Copy detaches it from the BytesIO stream.
            images.append(img.copy())
            img.close()

        if not images:
            raise ValueError(
                "Unable to create report pages."
            )

        first_page = images[0]
        remaining_pages = images[1:]

        first_page.save(
            output_path,
            "PDF",
            resolution=150.0,
            save_all=True,
            append_images=remaining_pages,
        )

    finally:
        for img in images:
            try:
                img.close()
            except Exception:
                pass

    return output_path


# ============================================================
# CAMPUS PDF BY DEFAULT FOLDER STRUCTURE
# ============================================================

def generate_campus_pdf_to_folder(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
    campus_output_dir: str | Path,
) -> Path:
    """
    Convenience helper using the standard project folder structure.

    Example output:
        output/feedback_reports/SVPCET/
            SVPCET_Campus_Feedback_Report.pdf
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
        "Campus_Feedback_Report.pdf"
    )

    return generate_campus_pdf(
        campus_name=campus_name,
        reports=reports,
        output_path=campus_output_dir / filename,
    )


# ============================================================
# STREAMLIT DOWNLOAD HELPERS
# ============================================================

def pdf_file_to_bytes(
    path: str | Path,
) -> bytes:
    """
    Read a generated PDF as bytes for st.download_button().
    """
    return Path(path).read_bytes()


def generate_trainer_pdf_bytes(
    report: Dict[str, Any],
) -> bytes:
    """
    Generate one trainer PDF completely in memory.

    Useful for:
        st.download_button(
            data=generate_trainer_pdf_bytes(report),
            file_name="Trainer_Report.pdf",
            mime="application/pdf"
        )
    """
    from io import BytesIO

    image_bytes = generate_trainer_report_image_bytes(
        report
    )

    image_stream = BytesIO(image_bytes)

    with Image.open(image_stream) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")

        pdf_stream = BytesIO()

        img.save(
            pdf_stream,
            "PDF",
            resolution=150.0,
            save_all=False,
        )

        pdf_stream.seek(0)

        return pdf_stream.getvalue()


def generate_campus_pdf_bytes(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
) -> bytes:
    """
    Generate the combined campus PDF in memory.

    Useful when the user clicks:
        Generate Campus PDF

    and you want to provide a Streamlit download button without
    permanently saving the file.
    """
    from io import BytesIO

    if not reports:
        raise ValueError(
            "No trainer reports were provided."
        )

    page_images: List[Image.Image] = []

    try:
        for report in reports:
            report_copy = dict(report)
            report_copy["campus_name"] = campus_name

            image_bytes = generate_trainer_report_image_bytes(
                report_copy
            )

            with Image.open(
                BytesIO(image_bytes)
            ) as img:
                if img.mode != "RGB":
                    img = img.convert("RGB")

                page_images.append(
                    img.copy()
                )

        output = BytesIO()

        first_page = page_images[0]
        remaining = page_images[1:]

        first_page.save(
            output,
            "PDF",
            resolution=150.0,
            save_all=True,
            append_images=remaining,
        )

        output.seek(0)
        return output.getvalue()

    finally:
        for image in page_images:
            try:
                image.close()
            except Exception:
                pass


# ============================================================
# VALIDATION
# ============================================================

def validate_reports_for_pdf(
    reports: Sequence[Dict[str, Any]],
) -> List[str]:
    """
    Return validation messages before generating PDF files.
    """
    messages: List[str] = []

    if not reports:
        messages.append(
            "No trainer reports are available."
        )
        return messages

    missing_trainer_names = 0

    for report in reports:
        if not report.get("trainer_name"):
            missing_trainer_names += 1

    if missing_trainer_names:
        messages.append(
            f"{missing_trainer_names} report(s) do not contain "
            "a trainer name."
        )

    return messages
