"""
WhatsApp Web Clone - Streamlit Edition
A fully-featured WhatsApp-like chat interface built with Streamlit.
No images used: only Unicode emojis, CSS shapes, and custom fonts.
Features:
- Light/Dark theme toggle
- Sidebar with user profile, contacts list, and search
- Chat window with sent/received message bubbles, timestamps, delivery ticks
- Emoji picker (popover)
- Typing indicator simulation and auto-replies
- Status (stories) tab
- Calls log tab
- Message input with send button
- Responsive layout mimicking real WhatsApp Web
"""

import streamlit as st
import datetime
import random
import string
import time
from typing import Dict, List, Tuple

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="WhatsApp Web",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"  # light or dark
if "current_user" not in st.session_state:
    st.session_state.current_user = {
        "name": "You",
        "status": "Hey there! I am using WhatsApp.",
        "avatar_color": "#25D366",
    }
if "contacts" not in st.session_state:
    # Each contact: name, last message, time, unread, status, avatar_color
    st.session_state.contacts = [
        {"name": "Alice", "last_msg": "See you tomorrow!", "time": "10:32 AM", "unread": 2, "status": "At work", "avatar_color": "#E91E63"},
        {"name": "Bob", "last_msg": "👍", "time": "Yesterday", "unread": 0, "status": "Available", "avatar_color": "#9C27B0"},
        {"name": "Charlie", "last_msg": "Did you see the match?", "time": "Monday", "unread": 1, "status": "Busy", "avatar_color": "#3F51B5"},
        {"name": "Diana", "last_msg": "Call me when free", "time": "12:45 PM", "unread": 0, "status": "Battery low", "avatar_color": "#FF5722"},
        {"name": "Eve", "last_msg": "LOL 😂", "time": "9:15 AM", "unread": 5, "status": "At the gym", "avatar_color": "#009688"},
        {"name": "Family Group", "last_msg": "Mom: Dinner at 8?", "time": "8:02 PM", "unread": 0, "status": "Muted", "avatar_color": "#795548"},
    ]
if "current_contact" not in st.session_state:
    st.session_state.current_contact = st.session_state.contacts[0]["name"]  # Default to first contact
if "messages" not in st.session_state:
    # Dict: key = contact name, value = list of message dicts: sender, text, time, status (sent/delivered/read)
    st.session_state.messages = {}
    # Pre-populate some messages for realism
    for contact in st.session_state.contacts:
        name = contact["name"]
        if name != "Family Group":
            st.session_state.messages[name] = [
                {"sender": name, "text": "Hi there!", "time": datetime.datetime.now() - datetime.timedelta(minutes=30), "status": "read"},
                {"sender": "You", "text": "Hello!", "time": datetime.datetime.now() - datetime.timedelta(minutes=29), "status": "read"},
                {"sender": name, "text": "How are you?", "time": datetime.datetime.now() - datetime.timedelta(minutes=28), "status": "read"},
            ]
        else:
            st.session_state.messages[name] = [
                {"sender": "Mom", "text": "Dinner at 8?", "time": datetime.datetime.now() - datetime.timedelta(hours=2), "status": "read"},
                {"sender": "You", "text": "Sure, see you then!", "time": datetime.datetime.now() - datetime.timedelta(hours=1, minutes=55), "status": "read"},
            ]
if "typing_contact" not in st.session_state:
    st.session_state.typing_contact = None
if "emoji_popover" not in st.session_state:
    st.session_state.emoji_popover = False

