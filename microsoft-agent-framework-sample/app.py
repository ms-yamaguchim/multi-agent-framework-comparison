# app.py
from typing import cast
import streamlit as st
import asyncio

from agent_framework import (
    AgentResponseUpdate,
    Message,
)
from agent_framework.orchestrations import (
    MagenticBuilder,
)


from agent_modules.triage_agent import triage_agent
from agent_modules.search_agent import search_agent
from agent_modules.evaluate_agent import evaluate_agent


# ------------------------------------------------------------------
# Streamlit 基本設定
# ------------------------------------------------------------------
st.set_page_config(page_title="Magentic Multi-Agent Demo", layout="wide")
st.title("🧠 Magentic Multi-Agent × Streamlit")


# ------------------------------------------------------------------
# Magentic Workflow 構築
# ------------------------------------------------------------------
workflow = MagenticBuilder(
    participants=[search_agent, evaluate_agent],
    manager_agent=triage_agent,
    intermediate_outputs=True,   # ストリーミング＆途中経過表示
    max_round_count=5,
    max_stall_count=2,
    max_reset_count=1,           # ← 再試行1回制御
).build()

# ------------------------------------------------------------------
# Session 初期化
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------------------------
# チャット履歴表示
# ------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------------------------------------------------------
# ユーザー入力
# ------------------------------------------------------------------
user_input = st.chat_input("質問を入力してください")


if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()

        async def run_magentic():
            full_response = ""
            async for event in workflow.run(
                user_input,
                stream=True,   # ✅ session は渡さない
            ):
                if event.type == "output" and isinstance(event.data, AgentResponseUpdate):
                    full_response += str(event.data)
                    placeholder.markdown(full_response)

                elif event.type == "magentic_orchestrator":
                    if isinstance(event.data.content, Message):
                        st.info(f"🧭 Manager Plan\n\n{event.data.content.text}")

            return full_response

        result = asyncio.run(run_magentic())

    st.session_state.messages.append(
        {"role": "assistant", "content": result}
    )

