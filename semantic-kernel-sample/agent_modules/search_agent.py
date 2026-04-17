#agent_modules.search_agent.py
from semantic_kernel import Kernel
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.agents import ChatCompletionAgent
from typing import Annotated
import os


from azure.identity import DefaultAzureCredential   
from azure.core.credentials import AzureKeyCredential  
from azure.ai.documentintelligence import DocumentIntelligenceClient  
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import DocumentAnalysisFeature

from modules import config


if config.ADI_KEY:
    credential = AzureKeyCredential(config.ADI_KEY)  
else:
    credential = DefaultAzureCredential()  

adi_client = DocumentIntelligenceClient(endpoint=config.ADI_ENDPOINT, credential=credential)  



class DocumentSearchPlugin:
    @kernel_function(name="get_documentname", description="ユーザーの指定するドキュメントの正式な名前を取得する")
    def get_documentname(self, user_input) -> Annotated[str, "file name"]:
        print("get_documentname関数を利用")
        directory = './doc'  
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]  
                
        return files

    @kernel_function(name="extract_data", description="ファイル名を指定し、Document Intelligenceサービスを利用して該当ファイルのOCR結果を取得する。")
    def extract_data(self, document_name) -> Annotated[str, "Document context"]:
        print("extract_data関数を利用")
        print(f"{document_name}を解析")
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
            
        print(markdown_content)
        return markdown_content


class SearchAgent:  
    def __init__(self, chat_completion_service, prompt, kernel, plugins=[]):  
        self.kernel = kernel    
        self.agent = ChatCompletionAgent(  
        service=chat_completion_service,  
        kernel=kernel,  
        name="SearchAgent",  
        instructions=prompt,  
        plugins=plugins,  
    )  


def set_search_agent(chat_completion_service, prompt, plugin=[]):  
    kernel = Kernel()  
    kernel.add_service(chat_completion_service)
    kernel.add_plugin(DocumentSearchPlugin(),plugin_name="DocumentSearchPlugin")
    agent = SearchAgent(chat_completion_service, prompt, kernel, plugin)  
    return agent
