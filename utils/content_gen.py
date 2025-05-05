from config import OPENAI_API_KEY, DEFAULT_TONE, TARGET_AUDIENCE, INSTAGRAM_USERNAME
import random
import openai

# Configure OpenAI
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
    
    Make sure the caption is substantial, detailed, and helpful to the audience.
    """

    try:
        print(f"Sending caption prompt to GPT-4o...")
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a social media content creator specializing in health topics who writes detailed, helpful multi-paragraph captions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=750,  # Increased token limit for longer captions
            temperature=0.7
        )
        
        caption = response.choices[0].message['content'].strip()
        print(f"Caption generated successfully, length: {len(caption)} characters")
        
        # Ensure we actually got a substantial caption
        if len(caption) < 100:
            print("Caption too short, using fallback")
            return generate_fallback_caption(topic, content_type, hashtags)
            
        return caption
    except Exception as e:
        print(f"Error generating caption: {e}")
        return generate_fallback_caption(topic, content_type, hashtags)

def generate_fallback_caption(topic, content_type="educational", hashtags=5):
    """Generate a fallback caption if the API call fails"""
    if content_type == "educational":
        return f"""Are you struggling with your thyroid health?

Many people don't realize that their fatigue, weight gain, and brain fog could be related to an underactive thyroid.

{topic} - this is something I see in my practice every day. Understanding these signs can help you take control of your health journey.

Book a consultation with Dr. Josh to discover personalized solutions for your thyroid concerns.

#thyroidhealth #hypothyroid #naturalhealing #holistichealth #wellnesswisdom"""
    
    elif content_type == "inspirational":
        return f"""Your health journey doesn't have to be a struggle!

I've seen countless patients transform their lives once they understood how to properly support their thyroid function.

{topic} - this can be your story too. Small daily changes can lead to remarkable improvements in how you feel.

Share your thyroid journey in the comments below. What's been your biggest challenge?

#thyroidwarrior #healingjourney #hypothyroid #wellnessjourney #holistichealth"""
    
    elif content_type == "funny":
        return f"""When your thyroid decides to take a vacation without telling the rest of your body... 🥱

{topic} - Anyone else feeling personally attacked by their own hormones?

The struggle is real, but so are the solutions! Dr. Josh here to help you whip that lazy thyroid back into shape.

Double tap if you've ever blamed "being tired" when it was actually your thyroid all along!

#thyroidhumor #doctorjokes #hypothyroidproblems #hormonehumor #wellnesswisdom"""
    
    else:
        return f"""Your body whispers before it screams. Are you listening?

{topic} - The subtle signals your thyroid sends when it needs support aren't always obvious, but they're important messengers.

I'm passionate about helping women decode these messages and find natural, effective solutions that work WITH their bodies.

What thyroid symptoms have you been experiencing? Let's chat in the comments.

#thyroidhealth #womenshealth #hypothyroid #holistichealing #wellnessjourney"""

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