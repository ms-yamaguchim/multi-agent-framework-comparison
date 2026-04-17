# modules/clients.py
from agent_framework.openai import OpenAIChatClient
from azure.identity import AzureCliCredential
import os
from modules import config



def create_chat_client():
    if config.AOAI_KEY:
        client = OpenAIChatClient(
                model=config.AOAI_MODEL_NAME,
                azure_endpoint=config.AOAI_ENDPOINT,
                api_version=config.AOAI_API_VERSION,
                api_key=config.AOAI_KEY,
            )
    else:
        client = OpenAIChatClient(
                model=config.AOAI_MODEL_NAME,
                azure_endpoint=config.AOAI_ENDPOINT,
                api_version=config.AOAI_API_VERSION,
                credential=AzureCliCredential(),
            )
    return client
