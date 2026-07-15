import os


class ImageHandler:

    def __init__(self, folder):
        self.folder = folder


    def get_image_path(self, emp_id):

        for file in os.listdir(self.folder):

            if str(emp_id) in file:
                return os.path.join(self.folder, file)

        return None