# 🏗️ Auditor de Patrones de Arquitectura y Diseño

Sistema completo de auditoría para evaluar patrones de arquitectura, diseño y principios de código limpio en proyectos de software, basado en los principios del repositorio [codigo-limpio](https://github.com/Ajguerrap/codigo-limpio).

## 🚀 Características

- ✅ **Auditoría de Arquitectura**: Detecta patrones MVC, Clean Architecture, Hexagonal, etc.
- ✅ **Principios SOLID**: Evalúa cumplimiento de principios de diseño
- ✅ **Código Limpio**: Verifica convenciones, funciones, comentarios
- ✅ **Patrones de Diseño**: Identifica Singleton, Factory, Observer, Strategy
- ✅ **Tipos de Proyecto**: Configuraciones específicas para Web, API, Microservicios
- ✅ **Reportes Detallados**: JSON y HTML con recomendaciones

## 📦 Instalación

### Desde GitHub
```bash
git clone https://github.com/juanjovip2490/architecture-auditor.git
cd architecture-auditor/architecture-auditor
pip install -r requirements.txt
```

### Desde Azure DevOps
```bash
git clone https://dev.azure.com/tu-organizacion/tu-proyecto/_git/architecture-auditor
cd architecture-auditor/architecture-auditor
pip install -r requirements.txt
```

## 🎯 Uso Rápido

### Auditoría Básica
```bash
python auditor_simple.py --project /ruta/del/proyecto
```

### Auditoría Inteligente (Recomendado)
```bash
python audit_runner_simple.py /ruta/del/proyecto
```

### Con Tipo Específico
```bash
python audit_runner_simple.py /ruta/del/proyecto rag_app
```

### Ejemplo con Proyecto Clonado
```bash
# Clonar proyecto a auditar
git clone https://github.com/usuario/mi-proyecto.git

# Ejecutar auditoría
python audit_runner_simple.py ./mi-proyecto

# O especificar tipo
python audit_runner_simple.py ./mi-proyecto web_app
```

### Generar Reporte Completo
```bash
# Generar reporte JSON
python auditor_clean.py --project /ruta/del/proyecto --output reporte.json

# Generar reporte HTML visual
python generate_html_report.py reporte.json reporte.html

# Ejemplo completo
python auditor_clean.py --project ./mi-proyecto --output audit.json
python generate_html_report.py audit.json audit_report.html
```

## 📊 Métricas Evaluadas

### 1. Estructura del Proyecto (0-100)
- Organización de directorios
- Archivos de configuración
- Documentación
- Separación de responsabilidades

### 2. Código Limpio (0-100)
- Longitud de funciones (máx. 20 líneas)
- Convenciones de nombres (snake_case, PascalCase)
- Calidad de comentarios (10-30% ratio)
- Principios SOLID

### 3. Patrones de Arquitectura (0-100)
- **MVC**: Model-View-Controller
- **Clean Architecture**: Entidades, Casos de Uso
- **Hexagonal**: Puertos y Adaptadores
- **Repository**: Abstracción de datos
- **Dependency Injection**: Inversión de control

### 4. Patrones de Diseño (0-100)
- **Creacionales**: Singleton, Factory, Builder
- **Estructurales**: Adapter, Decorator, Facade
- **Comportamiento**: Observer, Strategy, Command

## 🎨 Tipos de Proyecto Soportados

| Tipo | Patrones Recomendados | Estructura | Detección Automática |
|------|----------------------|------------|---------------------|
| **web_app** | MVC, Repository, Service Layer | src/, static/, templates/ | ✅ FastAPI, Flask, Django |
| **api_rest** | Repository, Service Layer, DI | src/, routes/, models/ | ✅ API endpoints, REST |
| **rag_app** | Factory, Repository, Service Layer | src/, data/, docs/ | ✅ LangChain, ChromaDB |
| **microservice** | Hexagonal, CQRS, Repository | src/, docker/, k8s/ | ✅ Docker, Kubernetes |
| **data_science** | Pipeline, Strategy | notebooks/, data/, models/ | ✅ Jupyter, Pandas |
| **library** | Factory, Builder, Facade | src/, tests/, docs/ | ✅ setup.py, pyproject.toml |

## 📋 Ejemplo de Salida

```
📊 RESULTADOS DE AUDITORÍA
============================================================
🎯 Puntuación Total Ponderada: 78.5/100
📁 Estructura: 85/100
🧹 Código Limpio: 72/100
🏗️ Arquitectura: 80/100
🎨 Patrones: 65/100

🔍 Patrones Detectados: MVC, Repository
🎨 Patrones de Diseño: Factory, Observer

💡 Recomendaciones (3):
1. [Alta] Estructura: Crear directorio tests/ para pruebas unitarias
2. [Media] Código Limpio: Reducir longitud de funciones en user_service.py
3. [Media] Patrón Recomendado: Considerar implementar Dependency Injection
```

## 🔧 Configuración Personalizada

### Reglas de Código Limpio
Edita `rules/clean_code_rules.json`:
```json
{
  "function_rules": {
    "max_lines": 20,
    "max_parameters": 5
  },
  "naming": {
    "functions": "snake_case",
    "classes": "PascalCase"
  }
}
```

### Nuevos Tipos de Proyecto
Añade en `config/project_types.json`:
```json
{
  "mi_tipo": {
    "name": "Mi Tipo de Proyecto",
    "required_structure": ["src/", "config/"],
    "recommended_patterns": ["Factory", "Strategy"]
  }
}
```

## 📚 Principios de Código Limpio

Basado en el repositorio [Ajguerrap/codigo-limpio](https://github.com/Ajguerrap/codigo-limpio):

### ✅ Funciones
- Máximo 20 líneas
- Una sola responsabilidad
- Nombres descriptivos
- Máximo 5 parámetros

### ✅ Clases
- Principio de responsabilidad única
- Alta cohesión, bajo acoplamiento
- Máximo 15 métodos por clase

### ✅ Nombres
- `snake_case` para funciones y variables
- `PascalCase` para clases
- `UPPER_CASE` para constantes
- Nombres descriptivos y pronunciables

### ✅ Comentarios
- Ratio 10-30% del código
- Explican el "por qué", no el "qué"
- Actualizados y relevantes

## 🎯 Integración en Flujo de Trabajo

### Pre-commit Hook
```bash
#!/bin/sh
python /ruta/audit_runner.py . > audit_result.txt
if grep -q "Puntuación.*: [0-6][0-9]" audit_result.txt; then
    echo "❌ Auditoría fallida. Revisar código antes del commit."
    exit 1
fi
```

### CI/CD Pipeline
```yaml
- name: Architecture Audit
  run: |
    python audit_runner.py .
    if [ $? -ne 0 ]; then exit 1; fi
```

## 📁 Estructura del Auditor

```
architecture-auditor/
├── auditor.py              # Script principal
├── audit_runner.py         # Auditor para nuevos proyectos
├── rules/
│   ├── clean_code_rules.json
│   └── architecture_patterns.json
├── config/
│   └── project_types.json
├── templates/
│   └── audit_template.html
└── README.md
```

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

MIT License - ver archivo LICENSE para detalles.

## 🔗 Referencias

- [Código Limpio - Ajguerrap](https://github.com/Ajguerrap/codigo-limpio)
- [Clean Architecture - Robert Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Design Patterns - Refactoring Guru](https://refactoring.guru/design-patterns)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)