
import streamlit as st
import os
import datetime
import sys
from PIL import Image
import io
import base64

# Add the current directory to Python's path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now import from utils
from utils.ghl_api import get_social_accounts, create_social_post, get_posts
from utils.content_gen import generate_topic, generate_caption, generate_image_prompt
from utils.image_gen import generate_image, save_image_from_url

# Page configuration
st.set_page_config(
    page_title="Hypothyroid Content Creator",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title
st.title("Hypothyroid Content Creation Agent")
st.subheader("Create engaging content for your audience")

# Sidebar for controls
with st.sidebar:
    st.header("Content Settings")
    
    content_type = st.selectbox(
        "Content Type",
        ["Educational", "Inspirational", "Funny", "Mixed"],
        index=0
    )
    
    target_emotion = st.selectbox(
        "Target Emotion",
        ["Frustrated with medical system", "Seeking solutions", "Wanting validation", "Ready for change"],
        index=0
    )
    
    hashtags = st.slider("Number of Hashtags", 1, 10, 5)
    
    st.divider()
    
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

# Main content area
tab1, tab2, tab3 = st.tabs(["Create Content", "Post History", "Settings"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Generate New Content")
        
        if st.button("Generate New Post Ideas", type="primary"):
            with st.spinner("Creating content..."):
                # Generate topic
                topic = generate_topic(content_type.lower())
                st.session_state.current_topic = topic
                
                # Generate caption
                caption = generate_caption(topic, content_type.lower(), hashtags)
                st.session_state.current_caption = caption
                
                # Generate image prompt
                image_prompt = generate_image_prompt(topic)
                st.session_state.current_image_prompt = image_prompt
                
                try:
                    # Generate image
                    image_url = generate_image(image_prompt)
                    st.session_state.current_image_url = image_url
                    
                    if image_url is None:
                        st.error("Failed to generate image. Please try again.")
                except Exception as e:
                    st.error(f"Error generating image: {e}")
                    st.session_state.current_image_url = None
        
        # Display generated content if available
        if 'current_topic' in st.session_state:
            st.success("Content generated successfully!")
            st.write("### Topic")
            st.write(st.session_state.current_topic)
            
            st.write("### Caption")
            st.text_area("Edit caption if needed:", value=st.session_state.current_caption, height=200, key="edited_caption")
            
            st.write("### Image Prompt")
            st.text_area("Image prompt:", value=st.session_state.current_image_prompt, height=100, disabled=True)
    
    with col2:
        st.subheader("Preview & Publish")
        
        if 'current_image_url' in st.session_state and st.session_state.current_image_url is not None:
            try:
                st.image(st.session_state.current_image_url, caption="Generated Image", use_column_width=True)
                
                # Publish options
                st.write("### Publish Options")
                
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
            st.warning("No image was generated. Please try again.")

with tab2:
    st.subheader("Post History")
    
    if st.button("Refresh Post History"):
        with st.spinner("Loading posts..."):
            posts = get_posts(limit=10)
            st.session_state.posts = posts
    
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
    else:
        st.info("No posts found. Create some content first!")

with tab3:
    st.subheader("Settings")
    st.info("Settings will be added in a future update.")

# Add footer
st.markdown("---")
st.markdown("Hypothyroid Content Creator | Developed by Muhammad")
