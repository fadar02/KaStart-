"""
KaStart AI Assistant - Web Interface
A ChatGPT-like web interface powered by Streamlit
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot import ChatBot

st.set_page_config(
    page_title="KaStart AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .main-header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    .main-header p {
        font-size: 1.2em;
        opacity: 0.9;
    }
    
    /* Chat messages */
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a2e;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        color: white;
    }
    
    /* Welcome section */
    .welcome-section {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        color: white;
    }
    .welcome-section h2 {
        color: #667eea;
        margin-bottom: 20px;
    }
    .welcome-section h3 {
        color: #764ba2;
        margin-top: 20px;
    }
    
    /* Quick action buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)


def initialize_chatbot():
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatBot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0


def display_header():
    st.markdown("""
    <div class="main-header">
        <h1>🤖 KaStart AI Assistant</h1>
        <p>Your AI-powered business assistant for SMEs</p>
    </div>
    """, unsafe_allow_html=True)


def display_sidebar():
    with st.sidebar:
        st.markdown("## ⚙️ Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.messages = []
                st.session_state.conversation_count = 0
                st.rerun()
        with col2:
            if st.button("📊 Stats", use_container_width=True):
                st.session_state.show_stats = not st.session_state.get('show_stats', False)
        
        if st.session_state.get('show_stats', False):
            st.metric("Messages", len(st.session_state.messages))
        
        st.divider()
        
        st.markdown("## 💼 Quick Actions")
        
        if st.button("💰 Add Invoice", use_container_width=True):
            st.session_state.quick_action = "Add invoice: "
        if st.button("🎫 Add Ticket", use_container_width=True):
            st.session_state.quick_action = "Add ticket: "
        if st.button("📄 Generate Proposal", use_container_width=True):
            st.session_state.quick_action = "Generate proposal: "
        if st.button("👥 Add Employee", use_container_width=True):
            st.session_state.quick_action = "Add employee: "
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.quick_action = "Dashboard"
        
        st.divider()
        
        st.markdown("## 🔍 Search")
        search_query = st.text_input("Search the web:", placeholder="What is Python?")
        if search_query:
            st.session_state.quick_action = f"Search for {search_query}"
        
        st.divider()
        
        st.markdown("## 📋 Commands")
        st.code("""
help          - All commands
agents        - AI team
plugins       - List plugins
status        - System status
        """, language=None)


def display_welcome():
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-section">
            <h2>Welcome to KaStart AI! 👋</h2>
            <p>I'm your AI-powered business assistant. Ask me anything!</p>
            
            <h3>💼 Business</h3>
            <ul>
                <li><strong>Invoicing</strong> - Create, track, and manage invoices</li>
                <li><strong>Support</strong> - Handle customer tickets and FAQs</li>
                <li><strong>Proposals</strong> - Generate business proposals and quotes</li>
                <li><strong>HR</strong> - Manage employees and leave requests</li>
                <li><strong>Reports</strong> - View business dashboards and analytics</li>
            </ul>
            
            <h3>🧠 AI</h3>
            <ul>
                <li><strong>Web Search</strong> - Get real-time answers from the internet</li>
                <li><strong>Multi-Agent</strong> - Talk to specialized AI agents</li>
                <li><strong>Reasoning</strong> - Step-by-step thinking</li>
                <li><strong>Knowledge Base</strong> - Store and search documents</li>
            </ul>
            
            <h3>💻 Development</h3>
            <ul>
                <li><strong>Code Generation</strong> - Create websites and apps</li>
                <li><strong>File Operations</strong> - Create, read, edit files</li>
                <li><strong>Git</strong> - Version control commands</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Try these:")
        cols = st.columns(3)
        with cols[0]:
            if st.button("🔍 What is Python?", use_container_width=True):
                st.session_state.quick_action = "What is Python?"
        with cols[1]:
            if st.button("💰 Add Invoice", use_container_width=True):
                st.session_state.quick_action = "Add invoice: Acme Corp, $1500, 2026-02-15, Website"
        with cols[2]:
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.quick_action = "Dashboard"


def main():
    initialize_chatbot()
    display_header()
    display_sidebar()
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if not st.session_state.messages:
        display_welcome()
    
    # Handle quick actions
    if 'quick_action' in st.session_state and st.session_state.quick_action:
        prompt = st.session_state.quick_action
        st.session_state.quick_action = None
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chatbot.process_input(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.conversation_count += 1
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
        st.rerun()
    
    if prompt := st.chat_input("💬 Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chatbot.process_input(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.conversation_count += 1
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})


if __name__ == "__main__":
    main()
