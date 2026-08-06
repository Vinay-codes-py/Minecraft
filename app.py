import streamlit as st
import streamlit.components.v1 as components
import os

# 1. Configure the Streamlit Page
# Setting layout to 'wide' gives the 3D engine maximum screen space
st.set_page_config(
    page_title="Streamlit Voxel World",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Page Header and Game Instructions
st.title("🧊 3D Voxel World (No-Texture Edition)")

# Using columns to create a clean UI layout for instructions
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### How to Play:
    * **Enter Game:** Click anywhere inside the blue game window to lock your mouse.
    * **Look Around:** Move your mouse.
    * **Movement:** Use **W, A, S, D** keys.
    * **Jump:** Press **Spacebar**.
    * **Mining:** **Left Click** to break blocks.
    * **Building:** **Right Click** to place new grass blocks.
    * **Exit:** Press **ESC** on your keyboard to free your mouse cursor.
    """)
    
with col2:
    st.info("💡 **Tech Stack:** Streamlit + Python + Three.js (WebGL). All textures are procedurally generated using hex color codes to keep the app ultra-fast and lightweight.")

# 3. Load and Inject the HTML/JS Engine
# We read the index.html file dynamically so you don't have to put massive
# strings of HTML inside your Python code.
html_file_path = "index.html"

if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # 4. Render the game frame
    # height=800 ensures it's large enough to act like a real game window.
    # scrolling=False prevents the user from accidentally scrolling the page while playing.
    st.markdown("---")
    components.html(html_content, height=800, scrolling=False)
else:
    # Fallback error just in case the file goes missing
    st.error(f"🚨 Error: Could not find `{html_file_path}`. Please make sure it is in the same folder as `app.py`.")
  
