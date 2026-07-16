import pandas as pd
import os

class ProjectExtractor:
    def __init__(self, excel_path="Projects.xlsx"):
        self.excel_path = excel_path

    def get_trainer_projects(self, emp_id):
        """
        Parses the sheet matching emp_id inside Projects.xlsx 
        and extracts ongoing and completed projects lists.
        """
        data = {"ongoing": [], "completed": []}
        
        if not os.path.exists(self.excel_path):
            return data

        try:
            xls = pd.ExcelFile(self.excel_path)
            # Match sheet regardless of subtle whitespace issues
            sheet_name = None
            for name in xls.sheet_names:
                if name.strip().lower() == str(emp_id).strip().lower():
                    sheet_name = name
                    break
            
            if not sheet_name:
                return data

            df = pd.read_excel(self.excel_path, sheet_name=sheet_name)
            
            current_section = None
            headers = []

            for _, row in df.iterrows():
                val_cell = str(row.iloc[0]).strip()
                
                if "Ongoing Projects" in val_cell:
                    current_section = "ongoing"
                    continue
                elif "Completed Projects" in val_cell:
                    current_section = "completed"
                    continue
                elif "S.No" in val_cell or "S. No" in val_cell:
                    headers = [str(c).strip() for c in row.values if pd.notna(c)]
                    continue

                # Process records if we are inside a section and row is valid
                if current_section and pd.notna(row.iloc[0]) and str(row.iloc[0]).strip().isdigit():
                    project_item = {
                        "S.No": str(row.iloc[0]).split('.')[0],
                        "College": str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "",
                        "Place": str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else "",
                        "Subject": str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else "",
                        "From": str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else "",
                        "To": str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else ""
                    }
                    data[current_section].append(project_item)
                    
        except Exception:
            pass # Gracefully fall back to empty data lists if sheet is corrupt or unreadable
            
        return data