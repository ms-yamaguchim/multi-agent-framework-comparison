# modules/config.py  
import os  
from dotenv import load_dotenv  
  
# .env読み込み（プロジェクトルートに配置）  
load_dotenv()  


# Azure OpenAI  
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")  
AOAI_MODEL_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")  
AOAI_KEY = os.getenv("AZURE_OPENAI_KEY")  # 無ければManaged ID  
  
# Azure AI Document Intelligence
ADI_ENDPOINT = os.getenv("ADI_ENDPOINT")
ADI_KEY = os.getenv("ADI_KEY")  # 無ければManaged ID  

  
# 実行時に不足している環境変数があれば警告  
_required_vars = {  
    "AOAI_ENDPOINT": AOAI_ENDPOINT,  
    "AOAI_MODEL_NAME": AOAI_MODEL_NAME  
}  
  
_missing = [name for name, value in _required_vars.items() if not value]  
if _missing:  
    print(f"[config.py] ⚠️ 必須環境変数が設定されていません: {', '.join(_missing)}") 