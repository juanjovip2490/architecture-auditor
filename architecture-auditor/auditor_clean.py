# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Architecture and Design Patterns Auditor
Based on clean code principles and architecture patterns
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
        """Execute complete project audit"""
        print(f"Auditing project: {self.project_path}")
        
        self._audit_structure()
        self._audit_clean_code()
        self._audit_architecture_patterns()
        self._audit_design_patterns()
        self._generate_recommendations()
        
        return self.results
    
    def _audit_structure(self):
        """Audit project structure"""
        structure_score = 0
        issues = []
        
        # Check basic structure
        if (self.project_path / 'src').exists():
            structure_score += 20
        elif (self.project_path / 'app').exists():
            structure_score += 15
        else:
            issues.append("Missing 'src' or 'app' directory for source code")
        
        if (self.project_path / 'tests').exists():
            structure_score += 20
        else:
            issues.append("Missing 'tests' directory for tests")
        
        if (self.project_path / 'docs').exists():
            structure_score += 10
        else:
            issues.append("Missing 'docs' directory for documentation")
        
        # Check configuration files
        config_files = ['README.md', 'requirements.txt', '.gitignore']
        for file in config_files:
            if (self.project_path / file).exists():
                structure_score += 10
            else:
                issues.append(f"Missing file {file}")
        
        # Check additional web project files
        web_files = ['Dockerfile', 'docker-compose.yml']
        for file in web_files:
            if (self.project_path / file).exists():
                structure_score += 5
        
        self.results['architecture_patterns']['structure'] = {
            'score': min(structure_score, 100),
            'issues': issues
        }
    
    def _audit_clean_code(self):
        """Audit clean code principles according to Robert Martin's Clean Code"""
        clean_code_score = 0
        issues = []
        
        # Find Python files for analysis
        py_files = list(self.project_path.rglob('*.py'))
        
        if not py_files:
            issues.append("No Python files found for analysis")
            self.results['clean_code_principles'] = {'score': 0, 'issues': issues}
            return
        
        total_files = len(py_files)
        analyzed_files = 0
        
        for file_path in py_files[:10]:  # Limit to 10 files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                analyzed_files += 1
                
                # 1. Meaningful names
                if self._check_meaningful_names(content, file_path.name):
                    clean_code_score += 15
                else:
                    issues.append(f"Non-meaningful names in {file_path.name}")
                
                # 2. Small and focused functions
                if self._check_function_quality(content, file_path.name):
                    clean_code_score += 20
                else:
                    issues.append(f"Functions too long or complex in {file_path.name}")
                
                # 3. Appropriate comments
                if self._check_comments_quality(content):
                    clean_code_score += 10
                else:
                    issues.append(f"Inadequate comments in {file_path.name}")
                
                # 4. Format and structure
                if self._check_formatting(content, file_path.name):
                    clean_code_score += 10
                else:
                    issues.append(f"Inconsistent format in {file_path.name}")
                
                # 5. Error handling
                if self._check_error_handling(content, file_path.name):
                    clean_code_score += 10
                else:
                    issues.append(f"Poor error handling in {file_path.name}")
                
                # 6. Well organized classes
                if self._check_class_organization(content, file_path.name):
                    clean_code_score += 15
                else:
                    issues.append(f"Poorly organized classes in {file_path.name}")
                
            except Exception as e:
                issues.append(f"Error reading {file_path}: {str(e)}")
        
        # Normalize score based on analyzed files
        if analyzed_files > 0:
            clean_code_score = clean_code_score // analyzed_files
        
        self.results['clean_code_principles'] = {
            'score': min(clean_code_score, 100),
            'issues': issues,
            'files_analyzed': analyzed_files,
            'total_files': total_files
        }
    
    def _audit_architecture_patterns(self):
        """Audit architecture patterns"""
        patterns_found = []
        
        # Detect MVC
        if self._detect_mvc_pattern():
            patterns_found.append("MVC")
        
        # Detect Repository Pattern
        if self._detect_repository_pattern():
            patterns_found.append("Repository")
        
        # Detect Dependency Injection
        if self._detect_dependency_injection():
            patterns_found.append("Dependency Injection")
        
        # Detect REST API
        if self._detect_api_pattern():
            patterns_found.append("API REST")
        
        # Detect service pattern
        if self._detect_service_pattern():
            patterns_found.append("Service Layer")
        
        self.results['architecture_patterns']['patterns_detected'] = patterns_found
        self.results['architecture_patterns']['score'] = len(patterns_found) * 20
    
    def _audit_design_patterns(self):
        """Audit design patterns"""
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
        """Generate recommendations based on audit"""
        recommendations = []
        
        # Structure recommendations
        structure_score = self.results['architecture_patterns']['structure']['score']
        if structure_score < 70:
            recommendations.append({
                'category': 'Structure',
                'priority': 'High',
                'description': 'Improve directory organization following standard conventions'
            })
        
        # Clean code recommendations
        clean_score = self.results['clean_code_principles']['score']
        if clean_score < 60:
            recommendations.append({
                'category': 'Clean Code',
                'priority': 'High',
                'description': 'Apply clean code principles: small functions, descriptive names'
            })
        
        # Pattern recommendations
        patterns_count = len(self.results['architecture_patterns']['patterns_detected'])
        if patterns_count < 2:
            recommendations.append({
                'category': 'Architecture Patterns',
                'priority': 'Medium',
                'description': 'Implement architecture patterns to improve maintainability'
            })
        
        # Web project specific recommendations
        if self._is_web_project():
            if not (self.project_path / 'static').exists():
                recommendations.append({
                    'category': 'Web Structure',
                    'priority': 'Low',
                    'description': 'Consider organizing static files in dedicated directory'
                })
            
            if not (self.project_path / 'templates').exists():
                recommendations.append({
                    'category': 'Web Structure',
                    'priority': 'Low',
                    'description': 'Consider organizing templates in dedicated directory'
                })
        
        self.results['recommendations'] = recommendations
    
    def _is_web_project(self) -> bool:
        """Detect if it's a web project"""
        web_indicators = [
            (self.project_path / 'templates').exists(),
            (self.project_path / 'static').exists(),
            any('flask' in str(f).lower() or 'django' in str(f).lower() or 'fastapi' in str(f).lower() 
                for f in self.project_path.rglob('*.py'))
        ]
        return any(web_indicators)
    
    # Helper methods for verification according to Clean Code
    def _check_meaningful_names(self, content: str, filename: str) -> bool:
        import re
        score = 0
        
        # Check descriptive function names
        functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
        for func in functions:
            if len(func) > 3 and not any(bad in func.lower() for bad in ['temp', 'data', 'info', 'mgr']):
                score += 1
        
        # Check class names (nouns)
        classes = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
        for cls in classes:
            if cls[0].isupper() and not any(bad in cls.lower() for bad in ['manager', 'processor', 'data']):
                score += 2
        
        # Check descriptive variables
        variables = re.findall(r'\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=', content)
        descriptive_vars = sum(1 for var in variables if len(var) > 2 and var not in ['i', 'j', 'k', 'x', 'y'])
        
        return score > 0 and (len(variables) == 0 or descriptive_vars > len(variables) * 0.7)
    
    def _check_function_quality(self, content: str, filename: str) -> bool:
        import re
        lines = content.split('\n')
        current_function = None
        function_lines = 0
        
        for line in lines:
            if line.strip().startswith('def '):
                if current_function and function_lines > 20:
                    return False
                current_function = line.strip()
                function_lines = 0
            elif current_function and (line.startswith('def ') or line.startswith('class ') or (not line.strip() and function_lines > 0)):
                if function_lines > 20:
                    return False
                current_function = None
            elif current_function and line.strip():
                function_lines += 1
        
        # Check function arguments (maximum 5)
        func_args = re.findall(r'def\s+\w+\(([^)]*)\)', content)
        for args in func_args:
            if args.count(',') > 4:  # More than 5 arguments
                return False
        
        return True
    
    def _check_comments_quality(self, content: str) -> bool:
        lines = content.split('\n')
        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('"""'))
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        
        if code_lines == 0:
            return True
        
        # Check that there's no commented code
        commented_code = sum(1 for line in lines if line.strip().startswith('#') and any(keyword in line for keyword in ['def ', 'class ', 'import ', 'if ', 'for ']))
        
        comment_ratio = comment_lines / code_lines if code_lines > 0 else 0
        return comment_ratio <= 0.3 and commented_code <= 2
    
    def _check_formatting(self, content: str, filename: str) -> bool:
        lines = content.split('\n')
        
        # Check lines not too long (120 characters)
        long_lines = sum(1 for line in lines if len(line) > 120)
        
        # Check consistent indentation (basic)
        indentation_consistent = True
        for line in lines:
            if line.strip() and line.startswith(' ') and not line.startswith('    '):
                if not line.startswith('  ') and not line.startswith('   '):
                    indentation_consistent = False
                    break
        
        return long_lines < len(lines) * 0.1 and indentation_consistent
    
    def _check_error_handling(self, content: str, filename: str) -> bool:
        import re
        
        # Check use of exceptions
        has_try_catch = 'try:' in content and 'except' in content
        
        # Check that None is not returned without reason
        return_none_count = len(re.findall(r'return\s+None', content))
        
        # If there are functions that can fail, there should be error handling
        risky_operations = ['open(', 'requests.', 'json.loads', 'int(', 'float(']
        has_risky_ops = any(op in content for op in risky_operations)
        
        if has_risky_ops and not has_try_catch:
            return False
        
        return return_none_count < 3
    
    def _check_class_organization(self, content: str, filename: str) -> bool:
        import re
        
        # Find class definitions
        class_matches = list(re.finditer(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', content))
        
        if not class_matches:
            return True  # No classes to evaluate
        
        for i, match in enumerate(class_matches):
            start_pos = match.start()
            # Find end of class (next class or end of file)
            if i + 1 < len(class_matches):
                end_pos = class_matches[i + 1].start()
            else:
                end_pos = len(content)
            
            class_content = content[start_pos:end_pos]
            
            # Check that classes are not too big (maximum 15 methods)
            methods = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', class_content)
            if len(methods) > 15:
                return False
        
        return True
    
    def _detect_mvc_pattern(self) -> bool:
        mvc_dirs = ['models', 'views', 'controllers']
        mvc_files = ['model.py', 'view.py', 'controller.py']
        
        # Check MVC directories
        dir_exists = any((self.project_path / d).exists() for d in mvc_dirs)
        
        # Check files with MVC names
        file_exists = any(list(self.project_path.rglob(f)) for f in mvc_files)
        
        return dir_exists or file_exists
    
    def _detect_repository_pattern(self) -> bool:
        repo_files = list(self.project_path.rglob('*repository*.py'))
        repo_dirs = list(self.project_path.rglob('repositories'))
        return len(repo_files) > 0 or len(repo_dirs) > 0
    
    def _detect_dependency_injection(self) -> bool:
        di_files = list(self.project_path.rglob('*inject*.py'))
        di_dirs = list(self.project_path.rglob('*dependencies*'))
        return len(di_files) > 0 or len(di_dirs) > 0
    
    def _detect_api_pattern(self) -> bool:
        api_indicators = [
            list(self.project_path.rglob('*api*.py')),
            list(self.project_path.rglob('*routes*.py')),
            list(self.project_path.rglob('*endpoints*.py'))
        ]
        return any(len(files) > 0 for files in api_indicators)
    
    def _detect_service_pattern(self) -> bool:
        service_files = list(self.project_path.rglob('*service*.py'))
        service_dirs = list(self.project_path.rglob('services'))
        return len(service_files) > 0 or len(service_dirs) > 0
    
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
    parser = argparse.ArgumentParser(description='Architecture and Design Auditor')
    parser.add_argument('--project', required=True, help='Path to project to audit')
    parser.add_argument('--output', help='Output file for report')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.project):
        print(f"Error: Project {args.project} does not exist")
        return
    
    auditor = ArchitectureAuditor(args.project)
    results = auditor.audit_project()
    
    # Calculate weighted total score
    structure_score = results['architecture_patterns']['structure']['score']
    clean_score = results['clean_code_principles']['score']
    arch_score = results['architecture_patterns']['score']
    design_score = results['design_patterns']['score']
    
    # Weights: structure 25%, clean code 35%, architecture 25%, design 15%
    total_score = (structure_score * 0.25 + clean_score * 0.35 + 
                   arch_score * 0.25 + design_score * 0.15)
    
    # Show summary
    print("\n" + "="*60)
    print("ARCHITECTURE AUDIT SUMMARY")
    print("="*60)
    print(f"Total Weighted Score: {total_score:.1f}/100")
    print(f"Project Structure: {structure_score}/100")
    print(f"Clean Code Principles: {clean_score}/100")
    print(f"Architecture Patterns: {arch_score}/100")
    print(f"Design Patterns: {design_score}/100")
    
    print(f"\nDetected Patterns: {', '.join(results['architecture_patterns']['patterns_detected']) or 'None'}")
    print(f"Design Patterns: {', '.join(results['design_patterns']['patterns_found']) or 'None'}")
    
    print(f"\nRECOMMENDATIONS ({len(results['recommendations'])})")
    print("-" * 40)
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. [{rec['priority']}] {rec['category']}: {rec['description']}")
    
    if results['architecture_patterns']['structure']['issues']:
        print(f"\nSTRUCTURE ISSUES ({len(results['architecture_patterns']['structure']['issues'])})")
        print("-" * 40)
        for issue in results['architecture_patterns']['structure']['issues']:
            print(f"- {issue}")
    
    if results['clean_code_principles'].get('issues'):
        print(f"\nCLEAN CODE ISSUES ({len(results['clean_code_principles']['issues'])})")
        print("-" * 40)
        for issue in results['clean_code_principles']['issues'][:5]:  # Show only first 5
            print(f"- {issue}")
        if len(results['clean_code_principles']['issues']) > 5:
            print(f"... and {len(results['clean_code_principles']['issues']) - 5} more")
    
    # Save report
    if args.output:
        results['total_score'] = total_score
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nReport saved to: {args.output}")

if __name__ == "__main__":
    main()