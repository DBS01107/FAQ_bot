# viewer.py

import sys
import os
import streamlit as st
import pandas as pd

# 🛠 Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modes.text_mode import handle_query  # used for inline querying (optional)
from src.modes.audio_mode import streamlit_voice_query


# 📊 File paths
LOG_PATH = "data/asked_questions_log.csv"
UNANSWERED_PATH = "data/unanswered_questions.csv"

# 🧠 Page setup
st.set_page_config(page_title="Recruitment FAQ Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Recruitment FAQ Chatbot Dashboard")
st.markdown("Monitor user queries, review unanswered questions, and manage FAQ promotion thresholds.")


# 🔘 Sidebar navigation
view = st.sidebar.radio("Choose View", ["Recent Questions", "Unanswered Questions", "Quick Ask"])

# 🧾 Load CSV safely
@st.cache_data
def load_csv(filepath):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        st.warning(f"⚠️ File not found: `{filepath}`")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        st.info("✅ File exists but is empty.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"🚨 Error loading file: {e}")
        return pd.DataFrame()

# 📍 Display logic
if view == "Recent Questions":
    st.subheader("📄 Asked Questions Log")
    df_log = load_csv(LOG_PATH)
    if not df_log.empty:
        st.dataframe(df_log.sort_values("timestamp", ascending=False), use_container_width=True)
    else:
        st.info("No questions logged yet.")

elif view == "Unanswered Questions":
    st.subheader("❓ Unanswered Questions")
    df_unanswered = load_csv(UNANSWERED_PATH)
    if not df_unanswered.empty:
        st.dataframe(df_unanswered.sort_values("timestamp", ascending=False), use_container_width=True)
    else:
        st.success("🎉 All questions have answers! No unanswered entries.")

elif view == "Quick Ask":
    st.subheader("💬 Try a quick query")
    st.markdown("## 🎤 Voice Query")
    if st.button("🎙️ Speak"):
        answer, source = streamlit_voice_query()
        if answer:
            st.markdown(f"**Answer ({source}):**")
            st.success(answer)
            
    st.markdown("## 📝 Text Query")
    user_input = st.text_input("Ask a question (English or मराठी):")
    if user_input:
        answer, source = handle_query(user_input)
        st.markdown(f"**Answer ({source}):**")
        st.success(answer if answer else "🤷 Sorry, no answer found.")
