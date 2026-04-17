# agents/triage_agent.py
import os
import random
from agent_framework import Agent
from modules.clients import create_chat_client


with open(os.path.join("prompt", "triage_instruction.txt"), 'r', encoding='utf-8') as file:  
    prompt = file.read()  



def get_current_location(self) -> str:  
    print("get_current_location関数を利用")

    items = ["群馬県","栃木県","茨城県","埼玉県","東京都","神奈川県","千葉県"]
    return random.choice(items)


triage_agent = Agent(
    name="ManagerAgent",
    client=create_chat_client(),
    instructions=prompt,
    tools=[get_current_location]
)