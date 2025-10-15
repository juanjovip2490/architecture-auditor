#!/usr/bin/env python3
"""
Auditor de Patrones de Arquitectura y Diseño
Basado en principios de código limpio y patrones de arquitectura
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class ArchitectureAuditor:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.results = {
            'project': str(self.project_path),
            'timestamp': datetime.now().isoformat(),
            'architecture_patterns': {},
            'clean_code_principles': {},
            'design_patterns': {},
            'recommendations': []
        }
    
    def audit_project(self) -> Dict[str, Any]:
        """Ejecuta auditoría completa del proyecto"""
        print(f"🔍 Auditando proyecto: {self.project_path}")
        
        self._audit_structure()
        self._audit_clean_code()
        self._audit_architecture_patterns()
        self._audit_design_patterns()
        self._generate_recommendations()
        
        return self.results
    
    def _audit_structure(self):
        """Audita estructura del proyecto"""
        structure_score = 0
        issues = []
        
        # Verificar estructura básica
        if (self.project_path / 'src').exists():
            structure_score += 20
        else:
            issues.append("Falta directorio 'src' para código fuente")
        
        if (self.project_path / 'tests').exists():
            structure_score += 20
        else:
            issues.append("Falta directorio 'tests' para pruebas")
        
        if (self.project_path / 'docs').exists():
            structure_score += 10
        else:
            issues.append("Falta directorio 'docs' para documentación")
        
        # Verificar archivos de configuración
        config_files = ['README.md', 'requirements.txt', '.gitignore']
        for file in config_files:
            if (self.project_path / file).exists():
                structure_score += 10
            else:
                issues.append(f"Falta archivo {file}")
        
        self.results['architecture_patterns']['structure'] = {
            'score': min(structure_score, 100),
            'issues': issues
        }
    
    def _audit_clean_code(self):
        """Audita principios de código limpio según Clean Code de Robert Martin"""
        clean_code_score = 0
        issues = []
        
        # Buscar archivos Python para análisis
        py_files = list(self.project_path.rglob('*.py'))
        
        if not py_files:
            issues.append("No se encontraron archivos Python para analizar")
            self.results['clean_code_principles'] = {'score': 0, 'issues': issues}
            return
        
        for file_path in py_files[:10]:  # Limitar a 10 archivos
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. Nombres significativos
                if self._check_meaningful_names(content, file_path.name):
                    clean_code_score += 15
                else:
                    issues.append(f"Nombres no significativos en {file_path.name}")
                
                # 2. Funciones pequeñas y enfocadas
                if self._check_function_quality(content, file_path.name):
                    clean_code_score += 20
                else:
                    issues.append(f"Funciones muy largas o complejas en {file_path.name}")
                
                # 3. Comentarios apropiados
                if self._check_comments_quality(content):
                    clean_code_score += 10
                else:
                    issues.append(f"Comentarios inadecuados en {file_path.name}")
                
                # 4. Formato y estructura
                if self._check_formatting(content, file_path.name):
                    clean_code_score += 10
                else:
                    issues.append(f"Formato inconsistente en {file_path.name}")
                
                # 5. Manejo de errores
                if self._check_error_handling(content, file_path.name):
                    clean_code_score += 10
                else:
                    issues.append(f"Manejo de errores deficiente en {file_path.name}")
                
                # 6. Clases bien organizadas
                if self._check_class_organization(content, file_path.name):
                    clean_code_score += 15
                else:
                    issues.append(f"Clases mal organizadas en {file_path.name}")
                
            except Exception as e:
                issues.append(f"Error leyendo {file_path}: {str(e)}")
        
        self.results['clean_code_principles'] = {
            'score': min(clean_code_score, 100),
            'issues': issues
        }
    
    def _audit_architecture_patterns(self):
        """Audita patrones de arquitectura"""
        patterns_found = []
        
        # Detectar MVC
        if self._detect_mvc_pattern():
            patterns_found.append("MVC")
        
        # Detectar Repository Pattern
        if self._detect_repository_pattern():
            patterns_found.append("Repository")
        
        # Detectar Dependency Injection
        if self._detect_dependency_injection():
            patterns_found.append("Dependency Injection")
        
        self.results['architecture_patterns']['patterns_detected'] = patterns_found
        self.results['architecture_patterns']['score'] = len(patterns_found) * 20
    
    def _audit_design_patterns(self):
        """Audita patrones de diseño"""
        patterns = {
            'singleton': self._detect_singleton(),
            'factory': self._detect_factory(),
            'observer': self._detect_observer(),
            'strategy': self._detect_strategy()
        }
        
        self.results['design_patterns'] = {
            'patterns_found': [k for k, v in patterns.items() if v],
            'score': sum(patterns.values()) * 15
        }
    
    def _generate_recommendations(self):
        """Genera recomendaciones basadas en la auditoría"""
        recommendations = []
        
        # Recomendaciones de estructura
        if self.results['architecture_patterns']['structure']['score'] < 70:
            recommendations.append({
                'category': 'Estructura',
                'priority': 'Alta',
                'description': 'Mejorar organización de directorios siguiendo convenciones estándar'
            })
        
        # Recomendaciones de código limpio
        if self.results['clean_code_principles']['score'] < 60:
            recommendations.append({
                'category': 'Código Limpio',
                'priority': 'Alta',
                'description': 'Aplicar principios de código limpio: funciones pequeñas, nombres descriptivos'
            })
        
        # Recomendaciones de patrones
        if len(self.results['architecture_patterns']['patterns_detected']) < 2:
            recommendations.append({
                'category': 'Patrones de Arquitectura',
                'priority': 'Media',
                'description': 'Implementar patrones de arquitectura para mejorar mantenibilidad'
            })
        
        self.results['recommendations'] = recommendations
    
    # Métodos auxiliares de verificación según Clean Code
    def _check_meaningful_names(self, content: str, filename: str) -> bool:
        import re
        score = 0
        
        # Verificar nombres de funciones descriptivos
        functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
        for func in functions:
            if len(func) > 3 and not any(bad in func.lower() for bad in ['temp', 'data', 'info', 'mgr']):
                score += 1
        
        # Verificar nombres de clases (sustantivos)
        classes = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
        for cls in classes:
            if cls[0].isupper() and not any(bad in cls.lower() for bad in ['manager', 'processor', 'data']):
                score += 2
        
        # Verificar variables descriptivas
        variables = re.findall(r'\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=', content)
        descriptive_vars = sum(1 for var in variables if len(var) > 2 and var not in ['i', 'j', 'k', 'x', 'y'])
        
        return score > 0 and descriptive_vars > len(variables) * 0.7
    
    def _check_function_quality(self, content: str, filename: str) -> bool:
        import re
        lines = content.split('\n')
        functions = []
        current_function = None
        function_lines = 0
        
        for line in lines:
            if line.strip().startswith('def '):
                if current_function and function_lines > 20:
                    return False
                current_function = line.strip()
                function_lines = 0
            elif current_function and (line.startswith('def ') or line.startswith('class ') or not line.strip()):
                if function_lines > 20:
                    return False
                current_function = None
            elif current_function:
                function_lines += 1
        
        # Verificar argumentos de función (máximo 3)
        func_args = re.findall(r'def\s+\w+\(([^)]*)\)', content)
        for args in func_args:
            if args.count(',') > 2:  # Más de 3 argumentos
                return False
        
        return True
    
    def _check_comments_quality(self, content: str) -> bool:
        lines = content.split('\n')
        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('"""'))
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        
        if code_lines == 0:
            return True
        
        # Verificar que no hay código comentado
        commented_code = sum(1 for line in lines if line.strip().startswith('#') and any(keyword in line for keyword in ['def ', 'class ', 'import ', 'if ', 'for ']))
        
        comment_ratio = comment_lines / code_lines
        return 0.05 <= comment_ratio <= 0.25 and commented_code == 0
    
    def _check_formatting(self, content: str, filename: str) -> bool:
        lines = content.split('\n')
        
        # Verificar líneas no muy largas (120 caracteres)
        long_lines = sum(1 for line in lines if len(line) > 120)
        
        # Verificar indentación consistente
        indentation_consistent = True
        for line in lines:
            if line.startswith('    ') or line.startswith('\t'):
                continue
            elif line.strip() and not line[0].isalpha() and line[0] not in ['#', '@']:
                indentation_consistent = False
                break
        
        return long_lines < len(lines) * 0.1 and indentation_consistent
    
    def _check_error_handling(self, content: str, filename: str) -> bool:
        import re
        
        # Verificar uso de excepciones en lugar de códigos de error
        has_try_catch = 'try:' in content and 'except' in content
        
        # Verificar que no se retorna None sin razón
        return_none_count = len(re.findall(r'return\s+None', content))
        
        # Verificar que no se pasa None como argumento
        none_args = len(re.findall(r'\(\s*None\s*[,)]', content))
        
        return return_none_count < 3 and none_args == 0
    
    def _check_class_organization(self, content: str, filename: str) -> bool:
        import re
        
        classes = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*).*?(?=class|\Z)', content, re.DOTALL)
        
        for class_content in classes:
            # Verificar que las clases no son muy grandes (máximo 15 métodos)
            methods = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', class_content)
            if len(methods) > 15:
                return False
            
            # Verificar principio de responsabilidad única (heurística simple)
            # Si una clase tiene métodos muy diversos, probablemente hace demasiado
            method_prefixes = set(method.split('_')[0] for method in methods if '_' in method)
            if len(method_prefixes) > 5:
                return False
        
        return True
    
    def _detect_mvc_pattern(self) -> bool:
        mvc_dirs = ['models', 'views', 'controllers']
        return any((self.project_path / d).exists() for d in mvc_dirs)
    
    def _detect_repository_pattern(self) -> bool:
        repo_files = list(self.project_path.rglob('*repository*.py'))
        return len(repo_files) > 0
    
    def _detect_dependency_injection(self) -> bool:
        di_files = list(self.project_path.rglob('*inject*.py'))
        return len(di_files) > 0
    
    def _detect_singleton(self) -> bool:
        py_files = list(self.project_path.rglob('*.py'))
        for file_path in py_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if '__new__' in content and 'instance' in content:
                    return True
            except:
                continue
        return False
    
    def _detect_factory(self) -> bool:
        factory_files = list(self.project_path.rglob('*factory*.py'))
        return len(factory_files) > 0
    
    def _detect_observer(self) -> bool:
        py_files = list(self.project_path.rglob('*.py'))
        for file_path in py_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'notify' in content and 'observer' in content.lower():
                    return True
            except:
                continue
        return False
    
    def _detect_strategy(self) -> bool:
        strategy_files = list(self.project_path.rglob('*strategy*.py'))
        return len(strategy_files) > 0

def main():
    parser = argparse.ArgumentParser(description='Auditor de Arquitectura y Diseño')
    parser.add_argument('--project', required=True, help='Ruta del proyecto a auditar')
    parser.add_argument('--output', help='Archivo de salida para el reporte')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.project):
        print(f"❌ Error: El proyecto {args.project} no existe")
        return
    
    auditor = ArchitectureAuditor(args.project)
    results = auditor.audit_project()
    
    # Mostrar resumen
    print("\n📊 RESUMEN DE AUDITORÍA")
    print("=" * 50)
    print(f"Estructura: {results['architecture_patterns']['structure']['score']}/100")
    print(f"Código Limpio: {results['clean_code_principles']['score']}/100")
    print(f"Patrones Arquitectura: {results['architecture_patterns']['score']}/100")
    print(f"Patrones Diseño: {results['design_patterns']['score']}/100")
    
    print(f"\n🎯 RECOMENDACIONES ({len(results['recommendations'])})")
    for rec in results['recommendations']:
        print(f"• [{rec['priority']}] {rec['category']}: {rec['description']}")
    
    # Guardar reporte
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Reporte guardado en: {args.output}")

if __name__ == "__main__":
    main()