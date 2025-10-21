#!/usr/bin/env python3
"""
HTML Report Generator for Architecture Auditor Pro
Creates beautiful, professional HTML reports from JSON audit results
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def generate_html_report(json_file: str, output_file: str = None):
    """Generate professional HTML report from JSON audit results"""
    
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Default output filename
    if not output_file:
        output_file = json_file.replace('.json', '_report.html')
    
    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Architecture Auditor Pro - Reporte de Análisis</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {{
            --primary: #2563eb;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --gray-50: #f9fafb;
            --gray-100: #f3f4f6;
            --gray-200: #e5e7eb;
            --gray-300: #d1d5db;
            --gray-600: #4b5563;
            --gray-800: #1f2937;
            --gray-900: #111827;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, var(--gray-900) 0%, var(--gray-800) 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .header p {{
            font-size: 1.1rem;
            opacity: 0.8;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .project-info {{
            background: var(--gray-50);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 32px;
            border-left: 4px solid var(--primary);
        }}
        
        .project-info h2 {{
            color: var(--gray-800);
            margin-bottom: 16px;
            font-size: 1.5rem;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }}
        
        .info-item {{
            display: flex;
            flex-direction: column;
        }}
        
        .info-label {{
            font-size: 0.875rem;
            color: var(--gray-600);
            font-weight: 500;
            margin-bottom: 4px;
        }}
        
        .info-value {{
            font-size: 1rem;
            color: var(--gray-900);
            font-weight: 600;
        }}
        
        .scores-section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.75rem;
            color: var(--gray-800);
            margin-bottom: 24px;
            font-weight: 600;
        }}
        
        .scores-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }}
        
        .score-card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid var(--gray-200);
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
            background: var(--primary);
        }}
        
        .score-card.excellent::before {{ background: var(--success); }}
        .score-card.good::before {{ background: var(--warning); }}
        .score-card.poor::before {{ background: var(--danger); }}
        
        .score-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}
        
        .score-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--gray-800);
        }}
        
        .score-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
        }}
        
        .score-bar {{
            width: 100%;
            height: 8px;
            background: var(--gray-200);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .score-fill {{
            height: 100%;
            background: var(--primary);
            transition: width 0.8s ease;
        }}
        
        .score-fill.excellent {{ background: var(--success); }}
        .score-fill.good {{ background: var(--warning); }}
        .score-fill.poor {{ background: var(--danger); }}
        
        .patterns-section {{
            margin-bottom: 40px;
        }}
        
        .patterns-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
        }}
        
        .pattern-card {{
            background: var(--gray-50);
            border-radius: 12px;
            padding: 24px;
            border: 1px solid var(--gray-200);
        }}
        
        .pattern-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--gray-800);
            margin-bottom: 16px;
        }}
        
        .pattern-list {{
            list-style: none;
        }}
        
        .pattern-item {{
            background: white;
            padding: 12px 16px;
            margin-bottom: 8px;
            border-radius: 8px;
            border-left: 4px solid var(--success);
            font-weight: 500;
        }}
        
        .no-patterns {{
            color: var(--gray-600);
            font-style: italic;
            text-align: center;
            padding: 20px;
        }}
        
        .recommendations-section {{
            margin-bottom: 40px;
        }}
        
        .recommendation-card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 16px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-left: 4px solid var(--warning);
        }}
        
        .recommendation-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        
        .recommendation-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--gray-800);
        }}
        
        .priority-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 500;
        }}
        
        .priority-alta {{ background: #fee2e2; color: #dc2626; }}
        .priority-media {{ background: #fef3c7; color: #d97706; }}
        .priority-baja {{ background: #dcfce7; color: #16a34a; }}
        .priority-critica {{ background: #fecaca; color: #b91c1c; }}
        
        .recommendation-description {{
            color: var(--gray-600);
            line-height: 1.6;
        }}
        
        .footer {{
            background: var(--gray-50);
            padding: 32px;
            text-align: center;
            border-top: 1px solid var(--gray-200);
        }}
        
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 32px;
            margin-bottom: 16px;
        }}
        
        .footer-link {{
            color: var(--primary);
            text-decoration: none;
            font-weight: 500;
        }}
        
        .footer-link:hover {{
            text-decoration: underline;
        }}
        
        .footer-text {{
            color: var(--gray-600);
            font-size: 0.875rem;
        }}
        
        @media (max-width: 768px) {{
            .container {{ margin: 10px; }}
            .content {{ padding: 20px; }}
            .scores-grid {{ grid-template-columns: 1fr; }}
            .patterns-grid {{ grid-template-columns: 1fr; }}
            .footer-links {{ flex-direction: column; gap: 16px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Architecture Auditor Pro</h1>
            <p>Reporte de Análisis de Arquitectura y Código Limpio</p>
        </div>
        
        <div class="content">
            <div class="project-info">
                <h2>Información del Proyecto</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Proyecto</div>
                        <div class="info-value">{data.get('project', 'N/A')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Tipo</div>
                        <div class="info-value">{data.get('project_type', 'N/A').replace('_', ' ').title()}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Fecha de Análisis</div>
                        <div class="info-value">{data.get('timestamp', 'N/A')[:19].replace('T', ' ')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Puntuación General</div>
                        <div class="info-value">{data.get('weighted_score', 0):.1f}/100</div>
                    </div>
                </div>
            </div>
            
            <div class="scores-section">
                <h2 class="section-title">Puntuaciones Detalladas</h2>
                <div class="scores-grid">
                    {generate_score_card("Estructura", data.get('structure', {}).get('score', 0))}
                    {generate_score_card("Código Limpio", data.get('clean_code', {}).get('score', 0))}
                    {generate_score_card("Arquitectura", data.get('architecture_patterns', {}).get('score', 0))}
                    {generate_score_card("Patrones de Diseño", data.get('design_patterns', {}).get('score', 0))}
                </div>
            </div>
            
            <div class="patterns-section">
                <h2 class="section-title">Patrones Detectados</h2>
                <div class="patterns-grid">
                    <div class="pattern-card">
                        <h3 class="pattern-title">Patrones de Arquitectura</h3>
                        {generate_pattern_list(data.get('architecture_patterns', {}).get('patterns_detected', []))}
                    </div>
                    <div class="pattern-card">
                        <h3 class="pattern-title">Patrones de Diseño</h3>
                        {generate_pattern_list(data.get('design_patterns', {}).get('patterns_found', []))}
                    </div>
                </div>
            </div>
            
            <div class="recommendations-section">
                <h2 class="section-title">Recomendaciones ({len(data.get('recommendations', []))})</h2>
                {generate_recommendations(data.get('recommendations', []))}
            </div>
        </div>
        
        <div class="footer">
            <div class="footer-links">
                <a href="https://github.com/juanjovip2490/CLEAN-CODE-AND-ARCHITECTURES" class="footer-link">Clean Code Reference</a>
                <a href="./arquitecturas-software-clase1.html" class="footer-link">Architecture Documentation</a>
                <a href="https://github.com/juanjovip2490/architecture-auditor" class="footer-link">Architecture Auditor</a>
            </div>
            <p class="footer-text">
                Generado por Architecture Auditor Pro - Basado en principios de Clean Code de Robert C. Martin
            </p>
        </div>
    </div>
    
    <script>
        // Animate score bars on load
        window.addEventListener('load', function() {{
            const scoreFills = document.querySelectorAll('.score-fill');
            scoreFills.forEach(fill => {{
                const width = fill.style.width;
                fill.style.width = '0%';
                setTimeout(() => {{
                    fill.style.width = width;
                }}, 500);
            }});
        }});
    </script>
</body>
</html>"""

    # Write HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML report generated: {output_file}")
    return output_file

