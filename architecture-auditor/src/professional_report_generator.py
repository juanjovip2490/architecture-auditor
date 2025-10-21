#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enterprise Report Generator Pro
Commercial-grade HTML report generator with Apple design system
"""

import json
import sys
from pathlib import Path

def generate_enterprise_report(json_file: str, output_file: str = None):
    """Generate enterprise HTML report with Apple design system"""
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not output_file:
        output_file = json_file.replace('.json', '_enterprise_report.html')
    
    project = data.get('project', 'N/A')
    project_name = project.split('\\')[-1] if '\\' in project else project.split('/')[-1]
    timestamp = data.get('timestamp', 'N/A')[:19].replace('T', ' ')
    project_type = data.get('project_type', 'generic')
    
    weighted_score = data.get('weighted_score', 0)
    structure_score = data.get('structure', {}).get('score', 0)
    clean_code_score = data.get('clean_code', {}).get('score', 0)
    architecture_score = data.get('architecture_patterns', {}).get('score', 0)
    design_score = data.get('design_patterns', {}).get('score', 0)
    
    structure_data = data.get('structure', {})
    clean_code_data = data.get('clean_code', {})
    architecture_data = data.get('architecture_patterns', {})
    design_data = data.get('design_patterns', {})
    recommendations = data.get('recommendations', [])
    
    def get_score_color(score):
        if score >= 75: return "var(--apple-green)"
        elif score >= 50: return "var(--apple-orange)"
        else: return "var(--apple-red)"
    
    def get_score_description(score):
        if score >= 75: return "Excellent"
        elif score >= 50: return "Good"
        else: return "Needs Improvement"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏗️ Enterprise Architecture Report - {project_name}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
        
        :root {{
            --apple-blue: #007AFF;
            --apple-gray: #8E8E93;
            --apple-gray-light: #F2F2F7;
            --apple-gray-dark: #1C1C1E;
            --apple-green: #34C759;
            --apple-orange: #FF9500;
            --apple-red: #FF3B30;
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
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 16px;
            letter-spacing: -0.02em;
        }}
        
        .header-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 24px;
        }}
        
        .header-card {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }}
        
        .content {{ padding: 40px; }}
        
        .executive-summary {{
            background: var(--apple-background);
            border: 1px solid var(--apple-separator);
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 32px;
            text-align: center;
        }}
        
        .main-score {{
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 16px;
            color: var(--apple-blue);
        }}
        
        .score-breakdown {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 32px 0;
        }}
        
        .score-card {{
            background: var(--apple-background);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            border: 1px solid var(--apple-separator);
            position: relative;
            overflow: hidden;
        }}
        
        .score-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--score-color, var(--apple-blue));
        }}
        
        .score-value {{
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--score-color, var(--apple-blue));
        }}
        
        .score-label {{
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--apple-text);
            margin-bottom: 4px;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: var(--apple-gray-light);
            border-radius: 4px;
            overflow: hidden;
            margin: 16px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: var(--score-color, var(--apple-blue));
            border-radius: 4px;
            transition: width 1s ease-out;
        }}
        
        .section {{
            margin-bottom: 40px;
            background: var(--apple-background);
            border-radius: 16px;
            padding: 32px;
            border: 1px solid var(--apple-separator);
        }}
        
        .section-title {{
            font-size: 2rem;
            color: var(--apple-text);
            margin-bottom: 24px;
            font-weight: 700;
            letter-spacing: -0.02em;
        }}
        
        .patterns-showcase {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 24px 0;
        }}
        
        .pattern-card {{
            background: var(--apple-green);
            color: white;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
        }}
        
        .pattern-card.design {{
            background: var(--apple-blue);
        }}
        
        .pattern-name {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 12px;
        }}
        
        .detailed-analysis {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 24px;
            margin: 32px 0;
        }}
        
        .analysis-card {{
            background: var(--apple-background);
            border-radius: 12px;
            padding: 24px;
            border: 1px solid var(--apple-separator);
        }}
        
        .analysis-card.success {{ border-left: 4px solid var(--apple-green); }}
        .analysis-card.warning {{ border-left: 4px solid var(--apple-orange); }}
        .analysis-card.error {{ border-left: 4px solid var(--apple-red); }}
        
        .analysis-title {{
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--apple-text);
        }}
        
        .metric-list {{
            list-style: none;
            padding: 0;
        }}
        
        .metric-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid var(--apple-separator);
        }}
        
        .metric-item:last-child {{ border-bottom: none; }}
        
        .metric-name {{
            font-weight: 500;
            color: var(--apple-text);
        }}
        
        .metric-value {{
            font-weight: 600;
            color: var(--apple-blue);
        }}
        
        .recommendations-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin: 24px 0;
        }}
        
        .recommendation-card {{
            background: var(--apple-background);
            border-radius: 12px;
            padding: 24px;
            border: 1px solid var(--apple-separator);
        }}
        
        .priority-critical {{ border-left: 4px solid var(--apple-red); }}
        .priority-alta {{ border-left: 4px solid var(--apple-orange); }}
        .priority-media {{ border-left: 4px solid var(--apple-blue); }}
        
        .priority-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .priority-critical .priority-badge {{ background: var(--apple-red); color: white; }}
        .priority-alta .priority-badge {{ background: var(--apple-orange); color: white; }}
        .priority-media .priority-badge {{ background: var(--apple-blue); color: white; }}
        
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
            <h1>🏗️ Enterprise Architecture Report</h1>
            <div class="header-info">
                <div class="header-card">
                    <h3>Project</h3>
                    <p>{project_name}</p>
                </div>
                <div class="header-card">
                    <h3>Type</h3>
                    <p>{project_type.title()}</p>
                </div>
                <div class="header-card">
                    <h3>Date</h3>
                    <p>{timestamp}</p>
                </div>
            </div>
        </div>
        
        <div class="content">
            <div class="executive-summary">
                <h2 style="margin-bottom: 24px; color: var(--apple-text);">📊 Executive Summary</h2>
                <div class="main-score">{weighted_score:.1f}/100</div>
                <p style="font-size: 1.2rem; color: var(--apple-gray);">{get_score_description(weighted_score)} - Overall Architecture Quality</p>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 32px;">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; font-weight: 700; color: var(--apple-blue);">{len(architecture_data.get('patterns_detected', []))}</div>
                        <div style="font-size: 0.9rem; color: var(--apple-gray);">Architecture Patterns</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; font-weight: 700; color: var(--apple-blue);">{len(design_data.get('patterns_found', []))}</div>
                        <div style="font-size: 0.9rem; color: var(--apple-gray);">Design Patterns</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; font-weight: 700; color: var(--apple-blue);">{len(recommendations)}</div>
                        <div style="font-size: 0.9rem; color: var(--apple-gray);">Recommendations</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; font-weight: 700; color: var(--apple-blue);">{clean_code_data.get('files_analyzed', 0)}</div>
                        <div style="font-size: 0.9rem; color: var(--apple-gray);">Files Analyzed</div>
                    </div>
                </div>
            </div>
            
            <div class="score-breakdown">
                <div class="score-card" style="--score-color: {get_score_color(structure_score)}">
                    <div class="score-value">{structure_score}</div>
                    <div class="score-label">Structure</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {structure_score}%; background: {get_score_color(structure_score)};"></div>
                    </div>
                </div>
                <div class="score-card" style="--score-color: {get_score_color(clean_code_score)}">
                    <div class="score-value">{clean_code_score}</div>
                    <div class="score-label">Clean Code</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {clean_code_score}%; background: {get_score_color(clean_code_score)};"></div>
                    </div>
                </div>
                <div class="score-card" style="--score-color: {get_score_color(architecture_score)}">
                    <div class="score-value">{architecture_score}</div>
                    <div class="score-label">Architecture</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {architecture_score}%; background: {get_score_color(architecture_score)};"></div>
                    </div>
                </div>
                <div class="score-card" style="--score-color: {get_score_color(design_score)}">
                    <div class="score-value">{design_score}</div>
                    <div class="score-label">Design Patterns</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {design_score}%; background: {get_score_color(design_score)};"></div>
                    </div>
                </div>
            </div>
            
            {generate_patterns_section(architecture_data, design_data)}
            
            {generate_detailed_analysis_section(structure_data, clean_code_data)}
            
            {generate_recommendations_section(recommendations)}
        </div>
        
        <div class="footer">
            <p>Enterprise-grade architecture analysis tool designed for commercial software development.<br>
            Created by <strong>Juan José Sáez</strong> • Professional License Available<br>
            Based on Clean Code principles by Robert Martin and enterprise architecture patterns.</p>
        </div>
    </div>
</body>
</html>"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Enterprise HTML report generated: {output_file}")
    return output_file

def generate_patterns_section(architecture_data, design_data):
    arch_patterns = architecture_data.get('patterns_detected', [])
    design_patterns = design_data.get('patterns_found', [])
    arch_details = architecture_data.get('details', {})
    
    if not arch_patterns and not design_patterns:
        return """
            <div class="section">
                <h2 class="section-title">🏗️ Architecture & Design Patterns</h2>
                <div class="analysis-card warning">
                    <div class="analysis-title">No Patterns Detected</div>
                    <p>No architecture or design patterns were identified. Consider implementing established patterns for better maintainability.</p>
                </div>
            </div>"""
    
    html = """
            <div class="section">
                <h2 class="section-title">🏗️ Architecture & Design Patterns</h2>
                <div class="patterns-showcase">"""
    
    for pattern in arch_patterns:
        description = arch_details.get(pattern, f"{pattern} pattern detected")
        html += f"""
                    <div class="pattern-card">
                        <div class="pattern-name">{pattern}</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">{description}</div>
                    </div>"""
    
    for pattern in design_patterns:
        if '(' in pattern and ')' in pattern:
            pattern_name = pattern.split('(')[0].strip()
            category = pattern.split('(')[1].split(')')[0]
            html += f"""
                    <div class="pattern-card design">
                        <div class="pattern-name">{pattern_name}</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">{category}</div>
                    </div>"""
        else:
            html += f"""
                    <div class="pattern-card design">
                        <div class="pattern-name">{pattern}</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Design pattern implementation</div>
                    </div>"""
    
    html += """
                </div>
            </div>"""
    
    return html

def generate_detailed_analysis_section(structure_data, clean_code_data):
    structure_issues = structure_data.get('issues', [])
    structure_recommendations = structure_data.get('recommendations', [])
    clean_issues = clean_code_data.get('issues', [])
    files_analyzed = clean_code_data.get('files_analyzed', 0)
    sections_evaluated = clean_code_data.get('sections_evaluated', [])
    
    html = f"""
            <div class="section">
                <h2 class="section-title">📈 Detailed Analysis</h2>
                <div class="detailed-analysis">
                    <div class="analysis-card {'error' if structure_issues else 'success'}">
                        <div class="analysis-title">📁 Project Structure Analysis</div>
                        <ul class="metric-list">
                            <li class="metric-item">
                                <span class="metric-name">Score</span>
                                <span class="metric-value">{structure_data.get('score', 0)}/100</span>
                            </li>
                            <li class="metric-item">
                                <span class="metric-name">Issues Found</span>
                                <span class="metric-value">{len(structure_issues)}</span>
                            </li>
                            <li class="metric-item">
                                <span class="metric-name">Recommendations</span>
                                <span class="metric-value">{len(structure_recommendations)}</span>
                            </li>
                        </ul>"""
    
    if structure_issues:
        html += """
                        <div style="margin-top: 16px;">
                            <strong>🚨 Issues Found:</strong>
                            <ul style="margin-top: 8px; padding-left: 20px;">"""
        for issue in structure_issues:
            html += f"<li>{issue}</li>"
        html += "</ul></div>"
    
    html += f"""
                    </div>
                    <div class="analysis-card {'success' if files_analyzed > 0 else 'warning'}">
                        <div class="analysis-title">✨ Clean Code Analysis</div>
                        <ul class="metric-list">
                            <li class="metric-item">
                                <span class="metric-name">Clean Code Score</span>
                                <span class="metric-value">{clean_code_data.get('score', 0)}/100</span>
                            </li>
                            <li class="metric-item">
                                <span class="metric-name">Files Analyzed</span>
                                <span class="metric-value">{files_analyzed}</span>
                            </li>
                            <li class="metric-item">
                                <span class="metric-name">Sections Evaluated</span>
                                <span class="metric-value">{len(sections_evaluated)}</span>
                            </li>
                            <li class="metric-item">
                                <span class="metric-name">Issues Found</span>
                                <span class="metric-value">{len(clean_issues)}</span>
                            </li>
                        </ul>"""
    
    if sections_evaluated:
        html += """
                        <div style="margin-top: 20px;">
                            <h4 style="margin-bottom: 12px; color: var(--apple-blue);">📋 Evaluated Sections:</h4>
                            <div style="display: flex; flex-wrap: wrap; gap: 8px;">"""
        for section in sections_evaluated:
            html += f'<span style="background: var(--apple-blue); color: white; padding: 4px 12px; border-radius: 16px; font-size: 0.8rem;">{section}</span>'
        html += "</div></div>"
    
    if clean_issues:
        html += """
                        <div style="margin-top: 16px;">
                            <strong style="color: var(--apple-red);">🚨 Clean Code Issues:</strong>
                            <ul style="margin-top: 8px; padding-left: 20px;">"""
        for issue in clean_issues[:10]:
            html += f"<li>{issue}</li>"
        if len(clean_issues) > 10:
            html += f'<li style="color: var(--apple-gray);">... and {len(clean_issues) - 10} more issues</li>'
        html += "</ul></div>"
    
    html += """
                    </div>
                </div>
            </div>"""
    
    return html

def generate_recommendations_section(recommendations):
    if not recommendations:
        return """
            <div class="section">
                <h2 class="section-title">💡 Recommendations</h2>
                <div class="analysis-card success">
                    <div class="analysis-title">No Critical Issues</div>
                    <p>No specific recommendations were generated. The project follows good practices.</p>
                </div>
            </div>"""
    
    html = """
            <div class="section">
                <h2 class="section-title">💡 Strategic Recommendations</h2>
                <div class="recommendations-grid">"""
    
    for rec in recommendations:
        priority = rec.get('priority', 'Media')
        priority_class = priority.lower().replace('í', 'i')
        
        html += f"""
                    <div class="recommendation-card priority-{priority_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <h3>{rec.get('category', 'General')}</h3>
                            <span class="priority-badge">{priority}</span>
                        </div>
                        <p>{rec.get('description', 'No description available')}</p>"""
        
        if 'actions' in rec:
            html += """
                        <div style="margin-top: 16px;">
                            <strong>Actions:</strong>
                            <ul style="margin-top: 8px; padding-left: 20px;">"""
            for action in rec['actions']:
                html += f"<li>{action}</li>"
            html += "</ul></div>"
        
        html += "</div>"
    
    html += "</div></div>"
    return html

def main():
    if len(sys.argv) < 2:
        print("Usage: python enterprise_report_pro.py <json_file> [output_file]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    generate_enterprise_report(json_file, output_file)

if __name__ == "__main__":
    main()