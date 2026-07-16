import os
import platform
import subprocess

IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    import pythoncom
    import win32com.client

class PDFService:
    def __init__(self):
        pass

    def _convert_via_libreoffice(self, abs_docx, out_dir, abs_pdf):
        """Cross-platform fallback helper using headless LibreOffice."""
        # Common locations for LibreOffice binaries
        commands = ["soffice", "libreoffice"]
        if IS_WINDOWS:
            commands.insert(0, r"C:\Program Files\LibreOffice\program\soffice.exe")
            
        for cmd in commands:
            try:
                result = subprocess.run(
                    [cmd, "--headless", "--convert-to", "pdf", "--outdir", out_dir, abs_docx],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True
                )
                if os.path.exists(abs_pdf):
                    return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        return False

    def convert(self, docx_file, pdf_file):
        abs_docx = os.path.abspath(docx_file)
        abs_pdf = os.path.abspath(pdf_file)
        out_dir = os.path.dirname(abs_pdf)

        # Method A: Try native Windows Win32COM if available
        if IS_WINDOWS:
            word_app = None
            doc = None
            try:
                pythoncom.CoInitialize()
                word_app = win32com.client.Dispatch("Word.Application")
                word_app.Visible = False
                
                doc = word_app.Documents.Open(abs_docx)
                doc.SaveAs(abs_pdf, FileFormat=17) # 17 == wdFormatPDF
                return True
            except Exception:
                # If MS Word COM fails on Windows, gracefully attempt LibreOffice fallback
                if self._convert_via_libreoffice(abs_docx, out_dir, abs_pdf):
                    return True
            finally:
                if doc:
                    doc.Close(False)
                if word_app:
                    word_app.Quit()
                pythoncom.CoUninitialize()
        
        # Method B: Linux/Mac or Fallback Execution Environment
        if self._convert_via_libreoffice(abs_docx, out_dir, abs_pdf):
            return True
            
        raise RuntimeError(
            "PDF Conversion Engine Failed: Ensure Microsoft Word or LibreOffice is installed on the hosting system."
        )