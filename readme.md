# Multi-Agent AI Sample
===
🌐 Language

English | [日本語](README_ja.md)


## Agent Framework vs Semantic Kernel

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-blue)
![Azure AI](https://img.shields.io/badge/Azure-Document%20Intelligence-blue)
![Framework](https://img.shields.io/badge/AI-Multi--Agent-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

This repository provides a comparison between Microsoft Agent Framework and Semantic Kernel for building multi-agent AI applications.

The sample demonstrates how multiple AI agents collaborate to process documents using Azure OpenAI and Azure AI Document Intelligence.
# Quick Start
Install dependencies in each sample directory.
> pip install -r requirements.txt

Run the Streamlit application.
> streamlit run app.py

# Project Structure
multi-agent-sample
├─ agent-framework-sample
└─ semantic-kernel-sample

Both implementations follow the same directory structure.

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
    └─ OCR target documents  

# System Architecture
Both implementations follow a Manager + Worker agent architecture.

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

<br>

# Agent Framework vs Semantic Kernel
## Architecture Comparison
The same multi-agent system is implemented using two frameworks to compare their design approaches.

### Agent Framework Architecture
Agent Framework focuses on agent orchestration.

```
                User  
                 │  
                 ▼  
        ┌─────────────────┐  
        │   ManagerAgent  │  
        │   (Triage)      │  
        │  Task Control   │  
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

#### Characteristics
 - Manager agent controls workflow
 - Agents communicate directly
 - Strong for multi-agent orchestration

<br>

### Semantic Kernel Architecture
Semantic Kernel is built around Kernel + Plugins.

```
                User  
                 │  
                 ▼  
        ┌─────────────────┐  
        │   TriageAgent   │  
        └────────┬────────┘  
                 │  
           ┌─────┴─────┐  
           │   Kernel  │  
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

#### Characteristics
 - Kernel-centric architecture
 - Features implemented as plugins
 - Easy tool integration

## Conceptual Difference
### Agent Framework
Agent  
 ├─ Agent  
 └─ Agent  

###Semantic Kernel
Kernel  
 ├─ Agent  
 └─ Plugin (Function)
 
# Agent Responsibilities
## TriageAgent
Manager of the agent team.
### Responsibilities
 - Understand user questions
 - Identify the target prefecture
 - Call SearchAgent
 - Call EvaluateAgent
 -  Generate the final answer

## SearchAgent
Responsible for document search and analysis.
### Responsibilities
 - Document search
 - OCR processing
 - Generate candidate answers

## EvaluateAgent
Responsible for result validation.
### Responsibilities
 - Evaluate answer quality
 - Identify missing information

# Azure Services Used
## Azure OpenAI
LLM inference
## Azure AI Document Intelligence
OCR document processing

# What This Sample Demonstrates
 - Multi-agent system design
 - Microsoft Agent Framework
 - Semantic Kernel agents
 - Tool calling with LLMs
 - OCR + LLM integration
 - AI application architecture comparison

# Why This Sample Matters
By implementing the same application with two AI frameworks, this repository highlights:
 - architectural differences
 - agent implementation approaches
 - tool integration patterns
 - This helps developers understand how different frameworks approach multi-agent AI systems.

# Data Source
Some sample documents are based on publicly available materials from the Ministry of Agriculture, Forestry and Fisheries (MAFF), Japan.

https://www.maff.go.jp/

These materials are used for demonstration purposes.