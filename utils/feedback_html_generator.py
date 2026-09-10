"""
feedback_html_generator.py
--------------------------
Creates a self-contained campus-wise HTML feedback report for
Trainer Profile Generator.

Each HTML file contains ONLY ONE campus/college.

Main options shown in the HTML:
    1. Consolidated Report
    2. Trainer-wise Feedback

Trainer-wise feedback features:
    - Trainer dropdown
    - View Report button
    - Previous Trainer
    - Next Trainer
    - Back to Summary
    - Print / Save as PDF

The file is fully self-contained:
    - No internet connection required
    - No external CSS
    - No external JavaScript
    - Trainer report images are embedded as Base64 data URIs

Save this file at:
    TrainerProfileGenerator/utils/feedback_html_generator.py
"""

from __future__ import annotations

import base64
import html
import io
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from utils.feedback_image_generator import (
    generate_trainer_report_image_bytes,
)


# ============================================================
# HELPERS
# ============================================================

def _safe_text(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback

    text = str(value).strip()
    return text if text else fallback


def _safe_slug(value: Any) -> str:
    text = _safe_text(value, "item")

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


def _safe_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None


def _rating_text(value: Any) -> str:
    number = _safe_float(value)

    if number is None:
        return "N/A"

    return f"{number:.2f} / 5"


def _percent_text(value: Any) -> str:
    number = _safe_float(value)

    if number is None:
        return "N/A"

    return f"{number:.1f}%"


def _image_bytes_to_data_uri(
    image_bytes: bytes,
    mime_type: str = "image/png",
) -> str:
    encoded = base64.b64encode(
        image_bytes
    ).decode("ascii")

    return f"data:{mime_type};base64,{encoded}"


# ============================================================
# CAMPUS SUMMARY / RANKING
# ============================================================

def _ranked_reports(
    reports: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Rank trainers within ONE campus only.

    Ranking rule:
        1. Higher average overall rating
        2. Higher response count as tie-breaker
    """
    ranked = [
        dict(report)
        for report in reports
    ]

    ranked.sort(
        key=lambda report: (
            report.get("overall_rating") is not None,
            _safe_float(
                report.get("overall_rating")
            ) or -999,
            int(
                report.get("responses") or 0
            ),
        ),
        reverse=True,
    )

    for index, report in enumerate(
        ranked,
        start=1,
    ):
        report["rank"] = index

    return ranked


def _campus_average_rating(
    reports: Sequence[Dict[str, Any]],
) -> Optional[float]:
    values = []

    for report in reports:
        value = _safe_float(
            report.get("overall_rating")
        )

        if value is not None:
            values.append(value)

    if not values:
        return None

    return round(
        sum(values) / len(values),
        2,
    )


def _total_responses(
    reports: Sequence[Dict[str, Any]],
) -> int:
    return sum(
        int(report.get("responses") or 0)
        for report in reports
    )


# ============================================================
# TRAINER REPORT PAYLOAD
# ============================================================

def _build_trainer_payload(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Prepare trainer information for JavaScript.

    Each trainer report image is generated using the same image
    generator already used by Streamlit/PDF/PPT.
    """
    payload: List[Dict[str, Any]] = []

    for index, report in enumerate(
        reports
    ):
        current = dict(report)
        current["campus_name"] = campus_name

        trainer_name = _safe_text(
            current.get("trainer_name"),
            f"Trainer {index + 1}",
        )

        image_bytes = (
            generate_trainer_report_image_bytes(
                current
            )
        )

        payload.append(
            {
                "index": index,
                "trainer_name": trainer_name,
                "responses": int(
                    current.get("responses") or 0
                ),
                "overall_rating": (
                    _safe_float(
                        current.get(
                            "overall_rating"
                        )
                    )
                ),
                "positive_percent": (
                    _safe_float(
                        current.get(
                            "positive_rating_percent"
                        )
                    )
                ),
                "overall_label": _safe_text(
                    current.get(
                        "overall_label"
                    ),
                    "Not Available",
                ),
                "image_data_uri": (
                    _image_bytes_to_data_uri(
                        image_bytes
                    )
                ),
            }
        )

    return payload


# ============================================================
# CONSOLIDATED HTML TABLE
# ============================================================

def _build_consolidated_rows_html(
    reports: Sequence[Dict[str, Any]],
) -> str:
    ranked = _ranked_reports(
        reports
    )

    rows = []

    for report in ranked:
        trainer_name = html.escape(
            _safe_text(
                report.get("trainer_name"),
                "Trainer",
            )
        )

        rank = report.get(
            "rank",
            "",
        )

        rating = html.escape(
            _rating_text(
                report.get(
                    "overall_rating"
                )
            )
        )

        rows.append(
            f"""
            <tr>
                <td class="rank-cell">{rank}</td>
                <td class="trainer-cell">{trainer_name}</td>
                <td class="rating-cell">{rating}</td>
            </tr>
            """
        )

    if not rows:
        return """
        <tr>
            <td colspan="3" class="empty-cell">
                No trainer feedback data available.
            </td>
        </tr>
        """

    return "\n".join(rows)


# ============================================================
# MAIN HTML GENERATOR
# ============================================================

def generate_campus_html_bytes(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
) -> bytes:
    """
    Generate one completely self-contained campus HTML report.

    Parameters
    ----------
    campus_name:
        College/campus name displayed at the top.

    reports:
        Trainer report dictionaries for ONE campus only.

    Returns
    -------
    bytes
        UTF-8 encoded .html content ready for st.download_button().
    """
    if not reports:
        raise ValueError(
            "No trainer reports were provided for HTML generation."
        )

    campus_name = _safe_text(
        campus_name,
        "Campus",
    )

    trainer_payload = (
        _build_trainer_payload(
            campus_name,
            reports,
        )
    )

    ranked = _ranked_reports(
        reports
    )

    campus_average = (
        _campus_average_rating(
            reports
        )
    )

    total_responses = (
        _total_responses(
            reports
        )
    )

    highest_rating = None
    highest_trainer = "N/A"

    if ranked:
        highest_rating = (
            ranked[0].get(
                "overall_rating"
            )
        )

        highest_trainer = _safe_text(
            ranked[0].get(
                "trainer_name"
            ),
            "N/A",
        )

    consolidated_rows = (
        _build_consolidated_rows_html(
            reports
        )
    )

    trainer_json = json.dumps(
        trainer_payload,
        ensure_ascii=False,
    )

    escaped_campus = html.escape(
        campus_name
    )

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>
<title>{escaped_campus} - Trainer Feedback Report</title>

<style>
    * {{
        box-sizing: border-box;
    }}

    :root {{
        --navy: #173A63;
        --blue: #2E67A3;
        --orange: #FF8A34;
        --bg: #F6F8FC;
        --card: #FFFFFF;
        --text: #1F2937;
        --muted: #667085;
        --border: #D9E0EA;
        --green-bg: #EEF7F2;
        --green-text: #235B3A;
    }}

    html {{
        scroll-behavior: smooth;
    }}

    body {{
        margin: 0;
        font-family:
            "Segoe UI",
            Arial,
            Helvetica,
            sans-serif;
        background: var(--bg);
        color: var(--text);
    }}

    .page-shell {{
        width: min(1180px, calc(100% - 32px));
        margin: 28px auto 50px auto;
    }}

    .header {{
        background:
            linear-gradient(
                110deg,
                var(--navy),
                var(--blue)
            );
        color: #FFFFFF;
        border-radius: 16px;
        padding: 28px 32px;
        border-left: 7px solid var(--orange);
        box-shadow:
            0 8px 22px
            rgba(23, 58, 99, 0.13);
    }}

    .header h1 {{
        margin: 0;
        font-size: 31px;
        line-height: 1.2;
    }}

    .header .campus-name {{
        margin-top: 9px;
        font-size: 21px;
        color: #DCE8F4;
        font-weight: 600;
    }}

    .header .subtitle {{
        margin-top: 8px;
        color: #DCE8F4;
        font-size: 14px;
    }}

    .metrics {{
        display: grid;
        grid-template-columns:
            repeat(4, minmax(0, 1fr));
        gap: 16px;
        margin: 20px 0;
    }}

    .metric {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 13px;
        padding: 18px;
        min-height: 105px;
    }}

    .metric-label {{
        color: var(--muted);
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.4px;
        text-transform: uppercase;
    }}

    .metric-value {{
        margin-top: 10px;
        color: var(--navy);
        font-size: 24px;
        font-weight: 750;
    }}

    .main-options {{
        display: grid;
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
        gap: 16px;
        margin: 22px 0;
    }}

    button {{
        font: inherit;
    }}

    .main-btn {{
        width: 100%;
        border: 0;
        border-radius: 12px;
        padding: 17px 20px;
        cursor: pointer;
        font-size: 17px;
        font-weight: 700;
        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease,
            background 0.15s ease;
    }}

    .main-btn:hover {{
        transform: translateY(-1px);
        box-shadow:
            0 7px 18px
            rgba(23, 58, 99, 0.12);
    }}

    .btn-primary {{
        background: var(--navy);
        color: #FFFFFF;
    }}

    .btn-secondary {{
        background: #FFFFFF;
        color: var(--navy);
        border: 1px solid var(--navy);
    }}

    .section {{
        display: none;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 24px;
        margin-top: 18px;
    }}

    .section.active {{
        display: block;
    }}

    .section-title {{
        margin: 0 0 18px 0;
        color: var(--navy);
        font-size: 23px;
    }}

    .section-note {{
        color: var(--muted);
        margin-top: -8px;
        margin-bottom: 18px;
        font-size: 14px;
    }}

    .summary-table {{
        width: 100%;
        border-collapse: collapse;
        overflow: hidden;
        border-radius: 10px;
    }}

    .summary-table th {{
        background: #E8EEF5;
        color: #344054;
        padding: 14px 16px;
        text-align: left;
        font-size: 13px;
        letter-spacing: 0.3px;
    }}

    .summary-table td {{
        border-bottom: 1px solid #E7ECF2;
        padding: 14px 16px;
    }}

    .summary-table tr:nth-child(even) {{
        background: #FAFBFD;
    }}

    .rank-cell {{
        width: 100px;
        font-weight: 800;
        color: var(--navy);
    }}

    .trainer-cell {{
        font-weight: 650;
    }}

    .rating-cell {{
        width: 190px;
        font-weight: 750;
        color: var(--navy);
    }}

    .empty-cell {{
        color: var(--muted);
        text-align: center;
    }}

    .trainer-controls {{
        display: grid;
        grid-template-columns:
            minmax(260px, 1fr)
            auto;
        gap: 12px;
        align-items: end;
        margin-bottom: 16px;
    }}

    label {{
        display: block;
        color: #344054;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 7px;
    }}

    select {{
        width: 100%;
        min-height: 44px;
        padding: 9px 11px;
        border: 1px solid #BFC9D6;
        border-radius: 8px;
        background: #FFFFFF;
        color: var(--text);
        font-size: 15px;
    }}

    .action-btn {{
        min-height: 44px;
        padding: 9px 18px;
        border: 0;
        border-radius: 8px;
        background: var(--orange);
        color: #FFFFFF;
        font-weight: 700;
        cursor: pointer;
    }}

    .trainer-toolbar {{
        display: none;
        grid-template-columns:
            auto auto 1fr auto auto;
        gap: 10px;
        align-items: center;
        margin: 13px 0 18px 0;
    }}

    .trainer-toolbar.active {{
        display: grid;
    }}

    .toolbar-btn {{
        border: 1px solid #BFC9D6;
        background: #FFFFFF;
        color: var(--navy);
        border-radius: 8px;
        min-height: 40px;
        padding: 8px 14px;
        font-weight: 650;
        cursor: pointer;
    }}

    .toolbar-spacer {{
        min-width: 10px;
    }}

    .print-btn {{
        border-color: var(--navy);
        background: var(--navy);
        color: #FFFFFF;
    }}

    .trainer-meta {{
        display: none;
        grid-template-columns:
            repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin-bottom: 16px;
    }}

    .trainer-meta.active {{
        display: grid;
    }}

    .mini-card {{
        background: #F8FAFC;
        border: 1px solid #E3E8EF;
        border-radius: 9px;
        padding: 11px 12px;
    }}

    .mini-label {{
        color: var(--muted);
        font-size: 11px;
        text-transform: uppercase;
        font-weight: 700;
    }}

    .mini-value {{
        margin-top: 5px;
        color: var(--navy);
        font-size: 16px;
        font-weight: 750;
    }}

    .report-wrap {{
        display: none;
        border: 1px solid #E3E8EF;
        border-radius: 10px;
        background: #FFFFFF;
        padding: 12px;
    }}

    .report-wrap.active {{
        display: block;
    }}

    .report-wrap img {{
        display: block;
        width: 100%;
        height: auto;
        border-radius: 8px;
    }}

    .back-row {{
        display: flex;
        justify-content: flex-end;
        margin-top: 18px;
    }}

    .back-btn {{
        border: 1px solid var(--border);
        background: #FFFFFF;
        color: var(--navy);
        border-radius: 8px;
        padding: 9px 14px;
        font-weight: 650;
        cursor: pointer;
    }}

    .footer {{
        text-align: center;
        color: var(--muted);
        font-size: 12px;
        margin-top: 25px;
    }}

    @media (max-width: 760px) {{
        .metrics {{
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }}

        .main-options {{
            grid-template-columns: 1fr;
        }}

        .trainer-controls {{
            grid-template-columns: 1fr;
        }}

        .trainer-toolbar {{
            grid-template-columns:
                1fr 1fr;
        }}

        .toolbar-spacer {{
            display: none;
        }}

        .trainer-meta {{
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }}

        .summary-table {{
            font-size: 13px;
        }}

        .summary-table th,
        .summary-table td {{
            padding: 10px;
        }}
    }}

    @media print {{
        body {{
            background: #FFFFFF;
        }}

        .page-shell {{
            width: 100%;
            margin: 0;
        }}

        .main-options,
        .trainer-controls,
        .trainer-toolbar,
        .back-row,
        .footer {{
            display: none !important;
        }}

        .header {{
            box-shadow: none;
        }}

        .section {{
            border: 0;
            padding: 8px 0;
        }}

        #consolidatedSection.active {{
            display: block;
        }}

        #trainerSection.active {{
            display: block;
        }}

        .report-wrap.active {{
            border: 0;
            padding: 0;
        }}
    }}
