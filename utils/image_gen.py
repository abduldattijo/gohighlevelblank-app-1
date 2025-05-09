"""
Updated image_gen.py module with GPT Image 1 implementation
"""

from openai import OpenAI
from config import OPENAI_API_KEY, BRAND_COLORS
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageColor
import random
import os
import base64

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Define brand styling constants 
# (These should match your config.py values - adjust as needed)
COLOR_PRIMARY = "#4267B2" if 'BRAND_COLORS' not in globals() else BRAND_COLORS[2]
COLOR_SECONDARY = "#00b2ff" if 'BRAND_COLORS' not in globals() else BRAND_COLORS[3]
COLOR_BACKGROUND = "#FFFFFF" if 'BRAND_COLORS' not in globals() else BRAND_COLORS[0]
COLOR_TEXT = "#333333"

def generate_realistic_prompt(topic, content_type="educational"):
    """Generate a realistic, professional medical image prompt for GPT Image 1"""
    
    # Define realistic medical scenarios based on content type
    scenarios = {
        "educational": [
            f"Professional photograph of doctor examining patient's thyroid with proper hand position below Adam's apple in naturally lit medical office. Topic: {topic}",
            f"Healthcare provider explaining thyroid anatomy model to attentive patient in realistic consultation room. Topic: {topic}",
            f"Medical professional showing thyroid test results to patient on computer screen in authentic clinical setting. Topic: {topic}"
        ],
        "inspirational": [
            f"Person preparing thyroid-supporting foods (fish, nuts, seaweed) in bright home kitchen with morning light. Topic: {topic}",
            f"Individual doing gentle yoga for thyroid health in serene home setting with natural lighting. Topic: {topic}",
            f"Person taking daily thyroid medication with water in realistic kitchen environment. Topic: {topic}"
        ],
        "funny": [
            f"Doctor with surprised expression looking at oversized thyroid chart in realistic medical office. Topic: {topic}",
            f"Person dramatically measuring their neck with exaggerated concern in bathroom mirror. Topic: {topic}",
            f"Patient wearing sunglasses indoors at doctor's appointment for thyroid check. Topic: {topic}"
        ],
        "mixed": [
            f"Split scene: doctor's office with thyroid exam on left, healthy meal preparation on right. Topic: {topic}",
            f"Thyroid medication bottles arranged with healthy foods and yoga mat in realistic home setting. Topic: {topic}",
            f"Medical professional and nutritionist discussing thyroid health plan with patient in office. Topic: {topic}"
        ]
    }
    
    # Select appropriate scenario
    if content_type.lower() not in scenarios:
        content_type = "educational"  # Default fallback
    
    scenario = random.choice(scenarios[content_type.lower()])
    
    # Build comprehensive prompt with professional photography direction
    prompt = f"""
    Create a photorealistic medical image: {scenario}
    
    Important details:
    - Use real-looking people with natural expressions and poses
    - Show authentic medical/healthcare environment with realistic details
    - Incorporate natural lighting with proper shadows and dimension
    - Include realistic skin textures and facial features
    - Ensure proper medical accuracy in any procedures or examinations shown
    - Use professional photography style like seen in medical journals
    
    The image should look completely realistic and professional, like it was taken by a healthcare photographer, not generated by AI.
    """
    
    return prompt.strip()

def generate_image(prompt, content_type="educational", quality="medium", size="1024x1024"):
    """Generate an image using GPT Image 1"""
    try:
        # Create a realistic medical prompt if not provided
        if len(prompt) < 50:
            prompt = generate_realistic_prompt(prompt, content_type)
            
        print(f"Generating image with GPT Image 1: {prompt[:100]}...")
        
        # Call GPT Image 1
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1
        )
        
        # Extract the image URL or base64 data from the response
        # GPT Image 1 returns b64_json by default
        image_base64 = response.data[0].b64_json
        
        # Save to a temp file and return the file path
        temp_path = f"temp_image_{random.randint(1000, 9999)}.png"
        image_bytes = base64.b64decode(image_base64)
        with open(temp_path, "wb") as f:
            f.write(image_bytes)
        
        # Convert to base64 data URL for Streamlit
        encoded = base64.b64encode(image_bytes).decode()
        return f"data:image/png;base64,{encoded}"
        
    except Exception as e:
        print(f"Error generating image: {e}")
        # Fallback to placeholder if API call fails
        safe_prompt = prompt.replace(" ", "+")[:50]
        return f"https://via.placeholder.com/1024x1024.png?text={safe_prompt}"

