from openai import OpenAI
from config import OPENAI_API_KEY
import requests
from io import BytesIO
from PIL import Image

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_image(prompt):
    """Generate an image using GPT-4o's DALL·E 3 tools"""
    try:
        response = client.chat.completions.create(
            model="dall-e-3",
            messages=[
                {
                    "role": "user",
                    "content": f"Create an image: {prompt}"
                }
            ],
            tools=[
                {
                    "type": "image_generation",
                    "parameters": {
                        "size": "1024x1024",
                        "n": 1
                    }
                }
            ]
        )

        return response.choices[0].message.tool_calls[0].output.data[0].url
    except Exception as e:
        print(f"Image generation error: {e}")
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
