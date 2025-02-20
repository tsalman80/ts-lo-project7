import openai
import requests
import config
from PIL import Image
import base64
import io


class ContentTransformer:
    """Transformations for content"""

    def __init__(self):
        """Initialize the transformations"""

        try:
            openai.api_key = config.OPENAI_API_KEY
            self.client = openai
        except Exception as e:
            raise ValueError(f"Error initializing OpenAI client: {str(e)}")

    def text_to_image(self, text: str) -> Image.Image:
        """Transform the image"""

        try:
            response = self.client.images.generate(prompt=text, n=1, size="1024x1024")
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            image = Image.open(io.BytesIO(image_response.content))

            return image
        except Exception as e:
            raise ValueError(f"Error transforming image: {str(e)}")

    def image_to_text(self, image: Image.Image) -> str:
        """Transform the image to text"""

        try:
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that can describe images in detail.",
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe the image in detail.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                            },
                        ],
                    },
                ],
                max_tokens=100,
            )

            description = response.choices[0].message.content
            return description
        except Exception as e:
            raise ValueError(f"Error transforming image to text: {str(e)}")