</style>
</head>

<body>

<div class="page-shell">

    <header class="header">
        <h1>Trainer Feedback Report</h1>

        <div class="campus-name">
            {escaped_campus}
        </div>

        <div class="subtitle">
            Campus-wise trainer feedback analysis
        </div>
    </header>

    <section class="metrics">
        <div class="metric">
            <div class="metric-label">
                Total Trainers
            </div>

            <div class="metric-value">
                {len(reports)}
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">
                Student Responses
            </div>

            <div class="metric-value">
                {total_responses}
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">
                Campus Avg Rating
            </div>

            <div class="metric-value">
                {_rating_text(campus_average)}
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">
                Highest Rated Trainer
            </div>

            <div class="metric-value"
                 style="font-size:18px;">
                {html.escape(highest_trainer)}
                <br>
                <span style="
                    font-size:14px;
                    color:#667085;
                ">
                    {_rating_text(highest_rating)}
                </span>
            </div>
        </div>
    </section>


    <section class="main-options">

        <button
            class="main-btn btn-primary"
            onclick="showConsolidated()"
        >
            Consolidated Report
        </button>

        <button
            class="main-btn btn-secondary"
            onclick="showTrainerSection()"
        >
            Trainer-wise Feedback
        </button>

    </section>


    <!-- ===================================================
         CONSOLIDATED REPORT
         =================================================== -->

    <section
        id="consolidatedSection"
        class="section active"
    >
        <h2 class="section-title">
            Consolidated Report
        </h2>

        <div class="section-note">
            Ranking and average ratings for trainers within
            {escaped_campus} only.
        </div>

        <table class="summary-table">

            <thead>
                <tr>
                    <th>RANK</th>
                    <th>TRAINER NAME</th>
                    <th>AVERAGE RATING</th>
                </tr>
            </thead>

            <tbody>
                {consolidated_rows}
            </tbody>

        </table>

        <div class="back-row">
            <button
                class="toolbar-btn print-btn"
                onclick="window.print()"
            >
                Print / Save as PDF
            </button>
        </div>
    </section>


    <!-- ===================================================
         TRAINER-WISE FEEDBACK
         =================================================== -->

    <section
        id="trainerSection"
        class="section"
    >

        <h2 class="section-title">
            Trainer-wise Feedback
        </h2>

        <div class="section-note">
            Select a trainer and click View Report.
        </div>

        <div class="trainer-controls">

            <div>
                <label for="trainerSelect">
                    Select Trainer
                </label>

                <select id="trainerSelect">
                </select>
            </div>

            <button
                class="action-btn"
                onclick="viewSelectedTrainer()"
            >
                View Report
            </button>

        </div>


        <div
            id="trainerToolbar"
            class="trainer-toolbar"
        >

            <button
                class="toolbar-btn"
                onclick="previousTrainer()"
            >
                Previous Trainer
            </button>

            <button
                class="toolbar-btn"
                onclick="nextTrainer()"
            >
                Next Trainer
            </button>

            <div class="toolbar-spacer"></div>

            <button
                class="toolbar-btn"
                onclick="showConsolidated()"
            >
                Back to Summary
            </button>

            <button
                class="toolbar-btn print-btn"
                onclick="window.print()"
            >
                Print / Save as PDF
            </button>

        </div>


        <div
            id="trainerMeta"
            class="trainer-meta"
        >

            <div class="mini-card">
                <div class="mini-label">
                    Trainer
                </div>
                <div
                    id="metaTrainer"
                    class="mini-value"
                >
                </div>
            </div>

            <div class="mini-card">
                <div class="mini-label">
                    Responses
                </div>
                <div
                    id="metaResponses"
                    class="mini-value"
                >
                </div>
            </div>

            <div class="mini-card">
                <div class="mini-label">
                    Overall Rating
                </div>
                <div
                    id="metaRating"
                    class="mini-value"
                >
                </div>
            </div>

            <div class="mini-card">
                <div class="mini-label">
                    Positive Feedback
                </div>
                <div
                    id="metaPositive"
                    class="mini-value"
                >
                </div>
            </div>

        </div>


        <div
            id="reportWrap"
            class="report-wrap"
        >

            <img
                id="trainerReportImage"
                src=""
                alt="Trainer Feedback Report"
            >

        </div>

    </section>


    <div class="footer">
        Trainer Profile Generator · Campus-wise Feedback Report
    </div>

