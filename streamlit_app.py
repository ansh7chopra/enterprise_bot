import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from datetime import datetime
import time
import os
from dotenv import load_dotenv
load_dotenv()

from agents.meeting_agent import get_meeting_agent
from utils.rag_search import enterprise_search_tool

# Assistant name
BOT_NAME = "Nexa"

# Init LLM
agent      = get_meeting_agent()
fallback_llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)

# Streamlit setup
st.set_page_config(page_title="Enterprise AI Assistant", page_icon="🤖", layout="centered")
st.markdown(f"<h2 style='text-align:center;'>🤖 {BOT_NAME} – Your AI Assistant</h2>", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
<style>
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        margin-bottom: 1.2rem;
    }
    .chat-message {
        padding: 0.7rem 1rem;
        border-radius: 1rem;
        max-width: 80%;
        line-height: 1.5;
        position: relative;
        font-size: 1rem;
    }
    .user-message {
        background-color: #DCF8C6;
        align-self: flex-end;
        margin-left: auto;
    }
    .bot-message {
        background-color: #F1F0F0;
        align-self: flex-start;
        margin-right: auto;
    }
    .timestamp {
        font-size: 0.7rem;
        color: gray;
        margin-top: 0.3rem;
        text-align: right;
    }
    .avatar {
        height: 38px;
        width: 38px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 0.6rem;
    }
    .msg-row {
        display: flex;
        align-items: flex-end;
    }
    .msg-row.bot { flex-direction: row; }
    .msg-row.user { flex-direction: row-reverse; }

    .typing {
        font-style: italic;
        font-size: 0.9rem;
        color: #888;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 0.3rem;
    }

    .dot {
        height: 8px;
        width: 8px;
        background-color: #999;
        border-radius: 50%;
        animation: blink 1s infinite;
    }

    .dot:nth-child(2) {
        animation-delay: 0.2s;
    }

    .dot:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes blink {
        0% { opacity: 0.2; }
        50% { opacity: 1; }
        100% { opacity: 0.2; }
    }
</style>
""", unsafe_allow_html=True)

# Init chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    greeting = f"Hi, I'm {BOT_NAME}. How can I help you today?"
    st.session_state.chat_history.append(AIMessage(content=greeting, additional_kwargs={"timestamp": datetime.now()}))

# Clear chat
if st.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.chat_history = []
    st.rerun()

# Profile pics
BOT_ICON = "https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
USER_ICON = "https://cdn-icons-png.flaticon.com/512/4333/4333609.png"   


# Display chat
for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "bot"
    icon = USER_ICON if role == "user" else BOT_ICON
    timestamp = msg.additional_kwargs.get("timestamp", datetime.now()).strftime("%I:%M %p")

    st.markdown(f"""
    <div class="chat-container">
        <div class="msg-row {role}">
            <img src="{icon}" class="avatar">
            <div class="chat-message {role}-message">
                {msg.content}
                <div class="timestamp">{timestamp}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# User input
user_input = st.chat_input(f"Message {BOT_NAME}...")

if user_input:
    now = datetime.now()

    # Append and render user message *first*
    st.session_state.chat_history.append(
        HumanMessage(content=user_input, additional_kwargs={"timestamp": now})
    )

    # Display updated chat history before bot responds
    # Show typing indicator
    # Check if last message was from user (just sent), then show typing & respond
if st.session_state.chat_history and isinstance(st.session_state.chat_history[-1], HumanMessage):
    with st.spinner(f"{BOT_NAME} is typing..."):
        st.markdown(f"""
        <div class="chat-container">
            <div class="msg-row bot">
                <img src="{BOT_ICON}" class="avatar">
                <div class="chat-message bot-message">
                    <div class="typing">Typing <span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1.5)

    # --- inside the response block ---
    latest_user_msg = st.session_state.chat_history[-1].content

    # 1) Try meeting agent first
    agent_result = agent.invoke({"input": latest_user_msg})

    if isinstance(agent_result, dict) and agent_result.get("output"):
        bot_reply = agent_result["output"]          # meeting confirmation
    else:
        # 2) Try RAG search
        rag_reply = enterprise_search_tool(latest_user_msg)
        if rag_reply:
            bot_reply = rag_reply                   # enterprise doc answer
        else:
            # 3) Fallback to basic chat
            bot_reply = fallback_llm.invoke(latest_user_msg).content

    # Append bot reply
    st.session_state.chat_history.append(
        AIMessage(content=bot_reply, additional_kwargs={"timestamp": datetime.now()})
    )
    st.rerun()




# uv run streamlit run streamlit_app.py

