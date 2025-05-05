"""
Enhanced streamlit_app.py with fixed column nesting issue
"""

import streamlit as st
import os
import datetime
import sys
from PIL import Image
import io
import base64
import pandas as pd
import json

# Add the current directory to Python's path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now import from utils
from utils.ghl_api import get_social_accounts, create_social_post, get_posts
from utils.content_gen import generate_topic, generate_caption, generate_image_prompt
from utils.image_gen import generate_image, save_image_from_url, create_graphic_with_text

# Page configuration with improved styling
st.set_page_config(
    page_title="Hypothyroid Content Creator",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #00b2ff;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4267B2;
        margin-top: 0;
    }
    .content-section {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .info-box {
        border-left: 4px solid #00b2ff;
        padding-left: 10px;
        margin: 20px 0;
    }
    .prompt-editor {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #dee2e6;
        margin-top: 10px;
    }
    .button-primary {
        background-color: #4267B2;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for content tracking
if 'created_content' not in st.session_state:
    st.session_state.created_content = []

if 'metrics' not in st.session_state:
    st.session_state.metrics = {
        'content_created': 0,
        'posts_published': 0,
        'top_content_type': 'Educational',
        'engagement_rate': 0
    }

# Initialize session state for image prompt
if 'image_prompt' not in st.session_state:
    st.session_state.image_prompt = ""

# Function to generate image
def generate_image_content(topic, prompt, content_type, use_text_graphic):
    with st.spinner("Creating image..."):
        try:
            if use_text_graphic:
                # Create text-based graphic
                image_path = create_graphic_with_text(topic, content_type.lower())
                
                # Handle local path vs URL
                if image_path.startswith("http"):
                    return image_path
                else:
                    # Load image from local path and convert to displayable format
                    with open(image_path, "rb") as img_file:
                        img_bytes = img_file.read()
                        encoded = base64.b64encode(img_bytes).decode()
                        return f"data:image/png;base64,{encoded}"
            else:
                # Generate image using the edited prompt
                image_url = generate_image(prompt, content_type.lower())
                return image_url
        except Exception as e:
            st.error(f"Error generating image: {e}")
            return None

# App header
st.markdown('<h1 class="main-header">Hypothyroid Content Creation Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Create engaging content for patients who deserve better answers</p>', unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.header("Content Settings")
    
    # Content strategy section
    st.subheader("Content Strategy")
    content_strategy = st.selectbox(
        "Choose your messaging approach",
        ["Root Cause Focus", "Patient Validation", "Beyond Labs", "Holistic Approach", "Mixed"],
        index=0,
        help="Select the overall approach for your content"
    )
    
    content_type = st.selectbox(
        "Content Type",
        ["Educational", "Inspirational", "Funny", "Mixed"],
        index=0,
        help="The overall tone and style of your content"
    )
    
    target_emotion = st.selectbox(
        "Target Emotion",
        ["Frustrated with medical system", "Seeking solutions", "Validation", "Ready for change", "Curious"],
        index=0,
        help="What is your audience feeling right now?"
    )
    
    st.divider()
    
    # Advanced content options
    st.subheader("Content Details")
    
    include_call_to_action = st.checkbox("Include call-to-action", value=True)
    
    if include_call_to_action:
        cta_type = st.selectbox(
            "Call-to-action Type",
            ["Book consultation", "Download guide", "Comment below", "Follow for more", "Join free webinar"],
            index=0
        )
        
    hashtags = st.slider("Number of Hashtags", 1, 10, 5)
    
    use_text_graphic = st.checkbox("Create text-based graphic instead of image", value=False, 
                                  help="Create a clean, branded text graphic instead of a generated image")
    
    # Add an option to enable prompt editing
    enable_prompt_editing = st.checkbox("Enable image prompt editing", value=True,
                                      help="Allow editing the image prompt before generation")
    
    # Auto-generate image with content
    auto_generate_image = st.checkbox("Auto-generate image with content", value=True,
                                    help="Automatically generate image when creating new content")
    
    st.divider()
    
    # Publishing section
    st.header("Publishing")
    auto_schedule = st.checkbox("Auto-schedule posts", value=False)
    
    if auto_schedule:
        schedule_date = st.date_input(
            "Schedule Date",
            datetime.datetime.now() + datetime.timedelta(days=1)
        )
        schedule_time = st.time_input(
            "Schedule Time",
            datetime.time(10, 0)  # 10:00 AM default
        )

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["Create Content", "Post History", "Settings"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.subheader("Generate New Content")
        
        # Topic generation
        if st.button("Generate New Post Ideas", type="primary", key="generate_content"):
            with st.spinner("Creating content ideas..."):
                # Generate topic
                topic = generate_topic(content_type.lower())
                st.session_state.current_topic = topic
                
                # Generate image prompt
                image_prompt = generate_image_prompt(topic)
                st.session_state.image_prompt = image_prompt
                
                # Generate caption with enhanced parameters
                caption = generate_caption(topic, content_type.lower(), hashtags)
                st.session_state.current_caption = caption
                
                # Auto-generate image if enabled
                if auto_generate_image:
                    image_url = generate_image_content(
                        topic, 
                        image_prompt, 
                        content_type, 
                        use_text_graphic
                    )
                    if image_url:
                        st.session_state.current_image_url = image_url
                        
                        # Store content in library
                        content_item = {
                            "id": len(st.session_state.created_content) + 1,
                            "topic": topic,
                            "caption": caption,
                            "image_prompt": image_prompt,
                            "image_url": image_url,
                            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "content_type": content_type,
                            "published": False
                        }
                        st.session_state.created_content.append(content_item)
                        
                        # Update metrics
                        st.session_state.metrics['content_created'] += 1
        
        # Display generated content if available
        if 'current_topic' in st.session_state:
            st.success("✅ Content generated successfully!")
            
            # Topic display
            st.markdown("### Topic")
            st.markdown(f"**{st.session_state.current_topic}**")
            
            # Caption display
            st.markdown("### Caption")
            caption_value = st.session_state.current_caption
            st.text_area("Edit caption if needed:", value=caption_value, height=200, key="edited_caption")
            
            # Image prompt display and editing
            st.markdown("### Image Prompt")
            
            # Display prompt editor if enabled
            if enable_prompt_editing:
                st.markdown('<div class="prompt-editor">', unsafe_allow_html=True)
                edited_prompt = st.text_area(
                    "Edit image prompt to customize the generated image:",
                    value=st.session_state.image_prompt,
                    height=150,
                    key="edited_image_prompt",
                    help="Customize how you want the image to look. Be specific about settings, people, and style."
                )
                st.session_state.image_prompt = edited_prompt
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.info("💡 **Tips for realistic images:** Include terms like 'professional photography', mention natural lighting, specify realistic settings, and request authentic human expressions.")
            else:
                st.text_area("Image prompt:", value=st.session_state.image_prompt, height=100, disabled=True)
            
            # Generate/Regenerate image buttons - FIXED: removed nested columns
            # Generate image button (only show if not auto-generated or no image exists)
            if not auto_generate_image or 'current_image_url' not in st.session_state:
                if st.button("Generate Image", type="primary"):
                    image_url = generate_image_content(
                        st.session_state.current_topic,
                        st.session_state.image_prompt,
                        content_type,
                        use_text_graphic
                    )
                    
                    if image_url:
                        st.session_state.current_image_url = image_url
                        
                        # Update content library if not already done
                        if auto_generate_image == False:
                            content_item = {
                                "id": len(st.session_state.created_content) + 1,
                                "topic": st.session_state.current_topic,
                                "caption": st.session_state.get("edited_caption", st.session_state.current_caption),
                                "image_prompt": st.session_state.image_prompt,
                                "image_url": image_url,
                                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "content_type": content_type,
                                "published": False
                            }
                            st.session_state.created_content.append(content_item)
                            st.session_state.metrics['content_created'] += 1
            
            # Regenerate image button (only show if image exists)
            if 'current_image_url' in st.session_state:
                if st.button("Regenerate Image"):
                    image_url = generate_image_content(
                        st.session_state.current_topic,
                        st.session_state.image_prompt,
                        content_type,
                        use_text_graphic
                    )
                    
                    if image_url:
                        st.session_state.current_image_url = image_url
                        
                        # Update the image URL in the content library
                        for item in st.session_state.created_content:
                            if item.get("topic") == st.session_state.current_topic:
                                item["image_url"] = image_url
                                item["image_prompt"] = st.session_state.image_prompt
            
            # Option to regenerate caption only
            if st.button("Regenerate Caption Only"):
                with st.spinner("Regenerating caption..."):
                    new_caption = generate_caption(st.session_state.current_topic, content_type.lower(), hashtags)
                    st.session_state.current_caption = new_caption
                    
                    # Update the caption in the content library
                    for item in st.session_state.created_content:
                        if item.get("topic") == st.session_state.current_topic:
                            item["caption"] = new_caption
                    
                    st.experimental_rerun()
                        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.subheader("Preview & Publish")
        
        if 'current_image_url' in st.session_state and st.session_state.current_image_url is not None:
            try:
                st.image(st.session_state.current_image_url, caption="Generated Image", use_column_width=True)
                
                # Publish options
                st.markdown("### Publish Options")
                
                # Get social accounts
                if 'social_accounts' not in st.session_state:
                    with st.spinner("Loading your social accounts..."):
                        st.session_state.social_accounts = get_social_accounts()
                
                if st.session_state.social_accounts:
                    # Create multiselect for account selection
                    account_options = {}
                    for account in st.session_state.social_accounts.get('data', []):
                        account_options[f"{account.get('type', 'Unknown')} - {account.get('name', 'Unnamed')}"] = account.get('id')
                    
                    selected_accounts = st.multiselect(
                        "Select Social Media Accounts",
                        options=list(account_options.keys())
                    )
                    
                    selected_account_ids = [account_options[account] for account in selected_accounts]
                    
                    # Publishing buttons - FIXED: use separate buttons instead of columns
                    publish_now = st.button("Publish Now", type="primary")
                    schedule_post = st.button("Schedule Post")
                    
                    if publish_now and selected_account_ids:
                        with st.spinner("Publishing post..."):
                            result = create_social_post(
                                content=st.session_state.get("edited_caption", st.session_state.current_caption),
                                media_urls=[st.session_state.current_image_url],
                                account_ids=selected_account_ids
                            )
                            
                            if result:
                                st.success("Post published successfully!")
                                # Update metrics
                                st.session_state.metrics['posts_published'] += 1
                                
                                # Update content item
                                for item in st.session_state.created_content:
                                    if item.get("topic") == st.session_state.current_topic:
                                        item["published"] = True
                                        item["published_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            else:
                                st.error("Failed to publish post. Please try again.")
                    
                    elif schedule_post and selected_account_ids:
                        if auto_schedule:
                            scheduled_datetime = datetime.datetime.combine(schedule_date, schedule_time)
                            with st.spinner("Scheduling post..."):
                                result = create_social_post(
                                    content=st.session_state.get("edited_caption", st.session_state.current_caption),
                                    media_urls=[st.session_state.current_image_url],
                                    scheduled_time=scheduled_datetime.isoformat(),
                                    account_ids=selected_account_ids
                                )
                                
                                if result:
                                    st.success(f"Post scheduled for {scheduled_datetime.strftime('%B %d, %Y at %I:%M %p')}")
                                    
                                    # Update content item
                                    for item in st.session_state.created_content:
                                        if item.get("topic") == st.session_state.current_topic:
                                            item["scheduled"] = True
                                            item["scheduled_for"] = scheduled_datetime.strftime("%Y-%m-%d %H:%M:%S")
                                else:
                                    st.error("Failed to schedule post. Please try again.")
                        else:
                            st.warning("Please enable auto-scheduling in the sidebar first.")
                else:
                    st.warning("No social media accounts found. Please connect accounts in GoHighLevel.")
            except Exception as e:
                st.error(f"Error displaying image: {e}")
                st.warning("Failed to load image. Please try generating a new one.")
        
        elif 'current_topic' in st.session_state:
            if auto_generate_image:
                st.info("Image generation in progress. If no image appears, try clicking 'Regenerate Image'.")
            else:
                st.info("Click 'Generate Image' to create an image for this content.")
        
        else:
            st.info("Generate content to preview and publish.")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Post History")
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Content Created", st.session_state.metrics["content_created"])
    
    with col2:
        st.metric("Posts Published", st.session_state.metrics["posts_published"])
    
    with col3:
        # Calculate publish percentage
        publish_percent = 0
        if st.session_state.metrics["content_created"] > 0:
            publish_percent = int((st.session_state.metrics["posts_published"] / st.session_state.metrics["content_created"]) * 100)
        st.metric("Publication Rate", f"{publish_percent}%")
    
    # Content library 
    st.markdown("### Content Library")
    
    if st.session_state.created_content:
        for item in reversed(st.session_state.created_content):
            with st.expander(f"{item.get('topic', 'Content Item')} - {item.get('created_at', 'Unknown date')}"):
                # FIXED: Removed nested columns
                st.write(f"**Topic:** {item.get('topic', 'No topic')}")
                st.write(f"**Type:** {item.get('content_type', 'Unknown')}")
                st.write(f"**Status:** {'Published' if item.get('published') else 'Draft'}")
                
                if item.get('image_url'):
                    try:
                        st.image(item['image_url'], width=300)
                    except Exception as e:
                        st.error(f"Error displaying image: {e}")
                
                st.text_area("Caption:", value=item.get('caption', 'No caption'), height=150, key=f"caption_{item.get('id')}", disabled=True)
                
                # Display image prompt
                st.text_area("Image Prompt:", value=item.get('image_prompt', 'No prompt'), height=100, key=f"prompt_{item.get('id')}", disabled=True)
                
                # Reuse content button
                if st.button("Reuse Content", key=f"reuse_{item.get('id')}"):
                    st.session_state.current_topic = item.get('topic')
                    st.session_state.current_caption = item.get('caption')
                    st.session_state.image_prompt = item.get('image_prompt', '')
                    st.session_state.current_image_url = item.get('image_url')
                    st.info("Content loaded to editor. Switch to the 'Create Content' tab to make edits.")
    else:
        st.info("No content created yet. Start creating content in the 'Create Content' tab.")

with tab3:
    st.subheader("Settings")
    
    # Brand settings
    st.markdown("### Brand Settings")
    
    # FIXED: removed nested columns here
    # Upload logo
    logo_upload = st.file_uploader("Upload logo (optional)", type=["png", "jpg", "jpeg"])
    if logo_upload is not None:
        # Display uploaded logo
        image = Image.open(logo_upload)
        st.image(image, caption="Uploaded Logo", use_column_width=True)
        # Save logo
        with open("logo.png", "wb") as f:
            f.write(logo_upload.getbuffer())
        st.success("Logo saved")
    
    # Brand colors
    st.markdown("Brand Colors")
    primary_color = st.color_picker("Primary Color", "#4267B2")
    secondary_color = st.color_picker("Secondary Color", "#00b2ff")
    
    if st.button("Save Brand Colors"):
        try:
            # Update configuration
            brand_settings = {
                "primary_color": primary_color,
                "secondary_color": secondary_color
            }
            
            with open("brand_settings.json", "w") as f:
                json.dump(brand_settings, f)
            
            st.success("Brand colors saved")
        except Exception as e:
            st.error(f"Error saving brand settings: {e}")

    # Image generation settings
    st.markdown("### Image Generation Settings")
    
    # Sample prompts for realistic images
    st.markdown("#### Sample Prompts for Realistic Images")
    
    sample_prompts = [
        "Professional medical photograph of doctor examining patient's thyroid area in naturally lit office with realistic medical equipment visible",
        "Healthcare photography of endocrinologist discussing lab results with middle-aged patient in authentic clinical setting",
        "Documentary-style medical photo of person preparing thyroid-healthy meal in bright home kitchen with natural morning light",
        "Professional healthcare photography of thyroid medication and supplements arranged on wooden table with soft natural lighting"
    ]
    
    selected_prompt = st.selectbox(
        "Load sample prompt template",
        ["Select a template..."] + sample_prompts
    )
    
    if selected_prompt != "Select a template...":
        st.code(selected_prompt, language="text")
        
        if st.button("Copy to Clipboard"):
            st.success("Prompt copied! You can paste this into the image prompt editor when creating content.")
            
    # Image tips
    with st.expander("Tips for Creating Realistic Medical Images"):
        st.markdown("""
        ### Creating Realistic Medical Images
        
        For most convincing medical photography:
        
        #### Key Elements to Include
        - **Professional environments**: Mention medical offices, consultation rooms with natural lighting
        - **Authentic interactions**: Request genuine facial expressions and natural poses
        - **Medical accuracy**: Specify correct positioning for thyroid examination (front of neck, below Adam's apple)
        - **Realistic details**: Include subtle medical elements like certificates, equipment, or charts
        
        #### Photography Terms to Use
        - **"Professional medical photography"**: Signals realistic style
        - **"Documentary-style healthcare photo"**: Creates journalistic realism
        - **"Natural lighting with soft shadows"**: Creates dimensional, realistic lighting
        - **"Authentic facial expressions"**: Helps avoid artificial-looking faces
        
        #### Example Prompt Structure
        
        ```
        Professional [type] photograph of [subject] in [setting] with [lighting] and [details].
        Style of [photography style] with natural colors and textures.
        ```
        """)

# Add footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #666;">Hypothyroid Content Creator | Developed by Muhammad</div>', unsafe_allow_html=True)