</div>


<script>
    const trainers = {trainer_json};

    const consolidatedSection =
        document.getElementById(
            "consolidatedSection"
        );

    const trainerSection =
        document.getElementById(
            "trainerSection"
        );

    const trainerSelect =
        document.getElementById(
            "trainerSelect"
        );

    const trainerToolbar =
        document.getElementById(
            "trainerToolbar"
        );

    const trainerMeta =
        document.getElementById(
            "trainerMeta"
        );

    const reportWrap =
        document.getElementById(
            "reportWrap"
        );

    const reportImage =
        document.getElementById(
            "trainerReportImage"
        );

    let currentTrainerIndex = 0;


    function ratingText(value) {{
        if (
            value === null ||
            value === undefined ||
            Number.isNaN(Number(value))
        ) {{
            return "N/A";
        }}

        return Number(value).toFixed(2) + " / 5";
    }}


    function percentText(value) {{
        if (
            value === null ||
            value === undefined ||
            Number.isNaN(Number(value))
        ) {{
            return "N/A";
        }}

        return Number(value).toFixed(1) + "%";
    }}


    function populateTrainerDropdown() {{

        trainerSelect.innerHTML = "";

        trainers.forEach(
            (trainer, index) => {{

                const option =
                    document.createElement(
                        "option"
                    );

                option.value = index;
                option.textContent =
                    trainer.trainer_name;

                trainerSelect.appendChild(
                    option
                );
            }}
        );
    }}


    function hideAllSections() {{
        consolidatedSection.classList.remove(
            "active"
        );

        trainerSection.classList.remove(
            "active"
        );
    }}


    function showConsolidated() {{
        hideAllSections();

        consolidatedSection.classList.add(
            "active"
        );

        window.scrollTo({{
            top: consolidatedSection.offsetTop - 20,
            behavior: "smooth"
        }});
    }}


    function showTrainerSection() {{
        hideAllSections();

        trainerSection.classList.add(
            "active"
        );

        window.scrollTo({{
            top: trainerSection.offsetTop - 20,
            behavior: "smooth"
        }});
    }}


    function viewSelectedTrainer() {{

        if (!trainers.length) {{
            return;
        }}

        currentTrainerIndex =
            Number(
                trainerSelect.value || 0
            );

        showTrainerReport(
            currentTrainerIndex
        );
    }}


    function showTrainerReport(index) {{

        if (!trainers.length) {{
            return;
        }}

        if (index < 0) {{
            index = trainers.length - 1;
        }}

        if (index >= trainers.length) {{
            index = 0;
        }}

        currentTrainerIndex = index;

        const trainer =
            trainers[
                currentTrainerIndex
            ];

        trainerSelect.value =
            currentTrainerIndex;

        document.getElementById(
            "metaTrainer"
        ).textContent =
            trainer.trainer_name;

        document.getElementById(
            "metaResponses"
        ).textContent =
            trainer.responses;

        document.getElementById(
            "metaRating"
        ).textContent =
            ratingText(
                trainer.overall_rating
            );

        document.getElementById(
            "metaPositive"
        ).textContent =
            percentText(
                trainer.positive_percent
            );

        reportImage.src =
            trainer.image_data_uri;

        trainerToolbar.classList.add(
            "active"
        );

        trainerMeta.classList.add(
            "active"
        );

        reportWrap.classList.add(
            "active"
        );

        showTrainerSection();
    }}


    function previousTrainer() {{
        showTrainerReport(
            currentTrainerIndex - 1
        );
    }}


    function nextTrainer() {{
        showTrainerReport(
            currentTrainerIndex + 1
        );
    }}


    populateTrainerDropdown();
    showConsolidated();
