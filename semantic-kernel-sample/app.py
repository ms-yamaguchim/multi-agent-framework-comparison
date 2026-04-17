#app.py
# ===== ライブラリ =====
import streamlit as st  
import os
from azure.identity import DefaultAzureCredential   

from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings  
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import ChatHistoryAgentThread  


# ===== エージェントモジュール =====  
from agent_modules.triage_agent import set_triage_agent  
from agent_modules.search_agent import set_search_agent  
from agent_modules.evaluate_agent import set_evaluate_agent  
  

# ===== その他モジュール =====
from modules import config



def read_prompt(filename):  
    with open(os.path.join("prompt", filename), 'r', encoding='utf-8') as file:  
        return file.read()  

# マネージドIDからトークンを取得する関数  
def get_azure_openai_token():  
    credential = DefaultAzureCredential()  
    token = credential.get_token("https://cognitiveservices.azure.com/.default")  
    return token.token  # 実際のアクセストークン文字列  


if config.AOAI_KEY:
    chat_completion_service = AzureChatCompletion(  
        deployment_name=config.AOAI_MODEL_NAME,
        endpoint=config.AOAI_ENDPOINT,  
        api_key=config.AOAI_KEY
    )  
else:
    print("マネージド")
    print(config.AOAI_ENDPOINT)
    print(config.AOAI_MODEL_NAME)
    # AzureChatCompletion をマネージドID認証で初期化  
    chat_completion_service = AzureChatCompletion(  
        deployment_name=config.AOAI_MODEL_NAME,  
        endpoint=config.AOAI_ENDPOINT,  
        ad_token_provider=get_azure_openai_token,
        api_version=config.AOAI_API_VERSION,
    )  



# ===== エージェント初期化関数 =====  
def set_agents():  
    print("エージェントを初期化")  
    search_agent = set_search_agent(chat_completion_service, read_prompt("search_instruction.txt"))  
    evaluate_agent = set_evaluate_agent(chat_completion_service, read_prompt("evaluate_instruction.txt"))  

    # triage_agentにほかのエージェントを紐づける
    triage_agent = set_triage_agent(  
        chat_completion_service,
        read_prompt("triage_instruction.txt"),  
        [  
            search_agent.agent,  
            evaluate_agent.agent,  
        ]  
    )  
    print("エージェント初期化OK")  
    thread = ChatHistoryAgentThread()  
    return triage_agent, thread 





# ===== Streamlit UI =====  
st.set_page_config(page_title="🗺 Semantic Kernelサンプル", layout="wide")  
st.title("🗺 Semantic Kernelサンプル")  

# ===== セッション初期化 =====  
if "triage_agent" not in st.session_state:  
    triage_agent, thread = set_agents()  
    st.session_state.triage_agent = triage_agent  
    st.session_state.thread = thread  
    st.session_state.messages = []  
  
# ===== チャット履歴表示 =====  
for msg in st.session_state.messages:  
    with st.chat_message(msg["role"]):  
        st.write(msg["content"])  
  
# ===== ユーザー入力 =====  
user_input = st.chat_input("メッセージを入力してください")  
  
if user_input:  
    # ユーザーメッセージ保存  
    st.session_state.messages.append({"role": "user", "content": user_input})  
  
    # ユーザー表示  
    with st.chat_message("user"):  
        st.write(user_input)  
  
    # エージェント実行  
    with st.chat_message("assistant"):  
        with st.spinner("エージェントが回答中..."):  
    
            placeholder = st.empty()  
    
            async def run_agent_stream():  
                full_response = ""  
            
                async for chunk in st.session_state.triage_agent.agent.invoke(  
                    messages=user_input,  
                    thread=st.session_state.thread  
                ):  
                    content = None  

                    if hasattr(chunk, "content"):  
                        if isinstance(chunk.content, str):  
                            content = chunk.content  
                        else:  
                            content = str(chunk.content)  

                    if hasattr(chunk, "message") and chunk.message:  
                        content = chunk.message.content  

                    if content:  
                        full_response += content  
                        placeholder.write(full_response)  
                                    
                return full_response  
    
            import asyncio  
            result = asyncio.run(run_agent_stream())  
    
    # 履歴保存  
    st.session_state.messages.append({"role": "assistant", "content": result})  