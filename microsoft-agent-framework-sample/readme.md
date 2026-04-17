Magentic Multi-Agent Sample
=======

Agent Framework を利用した マルチエージェント構成のサンプルアプリケーションです。
Streamlit を UI として利用し、複数のエージェントが協調してユーザーの質問に回答します。

このサンプルでは 都道府県の農林水産業・名産品情報を題材に、

 - ドキュメント検索
 - OCR解析
 - 検索結果評価
 - マルチエージェントオーケストレーション

を組み合わせた AI アプリケーションを実装しています。

<br>

# System Architecture
本システムは Manager + Worker エージェント構成です。

```
                ┌──────────────┐  
                │     User     │  
                └──────┬───────┘  
                       │  
                       ▼  
            ┌────────────────────┐  
            │   ManagerAgent     │  
            │   (Triage Agent)   │  
            │   タスク管理        │  
            └─────────┬──────────┘  
                      │  
        ┌─────────────┴─────────────┐  
        │                           │  
        ▼                           ▼  
 ┌───────────────┐           ┌───────────────┐  
 │  SearchAgent  │           │ EvaluateAgent │  
 │ ドキュメント検索│           │ 検索結果評価   │  
 │ OCR解析        │           │ 妥当性チェック │  
 └───────┬────────┘           └───────┬───────┘  
         │                            │  
         ▼                            ▼  
Azure Document Intelligence     LLM Evaluation  

```
<br><br>

# エージェント構成 
## ManagerAgent
エージェントチームの オーケストレーターです。

### 主な役割

 - ユーザー質問の理解
 - 対象都道府県の特定
 - SearchAgentへの検索依頼
 - valuateAgentへの評価依頼
 - 最終回答生成

## SearchAgent
ドキュメント検索と OCR を担当します。

doc フォルダ内の資料を Azure Document Intelligence で解析し、質問に関連する情報を取得します。

### 使用ツール
- get_documentname() :ドキュメント一覧取得
- search_document(document_name) : OCR解析

## EvaluateAgent
検索結果が ユーザー質問に十分回答できるかを評価します。

### 出力例
 - 問題なし または 問題あり。〇〇の情報が不足しています

<br>

# Sequence Flow
ユーザーの質問から回答生成までの流れ

User  
 │  
 │ 質問  
 ▼  
ManagerAgent  
 │  
 │ 対象都道府県特定  
 ▼  
SearchAgent  
 │  
 │ ドキュメント取得  
 ▼  
Azure Document Intelligence  
 │  
 │ OCR結果  
 ▼  
SearchAgent  
 │  
 │ 回答生成  
 ▼  
EvaluateAgent  
 │  
 │ 評価  
 │  
 ├─ 問題あり → 再検索  
 │  
 └─ 問題なし  
 ▼  
ManagerAgent  
 │  
 │ 最終回答  
 ▼  
User  

<br>

# ディレクトリ構成

.  
├─ app.py  
├─ requirements.txt  
├─ .env  
│  
├─ agent_modules  
│   ├─ triage_agent.py  
│   ├─ search_agent.py  
│   └─ evaluate_agent.py  
│  
├─ modules  
│   ├─ config.py  
│   └─ clients.py  
│  
├─ prompt  
│   ├─ triage_instruction.txt  
│   ├─ search_instruction.txt  
│   └─ evaluate_instruction.txt  
│  
└─ doc  
    └─ OCR対象ドキュメント  

<br>

# 環境変数の設置
.env ファイルに以下を設定します。
##  Azure OpenAI
 - AZURE_OPENAI_ENDPOINT=  
 - AZURE_OPENAI_DEPLOYMENT_NAME=  
 - AZURE_OPENAI_API_VERSION=  
 - AZURE_OPENAI_KEY=  

## Azure Document Intelligence
 - ADI_ENDPOINT=  
 - ADI_KEY=  
 APIキーが無い場合、Azure CLIまたはManaged Identityで認証できます。

<br>

# Setup
## 依存関係インストール
pip install -r requirements.txt  

## Run
streamlit run app.py  

<br>

# 検索仕様
doc フォルダ内のファイルが検索対象になります。

例
doc/  
 ├─ tokyo.pdf  
 ├─ kanagawa.pdf  
 └─ saitama.pdf  

<br>

# このサンプルの範囲
 - Agent Framework の基本構成
 - マルチエージェント設計
 - Manager / Worker パターン
 - LLMツール呼び出し
 - OCR + LLM の統合
 - Streamlit AI アプリ開発

