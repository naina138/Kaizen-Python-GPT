import streamlit as st
import json
from rapidfuzz import process
import time

# --- Page Config ---
st.set_page_config(
    page_title="KAIZEN PYTHON GPT | Python Expert",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Import Data ---
# We'll import the data dictionary from MCQGPT2.py
try:
    from MCQGPT2 import data
except ImportError:
    st.error("Could not find MCQGPT2.py. Please make sure it's in the same directory.")
    st.stop()

# --- Custom Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Outfit:wght@300;400;700&display=swap');

    :root {
        --primary-color: #6366f1;
        --secondary-color: #a855f7;
        --bg-color: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
        --text-color: #f8fafc;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism Card */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        border-color: var(--primary-color);
    }

    /* Header Styling */
    .main-header {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        background: linear-gradient(to right, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .subheader {
        text-align: center;
        color: #94a3b8;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }

    /* Custom Button */
    .stButton>button {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
    }

    /* Chat Bubbles */
    .chat-bubble-user {
        background: rgba(99, 102, 241, 0.2);
        border-left: 4px solid var(--primary-color);
        padding: 1rem;
        border-radius: 0 15px 15px 15px;
        margin: 1rem 0;
    }

    .chat-bubble-bot {
        background: rgba(168, 85, 247, 0.1);
        border-right: 4px solid var(--secondary-color);
        padding: 1rem;
        border-radius: 15px 0 15px 15px;
        margin: 1rem 0;
        text-align: left;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-in {
        animation: fadeIn 0.5s ease-out forwards;
    }
    </style>
""", unsafe_allow_html=True)

# --- Logic Functions ---
def get_answer(query):
    questions = list(data.keys())
    matches = process.extract(query, questions, limit=3)
    if matches:
        best_match, score = matches[0][0], matches[0][1]
        if score > 70: # Lowered threshold slightly for better UX
            return data[best_match], score
    return None, 0

def resolve_mcq(question, options):
    questions = list(data.keys())
    matches = process.extract(question, questions, limit=3)

    if matches:
        best_match, score = matches[0][0], matches[0][1]
        if score > 70:
            correct_answer = data[best_match]
            # Find which option best matches the database answer
            best_opt = process.extractOne(correct_answer, options)
            if best_opt:
                return best_opt[0], best_opt[1]
    return None, 0

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: white;'>Navigation</h1>", unsafe_allow_html=True)
    mode = st.radio("Choose Mode", ["💬 General Chat", "🎯 MCQ Solver"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 📊 Project Info")
    st.info("This AI assistant is trained on Python concepts, DSA, Web Dev, and more.")
    
    st.markdown("### 🛠 Technologies")
    st.code("Streamlit\nRapidFuzz\nPython 3.x")

# --- Main App ---
st.markdown("<div class='main-header'>MCQ GPT</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Your Intelligent Python Learning Companion</div>", unsafe_allow_html=True)

if mode == "💬 General Chat":
    st.markdown("<div class='glass-card animate-in'><h3>Ask me anything about Python!</h3></div>", unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What is list comprehension?"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Searching knowledge base..."):
                answer, confidence = get_answer(prompt)
                
                if answer:
                    full_response = f"**Answer:** {answer}\n\n*Confidence Score: {confidence:.2f}%*"
                    # Simulate typing effect
                    displayed_text = ""
                    for char in full_response:
                        displayed_text += char
                        message_placeholder.markdown(displayed_text + "▌")
                        time.sleep(0.005)
                    message_placeholder.markdown(full_response)
                else:
                    message_placeholder.markdown("😔 Sorry, I couldn't find a precise match for that in my database. Try rephrasing or asking something else!")
            
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response if answer else "Sorry, I couldn't find a match."})

elif mode == "🎯 MCQ Solver":
    st.markdown("<div class='glass-card animate-in'><h3>Solve your Python MCQs instantly</h3></div>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            q_input = st.text_area("Question", placeholder="Paste your question here...", height=150)
            
            st.markdown("#### Options")
            o1 = st.text_input("A", placeholder="Option 1")
            o2 = st.text_input("B", placeholder="Option 2")
            o3 = st.text_input("C", placeholder="Option 3")
            o4 = st.text_input("D", placeholder="Option 4")
            
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("🔍 Find Correct Answer"):
                if q_input and all([o1, o2, o3, o4]):
                    options = [o1, o2, o3, o4]
                    with st.spinner("Analyzing options..."):
                        time.sleep(1) # Visual effect
                        correct_opt, confidence = resolve_mcq(q_input, options)
                        
                        if correct_opt:
                            st.success(f"**Identified Answer:**\n\n{correct_opt}")
                            st.metric("Confidence", f"{confidence:.1f}%")
                            st.balloons()
                        else:
                            st.warning("Could not definitively determine the answer from the database.")
                else:
                    st.error("Please fill in both the question and all 4 options.")

    st.markdown("---")
    st.markdown("#### 💡 Pro Tip")
    st.write("For best results, ensure the question keyword (e.g., 'inheritance') is present as stored in the script.")
