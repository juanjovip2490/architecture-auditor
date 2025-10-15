import os
import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ProjectDocumentationGenerator:
    def __init__(self, notion_token):
        self.headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
    
    def create_architecture_doc(self, parent_page_id, project_name):
        """Create comprehensive project documentation"""
        doc_data = {
            "parent": {"page_id": parent_page_id},
            "properties": {"title": {"title": [{"text": {"content": f"{project_name} - Architecture & Documentation"}}]}},
            "children": [
                {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": f"{project_name} Project Documentation"}}]}},
                
                # Business Overview
                {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "📊 Business Overview"}}]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Project objectives, stakeholders, and business value proposition."}}]}},
                
                # Architecture Patterns
                {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🏗️ Architecture Patterns"}}]}},
                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "MVC/MVP/MVVM Pattern Implementation"}}]}},
                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Dependency Injection & IoC Container"}}]}},
                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Repository Pattern for Data Access"}}]}},
                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Observer Pattern for Event Handling"}}]}},
                
                # Folder Structure
                {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "📁 Project Structure"}}]}},
                {"object": "block", "type": "code", "code": {"language": "plain_text", "rich_text": [{"text": {"content": self.generate_folder_structure()}}]}},
                
                # Technical Stack
                {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "⚙️ Technical Stack"}}]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Frontend: React/Vue/Angular | Backend: Node.js/Python/Java | Database: PostgreSQL/MongoDB"}}]}},
                
                # Setup Instructions
                {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🚀 Quick Start"}}]}},
                {"object": "block", "type": "code", "code": {"language": "bash", "rich_text": [{"text": {"content": "git clone <repository>\ncd project\nnpm install\nnpm start"}}]}},
                
                # GitHub Integration
                {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔗 GitHub Integration"}}]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Repository: [GitHub Link] | CI/CD: GitHub Actions | Documentation: Auto-sync with Notion"}}]}}
            ]
        }
        
        response = requests.post("https://api.notion.com/v1/pages", headers=self.headers, json=doc_data, verify=False)
        return response.status_code == 200
    
    def generate_folder_structure(self):
        return """project/
├── src/
│   ├── components/     # Reusable UI components
│   ├── services/       # Business logic & API calls
│   ├── models/         # Data models & interfaces
│   ├── utils/          # Helper functions
│   └── config/         # Configuration files
├── tests/
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── e2e/           # End-to-end tests
├── docs/
│   ├── api/           # API documentation
│   ├── architecture/  # Architecture diagrams
│   └── deployment/    # Deployment guides
├── scripts/           # Build & deployment scripts
├── .github/
│   └── workflows/     # GitHub Actions
├── README.md          # Project overview
├── CONTRIBUTING.md    # Contribution guidelines
└── package.json       # Dependencies & scripts"""

# Usage
generator = ProjectDocumentationGenerator("ntn_H41399030117na79uOCJOgncxVbnqHlSUlzePEjflswe3U")

# Find Analista page and create documentation
search = requests.post("https://api.notion.com/v1/search", 
    headers=generator.headers, 
    json={"query": "Analista"}, 
    verify=False)

if search.status_code == 200:
    results = search.json().get("results", [])
    analista_page = next((p for p in results if "analista" in str(p).lower()), None)
    
    if analista_page:
        success = generator.create_architecture_doc(analista_page["id"], "Sample Project")
        print("Documentation created successfully!" if success else "Failed to create documentation")
    else:
        print("Analista page not found")
else:
    print(f"Search failed: {search.text}")