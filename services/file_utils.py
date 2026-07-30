import os
import tempfile
import time


class FileUtils:
    """
    Common utility functions for file handling.
    """

    @staticmethod
    def readable_size(file_size):
        """
        Convert bytes into a human-readable string.
        """

        units = ["B", "KB", "MB", "GB", "TB"]

        index = 0

        while file_size >= 1024 and index < len(units) - 1:
            file_size /= 1024
            index += 1

        return f"{file_size:.2f} {units[index]}"

    @staticmethod
    def file_size(path):
        """
        Return the size of a file.
        """

        if not os.path.exists(path):
            return "0 B"

        return FileUtils.readable_size(
            os.path.getsize(path)
        )

    @staticmethod
    def execution_time(start_time):
        """
        Return elapsed time in seconds.
        """

        return round(time.time() - start_time, 2)

    @staticmethod
    def create_temp_file(suffix):
        """
        Create a temporary file.
        """

        return tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        )

    @staticmethod
    def ensure_folder(folder):
        """
        Create folder if it doesn't exist.
        """

        os.makedirs(folder, exist_ok=True)

    @staticmethod
    def delete_file(path):
        """
        Delete a file safely.
        """

        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

    @staticmethod
    def clear_folder(folder):
        """
        Delete all files in a folder.
        """

        if not os.path.exists(folder):
            return

        for file in os.listdir(folder):

            path = os.path.join(folder, file)

            if os.path.isfile(path):

                try:
                    os.remove(path)
                except Exception:
                    pass