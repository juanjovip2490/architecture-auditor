# 🚀 Guía de Inicio Rápido

## Instalación en 1 Minuto

### Windows
```bash
git clone https://github.com/juanjovip2490/architecture-auditor.git
cd architecture-auditor
install.bat
```

### Linux/Mac
```bash
git clone https://github.com/juanjovip2490/architecture-auditor.git
cd architecture-auditor
chmod +x install.sh
./install.sh
```

### Instalación Manual
```bash
git clone https://github.com/juanjovip2490/architecture-auditor.git
cd architecture-auditor/architecture-auditor
pip install -r requirements.txt
python auditor_simple.py --project /ruta/tu/proyecto
```

## Uso Inmediato

### Auditoría Básica
```bash
python auditor_simple.py --project /ruta/del/proyecto
```

### Auditoría Inteligente (Recomendado)
```bash
python audit_runner_simple.py /ruta/del/proyecto
```

### Ejemplo Completo con Proyecto RAG
```bash
# Clonar proyecto de ejemplo
git clone https://github.com/juanjovip2490/LOCAL-RAG-JJ.git

# Auditar proyecto RAG
python audit_runner_simple.py ./LOCAL-RAG-JJ

# Resultado: Detecta automáticamente como 'rag_app'
# y aplica recomendaciones específicas para RAG
```

### Ejemplo de Salida
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
1. [Alta] Estructura: Crear directorio tests/
2. [Media] Código Limpio: Reducir funciones largas
3. [Media] Patrón: Implementar Dependency Injection
```

## Integración CI/CD

### GitHub Actions
```yaml
- name: Architecture Audit
  run: |
    git clone https://github.com/juanjovip2490/architecture-auditor.git
    cd architecture-auditor/architecture-auditor
    pip install -r requirements.txt
    python audit_runner_simple.py ../../
```

### Azure DevOps Pipeline
```yaml
- task: Bash@3
  displayName: 'Architecture Audit'
  inputs:
    targetType: 'inline'
    script: |
      git clone https://dev.azure.com/tu-org/architecture-auditor/_git/architecture-auditor
      cd architecture-auditor/architecture-auditor
      pip install -r requirements.txt
      python audit_runner_simple.py $(Build.SourcesDirectory)
```

### Pre-commit Hook
```bash
#!/bin/sh
# .git/hooks/pre-commit
cd path/to/architecture-auditor/architecture-auditor
python audit_runner_simple.py $(git rev-parse --show-toplevel) || exit 1
```

## Tipos de Proyecto Soportados

- ✅ **Web Apps** (Flask, Django, FastAPI)
- ✅ **APIs REST** (FastAPI, Flask-RESTful)
- ✅ **Microservicios** (Docker, Kubernetes)
- ✅ **Apps Desktop** (Tkinter, PyQt)
- ✅ **Data Science** (Jupyter, Pandas)
- ✅ **Librerías** (setuptools, poetry)

## Configuración Personalizada

Edita `rules/clean_code_rules.json` para personalizar:
```json
{
  "function_rules": {
    "max_lines": 15,
    "max_parameters": 3
  }
}
```

## Soporte

- 📖 [Documentación Completa](README.md)
- 🐛 [Reportar Issues](https://github.com/juanjovip2490/architecture-auditor/issues)
- 💡 [Solicitar Features](https://github.com/juanjovip2490/architecture-auditor/issues/new)