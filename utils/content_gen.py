from config import OPENAI_API_KEY, DEFAULT_TONE, TARGET_AUDIENCE, INSTAGRAM_USERNAME
import openai

# Configure OpenAI for the older version that's likely installed
openai.api_key = OPENAI_API_KEY

def generate_topic(content_type="educational"):
    """Generate a content topic for hypothyroid audience"""
    prompt = f"""
    Generate a compelling social media topic for {TARGET_AUDIENCE}.
    The content should be {content_type} in nature.
    The topic should be specific to hypothyroid issues, symptoms, or solutions.
    Format as a short, catchy title (max 10 words).
    """
    
    try:
        # Using the older style openai API call (0.28.x) with a current model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical content specialist focused on hypothyroid issues."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        return response.choices[0].message['content'].strip().strip('"')
    except Exception as e:
        print(f"Error generating topic: {e}")
        return "Hypothyroid Management Tips"

def generate_caption(topic, content_type="educational", hashtags=5):
    """Generate a caption for an Instagram post"""
    prompt = f"""
    Write an engaging Instagram caption for a post titled "{topic}".
    
    Target audience: {TARGET_AUDIENCE}
    Tone: {DEFAULT_TONE}, with a {content_type} focus
    
    The caption should:
    - Be 3-4 short paragraphs
    - Include an engaging hook
    - Provide valuable information about hypothyroid issues
    - End with a clear call-to-action
    - Include {hashtags} relevant hashtags at the end
    
    The Instagram account is @{INSTAGRAM_USERNAME}, a doctor who helps people with hypothyroid issues.
    """
    
    try:
        # Using the older style openai API call (0.28.x) with a current model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a social media content creator specializing in health topics."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating caption: {e}")
        return f"This is a post about {topic}. #hypothyroid #health"

def generate_image_prompt(topic):
    """Generate an image prompt for DALL-E based on the topic"""
    prompt = f"""
    Create a detailed image prompt for DALL-E to generate an Instagram-worthy image about:
    "{topic}"
    
    The image should:
    - Match the aesthetic of @{INSTAGRAM_USERNAME}'s Instagram (clean, minimalist, professional)
    - Use light backgrounds with blue accents
    - Be appropriate for a medical professional's account
    - Be visually appealing and shareable
    - NOT contain any text overlay (DALL-E struggles with text)
    - Be suitable for {TARGET_AUDIENCE}
    
    Format your response as a detailed description only, no explanations.
    """
    
    try:
        # Using the older style openai API call (0.28.x) with a current model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional image prompt engineer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating image prompt: {e}")
        return "A clean, minimal medical image with light background and blue accents, suitable for Instagram."