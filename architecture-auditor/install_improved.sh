#!/bin/bash

echo "========================================"
echo "  Architecture Auditor - Instalación"
echo "========================================"
echo

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar errores
error() {
    echo -e "${RED}ERROR: $1${NC}"
    exit 1
}

# Función para mostrar éxito
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Función para mostrar advertencias
warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Verificar Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        error "Python no está instalado. Instala Python 3.7+ desde https://python.org"
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

success "Python detectado"
$PYTHON_CMD --version

# Verificar versión de Python
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.7"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    error "Se requiere Python 3.7 o superior. Versión actual: $PYTHON_VERSION"
fi

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        warning "pip no encontrado, intentando instalar..."
        $PYTHON_CMD -m ensurepip --upgrade || error "No se pudo instalar pip"
        PIP_CMD="$PYTHON_CMD -m pip"
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

success "pip disponible"

# Crear entorno virtual (opcional)
echo
read -p "¿Crear entorno virtual? (recomendado) [y/N]: " create_venv

if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "Creando entorno virtual..."
    $PYTHON_CMD -m venv venv || error "No se pudo crear entorno virtual"
    
    # Activar entorno virtual
    source venv/bin/activate || error "No se pudo activar entorno virtual"
    success "Entorno virtual creado y activado"
    
    # Actualizar pip en el entorno virtual
    pip install --upgrade pip
fi

# Instalar dependencias
echo
echo "Instalando dependencias..."
$PIP_CMD install -r requirements.txt || error "Falló la instalación de dependencias"

success "Dependencias instaladas"

# Verificar instalación
echo
echo "Verificando instalación..."
$PYTHON_CMD auditor_simple.py --help > /dev/null 2>&1 || error "El auditor no funciona correctamente"

success "Auditor funcionando correctamente"

# Crear scripts de conveniencia
echo
read -p "¿Crear scripts de conveniencia? [y/N]: " create_scripts

if [[ $create_scripts =~ ^[Yy]$ ]]; then
    # Script para auditoría básica
    cat > audit << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi
python auditor_simple.py "$@"
EOF

    # Script para auditoría avanzada
    cat > audit-runner << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi
python audit_runner_simple.py "$@"
EOF

    chmod +x audit audit-runner
    success "Scripts creados: ./audit y ./audit-runner"
    
    # Sugerir añadir al PATH
    echo
    warning "Para usar globalmente, añade este directorio a tu PATH:"
    echo "export PATH=\"$(pwd):\$PATH\""
    echo "O copia los scripts a /usr/local/bin/"
fi

# Ejecutar test básico
echo
echo "Ejecutando test básico..."
if [ -d "../LOCAL-RAG-JJ" ]; then
    echo "Probando con proyecto LOCAL-RAG-JJ..."
    $PYTHON_CMD audit_runner_simple.py ../LOCAL-RAG-JJ > test_output.txt 2>&1
    if [ $? -eq 0 ]; then
        success "Test básico completado"
        echo "Resultado guardado en test_output.txt"
    else
        warning "Test básico falló, pero la instalación parece correcta"
    fi
else
    echo "Para probar, ejecuta:"
    echo "  $PYTHON_CMD audit_runner_simple.py /ruta/a/tu/proyecto"
fi

echo
echo "========================================"
echo "  INSTALACIÓN COMPLETADA"
echo "========================================"
echo
echo "Uso básico:"
echo "  $PYTHON_CMD auditor_simple.py --project /ruta/proyecto"
echo
echo "Uso avanzado:"
echo "  $PYTHON_CMD audit_runner_simple.py /ruta/proyecto"
echo
echo "Ejemplos:"
echo "  $PYTHON_CMD audit_runner_simple.py ."
echo "  $PYTHON_CMD audit_runner_simple.py /mi-proyecto web_app"
echo
echo "Para más información: README.md y EXAMPLES.md"
echo

if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "NOTA: Entorno virtual creado. Para activarlo manualmente:"
    echo "  source venv/bin/activate"
    echo
fi