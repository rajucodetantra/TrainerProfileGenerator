import os
import re

class ImageHandler:
    def __init__(self, folder):
        self.folder = folder

    def get_image_path(self, emp_id):
        if not self.folder or not os.path.exists(self.folder):
            return None
            
        clean_id = str(emp_id).strip()
        
        # Scan folder for files starting exactly with the Employee ID
        for file in os.listdir(self.folder):
            # Normalizes match pattern (e.g., checks if file starts with 'CT0375' followed by a separator)
            if file.startswith(clean_id):
                full_path = os.path.join(self.folder, file)
                # Force forward slashes to remain universally safe across Streamlit and python-docx
                return full_path.replace("\\", "/")
                
        return None