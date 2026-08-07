import streamlit as st
import streamlit.components.v1 as components
import os

# Set Streamlit Page Configuration for Mobile/Desktop layout
st.set_page_config(
    page_title="Mobile 3D Voxel Sandbox",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Application Header & Description
st.title("📱 Mobile 3D Voxel Sandbox")
st.markdown("""
Welcome to the Mobile-Optimized Procedural 3D Voxel Sandbox! Built entirely with **Three.js** and served by **Streamlit**.

### 🕹️ Mobile Touch Controls
- **Move:** Use the **Virtual Joystick** on the bottom-left of the screen.
- **Look Around:** **Swipe and drag** anywhere on the right half of the screen.
- **Actions:** Use the on-screen buttons on the bottom-right to **JUMP**, **MINE** (break blocks), and **PLACE** (build blocks).
""")

# Load and embed the mobile-friendly Three.js HTML file
def load_html_engine():
    html_file_path = "index.html"
    
    if os.path.exists(html_file_path):
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        st.markdown("---")
        # Render HTML component. Height is set larger for mobile display contexts.
        components.html(html_content, height=700, scrolling=False)
    else:
        st.error(f"⚠️ Error: `{html_file_path}` not found in the current directory.")

# Execute Loader
load_html_engine()

# Tech Stack footer
st.markdown("""
---
**Tech Stack:** `Streamlit` (Python Web Framework), `Three.js` (WebGL 3D Rendering), `HTML5/CSS3/JS` (Custom Mobile Touch Controllers).
""")