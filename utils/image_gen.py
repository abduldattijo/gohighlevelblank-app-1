import requests
from io import BytesIO
from PIL import Image
import openai
from config import OPENAI_API_KEY

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

def generate_image(prompt):
    """Generate an image using DALL-E"""
    try:
        # Using the older style openai API call (0.28.x)
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        # Fallback to placeholder if API call fails
        url_safe_prompt = prompt.replace(" ", "+").replace(",", "").replace(":", "")[:50]
        return f"https://via.placeholder.com/1024x1024.png?text={url_safe_prompt}"

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