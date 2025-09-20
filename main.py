import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import time
import random

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Boom AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT-inspired styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling - Ultra Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Hide default Streamlit elements */
    .stApp > header {
        background-color: transparent !important;
    }
    
    .stApp > div > div > div > div {
        padding-top: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Remove default spacing */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }
    
    /* Remove empty containers */
    .stMarkdown > div:empty {
        display: none !important;
    }
    
    /* Main header styling - Boom AI Dark */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 0 -1rem;
        text-align: center;
        border-radius: 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8), 0 0 20px rgba(0, 123, 255, 0.3);
        position: sticky;
        top: 0;
        z-index: 100;
        border-bottom: 2px solid #007bff;
    }
    
    .main-header h1 {
        color: #ffffff;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 800;
        letter-spacing: -0.02em;
        text-shadow: 0 0 20px rgba(0, 123, 255, 0.5), 0 4px 8px rgba(0, 0, 0, 0.8);
        background: linear-gradient(45deg, #ffffff, #007bff, #00ffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        color: #00ffff;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    
    /* Chat container - Ultra Dark with vibrant highlights */
    .chat-container {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
        border-radius: 25px;
        padding: 0.5rem;
        margin: 0;
        min-height: auto;
        max-height: none;
        overflow-y: auto;
        border: 3px solid #007bff;
        box-shadow: 
            0 0 30px rgba(0, 123, 255, 0.4),
            0 8px 32px rgba(0, 0, 0, 0.9),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Message styling - ChatGPT inspired with curved edges */
    .message-container {
        display: flex;
        flex-direction: column;
        width: 100%;
        margin: 0.5rem 0;
    }
    
    .user-message-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 0.8rem auto;
        border: 2px solid #007bff;
        box-shadow: 
            0 0 20px rgba(0, 123, 255, 0.3),
            0 4px 15px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        animation: highlightPulse 2s ease-in-out;
        width: 90%;
        max-width: 800px;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    @keyframes highlightPulse {
        0% {
            box-shadow: 
                0 0 20px rgba(0, 123, 255, 0.3),
                0 4px 15px rgba(0, 0, 0, 0.6),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        50% {
            box-shadow: 
                0 0 30px rgba(0, 123, 255, 0.6),
                0 0 40px rgba(0, 255, 255, 0.4),
                0 4px 15px rgba(0, 0, 0, 0.6),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        100% {
            box-shadow: 
                0 0 20px rgba(0, 123, 255, 0.3),
                0 4px 15px rgba(0, 0, 0, 0.6),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
    }
    
    .assistant-message-container {
        background: linear-gradient(135deg, #0f3460 0%, #1a1a2e 100%);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 0.8rem auto;
        border: 2px solid #00ffff;
        box-shadow: 
            0 0 20px rgba(0, 255, 255, 0.3),
            0 4px 15px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        width: 90%;
        max-width: 800px;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .message-content {
        max-width: 100%;
        margin: 0 auto;
        padding: 0 1rem;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        width: 100%;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .user-avatar {
        width: 45px;
        height: 45px;
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        color: white;
        font-weight: 800;
        flex-shrink: 0;
        box-shadow: 
            0 0 15px rgba(0, 123, 255, 0.5),
            0 4px 12px rgba(0, 0, 0, 0.4);
        border: 2px solid #00ffff;
        animation: avatarGlow 2s ease-in-out;
    }
    
    @keyframes avatarGlow {
        0% {
            box-shadow: 
                0 0 15px rgba(0, 123, 255, 0.5),
                0 4px 12px rgba(0, 0, 0, 0.4);
        }
        50% {
            box-shadow: 
                0 0 25px rgba(0, 123, 255, 0.8),
                0 0 35px rgba(0, 255, 255, 0.6),
                0 4px 12px rgba(0, 0, 0, 0.4);
        }
        100% {
            box-shadow: 
                0 0 15px rgba(0, 123, 255, 0.5),
                0 4px 12px rgba(0, 0, 0, 0.4);
        }
    }
    
    .assistant-avatar {
        width: 45px;
        height: 45px;
        background: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        color: #000000;
        font-weight: 800;
        flex-shrink: 0;
        box-shadow: 
            0 0 15px rgba(0, 255, 255, 0.5),
            0 4px 12px rgba(0, 0, 0, 0.4);
        border: 2px solid #007bff;
    }
    
    .user-message-text {
        background: transparent;
        color: #00bfff;
        padding: 0;
        margin: 0;
        border-radius: 0;
        box-shadow: none;
        word-wrap: break-word;
        overflow-wrap: break-word;
        line-height: 1.8;
        font-size: 1.3rem;
        font-weight: 700;
        flex: 1;
        text-shadow: 
            0 0 10px rgba(0, 191, 255, 0.8),
            0 0 20px rgba(0, 123, 255, 0.5),
            0 2px 4px rgba(0, 0, 0, 0.8);
        max-width: 100%;
        overflow: hidden;
    }
    
    .assistant-message-text {
        background: transparent;
        color: #ffffff;
        padding: 0;
        margin: 0;
        border-radius: 0;
        box-shadow: none;
        word-wrap: break-word;
        overflow-wrap: break-word;
        line-height: 1.8;
        font-size: 1.2rem;
        font-weight: 600;
        flex: 1;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
        max-width: 100%;
        overflow: hidden;
    }
    
    /* Optimized Chat input styling - Clean and minimal */
    .stChatInput {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        max-width: 600px !important;
        margin: 0 auto !important;
    }
    
    .stChatInput > div {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%) !important;
        border: 3px solid #007bff !important;
        border-radius: 25px !important;
        padding: 0 !important;
        margin: 1rem auto !important;
        box-shadow: 
            0 0 25px rgba(0, 123, 255, 0.4),
            0 8px 25px rgba(0, 0, 0, 0.8) !important;
        min-height: 60px !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        max-width: 600px !important;
    }
    
    .stChatInput > div > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        flex: 1 !important;
    }
    
    .stChatInput > div > div > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .stChatInput > div > div > div > textarea {
        background: transparent !important;
        color: #ffffff !important;
        border: none !important;
        font-size: 1.3rem !important;
        line-height: 1.6 !important;
        resize: none !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.2) !important;
        padding: 1rem 1.5rem !important;
        margin: 0 !important;
        min-height: 60px !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    .stChatInput > div > div > div > textarea::placeholder {
        color: #00ffff !important;
        font-weight: 500 !important;
        text-shadow: 0 0 5px rgba(0, 255, 255, 0.3) !important;
        opacity: 0.8 !important;
    }
    
    .stChatInput > div > div > div > textarea:focus {
        outline: none !important;
        box-shadow: none !important;
        border: none !important;
    }
    
    .stChatInput > div:focus-within {
        border-color: #00ffff !important;
        box-shadow: 
            0 0 30px rgba(0, 255, 255, 0.5),
            0 8px 25px rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Button styling - ChatGPT inspired with curved edges */
    .stButton > button {
        background: #10a37f !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        box-shadow: 0 3px 12px rgba(16, 163, 127, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: #0d8f6f !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16, 163, 127, 0.4) !important;
    }
    
    /* Sidebar styling with curved edges */
    .css-1d391kg {
        background: #202123 !important;
        border-right: 1px solid #40414f !important;
        border-radius: 0 20px 20px 0 !important;
    }
    
    .css-1d391kg .stSelectbox > div > div {
        background: #40414f !important;
        border: 2px solid #565869 !important;
        color: #ececf1 !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    .css-1d391kg .stSlider > div > div > div {
        background: #40414f !important;
        border-radius: 10px !important;
    }
    
    .css-1d391kg .stSlider > div > div > div > div {
        background: #10a37f !important;
        border-radius: 10px !important;
    }
    
    /* Sidebar text styling */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #ececf1 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    .css-1d391kg p, .css-1d391kg div {
        color: #ececf1 !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    /* Loading animation - ChatGPT style */
    .typing-animation {
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 0.5rem 0;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #10a37f;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { 
            transform: scale(0.8);
            opacity: 0.5;
        }
        40% { 
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #343541;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #565869;
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #8e8ea0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.5rem !important;
        }
        
        .message-content {
            padding: 0 0.5rem;
        }
        
        .stChatInput > div {
            margin: 0.5rem 0 !important;
        }
    }
    
    /* Hover effects for interactivity */
    .message-container:hover {
        background: rgba(255, 255, 255, 0.02);
        transition: background 0.2s ease;
    }
    
    /* Copy button styling with curved edges */
    .copy-button {
        background: #40414f;
        color: #8e8ea0;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        opacity: 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .assistant-message-container:hover .copy-button {
        opacity: 1;
        transform: translateY(-1px);
    }
    
    .copy-button:hover {
        background: #565869;
        color: #ececf1;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Enhanced header styling */
    .main-header h1 {
        color: white;
        font-size: 2.2rem;
        margin: 0;
        font-weight: 700;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'groq_client' not in st.session_state:
    try:
        st.session_state.groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    except Exception as e:
        st.session_state.groq_client = None
        st.error("Failed to initialize Groq client. Please check your API key.")
if 'greeting_shown' not in st.session_state:
    st.session_state.greeting_shown = False
if 'follow_up_questions' not in st.session_state:
    st.session_state.follow_up_questions = []
if 'tech_news' not in st.session_state:
    st.session_state.tech_news = []
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0

# Greeting system
def show_greeting():
    if not st.session_state.greeting_shown:
        greeting_message = {
            "role": "assistant", 
            "content": "🚀 Welcome to Boom AI! I'm your advanced AI assistant ready to help you with any questions or tasks. How can I assist you today?"
        }
        st.session_state.messages.append(greeting_message)
        st.session_state.greeting_shown = True

def generate_follow_up_questions(user_message):
    """Generate follow-up questions based on user input"""
    follow_up_prompts = {
        "code": ["Would you like me to explain any specific part in more detail?", "Do you need help with testing or debugging this?", "Would you like me to show you alternative approaches?"],
        "help": ["What specific area would you like help with?", "Are you looking for beginner or advanced guidance?", "Would you like step-by-step instructions?"],
        "explain": ["Would you like a simpler explanation?", "Do you need examples to illustrate this?", "Are there any specific aspects you'd like me to focus on?"],
        "create": ["What style or format would you prefer?", "Do you have any specific requirements?", "Would you like me to add any particular features?"],
        "analyze": ["What specific insights are you looking for?", "Would you like me to compare with alternatives?", "Do you need recommendations for improvements?"]
    }
    
    user_lower = user_message.lower()
    for keyword, questions in follow_up_prompts.items():
        if keyword in user_lower:
            return questions[:2]  # Return first 2 questions
    
    # Default follow-up questions
    return ["Would you like me to elaborate on any part of this?", "Is there anything specific you'd like me to focus on?"]

# Technology news data
tech_news_pool = [
    {
        "title": "🚀 OpenAI Releases GPT-5 with Enhanced Reasoning",
        "summary": "OpenAI announces GPT-5 featuring improved logical reasoning, better code generation, and enhanced multimodal capabilities."
    },
    {
        "title": "🔬 Quantum Computing Breakthrough at IBM",
        "summary": "IBM achieves new milestone in quantum error correction, bringing practical quantum computing closer to reality."
    },
    {
        "title": "🤖 Tesla Unveils Optimus Robot 2.0",
        "summary": "Tesla's humanoid robot demonstrates advanced manipulation skills and improved mobility for industrial applications."
    },
    {
        "title": "🌐 6G Network Development Accelerates",
        "summary": "Major tech companies collaborate on 6G standards, promising ultra-low latency and revolutionary connectivity."
    },
    {
        "title": "🧠 Neuralink Receives FDA Approval for Human Trials",
        "summary": "Elon Musk's brain-computer interface company begins human trials for medical applications."
    },
    {
        "title": "☀️ Breakthrough in Solar Panel Efficiency",
        "summary": "New perovskite-silicon tandem cells achieve 33% efficiency, revolutionizing renewable energy technology."
    },
    {
        "title": "🔋 Solid-State Battery Revolution Begins",
        "summary": "Toyota announces mass production of solid-state batteries for electric vehicles by 2027."
    },
    {
        "title": "🌍 Carbon Capture Technology Reaches Commercial Scale",
        "summary": "Direct air capture facilities now removing 1 million tons of CO2 annually from the atmosphere."
    },
    {
        "title": "🏥 AI-Powered Drug Discovery Accelerates",
        "summary": "Machine learning models identify new cancer treatment compounds 10x faster than traditional methods."
    },
    {
        "title": "🛰️ SpaceX Launches First Mars Sample Return Mission",
        "summary": "SpaceX successfully launches mission to collect and return Martian soil samples to Earth."
    }
]

def get_random_tech_news():
    """Get 3 random technology news items"""
    return random.sample(tech_news_pool, 3)

def update_tech_news():
    """Update technology news when a question is asked"""
    st.session_state.tech_news = get_random_tech_news()

# Show greeting on first load
show_greeting()

# Initialize tech news
if not st.session_state.tech_news:
    update_tech_news()

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Boom AI</h1>
    <p>Advanced AI Assistant - Dark Mode Edition</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Model selection
    model = st.selectbox(
        "Select Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama-3.1-70b-versatile"],
        index=0,
        help="Choose the AI model for responses"
    )
    
    # Temperature setting
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls randomness in responses"
    )
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Export chat button
    if st.button("📄 Export Chat", use_container_width=True):
        if st.session_state.messages:
            chat_text = ""
            for msg in st.session_state.messages:
                role = "User" if msg["role"] == "user" else "Assistant"
                chat_text += f"{role}: {msg['content']}\n\n"
            st.download_button(
                label="Download Chat",
                data=chat_text,
                file_name=f"chat_export_{int(time.time())}.txt",
                mime="text/plain"
            )
    
    st.markdown("---")
    
    # API status
    st.markdown("### 🔗 API Status")
    if st.session_state.groq_client:
        st.success("✅ Connected")
    else:
        st.error("❌ Connection Failed")
    
    # Technology News Section
    st.markdown("---")
    st.markdown("### 📰 Tech News")
    
    # Refresh news button
    if st.button("🔄 Refresh News", use_container_width=True):
        update_tech_news()
        st.rerun()
    
    if st.session_state.tech_news:
        for i, news in enumerate(st.session_state.tech_news):
            with st.expander(f"{news['title']}", expanded=False):
                st.write(f"**{news['summary']}**")
    else:
        st.info("📡 Loading latest tech news...")
        update_tech_news()
        st.rerun()
    
    # Statistics
    if st.session_state.messages:
        st.markdown("---")
        st.markdown("### 📊 Statistics")
        user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
        assistant_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        st.metric("Messages", f"{user_msgs + assistant_msgs}")
        st.metric("Conversations", f"{assistant_msgs}")
        st.metric("Questions Asked", f"{st.session_state.question_count}")

# Main chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages with ChatGPT-style layout
for i, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        st.markdown(f'''
        <div class="user-message-container">
            <div class="message-content">
                <div class="user-avatar">U</div>
                <div class="user-message-text">{message["content"]}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        # Add copy button functionality with proper escaping
        escaped_content = message["content"].replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n')
        st.markdown(f'''
        <div class="assistant-message-container">
            <div class="message-content">
                <div class="assistant-avatar">AI</div>
                <div class="assistant-message-text">{message["content"]}</div>
                <button class="copy-button" onclick="copyToClipboard('{escaped_content}')">Copy</button>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Show tech news after the greeting message (first assistant message)
        if i == 0 and message["role"] == "assistant" and "Welcome to Boom AI" in message["content"]:
            if st.session_state.tech_news:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown("### 🔥 Latest Tech Updates")
                    for j, news in enumerate(st.session_state.tech_news[:2]):  # Show top 2 news
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                                    padding: 1rem; border-radius: 10px; margin: 0.3rem 0; 
                                    border: 1px solid #007bff; box-shadow: 0 2px 10px rgba(0, 123, 255, 0.2);">
                            <h4 style="color: #00bfff; margin: 0 0 0.5rem 0;">{news['title']}</h4>
                            <p style="color: #ffffff; margin: 0; font-size: 0.9rem;">{news['summary']}</p>
                        </div>
                        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Follow-up questions display
if st.session_state.follow_up_questions:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 💡 Related Questions")
        for i, question in enumerate(st.session_state.follow_up_questions):
            if st.button(f"❓ {question}", key=f"followup_{i}", use_container_width=True):
                # Add the follow-up question as user input
                st.session_state.messages.append({"role": "user", "content": question})
                st.session_state.follow_up_questions = []  # Clear follow-ups
                st.rerun()

# Chat input with enhanced styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Update tech news when a question is asked
    update_tech_news()
    st.session_state.question_count += 1
    
    # Generate follow-up questions
    st.session_state.follow_up_questions = generate_follow_up_questions(user_input)
    
    # Show typing animation while processing
    with st.empty():
        st.markdown("""
        <div class="assistant-message-container">
            <div class="message-content">
                <div class="assistant-avatar">AI</div>
                <div class="typing-animation">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    try:
        if st.session_state.groq_client:
            # Prepare conversation history for context
            conversation_messages = []
            for msg in st.session_state.messages:
                conversation_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Get AI response
            chat_completion = st.session_state.groq_client.chat.completions.create(
                messages=conversation_messages,
                model=model,
                temperature=temperature,
            )
            
            assistant_response = chat_completion.choices[0].message.content
            
            # Add assistant response to session state
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Rerun to display the new messages
            st.rerun()
        else:
            st.error("API client not initialized. Please check your API key in the environment variables.")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error. Please try again."})

# Footer with Boom AI styling
st.markdown("""
<div style='text-align: center; color: #00ffff; padding: 2rem 1rem; font-size: 1rem; font-weight: 600;'>
    <p>Solution to your problems</p>
    <p style='margin-top: 0.5rem; opacity: 0.8; color: #007bff;'>Boom AI - Advanced Dark Mode Interface</p>
</div>
""", unsafe_allow_html=True)

# Add JavaScript for enhanced interactivity
st.markdown("""
<script>
// Auto-scroll to bottom when new messages are added
function scrollToBottom() {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// Scroll to bottom on page load
window.addEventListener('load', scrollToBottom);

// Add smooth scrolling behavior
document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.style.scrollBehavior = 'smooth';
    }
});

// Enhanced copy functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        // Show temporary feedback
        const button = event.target;
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.style.background = '#10a37f';
        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '#40414f';
        }, 2000);
    });
}
</script>
""", unsafe_allow_html=True)