"""
Updated content_gen.py module with OpenAI 1.0+ compatibility
"""

from config import OPENAI_API_KEY, DEFAULT_TONE, TARGET_AUDIENCE, INSTAGRAM_USERNAME
import random
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Key messaging themes derived from successful thyroid practitioners
MESSAGING_THEMES = [
    "Normal labs don't always mean normal health - your body might be adapting, not broken",
    "The body's systems are interconnected - thyroid health requires a whole-body approach",
    "Root causes often include gut health, stress, inflammation, and environmental factors",
    "When traditional approaches fail, it's time to look deeper than just thyroid medication",
    "True healing begins with understanding your body's signals, not just managing symptoms",
    "Your thyroid is part of a complex ecosystem - fixing just one part rarely solves everything"
]

# Content frameworks that resonate with thyroid patients
CONTENT_FRAMEWORKS = {
    "educational": [
        "The hidden connection between {topic} and thyroid function",
        "Why your doctor might be missing this key factor in {topic}",
        "Beyond TSH: Understanding how {topic} affects your energy and metabolism",
        "The science behind {topic} and its impact on cellular thyroid function",
        "What your labs aren't telling you about {topic} and thyroid health"
    ],
    "inspirational": [
        "You're not broken, you're adapting: How understanding {topic} can transform your health",
        "From struggling to thriving: How addressing {topic} changed everything",
        "Beyond medication: The {topic} approach that's helping women reclaim their energy",
        "Your body is trying to protect you: The truth about {topic} and thyroid adaptation",
        "The turning point: When {topic} becomes the missing piece in your thyroid journey"
    ],
    "funny": [
        "When your thyroid and {topic} are NOT on speaking terms...",
        "That awkward moment when your doctor says you're 'fine' but {topic} says otherwise",
        "Thyroid: 'It's not me, it's {topic}' - A complicated relationship",
        "Trying to fix your thyroid without addressing {topic} is like...",
        "The thyroid-{topic} comedy hour: When your body's communication breaks down"
    ],
    "mixed": [
        "Truth bomb: Why {topic} might be more important than your thyroid medication",
        "The {topic} factor: What every thyroid patient needs to know (but probably hasn't been told)",
        "Surprising ways {topic} might be hijacking your thyroid recovery",
        "Think it's just your thyroid? How {topic} might be the real puppetmaster",
        "The {topic} revolution: Changing how we think about hypothyroidism"
    ]
}

# Topics related to thyroid health, root causes, and recovery
TOPIC_CATEGORIES = {
    "gut_health": [
        "leaky gut syndrome", 
        "gut microbiome imbalance", 
        "hidden gut infections", 
        "intestinal permeability", 
        "food sensitivities"
    ],
    "stress_factors": [
        "HPA axis dysfunction", 
        "chronic stress response", 
        "adrenal fatigue", 
        "cortisol dysregulation",
        "stress hormone imbalance"
    ],
    "environmental": [
        "environmental toxins", 
        "heavy metal exposure", 
        "endocrine disruptors", 
        "chemical sensitivities",
        "mold exposure"
    ],
    "nutrient_status": [
        "iodine balance", 
        "selenium deficiency", 
        "zinc status", 
        "vitamin D levels",
        "B vitamin deficiencies"
    ],
    "metabolic_factors": [
        "insulin resistance", 
        "blood sugar dysregulation", 
        "cellular energy production", 
        "metabolic flexibility",
        "mitochondrial function"
    ],
    "inflammation": [
        "chronic inflammation", 
        "autoimmune triggers", 
        "inflammatory diet patterns", 
        "immune system regulation",
        "inflammatory pathway activation"
    ]
}

def generate_topic(content_type="educational"):
    """Generate a compelling content topic for hypothyroid audience"""
    
    # Select a random category and topic within that category
    category = random.choice(list(TOPIC_CATEGORIES.keys()))
    specific_topic = random.choice(TOPIC_CATEGORIES[category])
    
    # Select a content framework based on the content type
    framework = random.choice(CONTENT_FRAMEWORKS[content_type.lower()])
    
    # Insert the specific topic into the framework
    topic = framework.format(topic=specific_topic)
    
    prompt = f"""
    You are a thyroid health expert who understands that many patients struggle despite "normal" lab results.
    
    Create a compelling social media topic for {TARGET_AUDIENCE} based on this title idea:
    "{topic}"
    
    The content should be {content_type} in nature and focus on a root-cause approach to thyroid health.
    Format as a short, catchy title (max 10 words) that would grab attention on Instagram.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a medical content specialist focused on root-cause approaches to hypothyroid issues."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.7
        )
        return response.choices[0].message.content.strip().strip('"')
    except Exception as e:
        print(f"Error generating topic: {e}")
        return f"The Truth About {specific_topic.title()} and Your Thyroid Health"

def generate_caption(topic, content_type="educational", hashtags=5):
    """Generate a caption for an Instagram post"""
    
    # Select a random messaging theme to incorporate
    theme = random.choice(MESSAGING_THEMES)
    
    prompt = f"""
    Write an engaging Instagram caption for a post titled "{topic}".

    Target audience: {TARGET_AUDIENCE}
    Tone: {DEFAULT_TONE}, with a {content_type} focus
    
    Incorporate this key message: "{theme}"

    The caption should:
    - Begin with a compelling hook about a common frustration or misconception
    - Include 3-4 short paragraphs with line breaks between them
    - Emphasize a root-cause approach rather than just medication management
    - Validate the reader's experience of feeling unwell despite "normal" labs
    - End with a clear call-to-action
    - Include {hashtags} relevant hashtags at the end
    
    The Instagram account is @{INSTAGRAM_USERNAME}, a doctor who helps people look beyond conventional approaches to hypothyroid issues.
    
    Make it substantive, specific, and helpful - avoid generic advice.
    """

    try:
        print(f"Sending caption prompt to GPT-4o...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a social media content creator who specializes in functional medicine approaches to thyroid health. You focus on empowering patients to look beyond labs and medication to find true healing."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=750,
            temperature=0.7
        )
        
        caption = response.choices[0].message.content.strip()
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
    if content_type.lower() == "educational":
        return f"""Ever feel like your body is speaking a language your doctor doesn't understand?

