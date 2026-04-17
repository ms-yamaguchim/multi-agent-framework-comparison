Semantic Kernel Multi-Agent Sample
===
Semantic Kernel を利用した マルチエージェント構成のサンプルアプリケーションです。
Streamlit を UI として利用し、複数エージェントが協調してユーザーの質問に回答します。

このサンプルでは 都道府県の農林水産業・名産品情報を題材に、

 - ドキュメント検索
 - OCR解析
 - 検索結果評価
 - マルチエージェント連携

を実装しています。

Azure OpenAI と Azure Document Intelligence を組み合わせたSemantic Kernel Agent の実装例です。

<br>

# System Architecture
本システムは Triage Agent を中心としたマルチエージェント構成です。

```
                ┌──────────────┐  
                │     User     │  
                └──────┬───────┘  
                       │  
                       ▼  
            ┌────────────────────┐  
            │    TriageAgent     │  
            │   (Manager Agent)  │  
            │   タスク管理        │  
            └─────────┬──────────┘  
                      │  
        ┌─────────────┴─────────────┐  
        │                           │  
        ▼                           ▼  
 ┌───────────────┐           ┌───────────────┐  
 │  SearchAgent  │           │ EvaluateAgent │  
 │ OCR + 検索     │           │ 検索結果評価   │  
 └───────┬────────┘           └───────────────┘  
         │  
         ▼  
 Azure Document Intelligence  
```

# エージェント構成 
## TriageAgent
エージェントチームの マネージャーエージェントです。

### 主な役割

 - ユーザー質問の理解
 - 対象都道府県の特定
 - SearchAgentへの検索依頼
 - valuateAgentへの評価依頼
 - 最終回答生成

### 利用プラグイン

 - LocationPlugin:現在地（都道府県）を取得
 - TimePlugin: 現在時刻取得
 - ConversationSummaryPlugin:会話履歴要約

## SearchAgent
ドキュメント検索と OCR を担当するエージェントです。

doc フォルダ内の資料を Azure Document Intelligence で解析し、質問に関連する情報を取得します。

### 利用プラグイン

 - DocumentSearchPlugin

#### 提供機能

 - get_documentname :ドキュメント一覧取得
 - extract_data :Document Intelligence を利用した OCR 解析

#### 使用モデル
 - prebuilt-layout :高解像度OCR
 - OCR_HIGH_RESOLUTION  

## EvaluateAgent
検索結果の妥当性を評価するエージェントです。

### 主な役割

 - 検索結果がユーザー質問に対して十分か判定
 - 不足情報の指摘
 - 再検索の必要性判断

### 出力
問題なし または 問題あり。〇〇の取得が必要です

<br>

# Sequence Flow
ユーザー質問から回答生成までの流れ

User  
 │  
 │ 質問  
 ▼  
TriageAgent  
 │  
 │ 対象都道府県特定  
 ▼  
SearchAgent  
 │  
 │ ドキュメント取得  
 ▼  
Document Intelligence  
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
TriageAgent  
 │  
 │ 最終回答生成  
 ▼  
User  


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
│   └─ config.py  
│  
├─ prompt  
│   ├─ triage_instruction.txt  
│   ├─ search_instruction.txt  
│   └─ evaluate_instruction.txt  
│  
└─ doc  
    └─ OCR対象ドキュメント 

# 環境変数の設定
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

# 検索仕様
doc フォルダ内のファイルが検索対象になります。

例
doc/  
 ├─ tokyo.pdf  
 ├─ kanagawa.pdf  
 └─ saitama.pdf  

<br>

# このサンプルの範囲
 - Semantic Kernel Agent の基本構成
 - Plugin ベースのツール実装
 - マルチエージェント設計
 - Azure OpenAI 連携
 - Document Intelligence OCR 連携
 - Streamlit AI アプリ開発
