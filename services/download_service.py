import os
import shutil
from pathlib import Path


class DownloadService:
    """
    Handles saving generated files to the user's Downloads folder.
    """

    @staticmethod
    def get_download_folder():
        """
        Returns the Windows Downloads folder.
        """

        return Path.home() / "Downloads"

    @staticmethod
    def save_to_downloads(source_file):

        if not os.path.exists(source_file):
            return None

        downloads = DownloadService.get_download_folder()

        downloads.mkdir(parents=True, exist_ok=True)

        destination = downloads / os.path.basename(source_file)

        shutil.copy2(source_file, destination)

        return str(destination)