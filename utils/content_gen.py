# content_gen.py (updated image prompt formatting for DALL·E)

from config import OPENAI_API_KEY, DEFAULT_TONE, TARGET_AUDIENCE, INSTAGRAM_USERNAME
import random
import openai

# Configure OpenAI for older completions if needed
openai.api_key = OPENAI_API_KEY

def generate_topic(content_type="educational"):
    prompt = f"""
    Generate a compelling social media topic for {TARGET_AUDIENCE}.
    The content should be {content_type} in nature.
    The topic should be specific to hypothyroid issues, symptoms, or solutions.
    Format as a short, catchy title (max 10 words).
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
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
        response = openai.ChatCompletion.create(
            model="gpt-4o",
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
    """Generate a clean, medically themed image prompt for DALL-E 3 with refined visual formatting."""

    visual_styles = [
        "flat lay on a white background",
        "isometric hospital desk view",
        "top-down sterile lighting view",
        "side-angle with soft shadows",
        "3D clinical render with blue accents",
        "minimalist medical scene with clean design",
        "medical tray setup in natural lighting"
    ]

    prompt_groups = {
        "general_health": [
            "Minimalist medical icon like a blue stethoscope or health cross on a pure white background",
            "Sterile medical tools like gloves and a digital thermometer placed neatly on a white surface"
        ],
        "lab": [
            "Unlabeled test tubes, pipettes, and gloves on a sterile white lab tray",
            "Clean lab setup with unmarked vials and a blank surface"
        ],
        "thyroid": [
            "A clean desk setup with a wellness smart band, herbal tea, and a digital thermometer placed neatly on a white surface",
            "Thyroid-friendly foods like spinach, boiled eggs, and seaweed arranged on a sterile white plate",
            "A digital wellness tracker placed next to an unmarked pill organizer and glass water bottle on a clinical white background",
            "Flat lay of a medical table with a temperature sensor, smartwatch, and blank daily tracker pad (face down)"
        ],
        "hormone_balance": [
            "A modern clinical desk with a closed hormone-monitoring app tablet, digital watch, and blue stress ball",
            "A medical wristband, glass of water, and clean schedule tracker turned over on a white tray",
            "Flat lay of hormone-friendly supplements (in generic containers) next to iodine-rich greens on a sterile plate",
            "Medical workspace with a closed digital notepad and calming blue pulse oximeter"
        ],
        "mental_focus_medical": [
            "Minimalist mental health workspace with noise-canceling headphones, blank notepad (face down), and a sealed tea sachet",
            "A closed mindfulness tracker app device next to a plant and smart ring on a white hospital tray",
            "Clinical focus tools like blue stress ball, timer, and a muted smartwatch placed symmetrically",
            "Simple blue circle design on clean sterile background, paired with wellness accessories"
        ]
    }

    keyword_map = {
        "general_health": ["health", "clinic", "medical"],
        "lab": ["lab", "test", "blood", "sample", "diagnostic"],
        "thyroid": ["thyroid", "hormone", "levothyroxine", "gland"],
        "hormone_balance": ["balance", "hormonal", "estrogen", "testosterone"],
        "mental_focus_medical": ["mental", "focus", "clarity", "neuro"]
    }

    topic_lower = topic.lower()

    for key, keywords in keyword_map.items():
        if any(word in topic_lower for word in keywords):
            base_prompt = random.choice(prompt_groups[key])
            style = random.choice(visual_styles)
            return f"Highly detailed top-down photo: {base_prompt}, placed on a white medical tray, styled as {style}, no text, no labels, no human body parts."

    base_prompt = random.choice(prompt_groups["general_health"])
    style = random.choice(visual_styles)
    return f"Highly detailed top-down photo: {base_prompt}, placed on a white medical tray, styled as {style}, no text, no labels, no human body parts."
