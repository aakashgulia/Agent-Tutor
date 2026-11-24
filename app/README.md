# 🎓 AI Agent Tutor – Intelligent Academic Learning Assistant

An AI-powered academic tutoring assistant built using **Python, Streamlit, Large Language Models (LLMs), and Retrieval-Augmented Generation (RAG)**. The system helps students understand course concepts, interact with academic materials, maintain class reflections, and stay updated with industry collaboration news.

Designed to provide context-aware academic assistance using a curated knowledge base rather than relying entirely on generic LLM responses.

---

## 🚀 Project Overview

AI Agent Tutor is an intelligent learning platform developed to make academic learning more interactive, accessible, and personalized.

The application combines Large Language Models with document-based knowledge retrieval to generate responses grounded in relevant academic resources.

It also provides additional modules for reflection tracking, collaboration news, and prompt activity monitoring.

## ✨ Key Features

### 1. 🤖 AI-Powered Tutor Chat
- Interactive conversational interface for students.
- Answers questions related to course concepts.
- Uses retrieved academic context to improve response relevance.
- Supports natural-language queries.

### 2. 📚 Retrieval-Augmented Generation (RAG)
- Retrieves relevant information from uploaded academic resources.
- Uses a curated course knowledge base.
- Combines document retrieval with LLM-based response generation.
- Helps provide context-aware answers grounded in learning materials.

### 3. 📝 Class Reflection
- Dedicated section for recording class reflections.
- Helps students document their learning and insights.
- Encourages continuous academic engagement.

### 4. 📰 Fortnightly Collaboration News
- Dedicated section for fortnightly collaboration updates.
- Provides information relevant to corporate-startup collaborations.
- Connects classroom learning with real-world innovation.

### 5. 📋 Prompt Activity Log
- Maintains a visible record of prompts.
- Supports tracking and reviewing user interactions.
- Improves transparency in AI-assisted learning.

### 6. 🔄 Dynamic Knowledge Base
- Organizes academic learning resources.
- Supports adding course-related documents.
- Makes the tutoring system adaptable to evolving learning materials.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | Interactive web interface |
| Large Language Models | AI-powered response generation |
| Ollama | Local LLM execution |
| Retrieval-Augmented Generation (RAG) | Context-aware information retrieval |
| Vector-based Retrieval | Relevant document retrieval |
| Cloudflare Tunnel | Remote application access |

## 🧠 Knowledge Base

The initial knowledge base includes academic resources such as:

- Course Handout
- Open Innovation Presentation
- Harvard Business Review – *Big Companies Should Collaborate with Startups*

These resources provide the academic context used by the RAG pipeline.

## 🏗️ System Architecture

The application follows a retrieval-augmented AI architecture:

1. **User Query:** Student submits a question through the Streamlit interface.
2. **Query Processing:** The question is processed for relevant information retrieval.
3. **Knowledge Retrieval:** Relevant document chunks are retrieved from the knowledge base.
4. **Context Integration:** Retrieved information is supplied to the language model.
5. **Response Generation:** The LLM generates a context-aware answer.
6. **User Interaction:** The response is displayed through the chatbot interface.

## 📂 Application Modules

| Module | Description |
|---|---|
| Chat | AI-powered academic tutoring |
| Class Reflection | Student learning reflections |
| Fortnightly News | Corporate-startup collaboration updates |
| Prompt Log | Prompt activity tracking |
| Knowledge Base | Academic document management |

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- Ollama installed
- Git
- Required Python dependencies

### Step 1: Clone the repository

```bash
git clone https://github.com/aakasok/AI-Agent-Tutor.git
```

### Step 2: Navigate to the project directory

```bash
cd AI-Agent-Tutor
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Ollama

Install Ollama and ensure the required language model is available locally.

```bash
ollama list
```

If your configured model is not installed, download it using:

```bash
ollama pull phi3
```

Use the same model configuration as the application.

### Step 7: Run the application

```bash
streamlit run app.py
```

Replace `app.py` with the actual Streamlit entry-point filename if different.

---

## 🎯 Project Objectives

- Demonstrate practical implementation of AI agents in education.
- Apply RAG for document-grounded question answering.
- Integrate locally running LLMs into an interactive application.
- Improve accessibility of academic learning resources.
- Maintain transparency through prompt activity logging.
- Connect theoretical academic concepts with real-world industry developments.

## 🔮 Future Enhancements

- Multi-agent academic tutoring architecture.
- Student-specific learning progress analytics.
- Automated quiz and assessment generation.
- Multi-user authentication and role-based access.
- Advanced document processing and knowledge-base management.
- Conversation memory and personalized learning recommendations.

## 👨‍💻 Developer

**Aakash Gulia**

B.Tech – Computer Science and Engineering  
Artificial Intelligence & Data Science

Interested in Artificial Intelligence, LLMs, RAG Systems, AI Agents, and intelligent application development.

---

⭐ If you find this project interesting, consider giving the repository a star!

**Built with Python, AI, and a vision for smarter learning.**