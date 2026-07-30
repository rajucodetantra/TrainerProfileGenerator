import os
import platform
import tempfile
import shutil

IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    import pythoncom
    import win32com.client


class WordPDFService:
    """
    Service for converting Word (.docx) files to PDF.

    Supports:
    ----------
    • Single file conversion
    • Multiple file conversion
    • Preserves original filename
    • Creates output directory automatically
    """

    def __init__(self):
        self.is_windows = IS_WINDOWS

    def _ensure_output_folder(self, output_folder):
        """Create output folder if it doesn't exist."""
        os.makedirs(output_folder, exist_ok=True)

    def convert_file(self, input_file, output_folder):
        """
        Convert a single Word document to PDF.

        Parameters
        ----------
        input_file : str
            Path to input .docx file

        output_folder : str
            Folder where pdf should be created

        Returns
        -------
        dict
        {
            success : bool,
            input : str,
            output : str,
            error : str
        }
        """

        if not self.is_windows:
            return {
                "success": False,
                "input": input_file,
                "output": "",
                "error": "Word to PDF conversion is supported only on Windows (Microsoft Word required)."
            }

        if not os.path.exists(input_file):
            return {
                "success": False,
                "input": input_file,
                "output": "",
                "error": "Input file not found."
            }

        self._ensure_output_folder(output_folder)

        filename = os.path.splitext(os.path.basename(input_file))[0]
        output_pdf = os.path.join(output_folder, filename + ".pdf")

        word = None

        try:
            pythoncom.CoInitialize()

            word = win32com.client.DispatchEx("Word.Application")
            word.Visible = False
            word.DisplayAlerts = 0

            document = word.Documents.Open(os.path.abspath(input_file))

            # 17 = wdFormatPDF
            document.SaveAs(os.path.abspath(output_pdf), FileFormat=17)

            document.Close(False)

            return {
                "success": True,
                "input": input_file,
                "output": output_pdf,
                "error": ""
            }

        except Exception as e:

            return {
                "success": False,
                "input": input_file,
                "output": "",
                "error": str(e)
            }

        finally:

            try:
                if word:
                    word.Quit()
            except:
                pass

            try:
                pythoncom.CoUninitialize()
            except:
                pass

    def convert_files(self, uploaded_files, output_folder):
        """
        Convert multiple uploaded Streamlit files.

        Parameters
        ----------
        uploaded_files : list
            List of uploaded files from st.file_uploader()

        output_folder : str

        Returns
        -------
        list
            List of conversion results
        """

        results = []

        self._ensure_output_folder(output_folder)

        for uploaded_file in uploaded_files:

            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".docx"
            )

            try:

                temp_file.write(uploaded_file.read())
                temp_file.close()

                result = self.convert_file(
                    temp_file.name,
                    output_folder
                )

                # Preserve original filename

                if result["success"]:

                    new_name = os.path.splitext(uploaded_file.name)[0] + ".pdf"

                    new_path = os.path.join(
                        output_folder,
                        new_name
                    )

                    if result["output"] != new_path:

                        if os.path.exists(new_path):
                            os.remove(new_path)

                        shutil.move(result["output"], new_path)

                        result["output"] = new_path

                results.append(result)

            finally:

                if os.path.exists(temp_file.name):
                    os.remove(temp_file.name)

        return results

    def convert_directory(self, input_folder, output_folder):
        """
        Convert all Word files inside a folder.

        Parameters
        ----------
        input_folder : str
        output_folder : str

        Returns
        -------
        list
        """

        results = []

        if not os.path.exists(input_folder):
            return results

        for file in os.listdir(input_folder):

            if file.lower().endswith(".docx"):

                file_path = os.path.join(input_folder, file)

                results.append(
                    self.convert_file(
                        file_path,
                        output_folder
                    )
                )

        return results