import os
import tempfile

from pypdf import PdfReader, PdfWriter


class PDFSplitService:
    """
    Service for splitting PDF files.

    Features
    --------
    • Split by page range
    • Get total pages
    • Output filename:
      Pages_<start>_<end>.pdf
    """

    def __init__(self):
        pass

    def _ensure_output_folder(self, output_folder):
        os.makedirs(output_folder, exist_ok=True)

    def get_total_pages(self, uploaded_file):
        """
        Returns the number of pages in the uploaded PDF.
        """

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )

        try:

            temp_file.write(uploaded_file.read())
            temp_file.close()

            reader = PdfReader(temp_file.name)

            return len(reader.pages)

        finally:

            uploaded_file.seek(0)

            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)

    def split_pdf(
        self,
        uploaded_file,
        start_page,
        end_page,
        output_folder
    ):
        """
        Split PDF between start_page and end_page.

        Parameters
        ----------
        uploaded_file : UploadedFile

        start_page : int
            1-based page number

        end_page : int
            1-based page number

        output_folder : str

        Returns
        -------
        dict
        """

        self._ensure_output_folder(output_folder)

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )

        try:

            temp_file.write(uploaded_file.read())
            temp_file.close()

            reader = PdfReader(temp_file.name)

            total_pages = len(reader.pages)

            if start_page < 1:
                return {
                    "success": False,
                    "output": "",
                    "pages": total_pages,
                    "error": "Start page must be greater than 0."
                }

            if end_page > total_pages:
                return {
                    "success": False,
                    "output": "",
                    "pages": total_pages,
                    "error": f"PDF contains only {total_pages} pages."
                }

            if start_page > end_page:
                return {
                    "success": False,
                    "output": "",
                    "pages": total_pages,
                    "error": "Start page cannot be greater than End page."
                }

            writer = PdfWriter()

            for page in range(start_page - 1, end_page):
                writer.add_page(reader.pages[page])

            output_name = f"Pages_{start_page}_{end_page}.pdf"

            output_path = os.path.join(
                output_folder,
                output_name
            )

            with open(output_path, "wb") as output:
                writer.write(output)

            return {
                "success": True,
                "output": output_path,
                "pages": len(writer.pages),
                "error": ""
            }

        except Exception as e:

            return {
                "success": False,
                "output": "",
                "pages": 0,
                "error": str(e)
            }

        finally:

            uploaded_file.seek(0)

            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)

    def split_from_path(
        self,
        pdf_path,
        start_page,
        end_page,
        output_folder
    ):
        """
        Split a PDF using a file path.
        """

        self._ensure_output_folder(output_folder)

        if not os.path.exists(pdf_path):

            return {
                "success": False,
                "output": "",
                "pages": 0,
                "error": "PDF file not found."
            }

        try:

            reader = PdfReader(pdf_path)

            total_pages = len(reader.pages)

            if start_page < 1:
                return {
                    "success": False,
                    "output": "",
                    "pages": total_pages,
                    "error": "Invalid start page."
                }

            if end_page > total_pages:
                return {
                    "success": False,
                    "output": "",
                    "pages": total_pages,
                    "error": "Invalid end page."
                }

            writer = PdfWriter()

            for page in range(start_page - 1, end_page):
                writer.add_page(reader.pages[page])

            output_name = f"Pages_{start_page}_{end_page}.pdf"

            output_path = os.path.join(
                output_folder,
                output_name
            )

            with open(output_path, "wb") as output:
                writer.write(output)

            return {
                "success": True,
                "output": output_path,
                "pages": len(writer.pages),
                "error": ""
            }

        except Exception as e:

            return {
                "success": False,
                "output": "",
                "pages": 0,
                "error": str(e)
            }