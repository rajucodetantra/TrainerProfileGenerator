"""
feedback_zip_generator.py
-------------------------
Creates campus-wise ZIP packages for the Trainer Profile Generator.

IMPORTANT:
- Each ZIP contains ONE campus/college only.
- The Streamlit ZIP generation path is fully memory-based.
- No pathlib.WindowsPath objects are passed to python-pptx.
- Works locally on Windows and on Streamlit Cloud.

Typical ZIP contents:

    images/
        Trainer_1_Feedback_Report.png
        Trainer_2_Feedback_Report.png

    pdfs/
        Trainer_1_Feedback_Report.pdf
        Trainer_2_Feedback_Report.pdf

    SVPCET_Campus_Feedback_Report.pdf
    SVPCET_Campus_Feedback_Report.pptx
"""

from __future__ import annotations

import io
import re
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from utils.feedback_image_generator import (
    generate_trainer_report_image_bytes,
)
from utils.feedback_pdf_generator import (
    generate_trainer_pdf_bytes,
    generate_campus_pdf_bytes,
)
from utils.feedback_ppt_generator import (
    generate_campus_ppt_bytes,
)


# ============================================================
# HELPERS
# ============================================================

def _sanitize_filename(value: Any) -> str:
    """
    Create a safe Windows/Linux filename.
    """
    text = str(value or "").strip()

    text = re.sub(
        r'[<>:"/\\|?*]+',
        "_",
        text,
    )

    text = re.sub(
        r"\s+",
        "_",
        text,
    )

    text = re.sub(
        r"_+",
        "_",
        text,
    )

    return text.strip("._") or "item"


def _safe_text(
    value: Any,
    fallback: str = "Campus",
) -> str:
    if value is None:
        return fallback

    text = str(value).strip()

    return text if text else fallback


# ============================================================
# MAIN STREAMLIT ZIP GENERATOR
# ============================================================

