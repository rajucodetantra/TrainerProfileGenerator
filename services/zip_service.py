import os
import zipfile


class ZipService:

    def create_zip(self, files, zip_path):

        with zipfile.ZipFile(
            zip_path,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zipf:

            for file in files:

                if file and os.path.exists(file):

                    zipf.write(
                        file,
                        os.path.basename(file)
                    )

        return zip_path