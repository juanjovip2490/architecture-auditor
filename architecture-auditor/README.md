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

```bash
git clone <este-repositorio>
cd architecture-auditor
```

## 🎯 Uso Rápido

### Auditoría Básica
```bash
python auditor.py --project /ruta/del/proyecto
```

### Auditoría de Nuevo Proyecto (Recomendado)
```bash
python audit_runner.py /ruta/del/proyecto
```

### Con Tipo Específico
```bash
python audit_runner.py /ruta/del/proyecto web_app
```

### Generar Reporte HTML
```bash
python auditor.py --project /ruta/del/proyecto --output reporte.json
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

| Tipo | Patrones Recomendados | Estructura |
|------|----------------------|------------|
| **Web App** | MVC, Repository, DI | src/, static/, templates/ |
| **API REST** | Clean Architecture, Repository | src/, routes/, models/ |
| **Microservicio** | Hexagonal, CQRS | src/, api/, domain/, infrastructure/ |
| **Desktop App** | MVP, MVVM, Observer | src/, ui/, controllers/ |
| **Data Science** | Pipeline, Strategy | notebooks/, src/, data/, models/ |
| **Librería** | Factory, Builder, Facade | src/, tests/, docs/, examples/ |

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