# agents/evaluate_agent.py
import os
from agent_framework import Agent
from modules.clients import create_chat_client

with open(os.path.join("prompt", "evaluate_instruction.txt"), 'r', encoding='utf-8') as file:  
    prompt = file.read()  


evaluate_agent = Agent(
    name="EvaluateAgent",
    description="検索結果の十分性・妥当性を評価する",
    client=create_chat_client(),
    instructions=prompt,
)
