import os
import shutil

from pdf2docx import Converter

from services.logger import Logger
from services.file_utils import FileUtils


logger = Logger()


class PDFWordService:
    """
    Service for converting PDF files to Word (.docx).
    """

    def __init__(self):
        pass

    def _ensure_output_folder(self, output_folder):
        """Create output folder if it doesn't exist."""
        os.makedirs(output_folder, exist_ok=True)

    def convert_file(self, input_file, output_folder):
        """
        Convert a single PDF file to Word.
        """

        self._ensure_output_folder(output_folder)

        if not os.path.exists(input_file):

            return {
                "success": False,
                "input": input_file,
                "output": "",
                "error": "Input file not found."
            }

        filename = os.path.splitext(
            os.path.basename(input_file)
        )[0]

        output_docx = os.path.join(
            output_folder,
            filename + ".docx"
        )

        converter = None

        try:

            logger.info(f"Converting {input_file}")

            converter = Converter(input_file)

            converter.convert(output_docx)

            if not os.path.exists(output_docx):

                return {
                    "success": False,
                    "input": input_file,
                    "output": "",
                    "error": "Word file was not created."
                }

            logger.info(f"Created {output_docx}")

            return {
                "success": True,
                "input": input_file,
                "output": output_docx,
                "error": ""
            }

        except Exception as e:

            logger.error(str(e))

            return {
                "success": False,
                "input": input_file,
                "output": "",
                "error": f"PDF to Word conversion failed: {e}"
            }

        finally:

            if converter:
                converter.close()

    def convert_files(self, uploaded_files, output_folder):
        """
        Convert multiple uploaded PDF files.
        """

        self._ensure_output_folder(output_folder)

        results = []

        for uploaded_file in uploaded_files:

            temp_pdf = FileUtils.create_temp_file(".pdf")

            try:

                content = uploaded_file.read()

                if not content:

                    results.append({
                        "success": False,
                        "input": uploaded_file.name,
                        "output": "",
                        "error": "Uploaded file is empty."
                    })

                    continue

                temp_pdf.write(content)

                uploaded_file.seek(0)

                temp_pdf.close()

                result = self.convert_file(
                    temp_pdf.name,
                    output_folder
                )

                if result["success"]:

                    original_name = os.path.splitext(
                        uploaded_file.name
                    )[0]

                    new_output = os.path.join(
                        output_folder,
                        original_name + ".docx"
                    )

                    if result["output"] != new_output:

                        if os.path.exists(new_output):
                            os.remove(new_output)

                        shutil.move(
                            result["output"],
                            new_output
                        )

                        result["output"] = new_output

                results.append(result)

            finally:

                if os.path.exists(temp_pdf.name):
                    os.remove(temp_pdf.name)

        return results

    def convert_directory(self, input_folder, output_folder):
        """
        Convert every PDF inside a directory.
        """

        self._ensure_output_folder(output_folder)

        results = []

        if not os.path.exists(input_folder):
            return results

        pdf_files = [

            file

            for file in os.listdir(input_folder)

            if file.lower().endswith(".pdf")

        ]

        for file in pdf_files:

            result = self.convert_file(
                os.path.join(input_folder, file),
                output_folder
            )

            results.append(result)

        return results