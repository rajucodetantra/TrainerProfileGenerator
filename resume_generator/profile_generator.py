from pathlib import Path
import re

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


# =========================================================
# ITERATE THROUGH ALL PARAGRAPHS
# INCLUDING TABLE CELLS
# =========================================================

def iter_paragraphs(parent):
    """
    Iterate through all paragraphs in a document,
    including paragraphs inside table cells.
    """

    for paragraph in parent.paragraphs:
        yield paragraph

    for table in parent.tables:

        for row in table.rows:

            for cell in row.cells:

                yield from iter_paragraphs(
                    cell
                )


# =========================================================
# REPLACE TEXT IN PARAGRAPH
# =========================================================

def replace_text_in_paragraph(
    paragraph,
    replacements
):
    """
    Replace placeholders while preserving
    formatting as much as possible.

    Supports placeholders like:

    {{Name}}
    {{Emp ID}}
    {{Skills}}
    {{Summary}}
    """

    # -----------------------------------------------------
    # Normal replacement inside individual runs
    # -----------------------------------------------------

    for run in paragraph.runs:

        for old_text, new_text in replacements.items():

            if old_text in run.text:

                run.text = run.text.replace(
                    old_text,
                    str(new_text or "")
                )

    # -----------------------------------------------------
    # Some Word documents split placeholders
    # across multiple runs.
    # Example:
    # {{Na + me}}
    # -----------------------------------------------------

    full_text = "".join(
        run.text
        for run in paragraph.runs
    )

    placeholder_found = False

    for old_text in replacements:

        if old_text in full_text:

            placeholder_found = True
            break

    if not placeholder_found:
        return

    new_text = full_text

    for old_text, new_value in replacements.items():

        new_text = new_text.replace(
            old_text,
            str(new_value or "")
        )

    if paragraph.runs:

        paragraph.runs[0].text = (
            new_text
        )

        for run in paragraph.runs[1:]:

            run.text = ""

    else:

        paragraph.add_run(
            new_text
        )


# =========================================================
# REPLACE ALL PLACEHOLDERS
# =========================================================

def replace_all_placeholders(
    document,
    replacements
):
    """
    Replace placeholders in:

    - Document body
    - Tables
    - Headers
    - Footers
    """

    # -----------------------------------------------------
    # Main body + tables
    # -----------------------------------------------------

    for paragraph in iter_paragraphs(
        document
    ):

        replace_text_in_paragraph(
            paragraph,
            replacements
        )

    # -----------------------------------------------------
    # Headers and footers
    # -----------------------------------------------------

    for section in document.sections:

        for paragraph in iter_paragraphs(
            section.header
        ):

            replace_text_in_paragraph(
                paragraph,
                replacements
            )

        for paragraph in iter_paragraphs(
            section.footer
        ):

            replace_text_in_paragraph(
                paragraph,
                replacements
            )


# =========================================================
# INSERT PHOTO
# =========================================================

def insert_photo(
    document,
    photo_path
):
    """
    Find {{Image}} in the Word template
    and replace it with the trainer photo.
    """

    if not photo_path:
        return False

    photo_path = Path(
        photo_path
    )

    if not photo_path.exists():
        return False

    for paragraph in iter_paragraphs(
        document
    ):

        full_text = "".join(
            run.text
            for run in paragraph.runs
        )

        if "{{Image}}" not in full_text:
            continue

        # -------------------------------------------------
        # Remove image placeholder
        # -------------------------------------------------

        for run in paragraph.runs:

            run.text = run.text.replace(
                "{{Image}}",
                ""
            )

        # -------------------------------------------------
        # Insert photo
        # -------------------------------------------------

        picture_run = (
            paragraph.add_run()
        )

        picture_run.add_picture(
            str(photo_path),
            width=Inches(1.45)
        )

        paragraph.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER
        )

        return True

    return False


