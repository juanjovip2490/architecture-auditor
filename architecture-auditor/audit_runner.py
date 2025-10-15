#!/usr/bin/env python3
"""
Script para ejecutar auditorías automáticas en nuevos proyectos
"""

import os
import sys
import json
from pathlib import Path
from auditor import ArchitectureAuditor

class ProjectAuditRunner:
    def __init__(self):
        self.config_path = Path(__file__).parent / "config"
        self.rules_path = Path(__file__).parent / "rules"
    
    def audit_new_project(self, project_path: str, project_type: str = None):
        """Audita un nuevo proyecto con configuración específica"""
        
        print(f"🚀 Iniciando auditoría de nuevo proyecto: {project_path}")
        
        # Detectar tipo de proyecto si no se especifica
        if not project_type:
            project_type = self._detect_project_type(project_path)
            print(f"📋 Tipo de proyecto detectado: {project_type}")
        
        # Cargar configuración específica
        config = self._load_project_config(project_type)
        
        # Ejecutar auditoría
        auditor = ArchitectureAuditor(project_path)
        results = auditor.audit_project()
        
        # Aplicar pesos específicos del tipo de proyecto
        if config:
            results = self._apply_project_weights(results, config)
        
        # Generar recomendaciones específicas
        specific_recommendations = self._generate_specific_recommendations(results, config)
        results['recommendations'].extend(specific_recommendations)
        
        return results
    
    def _detect_project_type(self, project_path: str) -> str:
        """Detecta automáticamente el tipo de proyecto"""
        project_path = Path(project_path)
        
        # Cargar reglas de detección
        with open(self.config_path / "project_types.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        detection_rules = config['detection_rules']
        
        for project_type, indicators in detection_rules.items():
            score = 0
            for indicator in indicators:
                if (project_path / indicator).exists():
                    score += 1
                elif any(project_path.rglob(f"*{indicator}*")):
                    score += 0.5
            
            if score >= len(indicators) * 0.3:  # 30% de coincidencia mínima
                return project_type
        
        return "generic"
    
    def _load_project_config(self, project_type: str) -> dict:
        """Carga configuración específica del tipo de proyecto"""
        try:
            with open(self.config_path / "project_types.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config['project_types'].get(project_type, {})
        except FileNotFoundError:
            return {}
    
    def _apply_project_weights(self, results: dict, config: dict) -> dict:
        """Aplica pesos específicos según el tipo de proyecto"""
        if 'score_weights' not in config:
            return results
        
        weights = config['score_weights']
        
        # Calcular puntuación ponderada
        weighted_score = (
            results['architecture_patterns']['structure']['score'] * weights.get('structure', 0.25) +
            results['clean_code_principles']['score'] * weights.get('clean_code', 0.25) +
            results['architecture_patterns']['score'] * weights.get('architecture', 0.25) +
            results['design_patterns']['score'] * weights.get('design_patterns', 0.25)
        )
        
        results['weighted_total_score'] = round(weighted_score, 2)
        return results
    
    def _generate_specific_recommendations(self, results: dict, config: dict) -> list:
        """Genera recomendaciones específicas según el tipo de proyecto"""
        recommendations = []
        
        if not config:
            return recommendations
        
        # Verificar patrones recomendados
        recommended_patterns = config.get('recommended_patterns', [])
        detected_patterns = results['architecture_patterns']['patterns_detected']
        
        missing_patterns = set(recommended_patterns) - set(detected_patterns)
        
        for pattern in missing_patterns:
            recommendations.append({
                'category': 'Patrón Recomendado',
                'priority': 'Media',
                'description': f'Considerar implementar patrón {pattern} para este tipo de proyecto'
            })
        
        # Verificar estructura recomendada
        required_structure = config.get('required_structure', [])
        project_path = Path(results['project'])
        
        for required_dir in required_structure:
            if not (project_path / required_dir).exists():
                recommendations.append({
                    'category': 'Estructura',
                    'priority': 'Alta',
                    'description': f'Crear directorio {required_dir} según convenciones del tipo de proyecto'
                })
        
        return recommendations

def main():
    if len(sys.argv) < 2:
        print("Uso: python audit_runner.py <ruta_proyecto> [tipo_proyecto]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    project_type = sys.argv[2] if len(sys.argv) > 2 else None
    
    runner = ProjectAuditRunner()
    results = runner.audit_new_project(project_path, project_type)
    
    # Mostrar resultados
    print("\n" + "="*60)
    print("📊 RESULTADOS DE AUDITORÍA")
    print("="*60)
    
    if 'weighted_total_score' in results:
        print(f"🎯 Puntuación Total Ponderada: {results['weighted_total_score']}/100")
    
    print(f"📁 Estructura: {results['architecture_patterns']['structure']['score']}/100")
    print(f"🧹 Código Limpio: {results['clean_code_principles']['score']}/100")
    print(f"🏗️ Arquitectura: {results['architecture_patterns']['score']}/100")
    print(f"🎨 Patrones: {results['design_patterns']['score']}/100")
    
    print(f"\n🔍 Patrones Detectados: {', '.join(results['architecture_patterns']['patterns_detected'])}")
    print(f"🎨 Patrones de Diseño: {', '.join(results['design_patterns']['patterns_found'])}")
    
    print(f"\n💡 Recomendaciones ({len(results['recommendations'])}):")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. [{rec['priority']}] {rec['category']}: {rec['description']}")
    
    # Guardar reporte
    output_file = f"audit_report_{Path(project_path).name}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Reporte completo guardado en: {output_file}")

if __name__ == "__main__":
    main()