Multi-Agent AI Sample
===

# Agent Framework / Semantic Kernel Comparison

このプロジェクトは 同じマルチエージェントアプリケーションを2つのフレームワークで実装したサンプルです。

## 目的
 - マルチエージェント設計の理解
 - Agent Framework の使い方
 - Semantic Kernel Agent の使い方
 - 2つのフレームワークの違いの理解

サンプルアプリでは 都道府県の農林水産業・名産品情報を題材にしています。

ユーザーの質問に対して
 - 都道府県特定
 - ドキュメント検索
 - OCR解析
 - 検索結果評価
を行い回答を生成します。

<br>

# Repository Structure
multi-agent-sample    
├─ agent-framework-sample  
└─ semantic-kernel-sample  

両方とも 同じディレクトリ構造で実装されています。

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

<br>

# System Architecture
両サンプルとも Manager + Worker エージェント構成です。

```
                User  
                 │  
                 ▼  
           Manager Agent  
            (Triage)  
                 │  
        ┌────────┴────────┐  
        │                 │  
        ▼                 ▼  
   SearchAgent      EvaluateAgent  
        │  
        ▼  
Document Intelligence 
```


# Agent Framework vs Semantic Kernel

## Architecture Comparison
同じマルチエージェントアプリケーションを2つのフレームワークで実装した場合の構造の違い

### Agent Framework Architecture
Agent Framework は
エージェント同士のオーケストレーションを中心とした構造です。

```
                User  
                 │  
                 ▼  
        ┌─────────────────┐  
        │   ManagerAgent  │  
        │   (Triage)      │  
        │  タスク管理      │  
        └────────┬────────┘  
                 │  
        ┌────────┴────────┐  
        │                 │  
        ▼                 ▼  
   SearchAgent       EvaluateAgent  
        │  
        ▼  
 Document Intelligence  
```

### 特徴

 - Manager Agent がワークフローを管理
 - エージェント同士が直接連携
 - マルチエージェント orchestration が得意

## Semantic Kernel Architecture
Semantic Kernel は
Kernel + Plugin 中心の構造です。

```
                User  
                 │  
                 ▼  
        ┌─────────────────┐  
        │   TriageAgent   │  
        │                 │  
        └────────┬────────┘  
                 │  
           ┌─────┴─────┐  
           │  Kernel   │  
           └─────┬─────┘  
                 │  
        ┌────────┴────────┐  
        │                 │  
        ▼                 ▼  
   SearchAgent       EvaluateAgent  
        │  
        ▼  
   DocumentSearchPlugin  
        │  
        ▼  
 Document Intelligence  
```

### 特徴

 - Kernel が中心
 - 機能は Plugin として実装
 - ツール統合がしやすい

## Conceptual Difference
### Agent Framework

Agent  
 ├─ Agent  
 └─ Agent  

### Semantic Kernel

Kernel  
 ├─ Agent  
 └─ Plugin(Function)  

## Implementation Differences
### Agent Framework

エージェント同士が直接連携

ManagerAgent  
   ↓  
SearchAgent  
   ↓  
EvaluateAgent  

### Semantic Kernel

Kernel + Plugin 構造

Kernel  
   ↓  
Agent  
   ↓  
Plugin(Function)  

<br>



## When to Use Which
### Agent Framework が向くケース

 - マルチエージェントシステム
 - エージェントオーケストレーション
 - 複雑なワークフロー

### Semantic Kernel が向くケース

 - AIアプリケーション開発
 - ツール統合
 - プラグインベース設計

<br>


# Agent Responsibilities

## TriageAgent

エージェントチームのマネージャー

 - ユーザー質問の理解
 - 対象都道府県の特定
 - SearchAgent 呼び出し
 - EvaluateAgent 呼び出し
 - 最終回答生成

## SearchAgent

検索エージェント

 - ドキュメント検索
 - OCR解析
 - 回答生成

## EvaluateAgent

評価エージェント

 - 検索結果の妥当性判定
 - 不足情報の指摘

<br>




# 利用Azure サービス

### Azure OpenAI
 - LLM推論

### Azure AI Document Intelligence
 - OCR解析

<br>

# Setup
## ライブラリのインストール
各サンプルディレクトリで、
> pip install -r requirements.txt  
## Run
Streamlit アプリを起動

> streamlit run app.py  


## このサンプルの範囲

 - マルチエージェント設計
 - Agent Framework
 - Semantic Kernel
 - LLMツール呼び出し
 - OCR + LLM統合
 - AIアプリ開発

### Why This Sample Matters
同じアプリケーションを 2つのAIフレームワークで実装することで

・設計の違い
・エージェント実装方法
・ツール統合方法

を比較しながら学習できます。


# 出展
本リポジトリのサンプルドキュメントの一部には、農林水産省が公開している資料を使用しています。
これらは公開情報をそのまま参照しており、デモンストレーション目的で利用しています。

農林水産省
https://www.maff.go.jp/


The sample documents used in this project are based on publicly available materials from the Ministry of Agriculture, Forestry and Fisheries (MAFF), Government of Japan.

https://www.maff.go.jp/

The documents are used for demonstration purposes only.