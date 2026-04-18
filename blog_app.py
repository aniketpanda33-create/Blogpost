import streamlit as st
import json
import os
from datetime import datetime

# --- DATABASE SETUP ---
DB_FILE = "advanced_posts.json"


def load_data():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_data(posts):
    with open(DB_FILE, "w") as f:
        json.dump(posts, f, indent=4)


# --- STYLING (The Hue Background & Greek Key Border) ---
st.set_page_config(page_title="Personal Blog", layout="wide")

st.markdown("""
<style>
    /* 1. Colorful Hue Changing Background */
    .stApp {
        background: linear-gradient(125deg, #2c3e50, #2980b9, #8e44ad, #c0392b);
        background-size: 400% 400%;
        animation: hueShift 15s ease infinite;
    }
    @keyframes hueShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. Greek Key Pattern Border (Main Container) */
    .main-border {
        border: 15px solid;
        border-image-source: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR36_8iX_pAnwMv_V8y6J68pL_pE9Jb0I0_Sg&s'); /* Placeholder for Greek Key Pattern */
        border-image-slice: 30;
        border-image-repeat: round;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.9); /* Slight transparency to see hue */
        border-radius: 10px;
    }

    /* 3. Profile Card Styling */
    .profile-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #333;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- MAIN LAYOUT ---
import base64
import os

# Function to convert image to base64 for deployment stability
def render_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- PROFILE SECTION ---
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # IMPORTANT: Use the exact filename as it appears in GitHub
        image_filename = "IMG_20251231_134924309_HDR_PORTRAIT.jpg"
        
        if os.path.exists(image_filename):
            base64_img = render_image(image_filename)
            st.markdown(f"""
            <div class="profile-card">
                <img src="data:image/jpg;base64,{base64_img}" 
                     style="border-radius: 50%; width: 150px; height: 150px; object-fit: cover; border: 3px solid #333;">
                <h3>Amit</h3>
                <p>👨‍🍳 Sous Chef | 💻 Tech Enthusiast</p>
                <p>📧 contact@email.com | 🔗 <a href="#">LinkedIn</a></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Profile image not found in the repository.")

# 4 & 6. Categories and Storage Logic
categories = ["Science", "Travel", "Technology", "Miscellaneous"]
posts = load_data()

# --- SIDEBAR: PUBLISH SECTION ---
st.sidebar.header("✍️ Create a Post")
with st.sidebar.form("publish_form", clear_on_submit=True):
    title = st.text_input("Blog Title")
    category = st.selectbox("Category", categories)
    content = st.text_area("Write your thoughts...")

    # 5. Image Upload (Limit to 2)
    uploaded_files = st.file_uploader("Upload Images (Max 2)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    submit = st.form_submit_button("Publish")

    if submit:
        if title and content:
            if len(uploaded_files) > 2:
                st.error("You can only upload up to 2 pictures.")
            else:
                # In a real app, you'd save image paths. Here we simulate it.
                new_post = {
                    "title": title,
                    "category": category,
                    "content": content,
                    "date": datetime.now().strftime("%B %d, %Y"),
                    "images": [f.name for f in uploaded_files]
                }
                posts.append(new_post)
                save_data(posts)
                st.success("Published!")
                st.rerun()

# --- MAIN BLOG FEED ---
st.markdown('<div class="main-border">', unsafe_allow_html=True)

# Tabs for Filtering by Section
tab_all, tab_sci, tab_trav, tab_tech, tab_misc = st.tabs(["All", "Science", "Travel", "Technology", "Miscellaneous"])


def display_posts(category_filter=None):
    filtered_posts = [p for p in posts if p["category"] == category_filter] if category_filter else posts
    if not filtered_posts:
        st.write("No posts in this category yet.")
    for p in reversed(filtered_posts):
        st.subheader(f"[{p['category']}] {p['title']}")
        st.caption(f"Posted on {p['date']}")

        # 5. Display images above the content
        if p.get("images"):
            cols = st.columns(len(p["images"]))
            for idx, img_name in enumerate(p["images"]):
                cols[idx].image("https://via.placeholder.com/300x200?text=Blog+Image", caption=img_name)

        st.write(p["content"])
        st.markdown("---")


with tab_all: display_posts()
with tab_sci: display_posts("Science")
with tab_trav: display_posts("Travel")
with tab_tech: display_posts("Technology")
with tab_misc: display_posts("Miscellaneous")

st.markdown('</div>', unsafe_allow_html=True)
