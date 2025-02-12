from typing import BinaryIO
import os
from config import ALLOWED_EXTENSIONS
from config import MAX_FILE_SIZE


class ContentProcessor:
    """Base class for content processing"""

    @staticmethod
    def detect_content_type(content: BinaryIO) -> str:
        """
        Detect the content type of the file
        Steps:
        1. Get file name and extension
        2. Check which allowed extensions match the file extension
        3. Return the content type
        """

        file_name = getattr(content, "name", None)
        if not file_name:
            raise ValueError("File name not found")

        extension = os.path.splitext(file_name)[1].lower()

        for content_type, extensions in ALLOWED_EXTENSIONS.items():
            if extension in extensions:
                return content_type

        raise ValueError(f"Unsupported file type: {extension}")

    @staticmethod
    def validate_file_size(content: BinaryIO) -> bool:
        """Validate the file size"""

        try:
            content.seek(0, os.SEEK_END)
            file_size = content.tell()
            content.seek(0)
        except Exception as e:
            print(f"Error validating file size: {e}")
            return False

        print(f"File size: {file_size} - {MAX_FILE_SIZE}")
        if file_size > MAX_FILE_SIZE:
            return False

        content_type = ContentProcessor.detect_content_type(content)
        if content_type == "unknown":
            return False

        return True
