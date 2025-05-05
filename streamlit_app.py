"""
Enhanced streamlit_app.py with improved UI, content options and data tracking
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
    .button-primary {
        background-color: #4267B2;
        color: white;
    }
    /* Improve form styling */
    div[data-baseweb="select"] {
        margin-bottom: 15px;
    }
    /* Custom styling for metrics */
    .metric-container {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #4267B2;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
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
        
        posting_frequency = st.selectbox(
            "Post frequency",
            ["One-time post", "Weekly", "Twice per week", "Daily"],
            index=0
        )
    
    # Content library section
    st.header("Content Library")
    st.info("Your content is automatically saved to your library for reuse.")
    
    # Load content templates if available
    try:
        if os.path.exists("content_templates.json"):
            with open("content_templates.json", "r") as f:
                templates = json.load(f)
                
            if templates:
                template_options = ["None"] + [t.get("name", f"Template {i+1}") for i, t in enumerate(templates)]
                selected_template = st.selectbox(
                    "Use saved template",
                    template_options,
                    index=0
                )
    except Exception as e:
        st.error(f"Error loading templates: {e}")

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs(["Create Content", "Post History", "Analytics", "Settings"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.subheader("Generate New Content")
        
        # Content generation button
        if st.button("Generate New Post Ideas", type="primary", key="generate_content"):
            with st.spinner("Creating high-quality content..."):
                # Generate topic
                topic = generate_topic(content_type.lower())
                st.session_state.current_topic = topic
                
                # Prepare content parameters 
                content_params = {
                    "content_type": content_type.lower(),
                    "strategy": content_strategy,
                    "target_emotion": target_emotion,
                    "hashtags": hashtags
                }
                
                # Generate caption with enhanced parameters
                caption = generate_caption(topic, content_type.lower(), hashtags)
                st.session_state.current_caption = caption
                
                # Generate image prompt
                image_prompt = generate_image_prompt(topic)
                st.session_state.current_image_prompt = image_prompt
                
                try:
                    # Create either image or text graphic based on user selection
                    if use_text_graphic:
                        image_path = create_graphic_with_text(topic, content_type.lower())
                        # If it's a local path, need to display differently
                        if image_path.startswith("http"):
                            st.session_state.current_image_url = image_path
                        else:
                            # Load the image and convert to URL for display
                            with open(image_path, "rb") as img_file:
                                img_bytes = img_file.read()
                                encoded = base64.b64encode(img_bytes).decode()
                                st.session_state.current_image_url = f"data:image/png;base64,{encoded}"
                    else:
                        # Generate image
                        image_url = generate_image(image_prompt, content_type.lower())
                        st.session_state.current_image_url = image_url
                    
                    # Update content metrics
                    st.session_state.metrics['content_created'] += 1
                    
                    # Store content in library
                    content_item = {
                        "id": len(st.session_state.created_content) + 1,
                        "topic": topic,
                        "caption": caption,
                        "image_url": st.session_state.current_image_url,
                        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "content_type": content_type,
                        "published": False
                    }
                    st.session_state.created_content.append(content_item)
                    
                except Exception as e:
                    st.error(f"Error generating content: {e}")
                    st.session_state.current_image_url = None
        
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
            
            # Image prompt display (collapsible)
            with st.expander("Show image prompt"):
                st.text_area("Image prompt:", value=st.session_state.current_image_prompt, height=100, disabled=True)
            
            # Additional content options
            st.markdown("### Customize Content")
            
            # Option to regenerate caption only
            if st.button("Regenerate Caption Only"):
                with st.spinner("Regenerating caption..."):
                    new_caption = generate_caption(st.session_state.current_topic, content_type.lower(), hashtags)
                    st.session_state.current_caption = new_caption
                    st.experimental_rerun()
            
            # Option to regenerate image only
            if not use_text_graphic and st.button("Regenerate Image Only"):
                with st.spinner("Regenerating image..."):
                    new_image_url = generate_image(st.session_state.current_image_prompt, content_type.lower())
                    st.session_state.current_image_url = new_image_url
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
                    
                    # Publishing buttons
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        publish_now = st.button("Publish Now", type="primary")
                    
                    with col2:
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
                            
                    # Save as template option
                    st.markdown("### Save Content")
                    template_name = st.text_input("Template name (optional)")
                    if st.button("Save as Template"):
                        try:
                            template = {
                                "name": template_name or f"Template {len(st.session_state.created_content)}",
                                "topic": st.session_state.current_topic,
                                "caption": st.session_state.get("edited_caption", st.session_state.current_caption),
                                "content_type": content_type,
                                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            
                            # Load existing templates
                            templates = []
                            if os.path.exists("content_templates.json"):
                                with open("content_templates.json", "r") as f:
                                    templates = json.load(f)
                            
                            templates.append(template)
                            
                            # Save templates
                            with open("content_templates.json", "w") as f:
                                json.dump(templates, f)
                                
                            st.success("Template saved successfully!")
                        except Exception as e:
                            st.error(f"Error saving template: {e}")
                else:
                    st.warning("No social media accounts found. Please connect accounts in GoHighLevel.")
            except Exception as e:
                st.error(f"Error displaying image: {e}")
                st.warning("Failed to load image. Please try generating a new one.")
        
        elif 'current_topic' in st.session_state:
            st.warning("No image was generated. Please try again.")
        
        else:
            st.info("Generate content to preview and publish.")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Post History")
    
    # Dashboard metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{st.session_state.metrics["content_created"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Content Items Created</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{st.session_state.metrics["posts_published"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Posts Published</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        published_percent = 0
        if st.session_state.metrics["content_created"] > 0:
            published_percent = int((st.session_state.metrics["posts_published"] / st.session_state.metrics["content_created"]) * 100)
        st.markdown(f'<div class="metric-value">{published_percent}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Publication Rate</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Post history section
    st.markdown("### Recent Posts")
    
    if st.button("Refresh Post History"):
        with st.spinner("Loading posts..."):
            posts = get_posts(limit=10)
            st.session_state.posts = posts
    
    # Display posts from GoHighLevel
    if 'posts' in st.session_state and st.session_state.posts:
        for post in st.session_state.posts.get('data', []):
            with st.expander(f"Post: {post.get('id', 'Unknown ID')}"):
                st.write(f"**Content:** {post.get('content', 'No content')}")
                st.write(f"**Status:** {post.get('status', 'Unknown')}")
                st.write(f"**Created:** {post.get('createdAt', 'Unknown')}")
                
                if post.get('mediaUrls'):
                    try:
                        st.image(post['mediaUrls'][0], width=300)
                    except Exception as e:
                        st.error(f"Error displaying image: {e}")
    
    # Display locally created content
    st.markdown("### Content Library")
    
    if st.session_state.created_content:
        for item in reversed(st.session_state.created_content):
            with st.expander(f"{item.get('topic', 'Content Item')} - {item.get('created_at', 'Unknown date')}"):
                st.write(f"**Topic:** {item.get('topic', 'No topic')}")
                st.write(f"**Type:** {item.get('content_type', 'Unknown')}")
                st.write(f"**Status:** {'Published' if item.get('published') else 'Draft'}")
                
                if item.get('image_url'):
                    try:
                        st.image(item['image_url'], width=300)
                    except Exception as e:
                        st.error(f"Error displaying image: {e}")
                
                st.text_area("Caption:", value=item.get('caption', 'No caption'), height=150, key=f"caption_{item.get('id')}", disabled=True)
                
                # Reuse content button
                if st.button("Reuse Content", key=f"reuse_{item.get('id')}"):
                    st.session_state.current_topic = item.get('topic')
                    st.session_state.current_caption = item.get('caption')
                    st.session_state.current_image_url = item.get('image_url')
                    st.info("Content loaded to editor. Switch to the 'Create Content' tab to make edits.")
    else:
        st.info("No content created yet. Start creating content in the 'Create Content' tab.")

with tab3:
    st.subheader("Content Analytics")
    
    # Simple analytics based on created content
    if st.session_state.created_content:
        # Calculate content type distribution
        content_types = {}
        for item in st.session_state.created_content:
            content_type = item.get('content_type', 'Unknown')
            content_types[content_type] = content_types.get(content_type, 0) + 1
        
        # Create content type pie chart
        content_type_data = pd.DataFrame({
            'Content Type': list(content_types.keys()),
            'Count': list(content_types.values())
        })
        
        st.markdown("### Content Type Distribution")
        st.bar_chart(content_type_data.set_index('Content Type'))
        
        # Content creation timeline
        st.markdown("### Content Creation Timeline")
        
        # Extract dates from content
        dates = []
        for item in st.session_state.created_content:
            created_at = item.get('created_at')
            if created_at:
                try:
                    date = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").date()
                    dates.append(date)
                except:
                    pass
        
        # Count content by date
        date_counts = {}
        for date in dates:
            date_str = date.strftime("%Y-%m-%d")
            date_counts[date_str] = date_counts.get(date_str, 0) + 1
        
        # Create timeline chart
        if date_counts:
            timeline_data = pd.DataFrame({
                'Date': list(date_counts.keys()),
                'Content Count': list(date_counts.values())
            })
            timeline_data['Date'] = pd.to_datetime(timeline_data['Date'])
            timeline_data = timeline_data.sort_values('Date')
            
            st.line_chart(timeline_data.set_index('Date'))
        
        # Content stats
        st.markdown("### Content Stats")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Calculate average caption length
            caption_lengths = [len(item.get('caption', '')) for item in st.session_state.created_content]
            avg_caption_length = sum(caption_lengths) / len(caption_lengths) if caption_lengths else 0
            
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{int(avg_caption_length)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Avg Caption Length</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            # Calculate publishing rate by content type
            published_by_type = {}
            total_by_type = {}
            
            for item in st.session_state.created_content:
                content_type = item.get('content_type', 'Unknown')
                total_by_type[content_type] = total_by_type.get(content_type, 0) + 1
                if item.get('published'):
                    published_by_type[content_type] = published_by_type.get(content_type, 0) + 1
            
            # Find most successful content type
            success_rates = {}
            for content_type, total in total_by_type.items():
                success_rates[content_type] = published_by_type.get(content_type, 0) / total
            
            most_successful = max(success_rates.items(), key=lambda x: x[1])[0] if success_rates else "N/A"
            
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{most_successful}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Most Successful Type</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            # Find best day of week for content
            day_counts = {}
            for item in st.session_state.created_content:
                created_at = item.get('created_at')
                if created_at:
                    try:
                        date = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                        day_of_week = date.strftime("%A")
                        day_counts[day_of_week] = day_counts.get(day_of_week, 0) + 1
                    except:
                        pass
            
            best_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else "N/A"
            
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{best_day}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Most Active Day</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.info("Start creating content to view analytics.")
    
    # Future analytics enhancements suggestion
    st.markdown("### Future Analytics")
    st.info("Future updates will include engagement metrics, audience demographics, and content performance analytics.")

with tab4:
    st.subheader("Settings")
    
    # Brand settings
    st.markdown("### Brand Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
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
    
    with col2:
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
    
    # API keys and connections
    st.markdown("### API Keys & Connections")
    
    # GoHighLevel connection
    st.markdown("#### GoHighLevel")
    ghl_key = st.text_input("GoHighLevel API Key", value="*" * 20, type="password")
    ghl_location_id = st.text_input("Location ID", value="*" * 10, type="password")
    
    # OpenAI connection
    st.markdown("#### OpenAI")
    openai_key = st.text_input("OpenAI API Key", value="*" * 20, type="password")
    
    if st.button("Save API Keys"):
        # In a real app, save to .env or secure storage
        st.success("API keys saved")
        st.info("Note: In a production app, API keys should be stored securely")
    
    # Content library management
    st.markdown("### Content Library")
    
    if st.button("Export Content Library"):
        if st.session_state.created_content:
            try:
                # Create CSV from content
                content_df = pd.DataFrame(st.session_state.created_content)
                
                # Convert to CSV
                csv = content_df.to_csv(index=False)
                
                # Create download link
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="content_library.csv">Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error exporting content: {e}")
        else:
            st.warning("No content to export")
    
    # Reset library
    if st.button("Reset Content Library", key="reset_library"):
        confirm = st.checkbox("Confirm reset (this cannot be undone)")
        if confirm:
            st.session_state.created_content = []
            st.session_state.metrics = {
                'content_created': 0,
                'posts_published': 0,
                'top_content_type': 'Educational',
                'engagement_rate': 0
            }
            st.success("Content library reset")

# Add footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #666;">Hypothyroid Content Creator | Developed by Muhammad</div>', unsafe_allow_html=True)