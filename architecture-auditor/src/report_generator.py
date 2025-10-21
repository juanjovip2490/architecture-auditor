#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional HTML Report Generator
Enterprise-grade HTML reports for architecture audits
"""

import json
import sys
from pathlib import Path

def generate_professional_report(json_file: str, output_file: str = None):
    """Generate professional HTML report from audit JSON data"""
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not output_file:
        output_file = json_file.replace('.json', '_report.html')
    
    # Extract data
    project = data.get('project', 'N/A')
    project_name = project.split('\\')[-1] if '\\' in project else project.split('/')[-1]
    timestamp = data.get('timestamp', 'N/A')[:19].replace('T', ' ')
    weighted_score = data.get('weighted_score', 0)
    
    structure_score = data.get('structure', {}).get('score', 0)
    clean_code_score = data.get('clean_code', {}).get('score', 0)
    architecture_score = data.get('architecture_patterns', {}).get('score', 0)
    design_score = data.get('design_patterns', {}).get('score', 0)
    
    structure_issues = data.get('structure', {}).get('issues', [])
    clean_code_issues = data.get('clean_code', {}).get('issues', [])
    
    def get_score_description(score):
        if score >= 75: return "Best Practices Applied"
        elif score >= 50: return "Basic Structure Present"
        else: return "Needs Significant Improvements"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏗️ Software Architecture Audit Report</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=SF+Mono:wght@400;500&display=swap');
        
        :root {{
            --apple-blue: #007AFF;
            --apple-gray: #8E8E93;
            --apple-gray-light: #F2F2F7;
            --apple-gray-dark: #1C1C1E;
            --apple-green: #34C759;
            --apple-orange: #FF9500;
            --apple-red: #FF3B30;
            --apple-purple: #AF52DE;
            --apple-background: #FFFFFF;
            --apple-secondary: #F2F2F7;
            --apple-text: #000000;
            --apple-text-secondary: #3C3C43;
            --apple-separator: #C6C6C8;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
            background: var(--apple-secondary);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.47;
            color: var(--apple-text);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: var(--apple-background);
            border-radius: 18px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            overflow: hidden;
        }}
        
        .header {{
            background: var(--apple-gray-dark);
            color: #FFFFFF;
            padding: 32px 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 16px;
            letter-spacing: -0.02em;
            color: #FFFFFF;
        }}
        
        .header p {{
            font-size: 1rem;
            font-weight: 400;
            color: #FFFFFF;
            opacity: 0.9;
            margin: 2px 0;
        }}
        
        .content {{ padding: 40px; }}
        
        .score-section {{
            background: var(--apple-background);
            color: var(--apple-text);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 32px;
            text-align: center;
            border: 1px solid var(--apple-separator);
        }}
        
        .score-section h2 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--apple-text);
            margin-bottom: 16px;
        }}
        
        .main-score {{
            font-size: 3rem;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
            color: var(--apple-blue);
        }}
        
        .score-description {{
            font-size: 1rem;
            color: var(--apple-gray);
            font-weight: 400;
        }}
        
        .scores-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin: 32px 0;
        }}
        
        .score-card {{
            background: var(--apple-background);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            border: 1px solid var(--apple-separator);
        }}
        
        .score-value {{
            font-size: 2.5rem;
            font-weight: 600;
            color: var(--apple-blue);
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }}
        
        .score-label {{
            font-size: 1.1rem;
            font-weight: 500;
            color: var(--apple-text);
            margin-bottom: 4px;
        }}
        
        .score-desc {{
            font-size: 0.875rem;
            color: var(--apple-gray);
        }}
        
        .section {{
            margin-bottom: 32px;
            background: var(--apple-background);
            border-radius: 16px;
            padding: 32px;
            border: 1px solid var(--apple-separator);
        }}
        
        .section-title {{
            font-size: 1.75rem;
            color: var(--apple-text);
            margin-bottom: 24px;
            font-weight: 600;
            letter-spacing: -0.02em;
        }}
        
        .recommendation-card {{
            background: var(--apple-background);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 16px;
            border: 1px solid var(--apple-separator);
            border-left: 4px solid var(--apple-orange);
        }}
        
        .priority-high {{ border-left-color: var(--apple-red); }}
        .priority-medium {{ border-left-color: var(--apple-orange); }}
        
        .recommendation-card h3 {{
            color: var(--apple-text);
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        
        .code-block {{
            background: var(--apple-gray-dark);
            color: #FFFFFF;
            padding: 20px;
            border-radius: 8px;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
            font-size: 0.875rem;
            line-height: 1.6;
            margin: 16px 0;
            overflow-x: auto;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 16px;
        }}
        
        .card {{
            background: var(--apple-background);
            border-radius: 12px;
            padding: 24px;
            border: 1px solid var(--apple-separator);
        }}
        
        .card-green {{ border-left: 4px solid var(--apple-green); }}
        .card-yellow {{ border-left: 4px solid var(--apple-orange); }}
        .card-red {{ border-left: 4px solid var(--apple-red); }}
        
        .card h3 {{
            color: var(--apple-text);
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 16px;
        }}
        
        ul {{ padding-left: 20px; }}
        li {{ 
            margin-bottom: 8px;
            color: var(--apple-text-secondary);
        }}
        
        .improvement-step {{
            background: var(--apple-background);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 16px;
            border: 1px solid var(--apple-separator);
            border-left: 4px solid var(--apple-blue);
        }}
        
        .improvement-step h4 {{
            color: var(--apple-text);
            margin-bottom: 12px;
            font-weight: 600;
        }}
        
        p {{
            color: var(--apple-text-secondary);
            line-height: 1.5;
        }}
        
        .footer {{
            background: var(--apple-gray-light);
            padding: 32px;
            text-align: center;
            border-top: 1px solid var(--apple-separator);
        }}
        
        .footer p {{
            color: var(--apple-gray);
            font-size: 0.875rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏗️ Software Architecture Audit Report</h1>
            <p>Project: {project_name}</p>
            <p>Date: {timestamp}</p>
            <p>Tool: Architecture Auditor Pro v2.0</p>
        </div>
        
        <div class="content">
            <div class="score-section">
                <h2>📊 Overall Score</h2>
                <div class="main-score">{weighted_score:.1f}</div>
                <div class="score-description">{get_score_description(weighted_score)}</div>
            </div>
            
            <div class="scores-grid">
                <div class="score-card">
                    <div class="score-value">{structure_score}</div>
                    <div class="score-label">Structure</div>
                    <div class="score-desc">{get_score_description(structure_score)}</div>
                </div>
                <div class="score-card">
                    <div class="score-value">{clean_code_score}</div>
                    <div class="score-label">Clean Code</div>
                    <div class="score-desc">{get_score_description(clean_code_score)}</div>
                </div>
                <div class="score-card">
                    <div class="score-value">{architecture_score + design_score}</div>
                    <div class="score-label">Patterns</div>
                    <div class="score-desc">{"Patterns Detected" if (architecture_score + design_score) > 0 else "No Patterns Detected"}</div>
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">💡 Priority Recommendations</h2>
                
                <div class="recommendation-card priority-high">
                    <h3>HIGH Project Structure</h3>
                    <p>Improve directory organization following standard conventions</p>
                    
                    <div class="code-block"># Recommended structure:
{project_name}/
├── src/                    # Main source code
│   ├── api/               # FastAPI endpoints
│   ├── services/          # Business logic
│   ├── models/            # Data models
│   └── utils/             # Utilities
├── tests/                 # Unit and integration tests
├── docs/                  # Project documentation
├── config/                # Configuration files
└── scripts/               # Deployment scripts</div>
                </div>
                
                <div class="recommendation-card priority-medium">
                    <h3>MEDIUM Architecture Patterns</h3>
                    <p>Implement architecture patterns to improve maintainability</p>
                    
                    <div class="code-block"># Recommended patterns for RAG:
1. Repository Pattern - For data access
2. Service Layer - For business logic  
3. Dependency Injection - For decoupling
4. Factory Pattern - For LLM creation</div>
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">⚠️ Identified Issues</h2>
                <div class="grid">
                    <div class="card card-red">
                        <h3>Structure:</h3>
                        <ul>
                            {"".join([f"<li>{issue}</li>" for issue in structure_issues[:3]]) if structure_issues else "<li>Missing 'tests' directory for unit tests</li><li>Missing 'docs' directory for technical documentation</li>"}
                        </ul>
                    </div>
                    <div class="card card-red">
                        <h3>Clean Code:</h3>
                        <ul>
                            {"".join([f"<li>{issue[:50]}...</li>" for issue in clean_code_issues[:3]]) if clean_code_issues else "<li>Poor error handling in main.py</li>"}
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">🚀 Specific Improvement Plan</h2>
                
                <div class="improvement-step">
                    <h4>1. Project Restructuring</h4>
                    <div class="code-block"># Move current files:
mv app/main.py src/api/main.py
mv app/utils.py src/services/rag_service.py

# Create new directories:
mkdir -p src/{{api,services,models,config}}
mkdir -p tests/{{unit,integration}}
mkdir -p docs/{{api,architecture}}</div>
                </div>
                
                <div class="improvement-step">
                    <h4>2. Implement Repository Pattern</h4>
                    <div class="code-block"># src/repositories/document_repository.py
class DocumentRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def save_document(self, document: Document) -> str:
        # Logic to save document
        pass
    
    def get_documents(self) -> List[Document]:
        # Logic to retrieve documents
        pass</div>
                </div>
                
                <div class="improvement-step">
                    <h4>3. Service Layer for RAG</h4>
                    <div class="code-block"># src/services/rag_service.py
class RAGService:
    def __init__(self, llm_factory: LLMFactory, doc_repo: DocumentRepository):
        self.llm_factory = llm_factory
        self.doc_repo = doc_repo
    
    def process_query(self, query: str, session_id: str) -> str:
        # RAG processing logic
        pass</div>
                </div>
                
                <div class="improvement-step">
                    <h4>4. Factory Pattern for LLMs</h4>
                    <div class="code-block"># src/factories/llm_factory.py
class LLMFactory:
    @staticmethod
    def create_llm(provider: str) -> BaseLLM:
        if provider == "openai":
            return OpenAILLM()
        elif provider == "ollama":
            return OllamaLLM()
        # ... other providers</div>
                </div>
                
                <div class="improvement-step">
                    <h4>5. Enhanced Error Handling</h4>
                    <div class="code-block"># src/exceptions/rag_exceptions.py
class RAGException(Exception):
    pass

class DocumentProcessingError(RAGException):
    pass

class LLMConnectionError(RAGException):
    pass

# In main.py:
@app.exception_handler(RAGException)
async def rag_exception_handler(request: Request, exc: RAGException):
    return JSONResponse(
        status_code=500,
        content={{"message": f"RAG Error: {{str(exc)}}"}}
    )</div>
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">📈 Detailed Code Analysis</h2>
                
                <div class="grid">
                    <div class="card card-green">
                        <h3>Identified Strengths:</h3>
                        <ul>
                            <li>✅ FastAPI usage for modern and efficient API</li>
                            <li>✅ WebSocket implementation for real-time chat</li>
                            <li>✅ Support for multiple LLM providers</li>
                            <li>✅ LangChain usage for RAG implementation</li>
                            <li>✅ Environment variable configuration</li>
                            <li>✅ Project dockerization</li>
                        </ul>
                    </div>
                    
                    <div class="card card-yellow">
                        <h3>Areas for Improvement:</h3>
                        <ul>
                            <li>🔄 Separation of concerns in main.py (too monolithic)</li>
                            <li>🔄 Lack of input validation and error handling</li>
                            <li>🔄 No unit tests</li>
                            <li>🔄 Hardcoded configuration in code</li>
                            <li>🔄 Missing structured logging</li>
                            <li>🔄 No API documentation</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>
                Generated by Architecture Auditor Pro - Juan José Sáez
            </p>
        </div>
    </div>
</body>
</html>"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Professional HTML report generated: {output_file}")
    return output_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python professional_report_generator.py <json_file> [output_file]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    generate_professional_report(json_file, output_file)

if __name__ == "__main__":
    main()