def edit_image_with_mask(image_path, mask_path, prompt, quality="medium"):
    """Edit an image using a mask with GPT Image 1"""
    try:
        print(f"Editing image with mask using GPT Image 1: {prompt[:100]}...")
        
        response = client.images.edit(
            model="gpt-image-1",
            image=open(image_path, "rb"),
            mask=open(mask_path, "rb"),
            prompt=prompt,
            quality=quality
        )
        
        # Extract the image URL or base64 data from the response
        image_base64 = response.data[0].b64_json
        
        # Save to a temp file and return the file path
        temp_path = f"edited_image_{random.randint(1000, 9999)}.png"
        image_bytes = base64.b64decode(image_base64)
        with open(temp_path, "wb") as f:
            f.write(image_bytes)
        
        # Convert to base64 data URL for Streamlit
        encoded = base64.b64encode(image_bytes).decode()
        return f"data:image/png;base64,{encoded}"
        
    except Exception as e:
        print(f"Error editing image: {e}")
        return image_path  # Return original image as fallback

def generate_image_with_references(reference_image_paths, prompt, quality="medium"):
    """Generate a new image using reference images with GPT Image 1"""
    try:
        print(f"Generating image with references using GPT Image 1: {prompt[:100]}...")
        
        # Open reference images
        reference_images = [open(path, "rb") for path in reference_image_paths]
        
        response = client.images.edit(
            model="gpt-image-1",
            image=reference_images,
            prompt=prompt,
            quality=quality
        )
        
        # Extract the image URL or base64 data from the response
        image_base64 = response.data[0].b64_json
        
        # Save to a temp file and return the file path
        temp_path = f"referenced_image_{random.randint(1000, 9999)}.png"
        image_bytes = base64.b64decode(image_base64)
        with open(temp_path, "wb") as f:
            f.write(image_bytes)
        
        # Close all reference image file handles
        for img in reference_images:
            img.close()
        
        # Convert to base64 data URL for Streamlit
        encoded = base64.b64encode(image_bytes).decode()
        return f"data:image/png;base64,{encoded}"
        
    except Exception as e:
        print(f"Error generating image with references: {e}")
        return f"https://via.placeholder.com/1024x1024.png?text=Reference+Image+Error"

def generate_transparent_image(prompt, content_type="educational", quality="high", size="1024x1024"):
    """Generate an image with transparent background using GPT Image 1"""
    try:
        # Create a realistic medical prompt if not provided
        if len(prompt) < 50:
            prompt = generate_realistic_prompt(prompt, content_type)
            
        print(f"Generating transparent image with GPT Image 1: {prompt[:100]}...")
        
        # Call GPT Image 1 with transparent background
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=size,
            quality=quality,
            background="transparent",
            n=1
        )
        
        # Extract the image URL or base64 data from the response
        image_base64 = response.data[0].b64_json
        
        # Save to a temp file and return the file path
        temp_path = f"transparent_image_{random.randint(1000, 9999)}.png"
        image_bytes = base64.b64decode(image_base64)
        with open(temp_path, "wb") as f:
            f.write(image_bytes)
        
        # Convert to base64 data URL for Streamlit
        encoded = base64.b64encode(image_bytes).decode()
        return f"data:image/png;base64,{encoded}"
        
    except Exception as e:
        print(f"Error generating transparent image: {e}")
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