# =========================================================
# TABLE CELL SHADING
# =========================================================

def set_cell_shading(
    cell,
    fill
):
    """
    Set background color of a table cell.
    """

    tc_pr = (
        cell._tc.get_or_add_tcPr()
    )

    shading = OxmlElement(
        "w:shd"
    )

    shading.set(
        qn("w:fill"),
        fill
    )

    tc_pr.append(
        shading
    )


# =========================================================
# TABLE CELL VERTICAL ALIGNMENT
# =========================================================

def set_cell_vertical_center(
    cell
):
    """
    Vertically center cell contents.
    """

    tc_pr = (
        cell._tc.get_or_add_tcPr()
    )

    valign = OxmlElement(
        "w:vAlign"
    )

    valign.set(
        qn("w:val"),
        "center"
    )

    tc_pr.append(
        valign
    )


# =========================================================
# TABLE BORDERS
# =========================================================

def set_table_borders(
    table
):
    """
    Add borders directly using Word XML.

    This avoids dependency on Word table styles
    such as 'Table Grid'.

    Therefore this works even when the template
    does not contain the Table Grid style.
    """

    table_xml = (
        table._tbl
    )

    table_properties = (
        table_xml.tblPr
    )

    borders = (
        table_properties.first_child_found_in(
            "w:tblBorders"
        )
    )

    if borders is None:

        borders = OxmlElement(
            "w:tblBorders"
        )

        table_properties.append(
            borders
        )

    border_names = [
        "top",
        "left",
        "bottom",
        "right",
        "insideH",
        "insideV"
    ]

    for border_name in border_names:

        tag_name = (
            "w:" + border_name
        )

        border = borders.find(
            qn(tag_name)
        )

        if border is None:

            border = OxmlElement(
                tag_name
            )

            borders.append(
                border
            )

        border.set(
            qn("w:val"),
            "single"
        )

        border.set(
            qn("w:sz"),
            "6"
        )

        border.set(
            qn("w:space"),
            "0"
        )

        border.set(
            qn("w:color"),
            "808080"
        )


# =========================================================
# SET TABLE WIDTHS
# =========================================================

def set_project_table_widths(
    table
):
    """
    Set approximate widths for project table columns.
    """

    widths = [
        Inches(0.55),
        Inches(3.10),
        Inches(1.35),
        Inches(2.25)
    ]

    for row in table.rows:

        for index, width in enumerate(
            widths
        ):

            if index < len(
                row.cells
            ):

                row.cells[
                    index
                ].width = width


# =========================================================
# FIND TRAINING PROJECTS HEADING
# =========================================================

def find_training_projects_heading(
    document
):
    """
    Find paragraph containing:

    Training Projects:
    """

    for paragraph in document.paragraphs:

        text = (
            paragraph.text
            .strip()
            .lower()
        )

        if text.startswith(
            "training projects"
        ):

            return paragraph

    # -----------------------------------------------------
    # Fallback:
    # search inside tables
    # -----------------------------------------------------

    for paragraph in iter_paragraphs(
        document
    ):

        text = (
            paragraph.text
            .strip()
            .lower()
        )

        if text.startswith(
            "training projects"
        ):

            return paragraph

    return None


# =========================================================
# REMOVE TRAINING PROJECT PLACEHOLDER
# =========================================================

def remove_empty_project_placeholder(
    document
):
    """
    Remove {{Training Projects}}
    if present in template.

    Actual projects are inserted
    using a Word table.
    """

    replacements = {
        "{{Training Projects}}": ""
    }

    replace_all_placeholders(
        document,
        replacements
    )


# =========================================================
# CLEAN PROJECT VALUES
# =========================================================

def clean_project_value(
    value
):
    """
    Convert None / NaN-like values to blank.
    """

    if value is None:
        return ""

    value = str(
        value
    ).strip()

    if value.lower() in [
        "none",
        "nan"
    ]:

        return ""

    return value


