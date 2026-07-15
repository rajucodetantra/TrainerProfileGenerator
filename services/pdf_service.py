import os
import platform


IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    import pythoncom
    import win32com.client


class PDFService:

    def __init__(self):
        pass

    def convert(self, docx_file, pdf_file):

        if not IS_WINDOWS:
            raise Exception(
                "PDF generation using Microsoft Word is only supported on Windows."
            )

        word = None

        try:

            pythoncom.CoInitialize()

            word = win32com.client.Dispatch(
                "Word.Application"
            )

            word.Visible = False

            doc = word.Documents.Open(
                os.path.abspath(docx_file)
            )

            doc.SaveAs(
                os.path.abspath(pdf_file),
                FileFormat=17
            )

            doc.Close()

            return True

        finally:

            if word:
                word.Quit()

            pythoncom.CoUninitialize()