#!/bin/bash

# Script de instalación rápida del Architecture Auditor
echo "🏗️ Instalando Architecture Auditor..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Crear directorio de instalación
INSTALL_DIR="$HOME/.architecture-auditor"
mkdir -p "$INSTALL_DIR"

# Copiar archivos
cp -r . "$INSTALL_DIR/"

# Hacer ejecutables
chmod +x "$INSTALL_DIR/auditor.py"
chmod +x "$INSTALL_DIR/audit_runner.py"

# Crear enlaces simbólicos
sudo ln -sf "$INSTALL_DIR/auditor.py" /usr/local/bin/audit
sudo ln -sf "$INSTALL_DIR/audit_runner.py" /usr/local/bin/audit-runner

echo "✅ Instalación completada!"
echo ""
echo "Uso:"
echo "  audit --project /ruta/del/proyecto"
echo "  audit-runner /ruta/del/proyecto"
echo ""
echo "Para desinstalar: rm -rf $INSTALL_DIR && sudo rm /usr/local/bin/audit /usr/local/bin/audit-runner"