# -------------------------------
# THEME CSS
# -------------------------------
def inject_css():
    theme = st.session_state.theme
    bg_color = "#efeae2" if theme == "light" else "#111b21"
    sidebar_bg = "#ffffff" if theme == "light" else "#202c33"
    chat_bg = "#e5ddd5" if theme == "light" else "#0b141a"
    sent_bubble_bg = "#dcf8c6" if theme == "light" else "#005c4b"
    received_bubble_bg = "#ffffff" if theme == "light" else "#202c33"
    text_color = "#000000" if theme == "light" else "#e9edef"
    secondary_text = "#667781" if theme == "light" else "#8696a0"
    topbar_bg = "#075e54" if theme == "light" else "#202c33"
    topbar_text = "#ffffff"
    button_bg = "#ffffff" if theme == "light" else "#2a3942"
    button_hover = "#f5f6f6" if theme == "light" else "#374248"
    input_bg = "#ffffff" if theme == "light" else "#2a3942"
    border_color = "#e9edef" if theme == "light" else "#313d45"
    scrollbar_bg = "#ced0d1" if theme == "light" else "#374045"

    css = f"""
    <style>
    /* Global overrides */
    .stApp {{
        background-color: {bg_color};
    }}
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border_color};
    }}
    [data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}
    /* Make buttons in sidebar look like contact rows */
    .contact-row button {{
        width: 100%;
        text-align: left;
        padding: 10px 15px;
        background-color: transparent;
        border: none;
        border-radius: 0;
        color: {text_color};
        font-size: 16px;
        line-height: 1.4;
    }}
    .contact-row button:hover {{
        background-color: {button_hover};
    }}
    .contact-row button:focus {{
        background-color: {button_hover} !important;
        outline: none;
    }}
    .contact-avatar {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        font-size: 18px;
        margin-right: 10px;
    }}
    .unread-badge {{
        background-color: #25D366;
        color: white;
        border-radius: 50%;
        padding: 2px 6px;
        font-size: 12px;
        font-weight: bold;
        min-width: 20px;
        text-align: center;
        display: inline-block;
    }}
    /* Chat top bar */
    .chat-topbar {{
        background-color: {topbar_bg};
        color: {topbar_text};
        padding: 10px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid {border_color};
    }}
    .chat-topbar .contact-name {{
        font-size: 18px;
        font-weight: 600;
    }}
    .chat-topbar .last-seen {{
        font-size: 13px;
        color: {secondary_text};
    }}
    /* Chat messages area */
    .chat-messages {{
        background-color: {chat_bg};
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><path d="M10 10 L90 10 L90 90 L10 90 Z" fill="none" stroke="{border_color}" stroke-width="0.5" opacity="0.2"/></svg>');
        padding: 20px;
        overflow-y: auto;
        height: 65vh;
        display: flex;
        flex-direction: column;
    }}
    .message-row {{
        display: flex;
        margin-bottom: 12px;
    }}
    .message-sent {{
        justify-content: flex-end;
    }}
    .message-received {{
        justify-content: flex-start;
    }}
    .bubble {{
        max-width: 65%;
        padding: 8px 12px;
        border-radius: 7.5px;
        position: relative;
        word-wrap: break-word;
        box-shadow: 0 1px 0.5px rgba(0,0,0,0.13);
    }}
    .sent .bubble {{
        background-color: {sent_bubble_bg};
        border-top-right-radius: 0;
    }}
    .received .bubble {{
        background-color: {received_bubble_bg};
        border-top-left-radius: 0;
    }}
    .bubble .message-text {{
        font-size: 14.2px;
        line-height: 19px;
        color: {text_color};
    }}
    .bubble .message-meta {{
        font-size: 11px;
        color: {secondary_text};
        text-align: right;
        margin-top: 2px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 4px;
    }}
    .tick-double {{
        color: #34b7f1; /* blue ticks for read */
    }}
    .tick-delivered {{
        color: {secondary_text};
    }}
    /* Input area */
    .input-area {{
        background-color: {button_bg};
        padding: 10px 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-top: 1px solid {border_color};
    }}
    .emoji-btn, .mic-btn, .send-btn {{
        background: none;
        border: none;
        font-size: 24px;
        cursor: pointer;
        color: {secondary_text};
    }}
    .emoji-btn:hover, .mic-btn:hover, .send-btn:hover {{
        color: {text_color};
    }}
    .chat-input input {{
        background-color: {input_bg};
        border: 1px solid {border_color};
        border-radius: 21px;
        color: {text_color};
        padding: 9px 12px;
    }}
    /* Status tab */
    .status-circle {{
        width: 56px;
        height: 56px;
        border-radius: 50%;
        border: 3px solid #25D366;
        background-color: {button_bg};
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: {text_color};
        margin-right: 15px;
    }}
    .my-status .status-circle {{
        border: 3px dashed #25D366;
    }}
    /* Calls tab */
    .call-entry {{
        display: flex;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid {border_color};
    }}
    .call-icon {{
        font-size: 28px;
        margin-right: 15px;
    }}
    /* Scrollbar */
    .chat-messages::-webkit-scrollbar {{
        width: 6px;
    }}
    .chat-messages::-webkit-scrollbar-track {{
        background: transparent;
    }}
    .chat-messages::-webkit-scrollbar-thumb {{
        background: {scrollbar_bg};
        border-radius: 3px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def get_avatar_html(letter: str, color: str) -> str:
    """Return HTML for a colored circle with a letter."""
    return f'<div class="contact-avatar" style="background-color:{color};">{letter[0].upper()}</div>'

def get_contact_by_name(name: str) -> dict:
    """Find contact dict by name."""
    for c in st.session_state.contacts:
        if c["name"] == name:
            return c
    return None

def generate_message_bubble(msg: dict, align_right: bool) -> str:
    """Build HTML for a single message bubble."""
    text = msg["text"]
    timestamp = msg["time"].strftime("%I:%M %p") if isinstance(msg["time"], datetime.datetime) else msg["time"]
    status = msg.get("status", "sent")
    ticks = ""
    if align_right:
        if status == "sent":
            ticks = '<span class="tick-delivered">✔</span>'
        elif status == "delivered":
            ticks = '<span class="tick-delivered">✔✔</span>'
        elif status == "read":
            ticks = '<span class="tick-double">✔✔</span>'
    bubble_class = "sent" if align_right else "received"
    return f"""
    <div class="message-row message-{bubble_class}">
        <div class="bubble">
            <div class="message-text">{text}</div>
            <div class="message-meta">
                <span>{timestamp}</span>
                {ticks}
            </div>
        </div>
    </div>
    """

def send_message(contact_name: str, text: str):
    """Add a message from You to the conversation, then simulate a reply."""
    if text.strip() == "":
        return
    now = datetime.datetime.now()
    # Add user message
    st.session_state.messages[contact_name].append({
        "sender": "You",
        "text": text,
        "time": now,
        "status": "sent"
    })
    # Update last message in contacts
    contact = get_contact_by_name(contact_name)
    if contact:
        contact["last_msg"] = text
        contact["time"] = now.strftime("%I:%M %p")
    # Simulate auto-reply after a short delay (we'll just add directly for simplicity)
    auto_replies = [
        "Got it! 👍",
        "Sounds good!",
        "Haha 😂",
        "Let me think...",
        "Sure thing!",
        "I'll call you later.",
        "Thanks!",
        "Awesome!",
    ]
    reply_text = random.choice(auto_replies)
    reply_time = now + datetime.timedelta(seconds=random.randint(5, 20))
    st.session_state.messages[contact_name].append({
        "sender": contact_name,
        "text": reply_text,
        "time": reply_time,
        "status": "read"
    })
    # Mark user's message as delivered then read (simulate)
    if st.session_state.messages[contact_name]:
        for msg in reversed(st.session_state.messages[contact_name]):
            if msg["sender"] == "You" and msg["status"] == "sent":
                msg["status"] = "delivered"
            elif msg["sender"] == "You" and msg["status"] == "delivered":
                msg["status"] = "read"
                break
    # Update last message again for the reply
    contact["last_msg"] = reply_text
    contact["time"] = reply_time.strftime("%I:%M %p")
    # Simulate typing indicator (just a brief flag)
    st.session_state.typing_contact = contact_name

# -------------------------------
# UI COMPONENTS
# -------------------------------
def sidebar_ui():
    """Render the sidebar with profile, search, contacts."""
    with st.sidebar:
        # User profile header
        st.markdown("### 💬 WhatsApp Web", unsafe_allow_html=False)
        col1, col2 = st.columns([1, 4])
        with col1:
            # Avatar circle
            user_avatar = get_avatar_html("Y", st.session_state.current_user["avatar_color"])
            st.markdown(user_avatar, unsafe_allow_html=True)
        with col2:
            st.markdown(f"**{st.session_state.current_user['name']}**")
            st.markdown(f"_{st.session_state.current_user['status']}_")
        st.markdown("---")

        # Search bar
        search_query = st.text_input("🔍 Search or start new chat", placeholder="Search...", label_visibility="collapsed")

        # Filter contacts based on search
        contacts = st.session_state.contacts
        if search_query:
            contacts = [c for c in contacts if search_query.lower() in c["name"].lower()]

        # Contacts list header
        col_h1, col_h2 = st.columns([4, 1])
        with col_h1:
            st.markdown("**Chats**")
        with col_h2:
            st.markdown("📝")  # New chat icon

        # Render each contact as a clickable button with avatar
        for contact in contacts:
            name = contact["name"]
            avatar_html = get_avatar_html(name[0].upper(), contact["avatar_color"])
            unread = contact["unread"]
            last = contact["last_msg"]
            time_str = contact["time"]
            # Build row: avatar + text in button
            # Use a button that spans the whole width; on click set current_contact
            button_label = f"{name}\n{last} · {time_str}"
            col_av, col_btn = st.columns([1, 5])
            with col_av:
                st.markdown(avatar_html, unsafe_allow_html=True)
            with col_btn:
                # We'll use a button; style it via CSS class
                if st.button(button_label, key=f"contact_{name}", use_container_width=True):
                    st.session_state.current_contact = name
                # Show unread badge if any
                if unread > 0:
                    st.markdown(f'<span class="unread-badge">{unread}</span>', unsafe_allow_html=True)
        st.markdown("---")
        # Theme toggle
        theme_emoji = "🌙" if st.session_state.theme == "light" else "☀️"
        if st.button(f"{theme_emoji} Toggle Theme"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()

def chat_area_ui():
    """Render the main chat interface for the selected contact."""
    contact = get_contact_by_name(st.session_state.current_contact)
    if not contact:
        st.info("Select a contact to start chatting.")
        return

    # Top bar
    with st.container():
        col1, col2, col3 = st.columns([1, 8, 3])
        with col1:
            st.markdown(get_avatar_html(contact["name"][0].upper(), contact["avatar_color"]), unsafe_allow_html=True)
        with col2:
            st.markdown(f"<span class='contact-name'>{contact['name']}</span>", unsafe_allow_html=True)
            st.markdown(f"<span class='last-seen'>last seen today at 12:34 PM</span>", unsafe_allow_html=True)
        with col3:
            st.markdown("📞  📹  ⋮", unsafe_allow_html=False)  # Call, Video, Menu icons

    # Chat messages container
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
        # Display messages for current contact
        msgs = st.session_state.messages.get(contact["name"], [])
        for msg in msgs:
            is_me = msg["sender"] == "You"
            bubble_html = generate_message_bubble(msg, align_right=is_me)
            st.markdown(bubble_html, unsafe_allow_html=True)
        # Typing indicator
        if st.session_state.typing_contact == contact["name"]:
            st.markdown('<div class="message-row message-received"><div class="bubble"><em>typing...</em></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Input area
    with st.container():
        col_emoji, col_input, col_send, col_mic = st.columns([1, 6, 1, 1])
        with col_emoji:
            # Emoji picker button
            if st.button("😊", key="emoji_btn", help="Emoji"):
                st.session_state.emoji_popover = not st.session_state.emoji_popover
        with col_input:
            # Use a form to handle enter key
            with st.form(key="message_form", clear_on_submit=True):
                user_input = st.text_input("Type a message", label_visibility="collapsed", key="msg_input")
                submitted = st.form_submit_button("Send", help="Send message")
                if submitted and user_input.strip():
                    send_message(contact["name"], user_input.strip())
                    st.rerun()
        with col_send:
            # Alternate send button (same functionality, but form already has send; we can use a button that triggers rerun and uses the input value from session state? Better to use the form. The col_send can just be a send icon button that clicks the form? Simpler: we'll have the form submit button be the "send" button, so we don't need extra. I'll rearrange: form wraps input and a submit button.
            pass  # We'll restructure: Place the input inside a form that ends with the send button.
        with col_mic:
            st.button("🎤", key="mic_btn", help="Voice message")

    # Emoji popover (if toggled)
    if st.session_state.emoji_popover:
        with st.popover("Emoji", use_container_width=True):
            emoji_list = ["😀", "😂", "😍", "👍", "❤️", "🔥", "🎉", "😢", "😡", "🤔", "👋", "🙏",
                          "💪", "👀", "🎂", "🍕", "🚀", "🌈", "⭐", "✔️"]
            cols = st.columns(5)
            for i, emoji in enumerate(emoji_list):
                if cols[i % 5].button(emoji, key=f"emoji_{emoji}"):
                    # Append emoji to the text input (need to manipulate session state for the input)
                    current_input = st.session_state.get("msg_input", "")
                    st.session_state.msg_input = current_input + emoji
                    st.session_state.emoji_popover = False
                    st.rerun()

def status_tab_ui():
    """Display the Status (Stories) tab."""
    st.markdown("### Status")
    st.markdown("**My Status**")
    col_mine, col_add = st.columns([2, 6])
    with col_mine:
        st.markdown('<div class="status-circle my-status">📷</div>', unsafe_allow_html=True)
    with col_add:
        st.markdown("Add to my status")
    st.markdown("---")
    st.markdown("**Recent updates**")
    # Fake statuses
    statuses = [
        {"name": "Alice", "time": "2 hours ago", "color": "#E91E63"},
        {"name": "Bob", "time": "4 hours ago", "color": "#9C27B0"},
        {"name": "Charlie", "time": "Yesterday, 10:32 PM", "color": "#3F51B5"},
    ]
    for s in statuses:
        cols = st.columns([1, 8])
        with cols[0]:
            st.markdown(get_avatar_html(s["name"][0], s["color"]), unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"**{s['name']}**")
            st.markdown(f"_{s['time']}_")
        st.markdown("---")

def calls_tab_ui():
    """Display the Calls log."""
    st.markdown("### Calls")
    calls = [
        {"name": "Bob", "type": "outgoing", "time": "Today, 3:15 PM", "icon": "📞"},
        {"name": "Diana", "type": "missed", "time": "Today, 11:02 AM", "icon": "🔴"},
        {"name": "Alice", "type": "incoming", "time": "Yesterday, 8:40 PM", "icon": "📞"},
        {"name": "Eve", "type": "outgoing", "time": "Monday, 6:22 PM", "icon": "📞"},
    ]
    for call in calls:
        col1, col2, col3 = st.columns([1, 4, 2])
        with col1:
            avatar = get_avatar_html(call["name"][0], "#25D366" if call["type"] != "missed" else "#FF0000")
            st.markdown(avatar, unsafe_allow_html=True)
        with col2:
            st.markdown(f"**{call['name']}**")
            st.markdown(f"{call['icon']} {call['type'].capitalize()}")
        with col3:
            st.markdown(f"_{call['time']}_")
        st.markdown("---")

# -------------------------------
# MAIN LAYOUT
# -------------------------------
def main():
    inject_css()
    # Create tabs for Chats / Status / Calls
    tab1, tab2, tab3 = st.tabs(["💬 Chats", "📱 Status", "📞 Calls"])

    with tab1:
        # Sidebar handled separately, main area for chat
        chat_area_ui()

    with tab2:
        status_tab_ui()

    with tab3:
        calls_tab_ui()

    # Sidebar must be rendered after tabs to remain persistent
    sidebar_ui()

if __name__ == "__main__":
    main()