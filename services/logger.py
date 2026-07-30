import logging
import os


class Logger:

    def __init__(self):

        os.makedirs("logs", exist_ok=True)

        self.logger = logging.getLogger("PDFTools")

        if not self.logger.handlers:

            handler = logging.FileHandler(
                "logs/pdf_tools.log",
                encoding="utf-8"
            )

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            handler.setFormatter(formatter)

            self.logger.addHandler(handler)

            self.logger.setLevel(logging.INFO)

    def info(self, message):

        self.logger.info(message)

    def error(self, message):

        self.logger.error(message)