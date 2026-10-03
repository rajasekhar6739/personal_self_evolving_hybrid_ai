import json
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from core.hybrid_engine import HybridEngine

load_dotenv()

st.set_page_config(
    page_title="Personal Self-Evolving AI",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Personal Self-Evolving Hybrid Intelligence")
st.caption("Human + Main AI + Reviewer AI + Human Thinking AI")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "engine" not in st.session_state:
    st.session_state.engine = HybridEngine()

with st.sidebar:
    st.header("System")
    st.write("**AI-1:** Main AI — plans and performs")
    st.write("**AI-2:** Reviewer AI — checks AI-1")
    st.write("**AI-3:** Human Thinking AI — questions, creativity, decisions")
    st.divider()
    st.subheader("User Evolution")
    profile = st.session_state.engine.get_profile()
    st.write(f"Capabilities: **{len(profile['capabilities'])}**")
    st.write(f"Evolution proposals: **{len(profile['evolution_proposals'])}**")
    st.caption("User-specific evolution is isolated from the core.")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Tell your AI what you need...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI-1 is reasoning, AI-2 is reviewing, AI-3 is helping the human..."):
            result = st.session_state.engine.run(prompt)

        st.markdown("### AI-1 — Main AI")
        st.markdown(result["main"])

        st.markdown("### AI-2 — Workflow Reviewer")
        st.markdown(result["review"])

        st.markdown("### AI-3 — Human Thinking Partner")
        st.markdown(result["human"])

        if result["evolution"]:
            st.markdown("### ♻️ Personal Evolution Proposal")
            st.info(result["evolution"])

        combined = (
            "### AI-1 — Main AI\n" + result["main"] +
            "\n\n### AI-2 — Workflow Reviewer\n" + result["review"] +
            "\n\n### AI-3 — Human Thinking Partner\n" + result["human"]
        )
        st.session_state.messages.append({"role": "assistant", "content": combined})
