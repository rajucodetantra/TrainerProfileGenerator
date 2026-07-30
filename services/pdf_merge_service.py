import os
import tempfile
from pypdf import PdfReader, PdfWriter


class PDFMergeService:
    """
    Service for merging multiple PDF files.
    """

    DEFAULT_OUTPUT_NAME = "CTCombined.pdf"

    def __init__(self):
        pass

    def _ensure_output_folder(self, output_folder):
        os.makedirs(output_folder, exist_ok=True)

    def merge_files(self, uploaded_files, output_folder):

        self._ensure_output_folder(output_folder)

        output_pdf = os.path.join(
            output_folder,
            self.DEFAULT_OUTPUT_NAME
        )

        writer = PdfWriter()
        temp_files = []

        try:

            for uploaded_file in uploaded_files:

                # IMPORTANT
                uploaded_file.seek(0)

                data = uploaded_file.read()

                if not data:
                    continue

                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                )

                temp_file.write(data)
                temp_file.close()

                temp_files.append(temp_file.name)

                reader = PdfReader(temp_file.name)

                for page in reader.pages:
                    writer.add_page(page)

            if len(writer.pages) == 0:
                return {
                    "success": False,
                    "output": "",
                    "pages": 0,
                    "error": "No valid PDF pages found."
                }

            with open(output_pdf, "wb") as output:
                writer.write(output)

            return {
                "success": True,
                "output": output_pdf,
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

            for file in temp_files:
                try:
                    if os.path.exists(file):
                        os.remove(file)
                except:
                    pass

    def merge_paths(self, pdf_paths, output_folder):

        self._ensure_output_folder(output_folder)

        output_pdf = os.path.join(
            output_folder,
            self.DEFAULT_OUTPUT_NAME
        )

        writer = PdfWriter()

        try:

            for pdf in pdf_paths:

                if not os.path.exists(pdf):
                    continue

                reader = PdfReader(pdf)

                for page in reader.pages:
                    writer.add_page(page)

            if len(writer.pages) == 0:
                return {
                    "success": False,
                    "output": "",
                    "pages": 0,
                    "error": "No valid PDF pages found."
                }

            with open(output_pdf, "wb") as output:
                writer.write(output)

            return {
                "success": True,
                "output": output_pdf,
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

    def get_total_pages(self, uploaded_files):

        total_pages = 0
        temp_files = []

        try:

            for uploaded_file in uploaded_files:

                # IMPORTANT
                uploaded_file.seek(0)

                data = uploaded_file.read()

                if not data:
                    continue

                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                )

                temp_file.write(data)
                temp_file.close()

                temp_files.append(temp_file.name)

                reader = PdfReader(temp_file.name)

                total_pages += len(reader.pages)

            return total_pages

        except Exception:
            return 0

        finally:

            for file in temp_files:
                try:
                    if os.path.exists(file):
                        os.remove(file)
                except:
                    pass