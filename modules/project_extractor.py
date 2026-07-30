import pandas as pd
import os
import random


class ProjectExtractor:


    def __init__(self, excel_path="Projects.xlsx"):

        self.excel_path = excel_path



    # -------------------------------------------------------
    # Normalize Employee ID
    # -------------------------------------------------------

    def normalize_emp_id(self, emp_id):

        emp_id = str(emp_id).strip().upper()


        if emp_id.isdigit():

            return f"CT{int(emp_id):04d}"


        return emp_id



    # -------------------------------------------------------
    # Get Trainer Projects
    # -------------------------------------------------------

    def get_trainer_projects(self, emp_id):


        data = {

            "ongoing": [],

            "completed": []

        }



        if not os.path.exists(self.excel_path):

            return data



        emp_id = self.normalize_emp_id(emp_id)



        try:


            excel = pd.ExcelFile(
                self.excel_path
            )


            sheet_name = None



            for sheet in excel.sheet_names:


                if self.normalize_emp_id(sheet) == emp_id:

                    sheet_name = sheet

                    break



            if not sheet_name:


                print(
                    "Sheet not found:",
                    emp_id
                )

                return data




            df = pd.read_excel(

                self.excel_path,

                sheet_name=sheet_name,

                header=None

            )



            section = None




            for _, row in df.iterrows():


                first = str(
                    row.iloc[0]
                ).strip()



                # Section detection

                if "Ongoing Projects" in first:


                    section = "ongoing"

                    continue




                if "Completed Projects" in first:


                    section = "completed"

                    continue




                # Skip headings

                if first in [

                    "S.No",

                    "S. No",

                    "nan",

                    ""

                ]:

                    continue





                # Project rows

                if section and first.isdigit():



                    project = {


                        "S.No":

                            str(
                                len(data[section]) + 1
                            ),



                        "College":

                            str(row.iloc[1]).strip()

                            if len(row) > 1

                            and pd.notna(row.iloc[1])

                            else "",




                        "Place":

                            str(row.iloc[2]).strip()

                            if len(row) > 2

                            and pd.notna(row.iloc[2])

                            else "",





                        "Subject":

                            str(row.iloc[3]).strip()

                            if len(row) > 3

                            and pd.notna(row.iloc[3])

                            else ""

                    }




                    data[section].append(
                        project
                    )



            return data




        except Exception as e:


            print(
                "Project extraction error:",
                e
            )


            return data





    # -------------------------------------------------------
    # Get Random Completed Projects
    # -------------------------------------------------------

    def get_random_completed_projects(
            self,
            exclude_emp_id,
            required_count
    ):



        projects = []



        if not os.path.exists(self.excel_path):

            return projects



        try:



            exclude_emp_id = self.normalize_emp_id(
                exclude_emp_id
            )



            excel = pd.ExcelFile(
                self.excel_path
            )



            sheets = []



            for sheet in excel.sheet_names:


                if self.normalize_emp_id(sheet) != exclude_emp_id:


                    sheets.append(sheet)




            random.shuffle(
                sheets
            )





            for sheet in sheets:



                df = pd.read_excel(

                    self.excel_path,

                    sheet_name=sheet,

                    header=None

                )



                inside_completed = False




                for _, row in df.iterrows():



                    first = str(
                        row.iloc[0]
                    ).strip()





                    if "Completed Projects" in first:


                        inside_completed = True

                        continue




                    if "Ongoing Projects" in first:


                        inside_completed = False

                        continue





                    if inside_completed:



                        if first.isdigit():



                            project = {



                                "S.No":

                                    len(projects)+1,



                                "College":

                                    str(row.iloc[1]).strip()

                                    if len(row)>1

                                    and pd.notna(row.iloc[1])

                                    else "",




                                "Place":

                                    str(row.iloc[2]).strip()

                                    if len(row)>2

                                    and pd.notna(row.iloc[2])

                                    else "",




                                "Subject":

                                    str(row.iloc[3]).strip()

                                    if len(row)>3

                                    and pd.notna(row.iloc[3])

                                    else ""

                            }



                            projects.append(
                                project
                            )




                            if len(projects) >= required_count:


                                return projects[:required_count]




        except Exception as e:


            print(
                "Random completed project error:",
                e
            )



        return projects