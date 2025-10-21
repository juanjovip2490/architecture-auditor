#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple HTML Report Generator for Architecture Auditor Pro
"""

import json
import sys
from pathlib import Path

def generate_html_report(json_file: str, output_file: str = None):
    """Generate HTML report from JSON audit results"""
    
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Default output filename
    if not output_file:
        output_file = json_file.replace('.json', '_report.html')
    
    # Helper functions
    def get_score_class(score):
        if score >= 80: return "excellent"
        elif score >= 60: return "good"
        else: return "poor"
    
    def get_score_color(score):
        if score >= 80: return "#10b981"
        elif score >= 60: return "#f59e0b"
        else: return "#ef4444"
    
    # Extract data
    project = data.get('project', 'N/A')
    project_type = data.get('project_type', 'N/A').replace('_', ' ').title()
    timestamp = data.get('timestamp', 'N/A')[:19].replace('T', ' ')
    weighted_score = data.get('weighted_score', 0)
    
    structure_score = data.get('structure', {}).get('score', 0)
    clean_code_score = data.get('clean_code', {}).get('score', 0)
    architecture_score = data.get('architecture_patterns', {}).get('score', 0)
    design_score = data.get('design_patterns', {}).get('score', 0)
    
    arch_patterns = data.get('architecture_patterns', {}).get('patterns_detected', [])
    design_patterns = data.get('design_patterns', {}).get('patterns_found', [])
    recommendations = data.get('recommendations', [])
    
    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Architecture Auditor Pro - Reporte</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
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
            background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .content {{ padding: 40px; }}
        
        .project-info {{
            background: #f9fafb;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 32px;
            border-left: 4px solid #2563eb;
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
            color: #6b7280;
            font-weight: 500;
            margin-bottom: 4px;
        }}
        
        .info-value {{
            font-size: 1rem;
            color: #111827;
            font-weight: 600;
        }}
        
        .section-title {{
            font-size: 1.75rem;
            color: #1f2937;
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
            border: 1px solid #e5e7eb;
            border-top: 4px solid {get_score_color(structure_score)};
        }}
        
        .score-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}
        
        .score-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #1f2937;
        }}
        
        .score-value {{
            font-size: 2rem;
            font-weight: 700;
            color: #2563eb;
        }}
        
        .score-bar {{
            width: 100%;
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .score-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.8s ease;
        }}
        
        .patterns-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            margin-bottom: 40px;
        }}
        
        .pattern-card {{
            background: #f9fafb;
            border-radius: 12px;
            padding: 24px;
            border: 1px solid #e5e7eb;
        }}
        
        .pattern-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: #1f2937;
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
            border-left: 4px solid #10b981;
            font-weight: 500;
        }}
        
        .no-patterns {{
            color: #6b7280;
            font-style: italic;
            text-align: center;
            padding: 20px;
        }}
        
        .recommendation-card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 16px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #f59e0b;
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
            color: #1f2937;
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
        
        .footer {{
            background: #f9fafb;
            padding: 32px;
            text-align: center;
            border-top: 1px solid #e5e7eb;
        }}
        
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 32px;
            margin-bottom: 16px;
        }}
        
        .footer-link {{
            color: #2563eb;
            text-decoration: none;
            font-weight: 500;
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
                        <div class="info-value">{project}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Tipo</div>
                        <div class="info-value">{project_type}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Fecha de Análisis</div>
                        <div class="info-value">{timestamp}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Puntuación General</div>
                        <div class="info-value">{weighted_score:.1f}/100</div>
                    </div>
                </div>
            </div>
            
            <div class="scores-section">
                <h2 class="section-title">Puntuaciones Detalladas</h2>
                <div class="scores-grid">
                    <div class="score-card">
                        <div class="score-header">
                            <div class="score-title">Estructura</div>
                            <div class="score-value">{structure_score}</div>
                        </div>
                        <div class="score-bar">
                            <div class="score-fill" style="width: {structure_score}%; background: {get_score_color(structure_score)};"></div>
                        </div>
                    </div>
                    
                    <div class="score-card">
                        <div class="score-header">
                            <div class="score-title">Código Limpio</div>
                            <div class="score-value">{clean_code_score}</div>
                        </div>
                        <div class="score-bar">
                            <div class="score-fill" style="width: {clean_code_score}%; background: {get_score_color(clean_code_score)};"></div>
                        </div>
                    </div>
                    
                    <div class="score-card">
                        <div class="score-header">
                            <div class="score-title">Arquitectura</div>
                            <div class="score-value">{architecture_score}</div>
                        </div>
                        <div class="score-bar">
                            <div class="score-fill" style="width: {architecture_score}%; background: {get_score_color(architecture_score)};"></div>
                        </div>
                    </div>
                    
                    <div class="score-card">
                        <div class="score-header">
                            <div class="score-title">Patrones de Diseño</div>
                            <div class="score-value">{design_score}</div>
                        </div>
                        <div class="score-bar">
                            <div class="score-fill" style="width: {design_score}%; background: {get_score_color(design_score)};"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="patterns-section">
                <h2 class="section-title">Patrones Detectados</h2>
                <div class="patterns-grid">
                    <div class="pattern-card">
                        <h3 class="pattern-title">Patrones de Arquitectura</h3>
                        {"".join([f'<div class="pattern-item">{pattern}</div>' for pattern in arch_patterns]) if arch_patterns else '<div class="no-patterns">No se detectaron patrones de arquitectura</div>'}
                    </div>
                    <div class="pattern-card">
                        <h3 class="pattern-title">Patrones de Diseño</h3>
                        {"".join([f'<div class="pattern-item">{pattern}</div>' for pattern in design_patterns]) if design_patterns else '<div class="no-patterns">No se detectaron patrones de diseño</div>'}
                    </div>
                </div>
            </div>
            
            <div class="recommendations-section">
                <h2 class="section-title">Recomendaciones ({len(recommendations)})</h2>
                {"".join([f'''
                <div class="recommendation-card">
                    <div class="recommendation-header">
                        <div class="recommendation-title">{i}. {rec.get('category', 'General')}</div>
                        <div class="priority-badge priority-{rec.get('priority', 'Media').lower()}">{rec.get('priority', 'Media')}</div>
                    </div>
                    <div class="recommendation-description">{rec.get('description', '')}</div>
                </div>''' for i, rec in enumerate(recommendations, 1)]) if recommendations else '<div class="no-patterns">No hay recomendaciones</div>'}
            </div>
        </div>
        
        <div class="footer">
            <div class="footer-links">
                <a href="https://github.com/juanjovip2490/CLEAN-CODE-AND-ARCHITECTURES" class="footer-link">Clean Code Reference</a>
                <a href="./arquitecturas-software-clase1.html" class="footer-link">Architecture Documentation</a>
                <a href="https://github.com/juanjovip2490/architecture-auditor" class="footer-link">Architecture Auditor</a>
            </div>
            <p style="color: #6b7280; font-size: 0.875rem;">
                Generado por Architecture Auditor Pro - Basado en principios de Clean Code de Robert C. Martin
            </p>
        </div>
    </div>
</body>
</html>"""

    # Write HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML report generated: {output_file}")
    return output_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python html_report_generator.py <json_file> [output_file]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(json_file).exists():
        print(f"Error: JSON file '{json_file}' not found")
        sys.exit(1)
    
    generate_html_report(json_file, output_file)

if __name__ == "__main__":
    main()