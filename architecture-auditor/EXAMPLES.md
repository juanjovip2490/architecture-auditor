# 📚 Ejemplos de Uso del Architecture Auditor

## 🚀 Ejemplos Rápidos por Tipo de Proyecto

### 1. Aplicación RAG/LLM

```bash
# Clonar proyecto RAG de ejemplo
git clone https://github.com/juanjovip2490/LOCAL-RAG-JJ.git

# Auditar con detección automática
python audit_runner_simple.py ./LOCAL-RAG-JJ

# Resultado esperado:
# - Tipo detectado: rag_app
# - Recomendaciones específicas para RAG
# - Patrones recomendados: Factory, Repository, Service Layer
```

**Salida esperada:**
```
Tipo de proyecto detectado: rag_app
Puntuacion Total Ponderada: 37.5/100
Recomendaciones específicas para RAG:
- Implementar Factory Pattern para LLMs
- Separar lógica de embeddings
- Crear abstracción para base vectorial
```

### 2. API REST con FastAPI

```bash
# Clonar proyecto FastAPI
git clone https://github.com/usuario/fastapi-project.git

# Auditar especificando tipo
python audit_runner_simple.py ./fastapi-project api_rest

# O dejar que se detecte automáticamente
python audit_runner_simple.py ./fastapi-project
```

### 3. Aplicación Web Django/Flask

```bash
# Proyecto web existente
python audit_runner_simple.py ./mi-web-app web_app

# Recomendaciones específicas:
# - Estructura MVC
# - Separación de templates/static
# - Repository pattern para modelos
```

### 4. Microservicio

```bash
# Proyecto con Docker
python audit_runner_simple.py ./mi-microservicio microservice

# Detecta automáticamente por:
# - Presencia de Dockerfile
# - docker-compose.yml
# - Estructura de microservicio
```

## 🔧 Casos de Uso Avanzados

### Auditoría en CI/CD

#### GitHub Actions
```yaml
name: Architecture Audit
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Clone Auditor
      run: |
        git clone https://github.com/juanjovip2490/architecture-auditor.git
        cd architecture-auditor/architecture-auditor
        pip install -r requirements.txt
    
    - name: Run Architecture Audit
      run: |
        cd architecture-auditor/architecture-auditor
        python audit_runner_simple.py ../../ > audit_results.txt
        cat audit_results.txt
    
    - name: Check Score
      run: |
        if grep -q "ESTADO: Deficiente" audit_results.txt; then
          echo "❌ Architecture audit failed"
          exit 1
        fi
```

#### Azure DevOps
```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.9'

- script: |
    git clone https://dev.azure.com/tu-org/architecture-auditor/_git/architecture-auditor
    cd architecture-auditor/architecture-auditor
    pip install -r requirements.txt
    python audit_runner_simple.py $(Build.SourcesDirectory)
  displayName: 'Architecture Audit'
```

### Pre-commit Hook

```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "🔍 Ejecutando auditoría de arquitectura..."

# Ruta al auditor (ajustar según tu setup)
AUDITOR_PATH="$HOME/tools/architecture-auditor/architecture-auditor"

if [ -d "$AUDITOR_PATH" ]; then
    cd "$AUDITOR_PATH"
    RESULT=$(python audit_runner_simple.py $(git rev-parse --show-toplevel) 2>&1)
    
    # Extraer puntuación
    SCORE=$(echo "$RESULT" | grep "Puntuacion Total" | grep -o '[0-9]\+\.[0-9]\+')
    
    echo "$RESULT"
    
    # Fallar si la puntuación es muy baja
    if [ $(echo "$SCORE < 50" | bc -l) -eq 1 ]; then
        echo "❌ Auditoría fallida. Puntuación: $SCORE/100"
        echo "💡 Mejora la arquitectura antes del commit"
        exit 1
    fi
    
    echo "✅ Auditoría pasada. Puntuación: $SCORE/100"
else
    echo "⚠️  Auditor no encontrado en $AUDITOR_PATH"
fi
```

## 📊 Interpretación de Resultados

### Puntuaciones

| Rango | Estado | Acción Recomendada |
|-------|--------|-------------------|
| 80-100 | Excelente | Mantener buenas prácticas |
| 60-79 | Bueno | Mejoras menores |
| 40-59 | Regular | Mejoras significativas |
| 0-39 | Deficiente | Reestructuración completa |

### Tipos de Recomendaciones