</script>

</body>
</html>
"""

    return html_content.encode(
        "utf-8"
    )


# ============================================================
# SAVE TO DISK
# ============================================================

def generate_campus_html(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
    output_path: str | Path,
) -> Path:
    """
    Generate one campus HTML file and save it to disk.
    """
    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    html_bytes = (
        generate_campus_html_bytes(
            campus_name=campus_name,
            reports=reports,
        )
    )

    output_path.write_bytes(
        html_bytes
    )

    return output_path


# ============================================================
# STANDARD CAMPUS OUTPUT FOLDER
# ============================================================

def generate_campus_html_to_folder(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
    campus_output_dir: str | Path,
) -> Path:
    """
    Example output:
        output/feedback_reports/SVPCET/
            SVPCET_Feedback_Report.html
    """
    campus_output_dir = Path(
        campus_output_dir
    )

    campus_output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = (
        f"{_safe_slug(campus_name)}_"
        "Feedback_Report.html"
    )

    return generate_campus_html(
        campus_name=campus_name,
        reports=reports,
        output_path=(
            campus_output_dir
            / filename
        ),
    )


# ============================================================
# DOWNLOAD HELPER
# ============================================================

def html_file_to_bytes(
    path: str | Path,
) -> bytes:
    """
    Read generated HTML for Streamlit download.
    """
    return Path(path).read_bytes()


# ============================================================
# VALIDATION
# ============================================================

def validate_reports_for_html(
    reports: Sequence[Dict[str, Any]],
) -> List[str]:
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
