import os
import tempfile
from pypdf import PdfReader, PdfWriter


class PDFMergeService:
    """
    Service for merging multiple PDF files into a single PDF.

    Features
    --------
    • Merge uploaded PDF files
    • Merge PDFs from file paths
    • Output file name:
        CTCombined.pdf
    """

    DEFAULT_OUTPUT_NAME = "CTCombined.pdf"

    def __init__(self):
        pass

    def _ensure_output_folder(self, output_folder):
        os.makedirs(output_folder, exist_ok=True)

    def merge_files(self, uploaded_files, output_folder):
        """
        Merge uploaded Streamlit PDF files.

        Parameters
        ----------
        uploaded_files : list
            List returned by st.file_uploader()

        output_folder : str

        Returns
        -------
        dict
        """

        self._ensure_output_folder(output_folder)

        output_pdf = os.path.join(
            output_folder,
            self.DEFAULT_OUTPUT_NAME
        )

        writer = PdfWriter()
        temp_files = []

        try:

            for uploaded_file in uploaded_files:

                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                )

                temp_file.write(uploaded_file.read())
                temp_file.close()

                temp_files.append(temp_file.name)

                reader = PdfReader(temp_file.name)

                for page in reader.pages:
                    writer.add_page(page)

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
                if os.path.exists(file):
                    os.remove(file)

    def merge_paths(self, pdf_paths, output_folder):
        """
        Merge PDF files using their file paths.

        Parameters
        ----------
        pdf_paths : list
        output_folder : str

        Returns
        -------
        dict
        """

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
        """
        Returns total pages in all uploaded PDFs.
        """

        total_pages = 0
        temp_files = []

        try:

            for uploaded_file in uploaded_files:

                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                )

                temp_file.write(uploaded_file.read())
                temp_file.close()

                temp_files.append(temp_file.name)

                reader = PdfReader(temp_file.name)

                total_pages += len(reader.pages)

            return total_pages

        except:

            return 0

        finally:

            for file in temp_files:

                if os.path.exists(file):
                    os.remove(file)