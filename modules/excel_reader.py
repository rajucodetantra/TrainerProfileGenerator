# modules/excel_reader.py

import os
import pandas as pd


class ExcelReader:
    """
    Reads trainer details from Excel file.
    """

    def __init__(self, file_path, sheet_name=None):
        self.file_path = file_path
        self.sheet_name = sheet_name


    def validate_file(self):
        """
        Check whether Excel file exists.
        """

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(
                f"Excel file not found: {self.file_path}"
            )


    def read(self):
        """
        Read Excel file and return DataFrame.
        """

        self.validate_file()

        try:

            df = pd.read_excel(
                self.file_path,
                sheet_name=self.sheet_name
            )


            # If multiple sheets returned
            # convert first sheet into dataframe
            if isinstance(df, dict):
                df = list(df.values())[0]


            # Remove completely empty rows
            df.dropna(
                how="all",
                inplace=True
            )


            # Clean column names
            df.columns = (
                df.columns
                .astype(str)
                .str.strip()
            )


            return df


        except Exception as e:

            raise Exception(
                f"Error reading Excel file: {e}"
            )



    def get_trainers(self):
        """
        Alias method for reading trainers data.
        """

        return self.read()


    def read_trainers(self):
        """
        Backward compatibility method.
        Existing modules may call this method.
        """

        return self.read()
    


def read_excel(
        file_path="data/Trainers.xlsx",
        sheet_name=None
):
    """
    Helper function for Streamlit.

    Example:

        df = read_excel()

        df = read_excel(
              "data/Trainers.xlsx",
              "Trainers"
        )

    """

    reader = ExcelReader(
        file_path,
        sheet_name
    )

    return reader.read()