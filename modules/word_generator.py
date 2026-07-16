import os
import io
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from modules.project_extractor import ProjectExtractor

class WordGenerator:
    def __init__(self, template_path, trainer_data):
        self.template_path = template_path
        self.trainer = trainer_data
        # Load from dynamic configured or relative path safely
        project_file = "data/Projects.xlsx" if os.path.exists("data/Projects.xlsx") else "Projects.xlsx"
        self.project_extractor = ProjectExtractor(project_file)

    def set_cell_background(self, cell, fill_color):
        """Helper to style header row tables to match enterprise layout aesthetics"""
        tc_pr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), fill_color)
        tc_pr.append(shd)

    def set_table_borders(self, table):
        """Programmatically injects standard light-gray borders to prevent KeyError style missing issues"""
        tbl_pr = table._tbl.tblPr
        tbl_borders = OxmlElement('w:tblBorders')
        
        for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            border = OxmlElement(f'w:{border_name}')
            border.set(qn('w:val'), 'single')
            border.set(qn('w:sz'), '4')  # 0.5 pt width
            border.set(qn('w:space'), '0')
            border.set(qn('w:color'), 'D3D3D3')  # Light Gray
            tbl_borders.append(border)
            
        tbl_pr.append(tbl_borders)

    def replace_placeholders(self, doc):
        """Replaces standard string hooks in the template copy across paragraphs and tables."""
        for paragraph in doc.paragraphs:
            self._replace_in_paragraph(paragraph)
                    
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        self._replace_in_paragraph(paragraph)

        self.replace_image_placeholders(doc)

    def _replace_in_paragraph(self, paragraph):
        """Replaces placeholders while trying to preserve inline runs formatting"""
        for key, val in self.trainer.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in paragraph.text:
                if key == "Image":
                    continue
                paragraph.text = paragraph.text.replace(placeholder, str(val))

    def replace_image_placeholders(self, doc):
        """Finds raw image placeholders, replaces them with real inline images."""
        image_path = self.trainer.get("Image", "")
        if not image_path or not os.path.exists(image_path):
            self._clear_image_placeholder_text(doc)
            return

        for paragraph in doc.paragraphs:
            self._insert_image_in_runs(paragraph, image_path)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        self._insert_image_in_runs(paragraph, image_path)

    def _insert_image_in_runs(self, paragraph, image_path):
        """Scans runs to locate split {{Image}} segments, replaces with physical image."""
        p_text = paragraph.text
        if "{{Image}}" in p_text:
            paragraph.text = p_text.replace("{{Image}}", "")
            run = paragraph.add_run()
            try:
                run.add_picture(image_path, width=Inches(1.2))
            except Exception:
                pass

    def _clear_image_placeholder_text(self, doc):
        """Helper to cleanly strip out {{Image}} text if no image path exists."""
        for paragraph in doc.paragraphs:
            if "{{Image}}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{{Image}}", "")
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        if "{{Image}}" in paragraph.text:
                            paragraph.text = paragraph.text.replace("{{Image}}", "")

    def append_projects_table(self, doc, projects_list, section_title):
        """Constructs a beautifully formatted native Word table for the projects"""
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(section_title)
        run.bold = True
        run.font.size = Pt(11)
        run.font.name = 'Calibri'

        table = doc.add_table(rows=1, cols=5)
        self.set_table_borders(table)
        
        hdr_cells = table.rows[0].cells
        headers = ["S.No", "College / Client", "Location", "Domain / Subject Area", "Duration"]
        widths = [Inches(0.6), Inches(2.2), Inches(1.0), Inches(2.2), Inches(1.5)]
        
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            # Access the run to apply explicit coloring and font configurations
            header_run = hdr_cells[i].paragraphs[0].runs[0]
            header_run.font.bold = True
            header_run.font.size = Pt(9.5)
            header_run.font.name = 'Calibri'
            # FIX: Force text color to white (255, 255, 255) so it stands out against dark backgrounds
            header_run.font.color.rgb = RGBColor(255, 255, 255)
            
            self.set_cell_background(hdr_cells[i], "1F4E78") # Dark corporate Slate Blue
            hdr_cells[i].width = widths[i]

        for item in projects_list:
            row_cells = table.add_row().cells
            duration_str = f"{item.get('From', '')} to {item.get('To', '')}"
            
            row_cells[0].text = str(item.get("S.No", ""))
            row_cells[1].text = str(item.get("College", ""))
            row_cells[2].text = str(item.get("Place", ""))
            row_cells[3].text = str(item.get("Subject", ""))
            row_cells[4].text = duration_str
            
            for i in range(5):
                row_cells[i].width = widths[i]
                if len(row_cells[i].paragraphs[0].runs) > 0:
                    row_cells[i].paragraphs[0].runs[0].font.size = Pt(9)
                    row_cells[i].paragraphs[0].runs[0].font.name = 'Calibri'

    def _build_document(self):
        """Internal helper to load template, substitute data, and append projects."""
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template profile file missing at: {self.template_path}")
            
        doc = Document(self.template_path)
        
        # 1. Substitute basic placeholders
        self.replace_placeholders(doc)
        
        # 2. Process Projects with defensive ID structural fallback
        emp_id = self.trainer.get("Emp ID") or self.trainer.get("Employee ID") or ""
        emp_id = str(emp_id).strip()
        
        if not emp_id:
            print(f"[WARNING]: No valid identifier found in trainer dataset keys!", file=sys.stderr)
            
        project_data = self.project_extractor.get_trainer_projects(emp_id)
        
        ongoing_list = project_data.get("ongoing", []) if isinstance(project_data, dict) else []
        completed_list = project_data.get("completed", []) if isinstance(project_data, dict) else []
        
        has_ongoing = len(ongoing_list) > 0
        has_completed = len(completed_list) > 0
        
        if not has_ongoing and not has_completed:
            p_fallback = doc.add_paragraph()
            p_fallback.paragraph_format.space_before = Pt(14)
            p_fallback.paragraph_format.space_after = Pt(6)
            run_fallback = p_fallback.add_run("Project allocation not yet done.")
            run_fallback.italic = True
            run_fallback.font.size = Pt(11)
            run_fallback.font.name = 'Calibri'
        else:
            if has_ongoing:
                self.append_projects_table(doc, ongoing_list, "Ongoing Projects:")
                
            if has_completed:
                self.append_projects_table(doc, completed_list, "Completed Projects:")
        
        return doc

    def generate(self, output_path):
        """Generates and saves the document to a physical file path."""
        doc = self._build_document()
        doc.save(output_path)

    def generate_bytes(self):
        """Generates the document entirely in memory and returns a bytes stream."""
        doc = self._build_document()
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()