#### Alta Prioridad
- Estructura de directorios
- Manejo de errores críticos
- Archivos de configuración faltantes

#### Media Prioridad
- Patrones de arquitectura
- Separación de responsabilidades
- Documentación

#### Baja Prioridad
- Optimizaciones menores
- Convenciones de naming
- Archivos opcionales

## 🎯 Proyectos de Ejemplo para Practicar

### Proyectos Bien Estructurados (80+ puntos)
```bash
# Ejemplos de proyectos con buena arquitectura
git clone https://github.com/fastapi/full-stack-fastapi-postgresql.git
python audit_runner_simple.py ./full-stack-fastapi-postgresql
```

### Proyectos que Necesitan Mejoras (40-60 puntos)
```bash
# Proyectos típicos que necesitan reestructuración
git clone https://github.com/usuario/proyecto-basico.git
python audit_runner_simple.py ./proyecto-basico
```

### Proyectos para Refactorizar (0-40 puntos)
```bash
# Proyectos monolíticos que necesitan separación
git clone https://github.com/juanjovip2490/LOCAL-RAG-JJ.git
python audit_runner_simple.py ./LOCAL-RAG-JJ
```

## 🔄 Flujo de Mejora Continua

### 1. Auditoría Inicial
```bash
python audit_runner_simple.py ./mi-proyecto > baseline_audit.txt
```

### 2. Implementar Mejoras
- Seguir recomendaciones del reporte
- Implementar patrones sugeridos
- Reestructurar directorios

### 3. Re-auditoría
```bash
python audit_runner_simple.py ./mi-proyecto > improved_audit.txt
```

### 4. Comparar Progreso
```bash
# Comparar puntuaciones
grep "Puntuacion Total" baseline_audit.txt
grep "Puntuacion Total" improved_audit.txt
```

## 🛠️ Personalización del Auditor

### Modificar Pesos por Tipo de Proyecto

Editar `audit_runner_simple.py`:

```python
# Para proyectos de ML/AI, dar más peso a código limpio
"ml_project": {
    "score_weights": {
        "structure": 0.2,
        "clean_code": 0.5,  # Mayor peso
        "architecture": 0.2,
        "design_patterns": 0.1
    }
}
```

### Añadir Nuevos Tipos de Proyecto

```python
# En _detect_project_type()
detection_rules = {
    "blockchain_app": ["web3", "ethereum", "smart_contract", "truffle"],
    "mobile_backend": ["django-rest", "flask-restful", "mobile", "api"]
}
```

## 📈 Métricas de Seguimiento

### Dashboard de Calidad
```bash
# Script para generar métricas históricas
#!/bin/bash
DATE=$(date +%Y-%m-%d)
python audit_runner_simple.py ./proyecto > "audits/audit_$DATE.txt"

# Extraer métricas
SCORE=$(grep "Puntuacion Total" "audits/audit_$DATE.txt" | grep -o '[0-9]\+\.[0-9]\+')
echo "$DATE,$SCORE" >> metrics.csv
```

### Alertas Automáticas
```bash
# Slack notification si la puntuación baja
if [ $(echo "$SCORE < 60" | bc -l) -eq 1 ]; then
    curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"⚠️ Architecture score dropped to '$SCORE'/100"}' \
    $SLACK_WEBHOOK_URL
fi
```

## 🎓 Casos de Estudio

### Caso 1: Migración de Monolito a Microservicios
```bash
# Antes: Proyecto monolítico
python audit_runner_simple.py ./monolito
# Resultado: 25/100, sin patrones detectados

# Después: Separación en servicios
python audit_runner_simple.py ./servicio-usuarios microservice
python audit_runner_simple.py ./servicio-productos microservice
# Resultado: 75/100 cada uno, patrones implementados
```

### Caso 2: Mejora de Aplicación RAG
```bash
# Antes: LOCAL-RAG-JJ original
python audit_runner_simple.py ./LOCAL-RAG-JJ
# Resultado: 37.5/100

# Después: Implementar recomendaciones
# - Crear src/, tests/, docs/
# - Implementar Factory Pattern
# - Separar servicios
# Resultado esperado: 80+/100
```

## 🔗 Recursos Adicionales

- [Clean Architecture Guide](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python Design Patterns](https://python-patterns.guide/)
- [FastAPI Best Practices](https://fastapi-best-practices.readthedocs.io/)
- [LangChain Architecture Patterns](https://docs.langchain.com/docs/)