def generate_campus_zip_bytes(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
    include_images: bool = True,
    include_individual_pdfs: bool = True,
    include_campus_pdf: bool = True,
    include_campus_ppt: bool = True,
) -> bytes:
    """
    Generate a complete campus ZIP entirely in memory.

    This is the recommended function for Streamlit.

    It avoids temporary filesystem paths, which prevents Windows errors
    such as:

        'WindowsPath' object has no attribute 'seek'

    Parameters
    ----------
    campus_name:
        Name displayed in the report.

    reports:
        Trainer report dictionaries for ONE campus only.

    include_images:
        Include one PNG per trainer.

    include_individual_pdfs:
        Include one PDF per trainer.

    include_campus_pdf:
        Include combined campus PDF.

    include_campus_ppt:
        Include campus PPT with one trainer per slide.

    Returns
    -------
    bytes
        ZIP file bytes ready for st.download_button().
    """

    if not reports:
        raise ValueError(
            "No trainer reports were provided for ZIP generation."
        )

    campus_name = _safe_text(
        campus_name,
        "Campus",
    )

    campus_slug = _sanitize_filename(
        campus_name
    )

    output = io.BytesIO()

    with zipfile.ZipFile(
        output,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zf:

        # ====================================================
        # INDIVIDUAL TRAINER REPORTS
        # ====================================================

        for index, report in enumerate(
            reports,
            start=1,
        ):
            current_report = dict(report)

            # Force campus name so a report can never accidentally
            # use another campus name.
            current_report["campus_name"] = (
                campus_name
            )

            trainer_name = _safe_text(
                current_report.get(
                    "trainer_name"
                ),
                f"Trainer_{index}",
            )

            trainer_slug = _sanitize_filename(
                trainer_name
            )

            # ------------------------------------------------
            # IMAGE
            # ------------------------------------------------

            if include_images:

                image_bytes = (
                    generate_trainer_report_image_bytes(
                        current_report
                    )
                )

                zf.writestr(
                    (
                        f"images/"
                        f"{trainer_slug}_"
                        f"Feedback_Report.png"
                    ),
                    image_bytes,
                )

            # ------------------------------------------------
            # INDIVIDUAL PDF
            # ------------------------------------------------

            if include_individual_pdfs:

                trainer_pdf_bytes = (
                    generate_trainer_pdf_bytes(
                        current_report
                    )
                )

                zf.writestr(
                    (
                        f"pdfs/"
                        f"{trainer_slug}_"
                        f"Feedback_Report.pdf"
                    ),
                    trainer_pdf_bytes,
                )

        # ====================================================
        # COMBINED CAMPUS PDF
        # ====================================================

        if include_campus_pdf:

            campus_pdf_bytes = (
                generate_campus_pdf_bytes(
                    campus_name=campus_name,
                    reports=reports,
                )
            )

            zf.writestr(
                (
                    f"{campus_slug}_"
                    f"Campus_Feedback_Report.pdf"
                ),
                campus_pdf_bytes,
            )

        # ====================================================
        # CAMPUS PPT
        # ====================================================

        if include_campus_ppt:

            campus_ppt_bytes = (
                generate_campus_ppt_bytes(
                    campus_name=campus_name,
                    reports=reports,
                )
            )

            zf.writestr(
                (
                    f"{campus_slug}_"
                    f"Campus_Feedback_Report.pptx"
                ),
                campus_ppt_bytes,
            )

    output.seek(0)

    return output.getvalue()


# ============================================================
# OPTIONAL DISK-BASED ZIP
# ============================================================

def generate_campus_zip(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
    output_path: str | Path,
    include_images: bool = True,
    include_individual_pdfs: bool = True,
    include_campus_pdf: bool = True,
    include_campus_ppt: bool = True,
) -> Path:
    """
    Generate a campus ZIP and save it to disk.

    Internally, the ZIP is still built fully in memory first,
    then written once to disk.

    This avoids path-handling issues during report generation.
    """

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    zip_bytes = generate_campus_zip_bytes(
        campus_name=campus_name,
        reports=reports,
        include_images=include_images,
        include_individual_pdfs=include_individual_pdfs,
        include_campus_pdf=include_campus_pdf,
        include_campus_ppt=include_campus_ppt,
    )

    output_path.write_bytes(
        zip_bytes
    )

    return output_path


# ============================================================
# STANDARD CAMPUS OUTPUT FOLDER
# ============================================================

def generate_campus_zip_to_folder(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
    campus_output_dir: str | Path,
    include_images: bool = True,
    include_individual_pdfs: bool = True,
    include_campus_pdf: bool = True,
    include_campus_ppt: bool = True,
) -> Path:
    """
    Generate:
        output/feedback_reports/<Campus>/<Campus>_Feedback_Reports.zip
    """

    campus_output_dir = Path(
        campus_output_dir
    )

    campus_output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    campus_slug = _sanitize_filename(
        campus_name
    )

    output_path = (
        campus_output_dir
        / (
            f"{campus_slug}_"
            f"Feedback_Reports.zip"
        )
    )

    return generate_campus_zip(
        campus_name=campus_name,
        reports=reports,
        output_path=output_path,
        include_images=include_images,
        include_individual_pdfs=include_individual_pdfs,
        include_campus_pdf=include_campus_pdf,
        include_campus_ppt=include_campus_ppt,
    )


# ============================================================
# ZIP ALREADY GENERATED FILES
# ============================================================

def zip_existing_campus_outputs(
    campus_name: str,
    image_paths: Sequence[str | Path],
    pdf_paths: Sequence[str | Path],
    campus_pdf_path: Optional[str | Path],
    campus_ppt_path: Optional[str | Path],
    output_path: str | Path,
) -> Path:
    """
    ZIP already-generated files.

    This helper is retained for compatibility with any existing
    application code.
    """

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with zipfile.ZipFile(
        str(output_path),
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zf:

        for path in image_paths:

            current = Path(path)

            if current.exists():

                zf.write(
                    str(current),
                    arcname=(
                        f"images/"
                        f"{current.name}"
                    ),
                )

        for path in pdf_paths:

            current = Path(path)

            if current.exists():

                zf.write(
                    str(current),
                    arcname=(
                        f"pdfs/"
                        f"{current.name}"
                    ),
                )

        if campus_pdf_path:

            current = Path(
                campus_pdf_path
            )

            if current.exists():

                zf.write(
                    str(current),
                    arcname=current.name,
                )

        if campus_ppt_path:

            current = Path(
                campus_ppt_path
            )

            if current.exists():

                zf.write(
                    str(current),
                    arcname=current.name,
                )

    return output_path


# ============================================================
# VALIDATION
# ============================================================

def validate_reports_for_zip(
    reports: Sequence[Dict[str, Any]],
) -> List[str]:
    """
    Validate trainer reports before ZIP creation.
    """

    messages: List[str] = []

    if not reports:

        messages.append(
            "No trainer reports are available."
        )

        return messages

    missing_names = sum(
        1
        for report in reports
        if not report.get(
            "trainer_name"
        )
    )

    if missing_names:

        messages.append(
            (
                f"{missing_names} report(s) "
                "do not contain a trainer name."
            )
        )

    return messages
