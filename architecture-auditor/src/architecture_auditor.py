#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditoría Inteligente de Arquitectura y Código Limpio
Sistema completo basado en principios de Clean Code de Robert Martin
Repositorio de referencia: https://github.com/juanjovip2490/CLEAN-CODE-AND-ARCHITECTURES
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class IntelligentArchitectureAuditor:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.config_path = Path(__file__).parent / "config"
        self.rules_path = Path(__file__).parent / "rules"
        self.results = {
            'project': str(self.project_path),
            'timestamp': datetime.now().isoformat(),
            'project_type': None,
            'total_score': 0,
            'weighted_score': 0,
            'structure': {},
            'clean_code': {},
            'architecture_patterns': {},
            'design_patterns': {},
            'recommendations': []
        }
    
    def audit_project(self, project_type: Optional[str] = None) -> Dict[str, Any]:
        """Ejecuta auditoría inteligente completa del proyecto"""
        print(f"Iniciando auditoria inteligente: {self.project_path}")
        
        # 1. Detectar tipo de proyecto
        if not project_type:
            project_type = self._detect_project_type()
        self.results['project_type'] = project_type
        print(f"Tipo de proyecto: {project_type}")
        
        # 2. Cargar configuración específica
        config = self._load_project_config(project_type)
        
        # 3. Ejecutar auditorías
        self._audit_structure(config)
        self._audit_clean_code()
        self._audit_architecture_patterns()
        self._audit_design_patterns()
        
        # 4. Calcular puntuaciones
        self._calculate_scores(config)
        
        # 5. Generar recomendaciones inteligentes
        self._generate_intelligent_recommendations(config)
        
        return self.results
    
    def _detect_project_type(self) -> str:
        """Detecta automáticamente el tipo de proyecto usando IA heurística"""
        try:
            with open(self.config_path / "project_types.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
        except FileNotFoundError:
            return "generic"
        
        detection_rules = config.get('detection_rules', {})
        scores = {}
        
        for project_type, indicators in detection_rules.items():
            score = 0
            for indicator in indicators:
                # Búsqueda exacta de directorios/archivos
                if (self.project_path / indicator).exists():
                    score += 2
                # Búsqueda por patrones
                elif any(self.project_path.rglob(f"*{indicator}*")):
                    score += 1
                # Búsqueda en contenido de archivos
                elif self._search_in_files(indicator):
                    score += 0.5
            
            scores[project_type] = score
        
        # Retornar el tipo con mayor puntuación
        if scores:
            best_type = max(scores, key=scores.get)
            if scores[best_type] > 0:
                return best_type
        
        return "generic"
    
    def _search_in_files(self, pattern: str) -> bool:
        """Busca patrones en archivos Python del proyecto"""
        py_files = list(self.project_path.rglob('*.py'))[:10]  # Limitar búsqueda
        for file_path in py_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if pattern.lower() in content:
                        return True
            except:
                continue
        return False
    
    def _load_project_config(self, project_type: str) -> Dict:
        """Carga configuración específica del tipo de proyecto"""
        try:
            with open(self.config_path / "project_types.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get('project_types', {}).get(project_type, {})
        except FileNotFoundError:
            return {}
    
    def _audit_structure(self, config: Dict):
        """Audita estructura del proyecto según tipo detectado"""
        score = 0
        issues = []
        recommendations = []
        
        # Estructura básica universal
        basic_structure = {
            'src/': 25, 'tests/': 20, 'docs/': 10, 
            'README.md': 15, 'requirements.txt': 10, '.gitignore': 5
        }
        
        for item, points in basic_structure.items():
            if (self.project_path / item).exists():
                score += points
            else:
                issues.append(f"Falta {item}")
                recommendations.append(f"Crear {item}")
        
        # Estructura específica del tipo de proyecto
        required_structure = config.get('required_structure', [])
        for required_dir in required_structure:
            if (self.project_path / required_dir).exists():
                score += 5
            else:
                issues.append(f"Falta directorio específico: {required_dir}")
                recommendations.append(f"Crear {required_dir} según tipo {self.results['project_type']}")
        
        self.results['structure'] = {
            'score': min(score, 100),
            'issues': issues,
            'recommendations': recommendations
        }
    
    def _audit_clean_code(self):
        """Audita principios de código limpio según las 10 secciones de CLEAN-CODE-AND-ARCHITECTURES"""
        score = 0
        issues = []
        total_files = 0
        
        py_files = list(self.project_path.rglob('*.py'))
        if not py_files:
            self.results['clean_code'] = {'score': 0, 'issues': ['No se encontraron archivos Python']}
            return
        
        for file_path in py_files[:15]:  # Analizar máximo 15 archivos
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                total_files += 1
                file_score = 0
                
                # Sección 1: Introducción al código limpio - Principios SOLID
                if self._check_solid_principles(content):
                    file_score += 10
                else:
                    issues.append(f"No sigue principios SOLID en {file_path.name}")
                
                # Sección 2: Nombres significativos - Framework CLEAR
                if self._check_meaningful_names_clear(content):
                    file_score += 10
                else:
                    issues.append(f"Nombres no siguen framework CLEAR en {file_path.name}")
                
                # Sección 3: Funciones claras y cortas - Framework FIRST
                if self._check_clear_short_functions(content):
                    file_score += 15
                else:
                    issues.append(f"Funciones no siguen framework FIRST en {file_path.name}")
                
                # Sección 4: Manejo de errores - Framework ACID
                if self._check_proper_error_handling(content):
                    file_score += 10
                else:
                    issues.append(f"Manejo de errores no sigue framework ACID en {file_path.name}")
                
                # Sección 5: DRY y Modularidad
                if self._check_dry_modularity(content):
                    file_score += 10
                else:
                    issues.append(f"Código repetitivo o mal modularizado en {file_path.name}")
                
                # Sección 6: Documentación clara - Framework SMART
                if self._check_smart_documentation(content):
                    file_score += 10
                else:
                    issues.append(f"Documentación no sigue framework SMART en {file_path.name}")
                
                # Sección 7: Estructuras de datos apropiadas
                if self._check_appropriate_data_structures(content):
                    file_score += 10
                else:
                    issues.append(f"Estructuras de datos inapropiadas en {file_path.name}")
                
                # Sección 8: Código eficiente y legible - Framework CLEAR-FAST
                if self._check_efficient_readable_code(content):
                    file_score += 10
                else:
                    issues.append(f"Código no sigue framework CLEAR-FAST en {file_path.name}")
                
                # Sección 9: Checklist y mejores prácticas
                if self._check_best_practices_checklist(content):
                    file_score += 10
                else:
                    issues.append(f"No sigue checklist de mejores prácticas en {file_path.name}")
                
                # Sección 10: Evaluación y mejora continua
                if self._check_continuous_improvement(content):
                    file_score += 5
                else:
                    issues.append(f"Falta evidencia de mejora continua en {file_path.name}")
                
                score += file_score
                
            except Exception as e:
                issues.append(f"Error leyendo {file_path.name}: {str(e)}")
        
        # Promedio de puntuación
        final_score = (score / (total_files * 100)) * 100 if total_files > 0 else 0
        
        self.results['clean_code'] = {
            'score': min(int(final_score), 100),
            'issues': issues[:10],
            'files_analyzed': total_files,
            'sections_evaluated': [
                'Principios SOLID', 'Nombres CLEAR', 'Funciones FIRST', 'Errores ACID', 
                'DRY/Modularidad', 'Documentación SMART', 'Estructuras datos', 
                'Eficiencia CLEAR-FAST', 'Mejores prácticas', 'Mejora continua'
            ]
        }
    
    def _audit_architecture_patterns(self):
        """Audita patrones de arquitectura según enterprise-architecture-patterns.html"""
        patterns_detected = []
        score = 0
        
        # Patrones definidos en enterprise-architecture-patterns.html
        architecture_patterns = {
            'MVC': {
                'indicators': ['models/', 'views/', 'controllers/', 'model.py', 'view.py', 'controller.py'],
                'score': 25,
                'description': 'Model-View-Controller - Separa lógica de negocio, presentación y control'
            },
            'Hexagonal': {
                'indicators': ['ports/', 'adapters/', 'domain/', 'infrastructure/'],
                'score': 30,
                'description': 'Arquitectura Hexagonal - Aísla lógica de negocio mediante puertos y adaptadores'
            },
            'Clean Architecture': {
                'indicators': ['entities/', 'use_cases/', 'interfaces/', 'frameworks/'],
                'score': 35,
                'description': 'Clean Architecture - Capas concéntricas con dependencias hacia el interior'
            },
            'Repository': {
                'indicators': ['repository', 'repositories/', '*repository*.py'],
                'score': 20,
                'description': 'Repository Pattern - Abstrae acceso a datos con interfaz uniforme'
            },
            'Service Layer': {
                'indicators': ['services/', '*service*.py', 'service_layer/'],
                'score': 15,
                'description': 'Service Layer - Encapsula lógica de negocio en servicios'
            },
            'Dependency Injection': {
                'indicators': ['inject', 'di/', 'container', 'dependencies/'],
                'score': 20,
                'description': 'Dependency Injection - Inversión de control de dependencias'
            }
        }
        
        for pattern_name, pattern_info in architecture_patterns.items():
            if self._detect_pattern(pattern_info['indicators']):
                patterns_detected.append(pattern_name)
                score += pattern_info['score']
        
        self.results['architecture_patterns'] = {
            'patterns_detected': patterns_detected,
            'score': min(score, 100),
            'details': {p: architecture_patterns[p]['description'] for p in patterns_detected}
        }
    
    def _audit_design_patterns(self):
        """Audita patrones de diseño según arquitecturas-software-clase1.html"""
        patterns_found = []
        score = 0
        
        # Patrones de diseño definidos en arquitecturas-software-clase1.html
        design_patterns = {
            'Creacionales': {
                'Singleton': {
                    'indicators': ['__new__', '_instance', 'instance'],
                    'score': 10,
                    'description': 'Garantiza una única instancia de una clase'
                },
                'Factory': {
                    'indicators': ['*factory*.py', 'create()', 'Factory'],
                    'score': 15,
                    'description': 'Crea objetos sin especificar su clase exacta'
                }
            },
            'Estructurales': {
                'Adapter': {
                    'indicators': ['*adapter*.py', 'Adapter'],
                    'score': 10,
                    'description': 'Permite que interfaces incompatibles trabajen juntas'
                },
                'Decorator': {
                    'indicators': ['@', 'decorator', 'Decorator'],
                    'score': 15,
                    'description': 'Añade funcionalidad a objetos dinámicamente'
                }
            },
            'Comportamiento': {
                'Observer': {
                    'indicators': ['notify()', 'subscribe()', 'observer'],
                    'score': 15,
                    'description': 'Define dependencias uno-a-muchos entre objetos'
                },
                'Strategy': {
                    'indicators': ['*strategy*.py', 'Strategy'],
                    'score': 15,
                    'description': 'Define familia de algoritmos intercambiables'
                }
            }
        }
        
        for category, patterns in design_patterns.items():
            for pattern_name, pattern_info in patterns.items():
                if self._detect_pattern_in_code(pattern_info['indicators']):
                    patterns_found.append(f"{pattern_name} ({category})")
                    score += pattern_info['score']
        
        self.results['design_patterns'] = {
            'patterns_found': patterns_found,
            'score': min(score, 100)
        }
    
    def _detect_pattern(self, indicators: List[str]) -> bool:
        """Detecta patrones por estructura de directorios y archivos"""
        for indicator in indicators:
            # Verificar si existe como directorio o archivo exacto
            if (self.project_path / indicator).exists():
                return True
            
            # Verificar patrones con glob seguro
            try:
                if indicator.startswith('*') and indicator.endswith('*'):
                    # Para patrones como *repository*.py
                    pattern = indicator.replace('*', '')
                    if any(pattern in str(f) for f in self.project_path.rglob('*.py')):
                        return True
                elif indicator.endswith('/'):
                    # Para directorios
                    dir_name = indicator.rstrip('/')
                    if any(f.is_dir() and f.name == dir_name for f in self.project_path.rglob('*')):
                        return True
                else:
                    # Búsqueda simple por nombre
                    if any(indicator in f.name for f in self.project_path.rglob('*')):
                        return True
            except ValueError:
                # Si hay error con el patrón, buscar de forma simple
                if any(indicator in str(f) for f in self.project_path.rglob('*')):
                    return True
        return False
    
    def _detect_pattern_in_code(self, indicators: List[str]) -> bool:
        """Detecta patrones en el código fuente"""
        py_files = list(self.project_path.rglob('*.py'))[:10]
        for file_path in py_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for indicator in indicators:
                        # Limpiar indicadores de patrones especiales
                        clean_indicator = indicator.replace('*', '').replace('()', '')
                        if clean_indicator in content:
                            return True
            except:
                continue
        return False
    
    def _calculate_scores(self, config: Dict):
        """Calcula puntuaciones totales y ponderadas"""
        # Puntuación simple
        scores = [
            self.results['structure']['score'],
            self.results['clean_code']['score'],
            self.results['architecture_patterns']['score'],
            self.results['design_patterns']['score']
        ]
        self.results['total_score'] = sum(scores) / len(scores)
        
        # Puntuación ponderada según tipo de proyecto
        weights = config.get('score_weights', {
            'structure': 0.25, 'clean_code': 0.25, 
            'architecture': 0.25, 'design_patterns': 0.25
        })
        
        weighted_score = (
            self.results['structure']['score'] * weights.get('structure', 0.25) +
            self.results['clean_code']['score'] * weights.get('clean_code', 0.25) +
            self.results['architecture_patterns']['score'] * weights.get('architecture', 0.25) +
            self.results['design_patterns']['score'] * weights.get('design_patterns', 0.25)
        )
        
        self.results['weighted_score'] = round(weighted_score, 1)
    
    def _generate_intelligent_recommendations(self, config: Dict):
        """Genera recomendaciones inteligentes basadas en el análisis"""
        recommendations = []
        
        # Recomendaciones por puntuación baja
        if self.results['structure']['score'] < 70:
            recommendations.append({
                'category': 'Estructura',
                'priority': 'Alta',
                'description': 'Mejorar organización siguiendo convenciones del Clean Code',
                'actions': self.results['structure'].get('recommendations', [])
            })
        
        if self.results['clean_code']['score'] < 60:
            recommendations.append({
                'category': 'Código Limpio',
                'priority': 'Crítica',
                'description': 'Aplicar principios fundamentales de Clean Code de Robert Martin',
                'reference': 'https://github.com/juanjovip2490/CLEAN-CODE-AND-ARCHITECTURES'
            })
        
        # Recomendaciones específicas del tipo de proyecto basadas en arquitecturas-software-clase1.html
        recommended_patterns = config.get('recommended_patterns', [])
        detected_patterns = [p.lower() for p in self.results['architecture_patterns']['patterns_detected']]
        missing_patterns = set([p.lower() for p in recommended_patterns]) - set(detected_patterns)
        
        # Recomendaciones específicas según enterprise-architecture-patterns.html
        pattern_recommendations = {
            'mvc': 'Implementar MVC para separar responsabilidades (modelo-vista-controlador)',
            'hexagonal': 'Considerar Arquitectura Hexagonal para independencia de frameworks',
            'clean architecture': 'Aplicar Clean Architecture para reglas de negocio puras',
            'repository': 'Implementar Repository Pattern para abstracción de datos',
            'service layer': 'Añadir Service Layer para encapsular lógica de negocio'
        }
        
        for pattern in missing_patterns:
            description = pattern_recommendations.get(pattern, f'Implementar patrón {pattern.title()}')
            recommendations.append({
                'category': 'Patrón de Arquitectura',
                'priority': 'Media',
                'description': description,
                'reference': 'Ver enterprise-architecture-patterns.html para implementación detallada'
            })
        
        # Recomendaciones por falta de patrones de diseño
        if self.results['design_patterns']['score'] < 30:
            recommendations.append({
                'category': 'Patrones de Diseño',
                'priority': 'Media',
                'description': 'Implementar patrones de diseño para mejorar mantenibilidad',
                'suggestion': 'Comenzar con Factory o Repository patterns'
            })
        
        self.results['recommendations'] = recommendations
    
    # Métodos de verificación Clean Code - 10 Secciones
    def _check_solid_principles(self, content: str) -> bool:
        """Sección 1: Verifica principios SOLID básicos"""
        import re
        
        # SRP: Una clase, una responsabilidad
        classes = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
        for class_match in re.finditer(r'class\s+\w+.*?(?=class|\Z)', content, re.DOTALL):
            methods = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', class_match.group())
            if len(methods) > 10:  # Demasiados métodos = múltiples responsabilidades
                return False
        
        # DIP: Dependencias de abstracciones
        has_abstractions = 'ABC' in content or 'Protocol' in content or 'interface' in content.lower()
        return len(classes) == 0 or has_abstractions
    
    def _check_meaningful_names_clear(self, content: str) -> bool:
        """Sección 2: Framework CLEAR - Nombres significativos"""
        import re
        
        # C - Clear (claros)
        functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
        clear_names = sum(1 for func in functions if len(func) > 3 and '_' in func or func.islower())
        
        # L - Logical (lógicos)
        variables = re.findall(r'\b([a-z_][a-z0-9_]*)\s*=', content)
        logical_vars = sum(1 for var in variables if not any(bad in var for bad in ['temp', 'data', 'x', 'i']))
        
        return (len(functions) == 0 or clear_names / len(functions) > 0.7) and \
               (len(variables) == 0 or logical_vars / len(variables) > 0.6)
    
    def _check_clear_short_functions(self, content: str) -> bool:
        """Sección 3: Framework FIRST - Funciones claras y cortas"""
        import re
        lines = content.split('\n')
        
        # F - Fast (rápidas de leer)
        function_lengths = []
        current_function_lines = 0
        in_function = False
        
        for line in lines:
            if re.match(r'\s*def\s+', line):
                if in_function:
                    function_lengths.append(current_function_lines)
                in_function = True
                current_function_lines = 0
            elif in_function and line.strip():
                current_function_lines += 1
        
        # I - Independent (independientes)
        # R - Repeatable (repetibles)
        # S - Self-validating (auto-validantes)
        # T - Timely (oportunas)
        
        avg_length = sum(function_lengths) / len(function_lengths) if function_lengths else 0
        return avg_length <= 15  # Máximo 15 líneas por función
    
    def _check_proper_error_handling(self, content: str) -> bool:
        """Sección 4: Framework ACID - Manejo de errores"""
        # A - Atomicity (atomicidad)
        has_try_except = 'try:' in content and 'except' in content
        
        # C - Consistency (consistencia)
        # I - Isolation (aislamiento)
        # D - Durability (durabilidad)
        
        # Verificar excepciones específicas vs genéricas
        import re
        generic_except = len(re.findall(r'except:', content))
        specific_except = len(re.findall(r'except\s+\w+', content))
        
        return has_try_except and (generic_except == 0 or specific_except > generic_except)
    
    def _check_dry_modularity(self, content: str) -> bool:
        """Sección 5: DRY y Modularidad"""
        lines = content.split('\n')
        code_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
        
        # Verificar duplicación de código
        unique_lines = set(code_lines)
        duplication_ratio = 1 - (len(unique_lines) / len(code_lines)) if code_lines else 0
        
        # Verificar imports (modularidad)
        import_count = sum(1 for line in lines if line.strip().startswith('import') or line.strip().startswith('from'))
        
        return duplication_ratio < 0.3 and import_count > 0
    
    def _check_smart_documentation(self, content: str) -> bool:
        """Sección 6: Framework SMART - Documentación clara"""
        import re
        
        # S - Specific (específica)
        # M - Measurable (medible)
        # A - Achievable (alcanzable)
        # R - Relevant (relevante)
        # T - Time-bound (temporal)
        
        docstrings = re.findall(r'"""([^"""]+)"""', content)
        functions_with_docs = len(re.findall(r'def\s+\w+[^:]*:\s*"""', content))
        total_functions = len(re.findall(r'def\s+\w+', content))
        
        doc_ratio = functions_with_docs / total_functions if total_functions > 0 else 1
        return doc_ratio > 0.5
    
    def _check_appropriate_data_structures(self, content: str) -> bool:
        """Sección 7: Estructuras de datos apropiadas"""
        # Verificar uso de estructuras apropiadas
        has_dict = 'dict' in content or '{' in content
        has_list = 'list' in content or '[' in content
        has_set = 'set(' in content or '{' in content
        
        # Verificar que no se abuse de listas para todo
        import re
        list_operations = len(re.findall(r'\.append\(|\[.*\]', content))
        dict_operations = len(re.findall(r'\[.*\]\s*=|\w+\[', content))
        
        return (has_dict or has_list) and (list_operations + dict_operations > 0)
    
    def _check_efficient_readable_code(self, content: str) -> bool:
        """Sección 8: Framework CLEAR-FAST - Código eficiente y legible"""
        # C - Clarity (claridad)
        # L - Legibility (legibilidad)
        # E - Efficiency (eficiencia)
        # A - Alternatives (alternativas)
        # R - Refactor (refactorización)
        
        lines = content.split('\n')
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
        
        # F - Focus (enfoque)
        # A - Analysis (análisis)
        # S - Simplification (simplificación)
        # T - Testing (pruebas)
        
        return avg_line_length < 100  # Líneas no muy largas
    
    def _check_best_practices_checklist(self, content: str) -> bool:
        """Sección 9: Checklist de mejores prácticas"""
        import re
        
        # Verificar convenciones de naming
        snake_case_functions = len(re.findall(r'def\s+[a-z_][a-z0-9_]*', content))
        total_functions = len(re.findall(r'def\s+\w+', content))
        
        # Verificar imports organizados
        import_lines = [line for line in content.split('\n') if line.strip().startswith(('import', 'from'))]
        organized_imports = len(import_lines) <= 10  # No demasiados imports
        
        naming_ratio = snake_case_functions / total_functions if total_functions > 0 else 1
        return naming_ratio > 0.8 and organized_imports
    
    def _check_continuous_improvement(self, content: str) -> bool:
        """Sección 10: Evaluación y mejora continua"""
        # Verificar evidencia de refactoring y mejora
        has_version_info = 'version' in content.lower() or '__version__' in content
        has_todo_comments = 'TODO' in content or 'FIXME' in content
        
        # Verificar que el código no tiene deuda técnica obvia
        import re
        code_smells = len(re.findall(r'# hack|# fix|# temp|# quick', content, re.IGNORECASE))
        
        return has_version_info or (has_todo_comments and code_smells < 3)
    
    def _check_small_functions(self, content: str) -> bool:
        """Verifica funciones pequeñas (Clean Code Cap. 3)"""
        import re
        lines = content.split('\n')
        
        in_function = False
        function_lines = 0
        max_function_lines = 0
        
        for line in lines:
            if re.match(r'\s*def\s+', line):
                if in_function and function_lines > max_function_lines:
                    max_function_lines = function_lines
                in_function = True
                function_lines = 0
            elif in_function:
                if line.strip() and not line.startswith('#'):
                    function_lines += 1
                if re.match(r'\s*(def\s+|class\s+)', line) or (not line.strip() and function_lines > 0):
                    if function_lines > max_function_lines:
                        max_function_lines = function_lines
                    in_function = False
        
        # Verificar argumentos de función (máximo 3 según Clean Code)
        func_args = re.findall(r'def\s+\w+\(([^)]*)\)', content)
        complex_functions = sum(1 for args in func_args if args.count(',') > 2)
        
        return max_function_lines <= 20 and complex_functions == 0
    
    def _check_comments_quality(self, content: str) -> bool:
        """Verifica calidad de comentarios (Clean Code Cap. 4)"""
        lines = content.split('\n')
        code_lines = sum(1 for line in lines if line.strip() and 
                        not line.strip().startswith('#') and 
                        not line.strip().startswith('"""') and
                        not line.strip().startswith("'''"))
        
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        
        if code_lines == 0:
            return True
        
        # Verificar que no hay código comentado (malo según Clean Code)
        commented_code = sum(1 for line in lines 
                           if line.strip().startswith('#') and 
                           any(keyword in line for keyword in ['def ', 'class ', 'import ', 'if ', 'for ']))
        
        comment_ratio = comment_lines / code_lines if code_lines > 0 else 0
        return 0.05 <= comment_ratio <= 0.25 and commented_code == 0
    
    def _check_formatting(self, content: str) -> bool:
        """Verifica formato consistente (Clean Code Cap. 5)"""
        lines = content.split('\n')
        
        # Verificar líneas no muy largas
        long_lines = sum(1 for line in lines if len(line) > 120)
        
        # Verificar indentación consistente (4 espacios)
        indented_lines = [line for line in lines if line.startswith(' ') or line.startswith('\t')]
        consistent_indent = all(line.startswith('    ') or line.startswith('\t') 
                              for line in indented_lines if line.strip())
        
        return long_lines < len(lines) * 0.1 and consistent_indent
    
    def _check_error_handling(self, content: str) -> bool:
        """Verifica manejo de errores (Clean Code Cap. 7)"""
        # Verificar uso de excepciones en lugar de códigos de error
        has_proper_exceptions = 'try:' in content and 'except' in content
        
        # Verificar que no se retorna None sin razón
        import re
        return_none_count = len(re.findall(r'return\s+None', content))
        
        return return_none_count < 3 or has_proper_exceptions
    
    def _check_class_organization(self, content: str) -> bool:
        """Verifica organización de clases (Clean Code Cap. 10)"""
        import re
        
        # Verificar que las clases no son muy grandes
        class_blocks = re.findall(r'class\s+\w+.*?(?=class|\Z)', content, re.DOTALL)
        
        for class_content in class_blocks:
            methods = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', class_content)
            if len(methods) > 15:  # Máximo 15 métodos por clase
                return False
        
        return True

def main():
    parser = argparse.ArgumentParser(
        description='🏗️ Auditoría Inteligente de Arquitectura y Código Limpio',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python intelligent_auditor.py /ruta/proyecto
  python intelligent_auditor.py /ruta/proyecto --type web_app
  python intelligent_auditor.py /ruta/proyecto --output reporte.json
  python intelligent_auditor.py /ruta/proyecto --min-score 80

Basado en Clean Code de Robert Martin
Referencia: https://github.com/juanjovip2490/CLEAN-CODE-AND-ARCHITECTURES
        """
    )
    
    parser.add_argument('project', help='Ruta del proyecto a auditar')
    parser.add_argument('--type', help='Tipo de proyecto (web_app, api_rest, microservice, etc.)')
    parser.add_argument('--output', help='Archivo de salida para el reporte JSON')
    parser.add_argument('--min-score', type=int, default=70, help='Puntuación mínima requerida')
    parser.add_argument('--verbose', '-v', action='store_true', help='Salida detallada')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.project):
        print(f"❌ Error: El proyecto {args.project} no existe")
        return 1
    
    # Ejecutar auditoría
    auditor = IntelligentArchitectureAuditor(args.project)
    results = auditor.audit_project(args.type)
    
    # Mostrar resultados
    print("\n" + "="*70)
    print("AUDITORIA INTELIGENTE DE ARQUITECTURA Y CODIGO LIMPIO")
    print("="*70)
    print(f"Proyecto: {results['project']}")
    print(f"Tipo: {results['project_type']}")
    print(f"Fecha: {results['timestamp'][:19]}")
    
    print(f"\nPUNTUACIONES")
    print("-" * 30)
    print(f"Puntuacion Total: {results['total_score']:.1f}/100")
    print(f"Puntuacion Ponderada: {results['weighted_score']}/100")
    print(f"Estructura: {results['structure']['score']}/100")
    print(f"Codigo Limpio: {results['clean_code']['score']}/100")
    print(f"Arquitectura: {results['architecture_patterns']['score']}/100")
    print(f"Patrones Diseno: {results['design_patterns']['score']}/100")
    
    print(f"\nPATRONES DETECTADOS")
    print("-" * 30)
    print(f"Arquitectura: {', '.join(results['architecture_patterns']['patterns_detected']) or 'Ninguno'}")
    print(f"Diseno: {', '.join(results['design_patterns']['patterns_found']) or 'Ninguno'}")
    
    print(f"\nRECOMENDACIONES ({len(results['recommendations'])})")
    print("-" * 30)
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. [{rec['priority']}] {rec['category']}: {rec['description']}")
        if args.verbose and 'actions' in rec:
            for action in rec.get('actions', [])[:3]:
                print(f"   -> {action}")
    
    # Verificar puntuación mínima
    final_score = results['weighted_score']
    if final_score < args.min_score:
        print(f"\nFALLO: Puntuacion {final_score} < {args.min_score} requerida")
        exit_code = 1
    else:
        print(f"\nEXITO: Puntuacion {final_score} >= {args.min_score} requerida")
        exit_code = 0
    
    # Guardar reporte
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nReporte guardado en: {args.output}")
    
    print(f"\nBasado en Clean Code de Robert Martin")
    print(f"Referencia: https://github.com/juanjovip2490/CLEAN-CODE-AND-ARCHITECTURES")
    print(f"Documentacion: enterprise-architecture-patterns.html")
    
    return exit_code

if __name__ == "__main__":
    exit(main())