# =========================================================
# ADD TRAINING PROJECTS TABLE
# =========================================================

def add_training_projects(
    document,
    projects
):
    """
    Insert Training Projects table below the
    Training Projects heading.

    Columns:

    S.No
    College / Client
    Location
    Domain / Subject Area
    """

    heading = (
        find_training_projects_heading(
            document
        )
    )

    if heading is None:
        return

    # -----------------------------------------------------
    # Remove completely empty project entries
    # -----------------------------------------------------

    valid_projects = []

    if projects:

        for project in projects:

            college = (
                clean_project_value(
                    project.get(
                        "College / Client",
                        ""
                    )
                )
            )

            location = (
                clean_project_value(
                    project.get(
                        "Location",
                        ""
                    )
                )
            )

            subject = (
                clean_project_value(
                    project.get(
                        "Domain / Subject Area",
                        ""
                    )
                )
            )

            if (
                college
                or location
                or subject
            ):

                valid_projects.append(
                    {
                        "College / Client":
                            college,

                        "Location":
                            location,

                        "Domain / Subject Area":
                            subject
                    }
                )

    # -----------------------------------------------------
    # No projects
    # -----------------------------------------------------

    if not valid_projects:

        no_project_para = (
            document.add_paragraph()
        )

        no_project_run = (
            no_project_para.add_run(
                "Project allocation not yet done."
            )
        )

        no_project_run.font.size = (
            Pt(10)
        )

        heading._p.addnext(
            no_project_para._p
        )

        return

    # -----------------------------------------------------
    # Completed Projects heading
    # -----------------------------------------------------

    completed_para = (
        document.add_paragraph()
    )

    completed_run = (
        completed_para.add_run(
            "Completed Projects:"
        )
    )

    completed_run.bold = True

    completed_run.font.size = (
        Pt(11)
    )

    # -----------------------------------------------------
    # Create table
    # -----------------------------------------------------

    table = document.add_table(
        rows=1,
        cols=4
    )

    table.alignment = (
        WD_TABLE_ALIGNMENT.CENTER
    )

    # -----------------------------------------------------
    # IMPORTANT FIX:
    #
    # Do NOT use:
    #
    # table.style = "Table Grid"
    #
    # because your template does not
    # contain that style.
    # -----------------------------------------------------

    set_table_borders(
        table
    )

    # -----------------------------------------------------
    # Table Header
    # -----------------------------------------------------

    headers = [
        "S.No",
        "College / Client",
        "Location",
        "Domain / Subject Area"
    ]

    header_cells = (
        table.rows[0].cells
    )

    for index, header in enumerate(
        headers
    ):

        cell = (
            header_cells[index]
        )

        cell.text = (
            header
        )

        set_cell_shading(
            cell,
            "1F4E78"
        )

        set_cell_vertical_center(
            cell
        )

        for paragraph in (
            cell.paragraphs
        ):

            paragraph.alignment = (
                WD_ALIGN_PARAGRAPH.CENTER
            )

            for run in (
                paragraph.runs
            ):

                run.bold = True

                run.font.size = (
                    Pt(9)
                )

                run.font.color.rgb = (
                    RGBColor(
                        255,
                        255,
                        255
                    )
                )

    # -----------------------------------------------------
    # Add project rows
    # -----------------------------------------------------

    for serial_no, project in enumerate(
        valid_projects,
        start=1
    ):

        cells = (
            table.add_row().cells
        )

        cells[0].text = str(
            serial_no
        )

        cells[1].text = (
            project[
                "College / Client"
            ]
        )

        cells[2].text = (
            project[
                "Location"
            ]
        )

        cells[3].text = (
            project[
                "Domain / Subject Area"
            ]
        )

        for cell_index, cell in enumerate(
            cells
        ):

            set_cell_vertical_center(
                cell
            )

            for paragraph in (
                cell.paragraphs
            ):

                if cell_index == 0:

                    paragraph.alignment = (
                        WD_ALIGN_PARAGRAPH.CENTER
                    )

                else:

                    paragraph.alignment = (
                        WD_ALIGN_PARAGRAPH.LEFT
                    )

                for run in (
                    paragraph.runs
                ):

                    run.font.size = (
                        Pt(8.5)
                    )

    # -----------------------------------------------------
    # Apply borders again after adding rows
    # -----------------------------------------------------

    set_table_borders(
        table
    )

    set_project_table_widths(
        table
    )

    # -----------------------------------------------------
    # Put Completed Projects immediately after heading
    # -----------------------------------------------------

    heading._p.addnext(
        completed_para._p
    )

    # -----------------------------------------------------
    # Put table after Completed Projects
    # -----------------------------------------------------

    completed_para._p.addnext(
        table._tbl
    )


