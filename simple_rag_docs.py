import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "Authorization": "Bearer ntn_H41399030117na79uOCJOgncxVbnqHlSUlzePEjflswe3U",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Find Analista page
search = requests.post("https://api.notion.com/v1/search", headers=headers, json={"query": "Analista"}, verify=False)
analista_page = next((p for p in search.json()["results"] if "analista" in str(p).lower()), None)

if analista_page:
    # Create RAG documentation
    doc = {
        "parent": {"page_id": analista_page["id"]},
        "properties": {"title": {"title": [{"text": {"content": "RAG Chatbot - Architecture Documentation"}}]}},
        "children": [
            {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "🤖 RAG Chatbot Application"}}]}},
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "📊 Business Overview"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "AI-powered document Q&A system using RAG (Retrieval-Augmented Generation). Upload PDFs and chat with intelligent responses based on document content."}}]}},
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🏗️ Architecture"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Backend: FastAPI + Python 3.10"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "AI: OpenAI GPT-4o-mini + LangChain"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Vector DB: ChromaDB"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Frontend: HTML/CSS/JS + WebSocket"}}]}},
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🚀 Quick Start"}}]}},
            {"object": "block", "type": "code", "code": {"language": "bash", "rich_text": [{"text": {"content": "git clone https://github.com/jodog0412/rag-chatbot-app-with-fastapi.git\ncd rag-chatbot-app-with-fastapi\npip install -r requirements.txt\ncd app\nuvicorn main:app --reload"}}]}},
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔗 Repository"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "https://github.com/jodog0412/rag-chatbot-app-with-fastapi.git"}}]}}
        ]
    }
    
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=doc, verify=False)
    print("Documentation created!" if response.status_code == 200 else f"Error: {response.text}")
else:
    print("Analista page not found")