import os
import requests
import streamlit as st
import streamlit.components.v1 as components

FB = os.environ.get(
    "FB_URL",
    "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app",
)
HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "panel.html")

st.set_page_config(page_title="Fleet", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
      .block-container {padding: 0 !important; max-width: 100% !important;}
      header[data-testid="stHeader"] {display: none;}
      iframe {border: 0;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- passphrase gate (client-side convenience, not real security) ----
PASS = st.secrets.get("PANEL_PASS", "changeme")
if "ok" not in st.session_state:
    st.session_state.ok = False

if not st.session_state.ok:
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.write("### Fleet access")
        p = st.text_input("Passphrase", type="password", label_visibility="collapsed")
        if st.button("Enter", use_container_width=True):
            if p == PASS:
                st.session_state.ok = True
                st.rerun()
            else:
                st.error("Wrong passphrase")
    st.stop()


def fetch_devices():
    try:
        r = requests.get(f"{FB}/devices.json", timeout=8)
        return r.json() or {}
    except Exception:
        return {}


with st.sidebar:
    st.write("### Fleet")
    devs = fetch_devices()
    now = __import__("time").time()
    online = sum(1 for v in devs.values() if v and now - v.get("last", 0) < 45)
    st.metric("Online", online)
    st.metric("Total", len(devs))
    if st.button("Refresh", use_container_width=True):
        st.rerun()
    st.divider()
    if os.path.isfile(PANEL):
        st.download_button(
            "Download panel.html",
            open(PANEL, "rb").read(),
            file_name="panel.html",
            mime="text/html",
            use_container_width=True,
        )
    st.caption(f"DB: {FB.split('//')[-1].split('.')[0]}")

if not os.path.isfile(PANEL):
    st.error("panel.html missing from the repo root.")
    st.stop()

html = open(PANEL, "r", encoding="utf-8").read()
html = html.replace(
    "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app", FB
)

components.html(html, height=1000, scrolling=True)
