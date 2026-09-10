"""
feedback_image_generator.py
---------------------------
Creates one-page trainer feedback report images for the
Trainer Profile Generator.

Designed to work with report dictionaries produced by:
    utils.feedback_analysis.trainer_analysis_to_report_dict

Main functions:
    generate_trainer_report_image(...)
    generate_all_trainer_images(...)

Each trainer image is campus-specific.
No data from different colleges/campuses is combined.
"""

from __future__ import annotations

import os
import re
import textwrap
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# DEFAULT REPORT SETTINGS
# ============================================================

DEFAULT_WIDTH = 1600
DEFAULT_HEIGHT = 2200

BACKGROUND = "#F6F8FC"
CARD_BG = "#FFFFFF"
HEADER_BG = "#173A63"
HEADER_ACCENT = "#FF8A34"

TEXT_PRIMARY = "#1F2937"
TEXT_SECONDARY = "#667085"
TEXT_LIGHT = "#FFFFFF"

BORDER = "#D9E0EA"
BAR_BG = "#E8EDF4"
BAR_FILL = "#2E67A3"

STRENGTH_BG = "#EEF7F2"
FOCUS_BG = "#FFF5EB"
VOICE_BG = "#F7F3FF"

STRENGTH_TEXT = "#235B3A"
FOCUS_TEXT = "#8B4A12"
VOICE_TEXT = "#513779"

POSITIVE_BADGE_BG = "#EEF7F2"
POSITIVE_BADGE_TEXT = "#235B3A"


# ============================================================
# FONT HELPERS
# ============================================================

def _font_candidates() -> List[str]:
    """
    Cross-platform font candidates.
    """
    candidates = []

    # Windows
    candidates.extend([
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf",
    ])

    # Linux / Streamlit Cloud
    candidates.extend([
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ])

    # macOS fallback
    candidates.extend([
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ])

    return candidates


def _find_font_path(bold: bool = False) -> Optional[str]:
    """
    Find a usable font path.
    """
    candidates = _font_candidates()

    if bold:
        preferred = [
            p for p in candidates
            if any(
                token in Path(p).name.lower()
                for token in ["bold", "arialbd", "calibrib", "segoeuib"]
            )
        ]
        normal = [p for p in candidates if p not in preferred]
        candidates = preferred + normal

    for path in candidates:
        if os.path.exists(path):
            return path

    return None


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """
    Load a font safely.
    """
    path = _find_font_path(bold=bold)

    if path:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            pass

    # PIL default font fallback.
    return ImageFont.load_default()


# ============================================================
# GENERAL DRAWING HELPERS
# ============================================================

def _safe_text(value: Any, fallback: str = "-") -> str:
    if value is None:
        return fallback

    text = str(value).strip()

    if not text:
        return fallback

    return text


def _safe_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None


