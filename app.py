
import os, time, requests, streamlit as st
import streamlit.components.v1 as components

FB = os.environ.get("FB_URL", "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app")
HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "panel.html")

st.set_page_config(page_title="Fleet Console", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
.block-container{padding:0!important;max-width:100%!important}
header[data-testid="stHeader"]{display:none}
iframe{border:0}
#login{max-width:390px;margin:11vh auto;font-family:ui-monospace,monospace}
#login h1{font-size:19px;letter-spacing:5px;color:#38bdf8;margin-bottom:4px}
#login p{color:#5b7near;font-size:11px;color:#5b7a92;margin-bottom:22px}
.card{background:#0b1118;border:1px solid #1b2734;border-radius:10px;padding:22px}
</style>""", unsafe_allow_html=True)

def secret(k, d):
    try: return st.secrets.get(k, d)
    except Exception: return d

P_ADMIN = secret("PASS_ADMIN", "admin")
P_DIRECT = secret("PASS_DIRECT", "direct")
P_VIEW = secret("PASS_VIEW", "view")

if "role" not in st.session_state:
    st.session_state.role = None

if not st.session_state.role:
    _, mid, _ = st.columns([1, 1.6, 1])
    with mid:
        st.markdown('<div id="login"><div class="card"><h1>FLEET</h1>'
                    '<p>restricted console</p></div></div>', unsafe_allow_html=True)
        pw = st.text_input("Access key", type="password", label_visibility="collapsed", placeholder="access key")
        if st.button("Unlock", use_container_width=True):
            if pw == P_ADMIN: st.session_state.role = "admin"; st.rerun()
            elif pw == P_DIRECT: st.session_state.role = "direct"; st.rerun()
            elif pw == P_VIEW: st.session_state.role = "view"; st.rerun()
            else: st.error("rejected")
    st.stop()

with st.sidebar:
    st.write("### Session")
    st.write("role **%s**" % st.session_state.role)
    try:
        d = requests.get(f"{FB}/devices.json", timeout=6).json() or {}
    except Exception:
        d = {}
    now = time.time()
    on = sum(1 for v in d.values() if v and now - v.get("last", 0) < 45)
    st.metric("online", on); st.metric("total", len(d))
    if st.button("sign out", use_container_width=True):
        st.session_state.role = None; st.rerun()

html = open(PANEL, encoding="utf-8").read()
html = html.replace("__FB__", FB).replace("__ROLE__", st.session_state.role)
components.html(html, height=1450, scrolling=True)
