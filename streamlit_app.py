import streamlit as st
import os

st.set_page_config(page_title="Voxel Engine – Grand Edition", layout="wide")
st.title("⛏️ Voxel Engine – Grand Edition")
st.markdown("Full 3D world with biomes, caves, crafting, mobile & desktop controls. Press **ESC** to release mouse, click canvas to lock pointer.")

# Load the complete game HTML
with open("index.html", "r", encoding="utf-8") as f:
    game_html = f.read()

# Render the game inside a full‑width iframe
st.components.v1.html(game_html, height=650, scrolling=False)