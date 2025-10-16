# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
HTML Report Generator for Architecture Auditor
Generates detailed HTML reports from JSON audit results
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def generate_html_report(json_file: str, output_file: str = None):
    """Generate HTML report from JSON audit results"""
    
    # Load JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file {json_file} not found")
        return False
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {json_file}")
        return False
    
    # Extract data
    project_name = Path(data['project']).name
    timestamp = data.get('timestamp', datetime.now().isoformat())
    structure_score = data['architecture_patterns']['structure']['score']
    clean_score = data['clean_code_principles']['score']
    arch_score = data['architecture_patterns']['score']
    design_score = data['design_patterns']['score']
    total_score = data.get('total_score', data.get('weighted_total_score', 0))
    
    recommendations = data.get('recommendations', [])
    structure_issues = data['architecture_patterns']['structure'].get('issues', [])
    clean_issues = data['clean_code_principles'].get('issues', [])
    detected_patterns = data['architecture_patterns'].get('patterns_detected', [])
    design_patterns = data['design_patterns'].get('patterns_found', [])
    
    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Architecture Audit Report - {project_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .score-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .score-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .score-card.low {{ background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); }}
        .score-card.medium {{ background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); }}
        .score-card.high {{ background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%); }}
        .score-card.excellent {{ background: linear-gradient(135deg, #1dd1a1 0%, #10ac84 100%); }}
        
        .score-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            border-left: 4px solid #3498db;
            background: #f8f9fa;
        }}
        .recommendations {{
            background: #e8f5e8;
            border-left-color: #27ae60;
        }}
        .issues {{
            background: #ffeaa7;
            border-left-color: #fdcb6e;
        }}
        .critical {{
            background: #fab1a0;
            border-left-color: #e17055;
        }}
        .recommendation-item, .issue-item {{
            margin: 10px 0;
            padding: 15px;
            background: white;
            border-radius: 5px;
            border-left: 3px solid #3498db;
        }}
        .priority-high {{ border-left-color: #e74c3c; }}
        .priority-medium {{ border-left-color: #f39c12; }}
        .priority-low {{ border-left-color: #27ae60; }}
        
        .code-block {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
            overflow-x: auto;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 5px;
        }}
        .badge-high {{ background: #ffebee; color: #c62828; }}
        .badge-medium {{ background: #fff3e0; color: #ef6c00; }}
        .badge-low {{ background: #e8f5e8; color: #2e7d32; }}
        .pattern-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 10px 0;
        }}
        .pattern-tag {{
            background: #3498db;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
        }}
        .no-patterns {{
            color: #7f8c8d;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Architecture Audit Report</h1>
            <h2>Project: {project_name}</h2>
            <p><strong>Date:</strong> {timestamp[:19].replace('T', ' ')}</p>
            <p><strong>Tool:</strong> Architecture Auditor v2.0</p>
        </div>

        <div class="section">
            <h2>Overall Score</h2>
            <div class="score-grid">
                <div class="score-card {'low' if total_score < 40 else 'medium' if total_score < 60 else 'high' if total_score < 80 else 'excellent'}">
                    <h3>Total Score</h3>
                    <div class="score-number">{total_score:.1f}</div>
                    <p>{'Poor' if total_score < 40 else 'Fair' if total_score < 60 else 'Good' if total_score < 80 else 'Excellent'}</p>
                </div>
                <div class="score-card {'low' if structure_score < 40 else 'medium' if structure_score < 60 else 'high' if structure_score < 80 else 'excellent'}">
                    <h3>Structure</h3>
                    <div class="score-number">{structure_score}</div>
                    <p>Project Organization</p>
                </div>
                <div class="score-card {'low' if clean_score < 40 else 'medium' if clean_score < 60 else 'high' if clean_score < 80 else 'excellent'}">
                    <h3>Clean Code</h3>
                    <div class="score-number">{clean_score}</div>
                    <p>Code Quality</p>
                </div>
                <div class="score-card {'low' if arch_score < 40 else 'medium' if arch_score < 60 else 'high' if arch_score < 80 else 'excellent'}">
                    <h3>Architecture</h3>
                    <div class="score-number">{arch_score}</div>
                    <p>Architecture Patterns</p>
                </div>
                <div class="score-card {'low' if design_score < 40 else 'medium' if design_score < 60 else 'high' if design_score < 80 else 'excellent'}">
                    <h3>Design</h3>
                    <div class="score-number">{design_score}</div>
                    <p>Design Patterns</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Detected Patterns</h2>
            <h3>Architecture Patterns</h3>
            <div class="pattern-list">
                {' '.join([f'<span class="pattern-tag">{pattern}</span>' for pattern in detected_patterns]) if detected_patterns else '<span class="no-patterns">No architecture patterns detected</span>'}
            </div>
            <h3>Design Patterns</h3>
            <div class="pattern-list">
                {' '.join([f'<span class="pattern-tag">{pattern}</span>' for pattern in design_patterns]) if design_patterns else '<span class="no-patterns">No design patterns detected</span>'}
            </div>
        </div>

        <div class="section recommendations">
            <h2>Recommendations ({len(recommendations)})</h2>
            {generate_recommendations_html(recommendations)}
        </div>

        <div class="section issues">
            <h2>Issues Found</h2>
            {generate_issues_html(structure_issues, clean_issues)}
        </div>

        <div class="section">
            <h2>Improvement Roadmap</h2>
            <h3>Phase 1: Critical Issues (Week 1-2)</h3>
            <ul>
                <li>Fix structure issues: missing directories and files</li>
                <li>Implement basic error handling</li>
                <li>Add essential documentation</li>
            </ul>
            
            <h3>Phase 2: Architecture Patterns (Week 3-4)</h3>
            <ul>
                <li>Implement Repository pattern for data access</li>
                <li>Add Service layer for business logic</li>
                <li>Introduce Factory pattern for object creation</li>
            </ul>
            
            <h3>Phase 3: Code Quality (Week 5-6)</h3>
            <ul>
                <li>Refactor long functions (max 20 lines)</li>
                <li>Improve naming conventions</li>
                <li>Add comprehensive unit tests</li>
            </ul>
            
            <h3>Phase 4: Advanced Patterns (Week 7-8)</h3>
            <ul>
                <li>Implement Dependency Injection</li>
                <li>Add Observer pattern for events</li>
                <li>Optimize performance and scalability</li>
            </ul>
        </div>

        <div class="section">
            <h2>Code Examples</h2>
            <h3>Recommended Structure</h3>
            <div class="code-block">
{project_name}/
├── src/                    # Source code
│   ├── api/               # API endpoints
│   ├── services/          # Business logic
│   ├── models/            # Data models
│   └── utils/             # Utilities
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── config/                # Configuration
└── requirements.txt       # Dependencies
            </div>
            
            <h3>Repository Pattern Example</h3>
            <div class="code-block">
class DocumentRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def save(self, document: Document) -> str:
        # Implementation here
        pass
    
    def find_by_id(self, doc_id: str) -> Document:
        # Implementation here
        pass
            </div>
        </div>

        <div class="section">
            <h2>Summary</h2>
            <p>This project shows {'excellent' if total_score >= 80 else 'good' if total_score >= 60 else 'fair' if total_score >= 40 else 'poor'} architecture practices with a score of <strong>{total_score:.1f}/100</strong>.</p>
            
            <h3>Strengths:</h3>
            <ul>
                {generate_strengths_html(structure_score, clean_score, arch_score, design_score)}
            </ul>
            
            <h3>Areas for Improvement:</h3>
            <ul>
                {generate_improvements_html(structure_score, clean_score, arch_score, design_score)}
            </ul>
            
            <p><strong>Next Steps:</strong> Focus on the high-priority recommendations to improve the overall architecture quality.</p>
        </div>
    </div>
</body>
</html>"""

    # Set output filename
    if not output_file:
        output_file = f"audit_report_{project_name}.html"
    
    # Write HTML file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML report generated: {output_file}")
        return True
    except Exception as e:
        print(f"Error writing HTML file: {e}")
        return False

def generate_recommendations_html(recommendations):
    """Generate HTML for recommendations section"""
    if not recommendations:
        return "<p>No specific recommendations at this time.</p>"
    
    html = ""
    for i, rec in enumerate(recommendations, 1):
        priority_class = f"priority-{rec['priority'].lower()}"
        badge_class = f"badge-{rec['priority'].lower()}"
        html += f"""
            <div class="recommendation-item {priority_class}">
                <span class="badge {badge_class}">{rec['priority'].upper()}</span>
                <strong>{rec['category']}</strong>
                <p>{rec['description']}</p>
            </div>
        """
    return html

def generate_issues_html(structure_issues, clean_issues):
    """Generate HTML for issues section"""
    html = ""
    
    if structure_issues:
        html += "<h3>Structure Issues</h3>"
        for issue in structure_issues:
            html += f'<div class="issue-item">- {issue}</div>'
    
    if clean_issues:
        html += "<h3>Clean Code Issues</h3>"
        for issue in clean_issues[:10]:  # Limit to 10 issues
            html += f'<div class="issue-item">- {issue}</div>'
        if len(clean_issues) > 10:
            html += f'<div class="issue-item">... and {len(clean_issues) - 10} more issues</div>'
    
    if not structure_issues and not clean_issues:
        html = "<p>No critical issues found.</p>"
    
    return html

def generate_strengths_html(structure_score, clean_score, arch_score, design_score):
    """Generate HTML for strengths section"""
    strengths = []
    
    if structure_score >= 70:
        strengths.append("Well-organized project structure")
    if clean_score >= 70:
        strengths.append("Good clean code practices")
    if arch_score >= 40:
        strengths.append("Some architecture patterns implemented")
    if design_score >= 40:
        strengths.append("Design patterns in use")
    
    if not strengths:
        strengths.append("Basic project setup is functional")
    
    return ''.join([f'<li>{strength}</li>' for strength in strengths])

def generate_improvements_html(structure_score, clean_score, arch_score, design_score):
    """Generate HTML for improvements section"""
    improvements = []
    
    if structure_score < 70:
        improvements.append("Improve project structure and organization")
    if clean_score < 70:
        improvements.append("Apply clean code principles more consistently")
    if arch_score < 40:
        improvements.append("Implement architecture patterns for better maintainability")
    if design_score < 40:
        improvements.append("Add design patterns to improve code flexibility")
    
    if not improvements:
        improvements.append("Continue maintaining current good practices")
    
    return ''.join([f'<li>{improvement}</li>' for improvement in improvements])

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_html_report.py <json_file> [output_file]")
        print("Example: python generate_html_report.py audit_report.json report.html")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = generate_html_report(json_file, output_file)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()