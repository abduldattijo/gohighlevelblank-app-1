
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GoHighLevel API Configuration
GHL_API_KEY = os.getenv("GHL_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6IlVhT09uQUhpeWlUUkxXVHNTVTVLIiwiY29tcGFueV9pZCI6Ild3WGtoWVJxQXJhYnpmUGJUT3F2IiwidmVyc2lvbiI6MSwiaWF0IjoxNzEwOTU2Njc5MDY2LCJzdWIiOiJ1c2VyX2lkIn0.-lxD40YLkA4FThuHA9AVq2Rh48kFqF4BI67IygLQ_kE")
GHL_BASE_URL = "https://rest.gohighlevel.com/v1/"
LOCATION_ID = os.getenv("LOCATION_ID", "UaOOnAHiyiTRLWTsSU5K")  # From the API key

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Content Generation Settings
DEFAULT_TONE = "friendly and professional"
TARGET_AUDIENCE = "women aged 30-50 who are frustrated with traditional medical approaches to hypothyroid issues"
INSTAGRAM_USERNAME = "askdrjosh"
BRAND_COLORS = ["#ffffff", "#f5f5f5", "#4267B2", "#00b2ff"]  # White, Light gray, Blue, Light blue