# =========================================================
# REMOVE UNUSED PLACEHOLDERS
# =========================================================

def remove_remaining_placeholders(
    document
):
    """
    Remove remaining placeholders such as:

    {{Something}}

    if they were not populated.
    """

    placeholder_pattern = (
        re.compile(
            r"\{\{[^{}]+\}\}"
        )
    )

    for paragraph in iter_paragraphs(
        document
    ):

        full_text = "".join(
            run.text
            for run in paragraph.runs
        )

        if not full_text:
            continue

        cleaned_text = (
            placeholder_pattern.sub(
                "",
                full_text
            )
        )

        if cleaned_text == full_text:
            continue

        if paragraph.runs:

            paragraph.runs[0].text = (
                cleaned_text
            )

            for run in (
                paragraph.runs[1:]
            ):

                run.text = ""

        else:

            paragraph.add_run(
                cleaned_text
            )


# =========================================================
# REMOVE UNUSED PLACEHOLDERS FROM HEADERS / FOOTERS
# =========================================================

def remove_header_footer_placeholders(
    document
):
    """
    Remove unused placeholders from
    headers and footers.
    """

    placeholder_pattern = (
        re.compile(
            r"\{\{[^{}]+\}\}"
        )
    )

    for section in document.sections:

        for container in [
            section.header,
            section.footer
        ]:

            for paragraph in iter_paragraphs(
                container
            ):

                full_text = "".join(
                    run.text
                    for run in paragraph.runs
                )

                cleaned_text = (
                    placeholder_pattern.sub(
                        "",
                        full_text
                    )
                )

                if (
                    cleaned_text
                    == full_text
                ):

                    continue

                if paragraph.runs:

                    paragraph.runs[
                        0
                    ].text = cleaned_text

                    for run in (
                        paragraph.runs[1:]
                    ):

                        run.text = ""

                else:

                    paragraph.add_run(
                        cleaned_text
                    )


# =========================================================
# MAIN PROFILE GENERATOR
# =========================================================

