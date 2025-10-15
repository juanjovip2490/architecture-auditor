import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "Authorization": "Bearer ntn_H41399030117na79uOCJOgncxVbnqHlSUlzePEjflswe3U",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_rag_documentation(parent_page_id):
    doc_data = {
        "parent": {"page_id": parent_page_id},
        "properties": {"title": {"title": [{"text": {"content": "RAG Chatbot - Complete Architecture Documentation"}}]}},
        "children": [
            {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "🤖 RAG Chatbot Application"}}]}},
            
            # Business Overview
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "📊 Business Overview"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Intelligent document-based Q&A system using Retrieval-Augmented Generation (RAG). Users upload PDF documents and interact with an AI chatbot that provides accurate answers based on document content."}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Business Value: Automated document analysis and instant Q&A"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Target Users: Knowledge workers, researchers, customer support"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "ROI: Reduces manual document review time by 80%"}}]}},
            
            # Architecture Patterns
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🏗️ Architecture Patterns"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "RAG Pattern: Retrieval-Augmented Generation for context-aware responses"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "MVC Pattern: FastAPI (Controller), LangChain (Model), Jinja2 (View)"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Repository Pattern: ChromaDB for vector storage and retrieval"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Chain of Responsibility: LangChain pipeline processing"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "WebSocket Pattern: Real-time chat communication"}}]}},
            
            # Technical Stack
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "⚙️ Technical Stack"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Backend: FastAPI + Python 3.10 | AI: OpenAI GPT-4o-mini + LangChain | Vector DB: ChromaDB | Frontend: HTML/CSS/JS | Deployment: Docker"}}]}},
            
            # Project Structure
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "📁 Project Structure"}}]}},
            {"object": "block", "type": "code", "code": {"language": "plain_text", "rich_text": [{"text": {"content": """rag-chatbot-app-with-fastapi/
├── app/
│   ├── main.py          # FastAPI application & WebSocket endpoints
│   ├── utils.py         # RAG utility functions & LangChain chains
│   └── .env            # OpenAI API key configuration
├── db/                 # ChromaDB vector database storage
├── documents/          # Uploaded PDF files storage
├── static/
│   ├── chatting.css    # Chat interface styling
│   ├── main.css        # Main page styling
│   └── dog.png         # Application logo
├── templates/
│   ├── index.html      # File upload interface
│   └── chatting.html   # Chat interface
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation"""}}]}},
            
            # Core Components
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔧 Core Components"}}]}},
            {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "1. Document Processing Pipeline"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "PDF Upload → PyPDFLoader → RecursiveCharacterTextSplitter → ChromaDB"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Chunk Size: 1000 characters, Overlap: 200 characters"}}]}},
            
            {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "2. RAG Chain Architecture"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "History-Aware Retriever: Contextualizes questions with chat history"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "QA Chain: Generates concise answers from retrieved context"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Conversational Memory: Maintains session-based chat history"}}]}},
            
            # API Endpoints
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🌐 API Endpoints"}}]}},
            {"object": "block", "type": "code", "code": {"language": "http", "rich_text": [{"text": {"content": """GET  /              # Home page with file upload
POST /              # Upload PDF file
GET  /chatting      # Chat interface
WS   /chatting      # WebSocket for real-time chat"""}}]}},
            
            # Setup Instructions
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🚀 Setup & Deployment"}}]}},
            {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "Local Development"}}]}},
            {"object": "block", "type": "code", "code": {"language": "bash", "rich_text": [{"text": {"content": """git clone https://github.com/jodog0412/rag-chatbot-app-with-fastapi.git
cd rag-chatbot-app-with-fastapi
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
# Create app/.env with OPENAI_API_KEY
cd app
uvicorn main:app --reload"""}}]}},
            
            {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "Docker Deployment"}}]}},
            {"object": "block", "type": "code", "code": {"language": "bash", "rich_text": [{"text": {"content": """docker build -t rag-chatbot .
docker run -d -p 8000:8000 --name rag-chatbot-container rag-chatbot"""}}]}},
            
            # Security & Performance
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔒 Security & Performance"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "API Key Security: Environment variables for OpenAI credentials"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "File Validation: PDF-only upload restriction"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Memory Management: Session-based chat history storage"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Performance: Background tasks for document processing"}}]}},
            
            # Future Enhancements
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔮 Roadmap & Enhancements"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "✅ History-aware RAG implementation"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "✅ WebSocket real-time communication"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "🔄 Bug fixes for deployment issues"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "🔄 Local LLM support (currently GPT-only)"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "📋 Multi-format document support"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "📋 User authentication & multi-tenancy"}}]}},
            
            # GitHub Integration
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔗 Repository Information"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Repository: https://github.com/jodog0412/rag-chatbot-app-with-fastapi.git"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "License: Open Source | Contributors: @jodog0412 | Based on: @AshishSinha5's rag_api"}}]}}
        ]
    }
    
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=doc_data, verify=False)
    return response.status_code == 200

# Find Analista page and create documentation
search = requests.post("https://api.notion.com/v1/search", headers=headers, json={"query": "Analista"}, verify=False)

if search.status_code == 200:
    results = search.json().get("results", [])
    analista_page = next((p for p in results if "analista" in str(p).lower()), None)
    
    if analista_page:
        success = create_rag_documentation(analista_page["id"])
        print("RAG Chatbot documentation created successfully!" if success else "Failed to create documentation")
    else:
        print("Analista page not found")
else:
    print(f"Search failed: {search.text}")