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
cd architecture-auditor
python auditor.py --project /ruta/tu/proyecto
```

## Uso Inmediato

### Auditoría Básica
```bash
audit --project /ruta/del/proyecto
```

### Auditoría Inteligente (Recomendado)
```bash
audit-runner /ruta/del/proyecto
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
    python architecture-auditor/auditor.py --project .
```

### Pre-commit Hook
```bash
#!/bin/sh
audit-runner . || exit 1
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