def create_graphic_with_text(topic, content_type="educational"):
    """Create a text-based graphic with the topic and brand styling"""
    try:
        # Create a blank image with brand background
        width, height = 1024, 1024
        img = Image.new('RGB', (width, height), COLOR_BACKGROUND)
        draw = ImageDraw.Draw(img)
        
        # Get colors for content type
        primary_color = COLOR_PRIMARY
        secondary_color = COLOR_SECONDARY
        
        # Add brand accent elements
        # Top accent bar
        draw.rectangle([(0, 0), (width, 60)], fill=primary_color)
        
        # Bottom accent bar
        draw.rectangle([(0, height-60), (width, height)], fill=primary_color)
        
        # Add decorative elements based on content type
        if content_type.lower() == "educational":
            # Add circular elements
            for i in range(5):
                size = random.randint(20, 80)
                x = random.randint(size, width-size)
                y = random.randint(120, height-180)
                draw.ellipse([(x-size/2, y-size/2), (x+size/2, y+size/2)], 
                           fill=secondary_color if i % 2 == 0 else primary_color, 
                           outline=None)
                
        elif content_type.lower() == "inspirational":
            # Add gentle gradient overlay
            for y in range(height):
                # Create a gradient from top to bottom
                r = int(ImageColor.getrgb(primary_color)[0] * (1 - y/height) + 
                        ImageColor.getrgb(secondary_color)[0] * (y/height))
                g = int(ImageColor.getrgb(primary_color)[1] * (1 - y/height) + 
                        ImageColor.getrgb(secondary_color)[1] * (y/height))
                b = int(ImageColor.getrgb(primary_color)[2] * (1 - y/height) + 
                        ImageColor.getrgb(secondary_color)[2] * (y/height))
                draw.line([(0, y), (width, y)], fill=(r, g, b, 50))
                
        elif content_type.lower() == "funny":
            # Add playful diagonal stripes
            stripe_width = 40
            for i in range(-height*2, width*2, stripe_width*3):
                draw.line([(i, 0), (i+height, height)], fill=secondary_color, width=stripe_width)
        
        # Try to load a font or use default
        try:
            title_font = ImageFont.truetype("Arial Bold.ttf", 60)
            subtitle_font = ImageFont.truetype("Arial.ttf", 32)
        except IOError:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            
        # Break topic into lines if needed
        words = topic.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            # Check if text size estimation is available
            if hasattr(draw, 'textlength'):
                text_width = draw.textlength(test_line, font=title_font)
                if text_width < width - 100 or not current_line:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            else:
                # If textlength not available, use simpler approach
                if len(test_line) < 25 or not current_line:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
            
        # Position and draw text
        y_position = height // 2 - (len(lines) * 70) // 2
        
        for line in lines:
            # Draw text with slight shadow for readability
            if hasattr(draw, 'textlength'):
                text_width = draw.textlength(line, font=title_font)
                x_position = (width - text_width) // 2
            else:
                # Estimate position if textlength not available
                x_position = width // 10
                
            # Shadow
            draw.text((x_position+2, y_position+2), line, fill="#33333333", font=title_font)
            # Main text
            draw.text((x_position, y_position), line, fill=COLOR_TEXT, font=title_font)
            
            y_position += 70
        
        # Add subtitle about thyroid health
        subtitle = "Beyond the lab results"
        if hasattr(draw, 'textlength'):
            sub_width = draw.textlength(subtitle, font=subtitle_font)
            sub_x = (width - sub_width) // 2
        else:
            sub_x = width // 3
            
        draw.text((sub_x, y_position + 30), subtitle, fill=primary_color, font=subtitle_font)
        
        # Add logo element at bottom
        logo_size = 60
        padding = 30
        draw.ellipse(
            [(width - logo_size - padding, height - logo_size - padding), 
             (width - padding, height - padding)], 
            fill=primary_color
        )
        
        # Add small "dr" text in the circle
        if hasattr(draw, 'textlength'):
            try:
                text_width = draw.textlength("dr", font=subtitle_font)
                logo_text_x = width - logo_size//2 - padding - text_width//2
                logo_text_y = height - logo_size//2 - padding - subtitle_font.getsize("dr")[1]//2 if hasattr(subtitle_font, 'getsize') else height - logo_size//2 - padding - 15
            except:
                logo_text_x = width - logo_size//2 - padding - 15
                logo_text_y = height - logo_size//2 - padding - 15
        else:
            logo_text_x = width - logo_size//2 - padding - 15
            logo_text_y = height - logo_size//2 - padding - 15
            
        draw.text(
            (logo_text_x, logo_text_y),
            "dr",
            fill="#ffffff",
            font=subtitle_font
        )
        
        # Save to temporary file
        temp_path = "temp_text_graphic.png"
        img.save(temp_path)
        
        return temp_path
    except Exception as e:
        print(f"Error creating text graphic: {e}")
        # Return fallback
        safe_topic = topic.replace(" ", "+")[:50]
        return f"https://via.placeholder.com/1024x1024.png?text={safe_topic}"