# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Script to run automatic audits on new projects
Clean version without special characters for Windows compatibility
"""

import os
import sys
import json
from pathlib import Path
from auditor_clean import ArchitectureAuditor

class ProjectAuditRunner:
    def __init__(self):
        self.config_path = Path(__file__).parent / "config"
        self.rules_path = Path(__file__).parent / "rules"
    
    def audit_new_project(self, project_path: str, project_type: str = None):
        """Audit a new project with specific configuration"""
        
        print(f"Starting audit of new project: {project_path}")
        
        # Detect project type if not specified
        if not project_type:
            project_type = self._detect_project_type(project_path)
            print(f"Detected project type: {project_type}")
        
        # Load specific configuration
        config = self._load_project_config(project_type)
        
        # Execute audit
        auditor = ArchitectureAuditor(project_path)
        results = auditor.audit_project()
        
        # Apply project-specific weights
        if config:
            results = self._apply_project_weights(results, config)
        
        # Generate specific recommendations
        specific_recommendations = self._generate_specific_recommendations(results, config, project_type)
        results['recommendations'].extend(specific_recommendations)
        
        return results
    
    def _detect_project_type(self, project_path: str) -> str:
        """Automatically detect project type"""
        project_path = Path(project_path)
        
        # Basic detection rules
        detection_rules = {
            "web_app": ["app.py", "main.py", "templates/", "static/", "requirements.txt"],
            "api_rest": ["main.py", "routes/", "api/", "fastapi", "flask"],
            "microservice": ["Dockerfile", "docker-compose.yml", "kubernetes/", "helm/"],
            "data_science": ["notebooks/", "data/", "models/", "*.ipynb"],
            "library": ["setup.py", "pyproject.toml", "__init__.py", "src/"],
            "rag_app": ["langchain", "chroma", "embeddings", "vector", "documents/"]
        }
        
        for project_type, indicators in detection_rules.items():
            score = 0
            for indicator in indicators:
                if indicator.endswith('/'):
                    # It's a directory
                    if (project_path / indicator.rstrip('/')).exists():
                        score += 2
                elif indicator.startswith('*'):
                    # It's a file pattern
                    if list(project_path.rglob(indicator)):
                        score += 1
                elif (project_path / indicator).exists():
                    # It's a specific file
                    score += 2
                else:
                    # Search in file content
                    py_files = list(project_path.rglob('*.py'))
                    for py_file in py_files[:5]:  # Limit search
                        try:
                            with open(py_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if indicator.lower() in content.lower():
                                    score += 1
                                    break
                        except:
                            continue
            
            if score >= 2:  # Minimum threshold
                return project_type
        
        return "generic"
    
    def _load_project_config(self, project_type: str) -> dict:
        """Load project type specific configuration"""
        
        # Predefined configurations
        configs = {
            "web_app": {
                "score_weights": {
                    "structure": 0.3,
                    "clean_code": 0.3,
                    "architecture": 0.25,
                    "design_patterns": 0.15
                },
                "recommended_patterns": ["MVC", "Repository", "Service Layer"],
                "required_structure": ["templates/", "static/", "tests/", "config/"]
            },
            "api_rest": {
                "score_weights": {
                    "structure": 0.25,
                    "clean_code": 0.35,
                    "architecture": 0.3,
                    "design_patterns": 0.1
                },
                "recommended_patterns": ["Repository", "Service Layer", "Dependency Injection"],
                "required_structure": ["src/", "tests/", "docs/", "config/"]
            },
            "rag_app": {
                "score_weights": {
                    "structure": 0.2,
                    "clean_code": 0.4,
                    "architecture": 0.3,
                    "design_patterns": 0.1
                },
                "recommended_patterns": ["Factory", "Repository", "Service Layer"],
                "required_structure": ["src/", "tests/", "docs/", "config/", "data/"]
            },
            "microservice": {
                "score_weights": {
                    "structure": 0.2,
                    "clean_code": 0.3,
                    "architecture": 0.4,
                    "design_patterns": 0.1
                },
                "recommended_patterns": ["Hexagonal", "CQRS", "Repository", "Factory"],
                "required_structure": ["src/", "tests/", "docker/", "k8s/", "docs/"]
            }
        }
        
        return configs.get(project_type, {})
    
    def _apply_project_weights(self, results: dict, config: dict) -> dict:
        """Apply project-specific weights"""
        if 'score_weights' not in config:
            return results
        
        weights = config['score_weights']
        
        # Calculate weighted score
        weighted_score = (
            results['architecture_patterns']['structure']['score'] * weights.get('structure', 0.25) +
            results['clean_code_principles']['score'] * weights.get('clean_code', 0.25) +
            results['architecture_patterns']['score'] * weights.get('architecture', 0.25) +
            results['design_patterns']['score'] * weights.get('design_patterns', 0.25)
        )
        
        results['weighted_total_score'] = round(weighted_score, 2)
        results['project_type_weights'] = weights
        return results
    
    def _generate_specific_recommendations(self, results: dict, config: dict, project_type: str) -> list:
        """Generate project type specific recommendations"""
        recommendations = []
        
        if not config:
            return recommendations
        
        # Check recommended patterns
        recommended_patterns = config.get('recommended_patterns', [])
        detected_patterns = results['architecture_patterns']['patterns_detected']
        
        missing_patterns = set(recommended_patterns) - set(detected_patterns)
        
        for pattern in missing_patterns:
            recommendations.append({
                'category': f'Recommended Pattern ({project_type})',
                'priority': 'Medium',
                'description': f'Implement {pattern} pattern recommended for {project_type} applications'
            })
        
        # Check recommended structure
        required_structure = config.get('required_structure', [])
        project_path = Path(results['project'])
        
        for required_dir in required_structure:
            dir_name = required_dir.rstrip('/')
            if not (project_path / dir_name).exists():
                recommendations.append({
                    'category': f'Structure ({project_type})',
                    'priority': 'High',
                    'description': f'Create {required_dir} directory according to {project_type} conventions'
                })
        
        # Type-specific recommendations
        if project_type == "rag_app":
            recommendations.extend(self._get_rag_specific_recommendations(results, project_path))
        elif project_type == "web_app":
            recommendations.extend(self._get_web_specific_recommendations(results, project_path))
        elif project_type == "api_rest":
            recommendations.extend(self._get_api_specific_recommendations(results, project_path))
        
        return recommendations
    
    def _get_rag_specific_recommendations(self, results: dict, project_path: Path) -> list:
        """RAG application specific recommendations"""
        recommendations = []
        
        # Check RAG-specific files
        if not (project_path / "requirements.txt").exists():
            recommendations.append({
                'category': 'RAG Dependencies',
                'priority': 'High',
                'description': 'Create requirements.txt with LangChain, ChromaDB, etc. dependencies'
            })
        
        if not list(project_path.rglob("*embedding*")):
            recommendations.append({
                'category': 'RAG Architecture',
                'priority': 'Medium',
                'description': 'Separate embedding logic into dedicated module'
            })
        
        if not list(project_path.rglob("*vector*")) and not list(project_path.rglob("*chroma*")):
            recommendations.append({
                'category': 'RAG Architecture',
                'priority': 'Medium',
                'description': 'Create abstraction for vector database'
            })
        
        return recommendations
    
    def _get_web_specific_recommendations(self, results: dict, project_path: Path) -> list:
        """Web application specific recommendations"""
        recommendations = []
        
        if not (project_path / "static").exists():
            recommendations.append({
                'category': 'Web Structure',
                'priority': 'Low',
                'description': 'Organize CSS/JS files in static/ directory'
            })
        
        if not (project_path / "templates").exists():
            recommendations.append({
                'category': 'Web Structure',
                'priority': 'Low',
                'description': 'Organize HTML templates in templates/ directory'
            })
        
        return recommendations
    
    def _get_api_specific_recommendations(self, results: dict, project_path: Path) -> list:
        """REST API specific recommendations"""
        recommendations = []
        
        if not list(project_path.rglob("*route*")) and not list(project_path.rglob("*endpoint*")):
            recommendations.append({
                'category': 'API Structure',
                'priority': 'Medium',
                'description': 'Separate endpoints into dedicated route modules'
            })
        
        if not list(project_path.rglob("*model*")) and not list(project_path.rglob("*schema*")):
            recommendations.append({
                'category': 'API Structure',
                'priority': 'Medium',
                'description': 'Create models/schemas for data validation'
            })
        
        return recommendations

def main():
    if len(sys.argv) < 2:
        print("Usage: python audit_runner_clean.py <project_path> [project_type]")
        print("\nSupported project types:")
        print("- web_app: Web applications (Flask, Django, FastAPI)")
        print("- api_rest: REST APIs")
        print("- rag_app: RAG/LLM applications")
        print("- microservice: Microservices")
        print("- data_science: Data science projects")
        print("- library: Python libraries")
        print("- generic: Generic project")
        sys.exit(1)
    
    project_path = sys.argv[1]
    project_type = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(project_path):
        print(f"Error: Project {project_path} does not exist")
        sys.exit(1)
    
    runner = ProjectAuditRunner()
    results = runner.audit_new_project(project_path, project_type)
    
    # Show results
    print("\n" + "="*60)
    print("AUDIT RESULTS")
    print("="*60)
    
    if 'weighted_total_score' in results:
        print(f"Total Weighted Score: {results['weighted_total_score']}/100")
    else:
        # Calculate basic score
        structure_score = results['architecture_patterns']['structure']['score']
        clean_score = results['clean_code_principles']['score']
        arch_score = results['architecture_patterns']['score']
        design_score = results['design_patterns']['score']
        total_score = (structure_score * 0.25 + clean_score * 0.35 + 
                      arch_score * 0.25 + design_score * 0.15)
        print(f"Total Score: {total_score:.1f}/100")
    
    print(f"Project Structure: {results['architecture_patterns']['structure']['score']}/100")
    print(f"Clean Code Principles: {results['clean_code_principles']['score']}/100")
    print(f"Architecture Patterns: {results['architecture_patterns']['score']}/100")
    print(f"Design Patterns: {results['design_patterns']['score']}/100")
    
    detected_patterns = results['architecture_patterns']['patterns_detected']
    design_patterns = results['design_patterns']['patterns_found']
    
    print(f"\nDetected Patterns: {', '.join(detected_patterns) if detected_patterns else 'None'}")
    print(f"Design Patterns: {', '.join(design_patterns) if design_patterns else 'None'}")
    
    print(f"\nRECOMMENDATIONS ({len(results['recommendations'])})")
    print("-" * 40)
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. [{rec['priority']}] {rec['category']}: {rec['description']}")
    
    # Show specific issues
    if results['architecture_patterns']['structure']['issues']:
        print(f"\nSTRUCTURE ISSUES ({len(results['architecture_patterns']['structure']['issues'])})")
        print("-" * 40)
        for issue in results['architecture_patterns']['structure']['issues']:
            print(f"- {issue}")
    
    if results['clean_code_principles'].get('issues'):
        print(f"\nCLEAN CODE ISSUES ({len(results['clean_code_principles']['issues'])})")
        print("-" * 40)
        for issue in results['clean_code_principles']['issues'][:5]:
            print(f"- {issue}")
        if len(results['clean_code_principles']['issues']) > 5:
            print(f"... and {len(results['clean_code_principles']['issues']) - 5} more")
    
    # Save report
    project_name = Path(project_path).name
    output_file = f"audit_report_{project_name}.json"
    
    # Add additional information to report
    results['audit_metadata'] = {
        'project_type_detected': project_type or 'generic',
        'total_files_analyzed': results['clean_code_principles'].get('files_analyzed', 0),
        'audit_version': '2.0'
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nComplete report saved to: {output_file}")
    
    # Show final summary
    total_score = results.get('weighted_total_score', 0)
    if total_score >= 80:
        print("\nSTATUS: Excellent - Well structured project")
    elif total_score >= 60:
        print("\nSTATUS: Good - Some improvements recommended")
    elif total_score >= 40:
        print("\nSTATUS: Fair - Significant improvements needed")
    else:
        print("\nSTATUS: Poor - Complete restructuring required")

if __name__ == "__main__":
    main()