def _rounded_rectangle(
    draw: ImageDraw.ImageDraw,
    box: Tuple[int, int, int, int],
    radius: int,
    fill: str,
    outline: Optional[str] = None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(
        box,
        radius=radius,
        fill=fill,
        outline=outline,
        width=width,
    )


def _draw_text(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: str = TEXT_PRIMARY,
    anchor: Optional[str] = None,
) -> None:
    draw.text(
        xy,
        text,
        font=font,
        fill=fill,
        anchor=anchor,
    )


def _draw_multiline(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: str,
    max_width: int,
    line_spacing: int = 8,
    max_lines: Optional[int] = None,
) -> int:
    """
    Draw wrapped text and return the used height.
    """
    text = _safe_text(text, "")
    if not text:
        return 0

    words = text.split()
    if not words:
        return 0

    lines: List[str] = []
    current = ""

    for word in words:
        test = word if not current else f"{current} {word}"
        bbox = draw.textbbox((0, 0), test, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        if lines:
            last = lines[-1]
            if not last.endswith("..."):
                lines[-1] = last.rstrip(".") + "..."

    x, y = xy
    used_height = 0

    bbox = draw.textbbox((0, 0), "Ag", font=font)
    line_height = bbox[3] - bbox[1]

    for line in lines:
        draw.text((x, y + used_height), line, font=font, fill=fill)
        used_height += line_height + line_spacing

    return used_height


def _draw_section_title(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    title: str,
    width: int,
) -> None:
    _draw_text(
        draw,
        (x, y),
        title.upper(),
        _font(31, bold=True),
        TEXT_PRIMARY,
    )

    draw.line(
        (x, y + 48, x + width, y + 48),
        fill=BORDER,
        width=2,
    )


def _sanitize_filename(value: str) -> str:
    """
    Safe Windows/Linux filename.
    """
    value = re.sub(r'[<>:"/\\|?*]+', "_", str(value))
    value = re.sub(r"\s+", "_", value.strip())
    value = re.sub(r"_+", "_", value)
    return value.strip("._") or "Trainer"


# ============================================================
# REPORT ELEMENTS
# ============================================================

def _draw_header(
    draw: ImageDraw.ImageDraw,
    report: Dict[str, Any],
    width: int,
) -> None:
    """
    Main top banner.
    """
    draw.rectangle(
        (0, 0, width, 280),
        fill=HEADER_BG,
    )

    # Accent bar
    draw.rectangle(
        (0, 0, 18, 280),
        fill=HEADER_ACCENT,
    )

    _draw_text(
        draw,
        (80, 62),
        "TRAINER FEEDBACK SUMMARY",
        _font(52, bold=True),
        TEXT_LIGHT,
    )

    trainer = _safe_text(report.get("trainer_name"), "Trainer")
    campus = _safe_text(report.get("campus_name"), "Campus")

    _draw_text(
        draw,
        (80, 140),
        trainer,
        _font(43, bold=True),
        TEXT_LIGHT,
    )

    _draw_text(
        draw,
        (80, 202),
        campus,
        _font(29),
        "#DCE8F4",
    )


def _draw_kpi_cards(
    draw: ImageDraw.ImageDraw,
    report: Dict[str, Any],
    x: int,
    y: int,
    total_width: int,
) -> int:
    """
    Draw overall rating, responses and positive feedback.
    """
    gap = 24
    card_width = (total_width - (gap * 2)) // 3
    card_height = 220

    rating = _safe_float(report.get("overall_rating"))
    responses = int(report.get("responses") or 0)
    positive = _safe_float(report.get("positive_rating_percent"))

    cards = [
        (
            "OVERALL RATING",
            f"{rating:.2f} / 5" if rating is not None else "N/A",
            "★★★★★" if rating is not None else "—",
        ),
        (
            "STUDENT RESPONSES",
            str(responses),
            "Feedback submissions",
        ),
        (
            "POSITIVE FEEDBACK",
            f"{positive:.1f}%" if positive is not None else "N/A",
            "4★ and 5★ ratings",
        ),
    ]

    for index, (label, value, foot) in enumerate(cards):
        left = x + index * (card_width + gap)
        right = left + card_width

        _rounded_rectangle(
            draw,
            (left, y, right, y + card_height),
            radius=24,
            fill=CARD_BG,
            outline=BORDER,
            width=2,
        )

        _draw_text(
            draw,
            (left + 28, y + 30),
            label,
            _font(24, bold=True),
            TEXT_SECONDARY,
        )

        _draw_text(
            draw,
            (left + 28, y + 84),
            value,
            _font(48, bold=True),
            TEXT_PRIMARY,
        )

        if index == 0 and rating is not None:
            foot_fill = HEADER_ACCENT
        elif index == 2 and positive is not None:
            foot_fill = POSITIVE_BADGE_TEXT
        else:
            foot_fill = TEXT_SECONDARY

        _draw_text(
            draw,
            (left + 28, y + 157),
            foot,
            _font(23),
            foot_fill,
        )

    return y + card_height


def _draw_parameter_bars(
    draw: ImageDraw.ImageDraw,
    report: Dict[str, Any],
    x: int,
    y: int,
    width: int,
) -> int:
    """
    Draw detailed parameter score bars.
    Expected score range: -2 to +2.
    For presentation clarity, the visual fill is normalized from 0 to 2
    after clamping negative values at 0, while the original numeric value
    is still shown.
    """
    parameters = report.get("parameters") or []

    _draw_section_title(
        draw,
        x,
        y,
        "Performance Areas",
        width,
    )

    y += 82

    if not parameters:
        _draw_text(
            draw,
            (x, y),
            "Detailed parameter scores are not available.",
            _font(27),
            TEXT_SECONDARY,
        )
        return y + 70

    label_width = 485
    value_width = 125
    bar_x = x + label_width
    bar_width = width - label_width - value_width
    row_height = 95

    for p in parameters:
        label = _safe_text(p.get("label"), "Parameter")
        avg = _safe_float(p.get("average"))

        _draw_multiline(
            draw,
            (x, y + 8),
            label,
            _font(27, bold=True),
            TEXT_PRIMARY,
            max_width=label_width - 35,
            line_spacing=2,
            max_lines=2,
        )

        bar_y = y + 25
        _rounded_rectangle(
            draw,
            (
                bar_x,
                bar_y,
                bar_x + bar_width,
                bar_y + 28,
            ),
            radius=14,
            fill=BAR_BG,
        )

        if avg is not None:
            visual_score = max(0.0, min(2.0, avg))
            fill_ratio = visual_score / 2.0
            fill_width = int(bar_width * fill_ratio)

            if fill_width > 0:
                _rounded_rectangle(
                    draw,
                    (
                        bar_x,
                        bar_y,
                        bar_x + fill_width,
                        bar_y + 28,
                    ),
                    radius=14,
                    fill=BAR_FILL,
                )

            score_text = f"{avg:.2f} / 2"
        else:
            score_text = "N/A"

        _draw_text(
            draw,
            (
                x + width,
                bar_y + 14,
            ),
            score_text,
            _font(26, bold=True),
            TEXT_PRIMARY,
            anchor="rm",
        )

        y += row_height

    return y


def _draw_insight_box(
    draw: ImageDraw.ImageDraw,
    box: Tuple[int, int, int, int],
    title: str,
    items: Sequence[str],
    fill: str,
    title_fill: str,
    bullet: str,
) -> None:
    left, top, right, bottom = box

    _rounded_rectangle(
        draw,
        box,
        radius=24,
        fill=fill,
        outline=BORDER,
        width=1,
    )

    _draw_text(
        draw,
        (left + 30, top + 28),
        title,
        _font(29, bold=True),
        title_fill,
    )

    y = top + 84

    if not items:
        items = ["Not enough data available"]

    for item in list(items)[:3]:
        _draw_text(
            draw,
            (left + 30, y),
            bullet,
            _font(27, bold=True),
            title_fill,
        )

        used = _draw_multiline(
            draw,
            (left + 72, y),
            _safe_text(item),
            _font(25),
            TEXT_PRIMARY,
            max_width=(right - left) - 105,
            line_spacing=3,
            max_lines=2,
        )

        y += max(54, used + 13)

        if y > bottom - 42:
            break


def _draw_strength_focus(
    draw: ImageDraw.ImageDraw,
    report: Dict[str, Any],
    x: int,
    y: int,
    width: int,
) -> int:
    """
    Two side-by-side insight boxes.
    """
    gap = 24
    box_width = (width - gap) // 2
    box_height = 330

    strengths = report.get("strengths") or []
    focus = report.get("development_focus") or []

    _draw_insight_box(
        draw,
        (
            x,
            y,
            x + box_width,
            y + box_height,
        ),
        "KEY STRENGTHS",
        strengths,
        STRENGTH_BG,
        STRENGTH_TEXT,
        "✓",
    )

    _draw_insight_box(
        draw,
        (
            x + box_width + gap,
            y,
            x + width,
            y + box_height,
        ),
        "DEVELOPMENT FOCUS",
        focus,
        FOCUS_BG,
        FOCUS_TEXT,
        "→",
    )

    return y + box_height


def _draw_student_voice(
    draw: ImageDraw.ImageDraw,
    report: Dict[str, Any],
    x: int,
    y: int,
    width: int,
) -> int:
    """
    Student voice box.
    """
    comments = report.get("student_voice") or []
    box_height = 360

    _rounded_rectangle(
        draw,
        (
            x,
            y,
            x + width,
            y + box_height,
        ),
        radius=24,
        fill=VOICE_BG,
        outline=BORDER,
        width=1,
    )

    _draw_text(
        draw,
        (x + 30, y + 28),
        "STUDENT VOICE",
        _font(29, bold=True),
        VOICE_TEXT,
    )

    current_y = y + 86

    if not comments:
        _draw_text(
            draw,
            (x + 30, current_y),
            "No meaningful written comments were available.",
            _font(25),
            TEXT_SECONDARY,
        )
        return y + box_height

    for comment in comments[:3]:
        _draw_text(
            draw,
            (x + 30, current_y),
            "“",
            _font(32, bold=True),
            VOICE_TEXT,
        )

        used = _draw_multiline(
            draw,
            (x + 64, current_y),
            _safe_text(comment),
            _font(24),
            TEXT_PRIMARY,
            max_width=width - 110,
            line_spacing=3,
            max_lines=2,
        )

        current_y += max(68, used + 18)

        if current_y > y + box_height - 55:
            break

    return y + box_height


def _draw_footer(
    draw: ImageDraw.ImageDraw,
    report: Dict[str, Any],
    x: int,
    y: int,
    width: int,
) -> None:
    """
    Small final performance label and optional management summary.
    """
    label = _safe_text(report.get("overall_label"), "Not Available")
    summary = _safe_text(report.get("management_summary"), "")

    _rounded_rectangle(
        draw,
        (x, y, x + width, y + 170),
        radius=24,
        fill=CARD_BG,
        outline=BORDER,
        width=1,
    )

    _draw_text(
        draw,
        (x + 28, y + 28),
        f"Overall Performance: {label}",
        _font(28, bold=True),
        HEADER_BG,
    )

    if summary:
        _draw_multiline(
            draw,
            (x + 28, y + 76),
            summary,
            _font(22),
            TEXT_SECONDARY,
            max_width=width - 56,
            line_spacing=3,
            max_lines=3,
        )


# ============================================================
# MAIN IMAGE GENERATOR
# ============================================================

def generate_trainer_report_image(
    report: Dict[str, Any],
    output_path: Optional[str | Path] = None,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    image_format: str = "PNG",
) -> Path:
    """
    Generate one trainer feedback report image.

    Parameters
    ----------
    report:
        Dictionary returned by
        feedback_analysis.trainer_analysis_to_report_dict(...)

    output_path:
        Full file path. If omitted, a filename is created in the
        current working directory.

    width / height:
        Canvas size.

    image_format:
        PNG recommended. JPEG is also supported.

    Returns
    -------
    pathlib.Path
        Path to generated image.
    """
    trainer_name = _safe_text(report.get("trainer_name"), "Trainer")
    campus_name = _safe_text(report.get("campus_name"), "Campus")

    if output_path is None:
        filename = (
            f"{_sanitize_filename(campus_name)}_"
            f"{_sanitize_filename(trainer_name)}_Feedback_Report.png"
        )
        output_path = Path.cwd() / filename
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    image = Image.new(
        "RGB",
        (width, height),
        BACKGROUND,
    )
    draw = ImageDraw.Draw(image)

    _draw_header(
        draw,
        report,
        width,
    )

    margin_x = 70
    content_width = width - (margin_x * 2)

    y = 330

    y = _draw_kpi_cards(
        draw,
        report,
        margin_x,
        y,
        content_width,
    )

    y += 55

    y = _draw_parameter_bars(
        draw,
        report,
        margin_x,
        y,
        content_width,
    )

    y += 25

    y = _draw_strength_focus(
        draw,
        report,
        margin_x,
        y,
        content_width,
    )

    y += 28

    y = _draw_student_voice(
        draw,
        report,
        margin_x,
        y,
        content_width,
    )

    y += 28

    # If the fixed canvas is too short, extend it before footer.
    footer_height = 170
    required_height = y + footer_height + 45

    if required_height > height:
        extended = Image.new(
            "RGB",
            (width, required_height),
            BACKGROUND,
        )
        extended.paste(image, (0, 0))
        image = extended
        draw = ImageDraw.Draw(image)
        height = required_height

    _draw_footer(
        draw,
        report,
        margin_x,
        y,
        content_width,
    )

    # Save
    fmt = str(image_format).upper().strip()

    if fmt in {"JPG", "JPEG"}:
        image.save(
            output_path,
            format="JPEG",
            quality=95,
            optimize=True,
        )
    else:
        image.save(
            output_path,
            format="PNG",
            optimize=True,
        )

    return output_path


# ============================================================
# BULK CAMPUS IMAGE GENERATION
# ============================================================

def generate_all_trainer_images(
    campus_name: str,
    reports: Sequence[Dict[str, Any]],
    output_dir: str | Path,
    overwrite: bool = True,
) -> List[Path]:
    """
    Generate one image for every trainer in ONE campus.

    Example:
        reports = campus_report_data(campus)

        paths = generate_all_trainer_images(
            campus_name=campus.campus_name,
            reports=reports,
            output_dir="output/feedback_reports/SVPCET/images"
        )
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
            f"{_sanitize_filename(trainer_name)}_Feedback_Report.png"
        )

        output_path = output_dir / filename

        if output_path.exists() and not overwrite:
            generated.append(output_path)
            continue

        # Force correct campus name for this campus run.
        report_copy = dict(report)
        report_copy["campus_name"] = campus_name

        generated_path = generate_trainer_report_image(
            report=report_copy,
            output_path=output_path,
        )

        generated.append(generated_path)

    return generated


# ============================================================
# BYTES HELPERS FOR STREAMLIT
# ============================================================

def image_file_to_bytes(path: str | Path) -> bytes:
    """
    Read a generated image as bytes for st.download_button().
    """
    return Path(path).read_bytes()


def generate_trainer_report_image_bytes(
    report: Dict[str, Any],
) -> bytes:
    """
    Generate image directly in memory.
    Useful for:
        st.image(...)
        st.download_button(...)
    """
    from io import BytesIO

    trainer_name = _safe_text(report.get("trainer_name"), "Trainer")
    campus_name = _safe_text(report.get("campus_name"), "Campus")

    # Generate to a temporary in-memory-compatible image by using
    # the same drawing flow.
    width = DEFAULT_WIDTH
    height = DEFAULT_HEIGHT

    image = Image.new(
        "RGB",
        (width, height),
        BACKGROUND,
    )
    draw = ImageDraw.Draw(image)

    _draw_header(draw, report, width)

    margin_x = 70
    content_width = width - (margin_x * 2)

    y = 330
    y = _draw_kpi_cards(
        draw, report, margin_x, y, content_width
    )
    y += 55

    y = _draw_parameter_bars(
        draw, report, margin_x, y, content_width
    )
    y += 25

    y = _draw_strength_focus(
        draw, report, margin_x, y, content_width
    )
    y += 28

    y = _draw_student_voice(
        draw, report, margin_x, y, content_width
    )
    y += 28

    required_height = y + 215

    if required_height > height:
        extended = Image.new(
            "RGB",
            (width, required_height),
            BACKGROUND,
        )
        extended.paste(image, (0, 0))
        image = extended
        draw = ImageDraw.Draw(image)

    _draw_footer(
        draw,
        report,
        margin_x,
        y,
        content_width,
    )

    buffer = BytesIO()
    image.save(
        buffer,
        format="PNG",
        optimize=True,
    )
    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# SIMPLE VALIDATION
# ============================================================

def validate_report_dict(
    report: Dict[str, Any],
) -> List[str]:
    """
    Validate the minimum fields needed for an image report.
    """
    messages: List[str] = []

    if not report.get("trainer_name"):
        messages.append(
            "Trainer name is missing."
        )

    if not report.get("campus_name"):
        messages.append(
            "Campus/college name is missing."
        )

    if report.get("responses") in (None, ""):
        messages.append(
            "Response count is missing."
        )

    if not report.get("parameters"):
        messages.append(
            "Detailed parameter scores are not available."
        )

    return messages
