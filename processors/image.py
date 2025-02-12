from . import ContentProcessor
from PIL import Image
import io
from typing import BinaryIO


class ImageProcessor:
    """Processor for image files"""

    @staticmethod
    def process(content) -> Image.Image:
        
        """Process the image file and return the processed content"""
        
        
        try:
            image = Image.open(content)
            max_size = (800, 800)
            image.thumbnail(max_size)
            return image
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")
