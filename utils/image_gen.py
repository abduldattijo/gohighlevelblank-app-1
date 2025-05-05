from openai import OpenAI
from config import OPENAI_API_KEY
import requests
from io import BytesIO
from PIL import Image

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_image(prompt):
    """Generate an image using DALL-E 3"""
    try:
        # Use the correct images.generate method for DALL-E 3
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        # Extract the image URL from the response
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        # Fallback to placeholder if API call fails
        safe_prompt = prompt.replace(" ", "+")[:50]
        return f"https://via.placeholder.com/1024x1024.png?text={safe_prompt}"

def save_image_from_url(url, path):
    """Save an image from a URL to a local file"""
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image.save(path)
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False