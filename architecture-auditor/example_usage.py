#!/usr/bin/env python3
"""
Ejemplos de uso del Auditor de Arquitectura
"""

import os
from pathlib import Path
from auditor import ArchitectureAuditor
from audit_runner import ProjectAuditRunner

def example_basic_audit():
    """Ejemplo básico de auditoría"""
    print("🔍 Ejemplo 1: Auditoría Básica")
    print("-" * 40)
    
    # Crear proyecto de ejemplo
    project_path = Path("./example_project")
    project_path.mkdir(exist_ok=True)
    
    # Crear estructura básica
    (project_path / "src").mkdir(exist_ok=True)
    (project_path / "tests").mkdir(exist_ok=True)
    
    # Crear archivo de ejemplo
    with open(project_path / "src" / "main.py", "w") as f:
        f.write("""
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

class UserRepository:
    def __init__(self):
        self._users = []
    
    def save(self, user):
        self._users.append(user)
    
    def find_by_id(self, user_id):
        for user in self._users:
            if user.id == user_id:
                return user
        return None
""")
    
    # Ejecutar auditoría
    auditor = ArchitectureAuditor(str(project_path))
    results = auditor.audit_project()
    
    print(f"Estructura: {results['architecture_patterns']['structure']['score']}/100")
    print(f"Código Limpio: {results['clean_code_principles']['score']}/100")
    print(f"Patrones: {', '.join(results['architecture_patterns']['patterns_detected'])}")
    
    # Limpiar
    import shutil
    shutil.rmtree(project_path)

def example_web_app_audit():
    """Ejemplo de auditoría de aplicación web"""
    print("\n🌐 Ejemplo 2: Auditoría de Web App")
    print("-" * 40)
    
    # Crear proyecto web de ejemplo
    project_path = Path("./web_app_example")
    project_path.mkdir(exist_ok=True)
    
    # Estructura MVC
    (project_path / "src").mkdir(exist_ok=True)
    (project_path / "src" / "models").mkdir(exist_ok=True)
    (project_path / "src" / "views").mkdir(exist_ok=True)
    (project_path / "src" / "controllers").mkdir(exist_ok=True)
    (project_path / "templates").mkdir(exist_ok=True)
    (project_path / "static").mkdir(exist_ok=True)
    (project_path / "tests").mkdir(exist_ok=True)
    
    # Crear archivos
    with open(project_path / "app.py", "w") as f:
        f.write("from flask import Flask\napp = Flask(__name__)")
    
    with open(project_path / "src" / "models" / "user.py", "w") as f:
        f.write("""
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def validate_email(self):
        return '@' in self.email
""")
    
    with open(project_path / "src" / "controllers" / "user_controller.py", "w") as f:
        f.write("""
from flask import render_template
from models.user import User

class UserController:
    def __init__(self, user_repository):
        self.user_repository = user_repository
    
    def create_user(self, name, email):
        user = User(name, email)
        if user.validate_email():
            self.user_repository.save(user)
            return True
        return False
""")
    
    # Auditoría específica para web app
    runner = ProjectAuditRunner()
    results = runner.audit_new_project(str(project_path), "web_app")
    
    print(f"Puntuación Ponderada: {results.get('weighted_total_score', 'N/A')}/100")
    print(f"Patrones Detectados: {', '.join(results['architecture_patterns']['patterns_detected'])}")
    print(f"Recomendaciones: {len(results['recommendations'])}")
    
    # Limpiar
    import shutil
    shutil.rmtree(project_path)

def example_microservice_audit():
    """Ejemplo de auditoría de microservicio"""
    print("\n🔧 Ejemplo 3: Auditoría de Microservicio")
    print("-" * 40)
    
    # Crear proyecto microservicio
    project_path = Path("./microservice_example")
    project_path.mkdir(exist_ok=True)
    
    # Estructura hexagonal
    (project_path / "src").mkdir(exist_ok=True)
    (project_path / "src" / "domain").mkdir(exist_ok=True)
    (project_path / "src" / "infrastructure").mkdir(exist_ok=True)
    (project_path / "src" / "api").mkdir(exist_ok=True)
    (project_path / "tests").mkdir(exist_ok=True)
    
    # Crear Dockerfile
    with open(project_path / "Dockerfile", "w") as f:
        f.write("FROM python:3.9\nCOPY . /app\nWORKDIR /app")
    
    # Crear archivos de dominio
    with open(project_path / "src" / "domain" / "entities.py", "w") as f:
        f.write("""
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def calculate_tax(self, rate):
        return self.price * rate
""")
    
    with open(project_path / "src" / "infrastructure" / "repository.py", "w") as f:
        f.write("""
class ProductRepository:
    def __init__(self, database):
        self.database = database
    
    def save(self, product):
        return self.database.insert(product)
    
    def find_by_name(self, name):
        return self.database.query(name=name)
""")
    
    # Auditoría
    runner = ProjectAuditRunner()
    results = runner.audit_new_project(str(project_path))
    
    print(f"Tipo Detectado: Microservicio")
    print(f"Arquitectura: {results['architecture_patterns']['score']}/100")
    print(f"Patrones: {', '.join(results['design_patterns']['patterns_found'])}")
    
    # Limpiar
    import shutil
    shutil.rmtree(project_path)

def example_integration_workflow():
    """Ejemplo de integración en flujo de trabajo"""
    print("\n⚙️ Ejemplo 4: Integración en Workflow")
    print("-" * 40)
    
    # Simular verificación de calidad mínima
    project_path = Path("./quality_check_example")
    project_path.mkdir(exist_ok=True)
    
    # Crear código de baja calidad
    (project_path / "src").mkdir(exist_ok=True)
    with open(project_path / "src" / "bad_code.py", "w") as f:
        f.write("""
def process_data(data, type, format, options, config, debug, verbose, output_path, temp_dir, log_level):
    # Esta función hace demasiadas cosas
    if type == 'csv':
        # Procesar CSV
        for row in data:
            if format == 'json':
                # Convertir a JSON
                result = {}
                for i, item in enumerate(row):
                    result[f'field_{i}'] = item
                # Más procesamiento...
                if debug:
                    print(f"Processing row {i}")
                if verbose:
                    print(f"Row data: {row}")
                # ... 50 líneas más de código ...
    elif type == 'xml':
        # Procesar XML
        pass
    # ... más código ...
""")
    
    # Auditoría
    auditor = ArchitectureAuditor(str(project_path))
    results = auditor.audit_project()
    
    # Simular verificación de calidad
    min_score = 70
    clean_code_score = results['clean_code_principles']['score']
    
    print(f"Código Limpio: {clean_code_score}/100")
    
    if clean_code_score < min_score:
        print("❌ FALLO: Código no cumple estándares mínimos de calidad")
        print("Problemas encontrados:")
        for issue in results['clean_code_principles']['issues']:
            print(f"  • {issue}")
    else:
        print("✅ ÉXITO: Código cumple estándares de calidad")
    
    # Limpiar
    import shutil
    shutil.rmtree(project_path)

if __name__ == "__main__":
    print("🏗️ EJEMPLOS DE USO - AUDITOR DE ARQUITECTURA")
    print("=" * 60)
    
    example_basic_audit()
    example_web_app_audit()
    example_microservice_audit()
    example_integration_workflow()
    
    print("\n✅ Todos los ejemplos completados")
    print("\nPara usar en tus proyectos:")
    print("  python auditor.py --project /ruta/tu/proyecto")
    print("  python audit_runner.py /ruta/tu/proyecto")