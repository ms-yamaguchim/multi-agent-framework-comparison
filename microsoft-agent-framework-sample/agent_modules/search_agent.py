# agents/search_agent.py
import os
from azure.identity import DefaultAzureCredential   
from azure.core.credentials import AzureKeyCredential  
from azure.ai.documentintelligence import DocumentIntelligenceClient  
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import DocumentAnalysisFeature
from agent_framework import Agent
from modules import config
from modules.clients import create_chat_client

if config.ADI_KEY:
    credential = AzureKeyCredential(config.ADI_KEY)  
else:
    credential = DefaultAzureCredential()  

adi_client = DocumentIntelligenceClient(endpoint=config.ADI_ENDPOINT, credential=credential)  


with open(os.path.join("prompt", "search_instruction.txt"), 'r', encoding='utf-8') as file:  
    prompt = file.read()  


def get_documentname():
    print("get_documentname関数を利用")
    directory = './doc'  
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]  
    
    return files


def search_document(document_name) -> str:
    print("extract_data関数を利用")
    print(f"対象：{document_name}")
    file_path = os.path.join("doc",document_name)
    with open(file_path, "rb") as f:
        poller = adi_client.begin_analyze_document(  
            model_id = "prebuilt-layout", 
            body=f,
            locale="ja-JP",  
            features=[DocumentAnalysisFeature.OCR_HIGH_RESOLUTION],  
            content_type="application/octet-stream",  
            output_content_format="markdown"  
        ) 

        result: AnalyzeResult = poller.result()
        markdown_content = result.content

    return markdown_content

search_agent = Agent(
    name="SearchAgent",
    description="都道府県に関する資料を検索・OCRするエージェント",
    client=create_chat_client(),
    instructions=prompt,
    tools=[get_documentname,search_document],
)