def generate_profile(
    template_path,
    output_path,
    data,
    profile_type,
    photo_path=None,
    projects=None
):
    """
    Generate Technical Trainer or
    Aptitude Trainer Word profile.

    The original Word template is opened and
    populated, so the CodeTantra logo, formatting,
    page layout and existing design are retained.
    """

    template_path = Path(
        template_path
    )

    output_path = Path(
        output_path
    )

    # -----------------------------------------------------
    # Validate template
    # -----------------------------------------------------

    if not template_path.exists():

        raise FileNotFoundError(
            f"Template not found: "
            f"{template_path}"
        )

    # -----------------------------------------------------
    # Validate profile type
    # -----------------------------------------------------

    valid_profile_types = [
        "Technical Trainer",
        "Aptitude Trainer"
    ]

    if profile_type not in (
        valid_profile_types
    ):

        raise ValueError(
            "Invalid profile type. "
            "Expected 'Technical Trainer' "
            "or 'Aptitude Trainer'."
        )

    # -----------------------------------------------------
    # Create destination folder
    # -----------------------------------------------------

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------------------
    # Open template
    # -----------------------------------------------------

    document = Document(
        str(template_path)
    )

    # =====================================================
    # INSERT PHOTO FIRST
    # =====================================================

    insert_photo(
        document,
        photo_path
    )

    # =====================================================
    # PLACEHOLDER MAPPING
    # =====================================================

    replacements = {

        # -------------------------------------------------
        # Common Fields
        # -------------------------------------------------

        "{{Name}}":
            data.get(
                "Name",
                ""
            ),

        "{{Emp ID}}":
            data.get(
                "Emp ID",
                ""
            ),

        "{{Designation}}":
            data.get(
                "Designation",
                profile_type
            ),

        "{{Qualification}}":
            data.get(
                "Qualification",
                ""
            ),

        "{{Date of Joining}}":
            data.get(
                "Date of Joining",
                ""
            ),

        "{{Experience}}":
            data.get(
                "Experience",
                ""
            ),

        "{{Company Mail}}":
            data.get(
                "Company Mail",
                ""
            ),

        "{{Phone Number}}":
            data.get(
                "Phone Number",
                ""
            ),

        "{{Rating}}":
            data.get(
                "Rating",
                ""
            ),

        "{{Skills}}":
            data.get(
                "Skills",
                ""
            ),

        "{{Summary}}":
            data.get(
                "Summary",
                ""
            ),

        "{{Certifications}}":
            data.get(
                "Certifications",
                ""
            ),

        "{{Professional Highlights}}":
            data.get(
                "Professional Highlights",
                ""
            ),

        "{{Training Expertise}}":
            data.get(
                "Training Expertise",
                ""
            ),

        "{{Core Competencies}}":
            data.get(
                "Core Competencies",
                ""
            ),

        # -------------------------------------------------
        # Aptitude Trainer Fields
        # -------------------------------------------------

        "{{Subjects Handled}}":
            data.get(
                "Subjects Handled",
                ""
            ),

        "{{Exam Placement Expertise}}":
            data.get(
                "Exam Placement Expertise",
                ""
            ),

        "{{Exam / Placement Expertise}}":
            data.get(
                "Exam Placement Expertise",
                ""
            ),

        "{{Languages}}":
            data.get(
                "Languages",
                ""
            ),

        # -------------------------------------------------
        # Technical Trainer Fields
        # -------------------------------------------------

        "{{LeetCode Profile Link}}":
            data.get(
                "LeetCode Profile Link",
                ""
            ),

        "{{No of Problems Done}}":
            data.get(
                "No of Problems Done",
                ""
            ),

        "{{Other Profiles}}":
            data.get(
                "Other Profiles",
                ""
            )
    }

    # =====================================================
    # PROFILE TITLE
    # =====================================================

    if profile_type == (
        "Aptitude Trainer"
    ):

        replacements[
            "Profile - Technical Trainer"
        ] = (
            "Profile - Aptitude Trainer"
        )

    else:

        replacements[
            "Profile - Aptitude Trainer"
        ] = (
            "Profile - Technical Trainer"
        )

    # =====================================================
    # REPLACE PLACEHOLDERS
    # =====================================================

    replace_all_placeholders(
        document,
        replacements
    )

    # =====================================================
    # TRAINING PROJECTS
    # =====================================================

    remove_empty_project_placeholder(
        document
    )

    if projects is None:

        projects = data.get(
            "Training Projects",
            []
        )

    add_training_projects(
        document,
        projects
    )

    # =====================================================
    # REMOVE ANY UNUSED PLACEHOLDERS
    # =====================================================

    remove_remaining_placeholders(
        document
    )

    remove_header_footer_placeholders(
        document
    )

    # =====================================================
    # SAVE FINAL WORD FILE
    # =====================================================

    document.save(
        str(output_path)
    )

    return str(
        output_path
    )