When your labs say "normal" but you feel anything but, it's not in your head. {topic} - this connection is something conventional medicine often misses.

Your body isn't broken - it's adapting to underlying stressors that standard testing doesn't capture. Understanding this difference is the first step toward true healing.

Book a consultation to discover what might be driving your thyroid symptoms beneath the surface.

#thyroidhealth #hypothyroid #rootcause #functionalmedicine #beyondthelabs"""
    
    elif content_type.lower() == "inspirational":
        return f"""You're not broken, your body is trying to tell you something.

After seeing countless patients with "perfect" lab results but persistent symptoms, I've learned this truth: {topic} - this is often where real healing begins.

The conventional approach treats lab numbers, not people. But your experience matters more than what a reference range says is "normal."

Share your thyroid journey in the comments. What symptoms have persisted despite being told everything looks fine?

#thyroidhealing #beyondthelabs #rootcause #hypothyroidjourney #holistichealth"""
    
    elif content_type.lower() == "funny":
        return f"""When your doctor says "your labs are normal" but your body says "LOL, NOPE!" 🥱

{topic} - Anyone else feel like their thyroid and their doctor are having two completely different conversations?

If your energy levels are sending an SOS but your TSH looks "fine," you're not alone. It's like your body is speaking Italian and your labs are only fluent in French.

Double tap if you've mastered the art of looking functional while feeling like a phone battery at 2%!

#thyroidhumor #normallabs #stillexhausted #hypothyroidproblems #doctorjokes"""
    
    else:
        return f"""The gap between "normal" labs and feeling normal is where most thyroid patients live.

{topic} - If you've tried everything but still struggle with fatigue, brain fog, weight, or mood issues, this might be the missing piece.

I'm passionate about looking beyond numbers on a page to find what your body is actually trying to tell you. Sometimes the most important clues are in the symptoms, not the tests.

What thyroid symptom impacts your life most despite "normal" labs? Let's chat in the comments.

#thyroidhealth #functionalmedicine #rootcause #beyondthelabs #thyroidrecovery"""

def generate_image_prompt(topic):
    """Generate a clean, medically themed image prompt for DALL-E 3 with refined visual formatting."""

    visual_styles = [
        "clean medical aesthetic with light teal accents",
        "minimalist wellness scene with soft lighting",
        "functional medicine style with clean lines and blue tones",
        "professional healthcare setting with subtle thyroid imagery",
        "holistic health visual with calming natural elements",
        "modern clinical aesthetic with soothing color palette"
    ]

    prompt_categories = {
        "conceptual": [
            "Professional photograph of doctor examining patient's thyroid area in naturally lit medical office",
            "Healthcare provider and patient reviewing thyroid lab results together in realistic consultation room",
            "Documentary-style medical photo of thyroid examination with proper hand placement on neck"
        ],
        "lifestyle": [
            "Natural lifestyle photo of person preparing thyroid-supporting meal with selenium-rich foods",
            "Authentic photograph of individual doing gentle yoga for thyroid health in morning sunlight",
            "Realistic healthcare photography of person taking thyroid medication with glass of water"
        ],
        "medical": [
            "Professional medical photographer's perspective of thyroid ultrasound procedure in hospital setting",
            "Realistic clinical photograph of doctor using thyroid model to explain condition to patient",
            "Documentary-style healthcare photo of blood test being taken for thyroid panel"
        ]
    }
    
    # Choose random elements to create a unique prompt
    category = random.choice(list(prompt_categories.keys()))
    base_prompt = random.choice(prompt_categories[category])
    style = random.choice(visual_styles)
    
    # Create the final prompt with detailed restrictions for realistic imagery
    final_prompt = f"""
    Create a photorealistic medical image: {base_prompt}

    Topic connection: {topic}

    Style specifications:
    - {style}
    - Realistic medical photography style with authentic details
    - Natural lighting that creates proper shadows and dimension
    - Realistic human expressions and skin textures
    - Proper medical accuracy in any procedures shown
    - Professional composition like editorial healthcare photography

    The image must look like it was taken by a professional medical photographer, 
    not generated by AI. It should have realistic imperfections and natural details
    that make it appear authentic and professional.
    """
    
    return final_prompt.strip()