def generate_score_card(title: str, score: int):
    """Generate HTML for a score card"""
    score_class = "excellent" if score >= 80 else "good" if score >= 60 else "poor"
    
    return f"""
    <div class="score-card {score_class}">
        <div class="score-header">
            <div class="score-title">{title}</div>
            <div class="score-value">{score}</div>
        </div>
        <div class="score-bar">
            <div class="score-fill {score_class}" style="width: {score}%"></div>
        </div>
    </div>"""

def generate_pattern_list(patterns: list):
    """Generate HTML for pattern list"""
    if not patterns:
        return '<div class="no-patterns">No se detectaron patrones</div>'
    
    pattern_items = ""
    for pattern in patterns:
        pattern_items += f'<li class="pattern-item">{pattern}</li>'
    
    return f'<ul class="pattern-list">{pattern_items}</ul>'

def generate_recommendations(recommendations: list):
    """Generate HTML for recommendations"""
    if not recommendations:
        return '<div class="no-patterns">No hay recomendaciones</div>'
    
    rec_html = ""
    for i, rec in enumerate(recommendations, 1):
        priority = rec.get('priority', 'Media').lower()
        rec_html += f"""
        <div class="recommendation-card">
            <div class="recommendation-header">
                <div class="recommendation-title">{i}. {rec.get('category', 'General')}</div>
                <div class="priority-badge priority-{priority}">{rec.get('priority', 'Media')}</div>
            </div>
            <div class="recommendation-description">{rec.get('description', '')}</div>
        </div>"""
    
    return rec_html

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_html_report.py <json_file> [output_file]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(json_file).exists():
        print(f"Error: JSON file '{json_file}' not found")
        sys.exit(1)
    
    generate_html_report(json_file, output_file)

if __name__ == "__main__":
    main()